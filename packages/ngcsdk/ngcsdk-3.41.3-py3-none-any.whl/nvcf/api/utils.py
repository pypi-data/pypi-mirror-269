#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#

from nvcf.constants import NVCF_GRPC_URL_MAPPING, NVCF_URL_MAPPING

from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV
from ngcbpc.util.utils import get_environ_tag

env_mapping = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}


def get_nvcf_url_per_environment() -> str:
    """Return the appropriate URL for NVCF direct calls"""
    tag = get_environ_tag()
    env = env_mapping.get(tag)
    return NVCF_URL_MAPPING[env]


def get_nvcf_grpc_url_per_environment() -> str:
    """Return the appropriate grpc URL for NVCF grpc calls"""
    tag = get_environ_tag()
    env = env_mapping.get(tag)
    return NVCF_GRPC_URL_MAPPING[env]
