#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from argparse import ArgumentTypeError
from collections.abc import Iterable
from fnmatch import fnmatch
import json
import os
import posixpath
from typing import ByteString, List, Optional, Union

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.pagination import pagination_helper_use_page_reference
from ngcbpc.errors import (
    AuthenticationException,
    NgcException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)
from ngcbpc.util.file_utils import (
    get_file_contents,
    get_incremented_filename,
    helm_format,
)
from ngcbpc.util.utils import extra_args
from ngccli.data.model.Artifact import Artifact
from ngccli.data.model.ArtifactCreateRequest import ArtifactCreateRequest
from ngccli.data.model.ArtifactResponse import ArtifactResponse
from ngccli.data.model.ArtifactUpdateRequest import ArtifactUpdateRequest
from ngccli.data.model.ArtifactVersion import ArtifactVersion
from ngccli.data.model.ArtifactVersionFileListResponse import (
    ArtifactVersionFileListResponse,
)
from ngccli.data.model.ArtifactVersionListResponse import ArtifactVersionListResponse
from ngccli.data.model.ArtifactVersionResponse import ArtifactVersionResponse
from ngccli.data.model.File import File
from registry.api.utils import ChartRegistryTarget, get_label_set_labels
from registry.errors import ChartAlreadyExistsException, ChartNotFoundException
from registry.transformer.chart import ChartSearchTransformer

PAGE_SIZE = 1000


class ChartAPI:
    """
    public methods returns unwrapped objects \n
    private methods returns wrapped api reponses \n
    private methods set endpoints
    """

    def __init__(
        self,
        connection,
        api_client,
        repo_connection: Optional[Connection] = None,
    ):
        self.connection = connection
        self.api_client = api_client
        self.repo_connection = repo_connection
        self.config = Configuration()

    # PUBLIC FUNCTIONS

    @extra_args
    def list(
        self, target: Optional[str] = None, access_type: Optional[str] = None, product_names: Optional[str] = None
    ) -> Union[List[ChartSearchTransformer], List[ArtifactVersion]]:
        """List Resources given a pattern glob or list a resource's versions depending if version included in target,
        offering similar interface with other registry list APIs"""
        crt = ChartRegistryTarget(target, glob_allowed=True)
        if crt.version:
            return list(self.list_versions(target))

        return [i for c in self.list_charts(target, access_type=access_type, product_names=product_names) for i in c]

    def list_charts(
        self,
        target: Optional[str] = None,
        access_type: Optional[str] = None,
        product_names: Optional[str] = None,
    ) -> Iterable[List[ChartSearchTransformer]]:
        """List charts given a chart name pattern glob, yield one by one"""

        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)
        crt = ChartRegistryTarget(target, glob_allowed=True)
        org = crt.org or self.config.org_name
        team = crt.team or self.config.team_name
        # we would like to remove version info from the search query
        resource_matcher = target if not crt.version else "/".join([i for i in (org, team, crt.name) if i])
        # get all matching charts

        try:
            return self.api_client.registry.search.search_charts(
                org=org,
                team=team,
                resource_matcher=resource_matcher,
                access_type=access_type,
                product_names=product_names,
            )
        except ResourceNotFoundException as e:
            raise ResourceNotFoundException(f"Target '{target}' could not be found.") from e

    def list_versions(
        self,
        target: str,
    ) -> Iterable[ArtifactVersion]:
        """List chart versions given a version in target, if version/version_regex provided on target,
        filter for matches, * or omit version to list all versions."""

        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)
        crt = ChartRegistryTarget(target, glob_allowed=True, version_required=False)
        org = crt.org or self.config.org_name
        team = crt.team or self.config.team_name

        try:
            # get all matching versions
            for resp in self._list_versions_resps(org, team, crt.name):
                for ver in resp.artifactVersions:
                    if fnmatch(str(ver.id), crt.version or "*"):
                        yield ver
        except (ResourceNotFoundException, ChartNotFoundException) as e:
            raise ResourceNotFoundException(f"Target '{target}' versions could not be found.") from e

    def list_files(self, target: str) -> Iterable[File]:
        """List files given a exact chart version"""

        self.config.validate_configuration(guest_mode_allowed=True)
        crt = ChartRegistryTarget(target, glob_allowed=False, name_required=True, version_required=True)
        try:
            for resp in self._list_files_resps(crt.org, crt.team, crt.name, crt.version):
                for file in resp.artifactFiles:
                    yield file
        except (ResourceNotFoundException, ChartNotFoundException, AttributeError) as e:
            raise ResourceNotFoundException(f"Target '{target}' versions could not be found.") from e

    @extra_args
    def info(self, target: str) -> Union[Artifact, ArtifactVersion]:
        """Get info for a chart or chart version
           If version in target, return chart version object
           If version not in target, return chart object

        Args:
            target (str): a target containing exact chart name, no regex allowed

        Returns:
            Union[Artifact,ArtifactVersion]: If no version provided in target, return chart details
                If version provided, return version details
        """
        crt = ChartRegistryTarget(target, glob_allowed=False, name_required=True, org_required=True)
        if crt.version is None:
            return self.info_chart(target)
        return self.info_chart_version(target)

    def info_chart(self, target: str) -> Artifact:
        """get info for one chart, with latest version

        Args:
            target (str): a target containing the exact chart name, no regex allowed

        Raises:
            ChartNotFoundException: thrown if not found

        Returns:
            Artifact: chart details
        """
        crt = ChartRegistryTarget(target, glob_allowed=False, name_required=True, org_required=True)
        try:
            return self._info_chart_resp(crt.org, crt.team, crt.name).artifact
        except (ResourceNotFoundException, ChartNotFoundException, AttributeError) as e:
            raise ChartNotFoundException("Target '{}' could not be found.".format(target)) from e

    def info_chart_version(self, target: str) -> ArtifactVersion:
        """get info for one chart version, version is required

        Args:
            target (str): a target containing the exact chart name + version, no regex allowed

        Raises:
            ChartNotFoundException: thrown if not found

        Returns:
            ArtifactVersion: version details
        """
        crt = ChartRegistryTarget(
            target, glob_allowed=False, name_required=True, org_required=True, version_required=True
        )
        try:
            return self._info_chart_version_resp(crt.org, crt.team, crt.name, str(crt.version)).artifactVersion
        except (ResourceNotFoundException, ChartNotFoundException, AttributeError) as e:
            raise ChartNotFoundException("Target '{}' could not be found.".format(target)) from e

    def get_latest_chart_version(self, target: str) -> str:
        chart = self.info_chart(target)
        if not chart.latestVersionId:
            raise NgcException("Target '{}' has no version available.".format(target))
        return chart.latestVersionId

    @extra_args
    def remove(self, target: str) -> Union[ArtifactVersion, Artifact]:
        """Remove a chart or chart version
           If version in target, remove a version and return removed chart version object
           If version not in target, remove all versions and return removed chart object

        Args:
            target (str): a target containing exact chart name, no regex allowed
        """
        crt = ChartRegistryTarget(target, glob_allowed=False, name_required=True, org_required=True)
        if crt.version is None:
            return self.remove_chart(target)
        return self.remove_chart_version(target)

    def remove_chart(self, target: str) -> Artifact:
        """Remove a chart and its versions"""
        self.config.validate_configuration()

        crt = ChartRegistryTarget(target, glob_allowed=False, name_required=True, org_required=True)

        try:
            version_obj_list = self.list_versions(target)
            for version_obj in version_obj_list:
                self._remove_chart_version_resp(crt.org, crt.team, crt.name, version_obj.id)
            return self._remove_chart_resp(crt.org, crt.team, crt.name).artifact
        except (ResourceNotFoundException, ChartNotFoundException, AttributeError) as e:
            raise ChartNotFoundException("Target '{}' could not be found.".format(target)) from e

    def remove_chart_version(self, target: str) -> ArtifactVersion:
        """Remove a chart version"""

        self.config.validate_configuration()
        crt = ChartRegistryTarget(
            target, glob_allowed=False, name_required=True, org_required=True, version_required=True
        )
        try:
            return self._remove_chart_version_resp(crt.org, crt.team, crt.name, crt.version).artifactVersion
        except (ResourceNotFoundException, ChartNotFoundException, AttributeError) as e:
            raise ChartNotFoundException("Target '{}' could not be found.".format(target)) from e

    def pull(self, target: str, download_dir: Optional[str] = None) -> str:
        """pull a helm chart to destination or default package name, download_dir must exist if specified"""
        self.config.validate_configuration(guest_mode_allowed=True)
        crt = ChartRegistryTarget(target, org_required=True, name_required=True)

        if not crt.version:
            crt.version = self.get_latest_chart_version(target)
            target += f":{crt.version}"

        download_dir = os.path.abspath(download_dir or ".")
        if not os.path.isdir(download_dir):
            raise NgcException(f"The path: '{download_dir}' does not exist.")
        if not os.access(download_dir, os.W_OK):
            raise NgcException(f"You do not have permission to write files to '{download_dir}'.")

        if self.info_chart_version(target).status != "UPLOAD_COMPLETE":
            raise NgcException(f"'{target}' is not in state UPLOAD_COMPLETE.")

        chart_package = helm_format(crt.name, crt.version)
        output_path = get_incremented_filename(posixpath.join(download_dir, chart_package))
        resp = self._pull_chart_resp(crt.org, crt.team, chart_package)
        try:
            with open(output_path, "wb") as ff:
                ff.write(resp)
        except (
            PermissionError
        ):  # Still need to check permission, as python's `os.access()` doesn't work correctly under Windows.
            raise NgcException(f"You do not have permission to write files to '{download_dir}'.") from None
        return output_path

    @extra_args
    def create(
        self,
        target: str,
        short_description: str,
        overview_filepath: Optional[str] = None,
        display_name: Optional[str] = None,
        labels: Optional[List[str]] = None,
        label_sets: Optional[List[str]] = None,
        logo: Optional[str] = None,
        publisher: Optional[str] = None,
        built_by: Optional[str] = None,
    ) -> Artifact:
        """Create a chart's metadata"""
        self.config.validate_configuration()
        crt = ChartRegistryTarget(
            target, glob_allowed=False, name_required=True, org_required=True, version_allowed=False
        )

        if overview_filepath:
            abs_path = os.path.abspath(overview_filepath)
            if not os.path.exists(abs_path):
                raise NgcException(f"The path: '{abs_path}' does not exist.")

        chart_create_request = ArtifactCreateRequest(
            {
                # should we limit overview_file size or reach up to size?
                "description": get_file_contents(overview_filepath, "overview_file"),
                "displayName": display_name,
                "labelsV2": get_label_set_labels(self.api_client, "HELM_CHART", label_sets, labels),
                "logo": logo,
                "name": crt.name,
                "publisher": publisher,
                "builtBy": built_by,
                "shortDescription": short_description,
            }
        )
        chart_create_request.isValid()

        try:
            return self._create_chart_resp(crt.org, crt.team, chart_create_request).artifact
        except ResourceAlreadyExistsException as e:
            raise ChartAlreadyExistsException(f"Chart '{target}' already exists.") from e

    # this func is no longer used anywhere, investigate and document
    def create_version(self, org_name, team_name, name, chart_version_create_request, short_desc=None):
        """Create a chart version's metadata"""
        ep = self._get_versions_endpoint(org=org_name, team=team_name, name=name)
        payload_dict = chart_version_create_request.toDict()
        if short_desc:
            payload_dict["shortDesc"] = short_desc
        payload = json.dumps(payload_dict)
        resp = self.connection.make_api_request(
            "PATCH", ep, payload=payload, auth_org=org_name, auth_team=team_name, operation_name="create chart version"
        )
        return ArtifactVersionResponse(resp).artifactVersion

    @extra_args
    def update(
        self,
        target: str,
        overview_filepath: Optional[str] = None,
        display_name: Optional[str] = None,
        labels: Optional[List[str]] = None,
        label_sets: Optional[List[str]] = None,
        logo: Optional[str] = None,
        publisher: Optional[str] = None,
        built_by: Optional[str] = None,
        short_description: Optional[str] = None,
    ) -> Artifact:
        """Update a chart's metadata"""
        self.config.validate_configuration()
        crt = ChartRegistryTarget(target, org_required=True, name_required=True)

        if crt.version:
            raise NgcException("You cannot update a chart version.")

        # this condition blocks because labels reset if empty, we do not want user to run empty update, yet
        if not any([overview_filepath, display_name, labels, label_sets, logo, publisher, built_by, short_description]):
            raise ArgumentTypeError("No arguments provided for chart update; there is nothing to do.")

        chart_update_request = ArtifactUpdateRequest(
            {
                # should we limit overview_file size or reach up to size?
                "description": get_file_contents(overview_filepath, "overview_file"),
                "displayName": display_name,
                "labelsV2": get_label_set_labels(self.api_client, "HELM_CHART", label_sets, labels),
                "logo": logo,
                "name": crt.name,
                "publisher": publisher,
                "builtBy": built_by,
                "shortDescription": short_description,
            }
        )
        chart_update_request.isValid()

        try:
            return self._update_chart_resp(crt.org, crt.team, crt.name, chart_update_request).artifact
        except (ResourceNotFoundException, AuthenticationException, AttributeError) as e:
            raise ResourceNotFoundException(f"Chart '{target}' was not found.") from e

    def push_chart(self, org_name, team_name, payload):
        """Upload a chart to the helm repository"""
        ep = self._get_helm_push_endpoint(org_name, team_name)
        resp = self.repo_connection.make_api_request(
            "POST",
            ep,
            payload=payload,
            auth_org=org_name,
            auth_team=team_name,
            content_type="application/gzip",
            operation_name="push chart",
        )
        return ArtifactVersionResponse(resp).artifactVersion

    def set_chart_state(self, org_name, team_name, chart_name, version, body):
        """Mark chart upload as complete."""
        ep = self._get_versions_endpoint(org=org_name, team=team_name, name=chart_name, version=version)
        resp = self.connection.make_api_request(
            "PATCH", ep, auth_org=org_name, payload=body, operation_name="set chart state"
        )
        return ArtifactResponse(resp).artifact

    # END PUBLIC Functions

    @classmethod
    def _get_chart_endpoint(cls, org: str, team: str, name: Optional[str] = None):
        """Create the chart URL: `v2/org/{org-name}/team/{team-name}/helm-charts/{chart-name}`"""
        return f"v2/org/{org}{('/team/'+team) if team else ''}/helm-charts{'/'+name if name else ''}"

    @classmethod
    def _get_versions_endpoint(cls, org: str, team: str, name: str, version: Optional[str] = None):
        """Create the chart version URL:
        `v2/org/{org-name}/team/{team-name}/helm-charts/{chart_name}/versions[/{version-name}]`"""

        return (
            "v2"
            f"/org/{org}"
            f"{('/team/'+team) if team else ''}"
            f"/helm-charts/{name}"
            f"/versions{('/'+version) if version else ''}"
        )

    @classmethod
    def _get_helm_pull_endpoint(cls, org: str, team: str, name: str):
        """Create the base URL for pull: `{org-name}[/{team-name}]/charts/{chart-name}`"""
        return f"{org}{('/'+team) if team else ''}/charts/{name}"

    @classmethod
    def _get_helm_push_endpoint(cls, org: str, team: str):
        """Create the base URL for push: `api/{org-name}[/{team-name}]/charts`"""
        return f"api/{org}{('/'+team) if team else ''}/charts"

    @classmethod
    def _get_files_endpoint(cls, org: str, team: str, name: str, version: str):
        """Create a files endpoint.
        `v2/org/{org-name}/team/{team-name}/helm-charts/{chart_name}/versions/{version-name}/files`"""
        return f"v2/org/{org}{('/team/'+team) if team else ''}/helm-charts/{name}/versions/{version}/files"

    def _list_files_resps(
        self, org_name, team_name, resource_name, version, page_size=PAGE_SIZE
    ) -> Iterable[ArtifactVersionFileListResponse]:
        """Returns a generator of response objects, each response object contains a chart file list"""
        base_url = self._get_files_endpoint(org=org_name, team=team_name, name=resource_name, version=version)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)
        for res in pagination_helper_use_page_reference(
            self.connection,
            query,
            org_name=self.config.org_name,
            team_name=self.config.team_name,
            operation_name="list chart files",
        ):
            if ArtifactVersionFileListResponse(res):
                yield ArtifactVersionFileListResponse(res)

    def _list_versions_resps(
        self, org_name, team_name, chart_name, page_size=PAGE_SIZE
    ) -> Iterable[ArtifactVersionListResponse]:
        """Returns a generator of response objects, each response object contains a chart version list"""
        base_url = self._get_versions_endpoint(org=org_name, team=team_name, name=chart_name)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)
        for res in pagination_helper_use_page_reference(
            self.connection,
            query,
            org_name=self.config.org_name,
            team_name=self.config.team_name,
            operation_name="list chart versions",
        ):
            if ArtifactVersionListResponse(res):
                yield ArtifactVersionListResponse(res)

    def _info_chart_version_resp(self, org_name, team_name, chart_name, version):
        """Returns a response object of one specific chart version"""
        ep = self._get_versions_endpoint(org=org_name, team=team_name, name=chart_name, version=version)
        params = {"resolve-labels": "true"}
        resp = self.connection.make_api_request(
            "GET",
            ep,
            auth_org=self.config.org_name,
            auth_team=self.config.team_name,
            operation_name="get chart version",
            params=params,
        )
        return ArtifactVersionResponse(resp)

    def _info_chart_resp(self, org_name, team_name, name):
        """Returns a response object of one specific chart"""
        ep = self._get_chart_endpoint(org=org_name, team=team_name, name=name)
        resp = self.connection.make_api_request(
            "GET",
            ep,
            auth_org=self.config.org_name,
            auth_team=self.config.team_name,
            operation_name="get chart",
        )
        return ArtifactResponse(resp)

    def _pull_chart_resp(self, org, team, name) -> ByteString:
        """Download a chart, name has to be full chart name"""
        ep = self._get_helm_pull_endpoint(org=org, team=team, name=name)
        return self.repo_connection.make_api_request(
            "GET",
            ep,
            auth_org=self.config.org_name,
            auth_team=self.config.team_name,
            operation_name="pull chart",
            json_response=False,
            return_content=True,
        )

    def _create_chart_resp(self, org: str, team: str, request_payload: ArtifactCreateRequest) -> ArtifactResponse:
        ep = self._get_chart_endpoint(org=org, team=team)
        resp = self.connection.make_api_request(
            "POST",
            ep,
            payload=request_payload.toJSON(),
            auth_org=self.config.org_name,
            auth_team=self.config.team_name,
            operation_name="create chart",
        )
        return ArtifactResponse(resp)

    def _update_chart_resp(
        self, org: str, team: str, name: str, request_payload: ArtifactUpdateRequest
    ) -> ArtifactResponse:
        ep = self._get_chart_endpoint(org=org, team=team, name=name)
        resp = self.connection.make_api_request(
            "PATCH",
            ep,
            payload=request_payload.toJSON(),
            auth_org=self.config.org_name,
            auth_team=self.config.team_name,
            operation_name="update chart",
        )
        return ArtifactResponse(resp)

    def _remove_chart_resp(self, org: str, team: str, name: str) -> ArtifactResponse:

        ep = self._get_chart_endpoint(org=org, team=team, name=name)
        resp = self.connection.make_api_request(
            "DELETE", ep, auth_org=self.config.org_name, auth_team=self.config.team_name, operation_name="delete chart"
        )
        return ArtifactResponse(resp)

    def _remove_chart_version_resp(self, org: str, team: str, name: str, version: str) -> ArtifactVersionResponse:
        ep = self._get_versions_endpoint(org=org, team=team, name=name, version=version)
        resp = self.connection.make_api_request(
            "DELETE",
            ep,
            auth_org=self.config.org_name,
            auth_team=self.config.team_name,
            operation_name="delete chart version",
        )
        return ArtifactVersionResponse(resp)


class GuestChartAPI(ChartAPI):

    """
    define guest endpoints here to override parent class methods
    """

    @classmethod
    def _get_chart_endpoint(cls, org: Optional[str] = None, team: Optional[str] = None, name: Optional[str] = None):
        """override parent endpoints
        Create the chart URL: `v2/helm-charts[/{org}[/{team}[/{name}]]]`"""
        return f"v2/helm-charts{'/'+org if org else ''}{('/'+team) if team else ''}{('/'+name) if name else ''}"

    @classmethod
    def _get_versions_endpoint(
        cls,
        org: Optional[str] = None,
        team: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """Create the chart version URL:
        `v2/helm-charts[/{org}[/{team}[/{name}]]]/versions[/{version-name}]/versions[/{version}]`"""
        return (
            "v2/helm-charts"
            f"{('/'+org) if org else ''}"
            f"{('/'+team) if team else ''}"
            f"{('/'+name) if name else ''}"
            f"/versions{('/'+version) if version else ''}"
        )
