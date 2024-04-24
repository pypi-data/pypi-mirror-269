#
# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import asyncio
import ctypes
import datetime
from functools import lru_cache
import hashlib
from itertools import chain
import multiprocessing
import signal
import sys
import threading

import boto3
from botocore.config import Config

from ngcbpc.api.configuration import Configuration
from ngcbpc.constants import KiB
from ngcbpc.errors import NgcException
from ngcbpc.util.file_utils import glob_filter_in_paths, glob_filter_out_paths

if sys.platform == "win32":
    from ctypes import wintypes

# Default for reading in files for sha256 checksums
DEFAULT_CHUNK_SIZE = 64 * KiB


# NOTE: since the design is still in flux, the access key ID and the access key functions may merge into one
def get_S3_access_key_id():
    # TODO: Contact NvSTS with the JWT to get S3 user ID
    pass


def get_S3_access_key():
    # TODO: Contact NvSTS with the JWT to get the S3 password
    pass


class CreateWindowsCtrlCHandler:
    def __init__(self, handler_function):
        self.handle_ctrl_c = handler_function
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        HANDLER_ROUTINE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)
        self.kernel32.SetConsoleCtrlHandler.argtypes = (HANDLER_ROUTINE, wintypes.BOOL)
        self.HANDLER_ROUTINE = HANDLER_ROUTINE

    def get_handler(self):
        @self.HANDLER_ROUTINE
        def handler(ctrl):
            if ctrl == signal.CTRL_C_EVENT:  # pylint: disable=no-member
                handled = self.handle_ctrl_c()
            else:
                handled = False
            # If not handled, call the next handler.
            return handled

        if not self.kernel32.SetConsoleCtrlHandler(handler, True):
            raise ctypes.WinError(ctypes.get_last_error())

        return handler


def create_ctrl_c_handler(process_pool):
    def handle_ctrl_c(*_):
        print("Caught Ctrl-C, terminating dataset upload.")
        # Stop existing upload processes.
        process_pool.terminate()
        # Wait for the processes to come back.
        process_pool.join()
        print("Terminated dataset upload.")
        return True

    return handle_ctrl_c


def get_download_files(files, dirs, file_patterns=None, dir_patterns=None, exclude_patterns=None):
    file_paths = files.keys()
    # if no file/dir patterns given, do not filter these at all
    if file_patterns or dir_patterns:
        file_paths = glob_filter_in_paths(file_paths, file_patterns)
        dirs = glob_filter_in_paths(dirs, dir_patterns)

    # remove all dirs which are children of dirs_filtered_by_exclude
    dirs_filtered_by_exclude = [dir_ for dir_ in dirs if dir_ not in glob_filter_out_paths(dirs, exclude_patterns)]
    for dir_ in dirs:
        if _parent_exists(dir_, dirs_filtered_by_exclude):
            dirs_filtered_by_exclude.append(dir_)
    dirs = [dir_ for dir_ in dirs if dir_ not in dirs_filtered_by_exclude]
    # remove parents of the dirs_filtered_by_exclude to avoid downloading the excluded directories through ancestors
    parents_of_excluded_dirs = list(
        set(chain.from_iterable([_get_ancestors(dir_, dirs) for dir_ in dirs_filtered_by_exclude]))
    )
    dirs = [dir_ for dir_ in dirs if dir_ not in parents_of_excluded_dirs]

    # remove files that are in directories excluded by an exclude pattern
    file_paths = [file_ for file_ in file_paths if not _see_if_file_in_dirs(file_, dirs_filtered_by_exclude)]

    # filter all the child directories so that they don't get downloaded again.
    # do this last or it interferes with prior user filtering
    dirs = _filter_child_directories(dirs)

    individual_file_paths_from_dirs = []
    for dir_ in dirs:
        # NOTE: need to remove "/" from directory paths because the paths are specified absolute paths in storage
        individual_file_paths_from_dirs = [file_path for file_path in files.keys() if file_path.startswith(dir_)]

    # add files that are in directories and not in file paths
    file_paths = list(set(chain(file_paths, individual_file_paths_from_dirs)))
    # filter out the files which matches the exclude pattern
    file_paths = glob_filter_out_paths(file_paths, exclude_patterns)
    # raise if no files to download
    if not file_paths:
        raise NgcException("No files to download, exiting.")

    # Sum the sizes of individual files
    download_size = sum([files[file_path] for file_path in file_paths])

    return file_paths, download_size


def get_download_files_size(files, dir_patterns, exclude_patterns):
    file_paths = files.keys()
    # filter in the files which matches the dirs pattern
    if dir_patterns:
        file_paths = glob_filter_in_paths(file_paths, dir_patterns)
    # filter out the files which matches the exclude pattern
    if exclude_patterns:
        file_paths = glob_filter_out_paths(file_paths, exclude_patterns)
    # raise if no files to download
    if not file_paths:
        raise NgcException("No files to download, exiting.")

    # Sum the sizes of individual files
    download_size = sum([files[file_path] for file_path in file_paths])

    return file_paths, download_size


def _filter_child_directories(dirs):
    if dirs:
        return [_target for _target in dirs if not _parent_exists(_target, dirs)]
    return dirs


def _parent_exists(_target, _dir_list):
    """
    Determine if any parent dirs exist.

    Given a target and directory list,
    check if any dirs in the directory list
    are a parent of the target.
    """
    _target_split = [_f for _f in _target.split("/") if _f]
    for _dir in _dir_list:
        _dir_split = [_f for _f in _dir.split("/") if _f]
        _len = len(_dir_split)
        # don't process the target
        if _target_split == _dir_split:
            continue
        # potential parents will have len >= target
        if len(_target_split) < _len:
            continue
        if _dir_split == _target_split[:_len]:
            return True
    return False


def _get_ancestors(_target, _dir_list):
    """
    Get all of the ancestors of the target.
    """
    parents = list()
    _target_split = [_f for _f in _target.split("/") if _f]
    for dir_ in _dir_list:
        _dir_split = [_f for _f in dir_.split("/") if _f]
        _len = len(_dir_split)
        # don't process the target
        if _target_split == _dir_split:
            continue
        # potential parents will have len >= target
        if len(_target_split) < _len:
            continue
        if _dir_split == _target_split[:_len]:
            parents.append(dir_)
    return parents


def _see_if_file_in_dirs(name, dirs):
    if not name or not dirs:
        return False
    if "/" in dirs and name != "/":
        return True
    while name and name.rfind("/") > 0:
        name = name[: name.rfind("/")]
        if any(True for dir_ in dirs if name.strip("/") == dir_.strip("/")):
            return True
    return False


def get_sha256_checksum(pth=None, content=None, chunk_size=None, return_object=False, as_digest=False):
    """Returns the SHA256 checksum for the given file or bytes.

    You may specify either a path with the `pth` parameter, or the literal bytes with the `content` parameter. If you
    specify both, the `pth` will be ignored, and the `content` used instead.

    Because files may be very large, they will be read in chunks determined by the `chunk_size` parameter. If that is
    not specified, a default chunk_size of 64KiB will be used. If you pass content directly, the `chunk_size` parameter
    is ignored.

    There are 2 parameters that determine what is returned. If `return_object` is True, the sha256 hash object is
    returned. If `as_digest` is True, then the digest() version (bytes) is returned. If neither are set to True, the
    hexdigest() value (string) will be returned instead.
    """
    result = hashlib.sha256()
    if content:
        if isinstance(content, str):
            content = content.encode()
        result.update(content)
    else:
        # Read in the file in chunk_size parts
        chunk_size = chunk_size or DEFAULT_CHUNK_SIZE
        with open(pth, "rb") as ff:
            chunk = ff.read(chunk_size)
            while chunk:
                result.update(chunk)
                chunk = ff.read(chunk_size)
    if return_object:
        return result
    if as_digest:
        return result.digest()
    return result.hexdigest()


async def gather(coroutines, count=None, return_exceptions=True):
    """
    Override aysncio gather to implement semaphore handling
    :param coroutines args: Coroutines to run with a limited number of semaphores
    :param int count: Number of semaphores to have
    :return list: list of returns from coroutines
    """
    if not count:
        # Default to a reasonable value based on available CPUs
        count = multiprocessing.cpu_count() * 4
    semaphore = asyncio.Semaphore(value=count)

    async def func(coroutine):
        async with semaphore:
            try:
                return await coroutine
            except asyncio.CancelledError:
                pass

    return await asyncio.gather(*[func(coro) for coro in coroutines], return_exceptions=return_exceptions)


def get_headers(headers, auth_org, auth_team):
    # Need to import here to avoid circular import issues
    # pylint: disable=import-outside-toplevel
    from ngcbpc.api.authentication import Authentication

    header_override = Authentication.auth_header(auth_org=auth_org, auth_team=auth_team)
    headers.update(header_override)
    return headers


global credential_lock
credential_lock = threading.Lock()


class DatasetCredentials:
    def __init__(self, credential_provider, dataset_id, org_name, access_type):
        self.upload_overrides = {}
        self.credential_provider = credential_provider
        self.dataset_id = dataset_id
        self.org_name = org_name
        self.access_type = access_type

    def get_credentials(self):
        expire_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=15)).isoformat()
        if "expiration" not in self.upload_overrides or self.upload_overrides["expiration"] < expire_time:
            self._update_dataset_upload_options()
        return self.upload_overrides

    def _update_dataset_upload_options(self):
        with credential_lock:
            # due to get_headers circular import issue Authentication needs to be imported here
            # pylint: disable=import-outside-toplevel
            from ngcbpc.api.authentication import Authentication

            Authentication.config = Configuration()
            self.upload_overrides["dataset_service_enabled"] = True
            getStorageAccessResponse = self.credential_provider.get_storage_access_credentials(
                dataset_id=self.dataset_id, org_name=self.org_name, access_type=self.access_type
            )
            self.upload_overrides["endpoint_url"] = getStorageAccessResponse["endpoint_url"]
            self.upload_overrides["region"] = getStorageAccessResponse["region"]
            self.upload_overrides["base_path"] = getStorageAccessResponse["base_path"]
            credentials = getStorageAccessResponse["Credentials"]["S3Credentials"]
            self.upload_overrides["access_key"] = credentials["access_key"]
            self.upload_overrides["secret_key"] = credentials["secret_key"]
            self.upload_overrides["token"] = credentials["token"]
            self.upload_overrides["expiration"] = credentials["expiration"]
            self.upload_overrides["bucket"], self.upload_overrides["prefix"] = getStorageAccessResponse[
                "base_path"
            ].split("/", 1)


@lru_cache()
def get_s3_client(aws_access_key_id, aws_secret_access_key, aws_session_token, endpoint_url, region_name):
    config = Config(max_pool_connections=20)
    return boto3.Session().client(
        service_name="s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        endpoint_url=endpoint_url,
        region_name=region_name,
        config=config,
    )
