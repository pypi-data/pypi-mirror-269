#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.


class PublishAPI:
    PAGE_SIZE = 1000

    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def get_base_url(artifact_type):
        """Return the base URL.  Most endpoints should be built off of this."""
        return f"v2/catalog/{artifact_type}"

    @staticmethod
    def get_product_base_url(artifact_type):
        """
        Return the base URL for publishing an entity under a Product.
        For models, resources, helm-charts, and images. To publish a collection under a Product,
        use the `get_base_url`.
        """
        return f"v2/catalog/{artifact_type}/product"

    def publish_artifact(self, publish_request, artifact_type, org=None, team=None):
        """Publish an artifact: Model, Resource, Helm-Chart"""
        if publish_request.toDict().get("productNames", None) and publish_request.toDict().get("accessType", None):
            url = self.get_product_base_url(artifact_type)
        else:
            url = f"{self.get_base_url(artifact_type)}/publish"
        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name="post artifact",
        )

    # pylint: disable=unused-argument
    def publish_collection(self, publish_request, artifact_type, org=None, team=None):
        """Publish a collection by copying collection items and publishing collection metadata."""
        url = self.get_base_url("collections")
        ops_urls = []
        ops_urls.append(("copy collection metadata", f"{url}/metadata/copy"))
        ops_urls.append(("publish collection", f"{url}/metadata/share"))
        responses = []
        payload = publish_request.toJSON()
        for operation, url in ops_urls:
            responses.append(
                (
                    operation,
                    self.connection.make_api_request(
                        "POST",
                        url,
                        payload=payload,
                        auth_org=org,
                        auth_team=team,
                        extra_scopes=["artifact"],
                        renew_token=True,
                        operation_name=operation,
                    ),
                )
            )
        return responses

    def copy_metadata_artifact(self, publish_request, artifact_type, org=None, team=None):
        """Copy the metadata of an artifact instead of a deep copy."""
        url = f"{self.get_base_url(artifact_type)}/metadata/copy"
        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} metadata copy",
        )

    def copy_version_artifact(self, publish_request, artifact_type, org=None, team=None):
        """Copy the specified version of an artifact with no metadata changes to the main artifact."""

        for key in ("publishToPublic", "publishAsListedToPublic", "publishWithGuestAccess"):
            setattr(publish_request, key, None)

        if artifact_type == "containers":
            file_url = f"{self.get_base_url(artifact_type)}/images/copy"
            return self.connection.make_api_request(
                "POST",
                file_url,
                payload=publish_request.toJSON(),
                auth_org=org,
                auth_team=team,
                extra_scopes=["artifact"],
                renew_token=True,
                operation_name=f"post {artifact_type} version files copy",
            )

        meta_url = f"{self.get_base_url(artifact_type)}/versions/metadata/copy"
        file_url = f"{self.get_base_url(artifact_type)}/versions/files/copy"

        # First, copy the version metadata
        self.connection.make_api_request(
            "POST",
            meta_url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} version metadata copy",
        )
        # Next, copy the file(s) for the version
        return self.connection.make_api_request(
            "POST",
            file_url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} version files copy",
        )

    def update_visibility(self, publish_request, artifact_type, org=None, team=None):
        """Update the visibility settings without changing the metadata or versions/files."""
        url = f"{self.get_base_url(artifact_type)}/share"
        # Only the target info is needed
        publish_request.sourceArtifact = None

        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} update visibility",
        )

    # pylint: disable=unused-argument
    def publish_image(self, publish_request, artifact_type, org=None, team=None, sign=False):
        """Publish an image."""
        if publish_request.toDict().get("productNames", None) and publish_request.toDict().get("accessType", None):
            url = self.get_product_base_url(artifact_type)
        else:
            url = f"{self.get_base_url('containers')}/publish"
        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name="post image publish",
        )
