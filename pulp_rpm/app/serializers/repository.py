import logging
from gettext import gettext as _

from django.conf import settings
from jsonschema import Draft7Validator
from pulpcore.plugin.models import AsciiArmoredDetachedSigningService, Publication, Remote
from pulpcore.plugin.serializers import (
    DetailRelatedField,
    DistributionSerializer,
    PublicationSerializer,
    RelatedField,
    RemoteSerializer,
    RepositorySerializer,
    RepositorySyncURLSerializer,
    ValidateFieldsMixin,
)
from pulpcore.plugin.util import get_domain
from rest_framework import serializers
from pulp_rpm.app.fields import CustomJSONField

from pulp_rpm.app.constants import (
    ALLOWED_CHECKSUM_ERROR_MSG,
    ALLOWED_PUBLISH_CHECKSUM_ERROR_MSG,
    ALLOWED_PUBLISH_CHECKSUMS,
    CHECKSUM_CHOICES,
    COMPRESSION_CHOICES,
    SKIP_TYPES,
    SYNC_POLICY_CHOICES,
)
from pulp_rpm.app.models import (
    RpmDistribution,
    RpmPackageSigningService,
    RpmPublication,
    RpmRemote,
    RpmRepository,
    UlnRemote,
)
from pulp_rpm.app.schema import COPY_CONFIG_SCHEMA
from urllib.parse import urlparse


class RpmRepositorySerializer(RepositorySerializer):
    """
    Serializer for Rpm Repositories.
    """

    autopublish = serializers.BooleanField(
        help_text=_(
            "Whether to automatically create publications for new repository versions, "
            "and update any distributions pointing to this repository."
        ),
        default=False,
        required=False,
    )
    metadata_signing_service = RelatedField(
        help_text="A reference to an associated signing service.",
        view_name="signing-services-detail",
        queryset=AsciiArmoredDetachedSigningService.objects.all(),
        many=False,
        required=False,
        allow_null=True,
    )
    package_signing_service = RelatedField(
        help_text="A reference to an associated package signing service.",
        view_name="signing-services-detail",
        queryset=RpmPackageSigningService.objects.all(),
        many=False,
        required=False,
        allow_null=True,
    )
    package_signing_fingerprint = serializers.CharField(
        help_text=_(
            "The pubkey V4 fingerprint (160 bits) to be passed to the package signing service."
            "The signing service will use that on signing operations related to this repository."
        ),
        max_length=40,
        required=False,
        allow_blank=True,
        default="",
    )
    retain_package_versions = serializers.IntegerField(
        help_text=_(
            "The number of versions of each package to keep in the repository; "
            "older versions will be purged. The default is '0', which will disable "
            "this feature and keep all versions of each package."
        ),
        min_value=0,
        required=False,
    )
    checksum_type = serializers.ChoiceField(
        help_text=_("The preferred checksum type during repo publish."),
        choices=CHECKSUM_CHOICES,
        required=False,
        allow_null=True,
    )
    metadata_checksum_type = serializers.ChoiceField(
        help_text=_("DEPRECATED: use CHECKSUM_TYPE instead."),
        choices=CHECKSUM_CHOICES,
        required=False,
        allow_null=True,
    )
    package_checksum_type = serializers.ChoiceField(
        help_text=_("DEPRECATED: use CHECKSUM_TYPE instead."),
        choices=CHECKSUM_CHOICES,
        required=False,
        allow_null=True,
    )
    compression_type = serializers.ChoiceField(
        help_text=_("The compression type to use for metadata files."),
        choices=COMPRESSION_CHOICES,
        required=False,
        allow_null=True,
    )
    gpgcheck = serializers.IntegerField(
        max_value=1,
        min_value=0,
        required=False,
        allow_null=True,
        help_text=_(
            "DEPRECATED: An option specifying whether a client should perform "
            "a GPG signature check on packages."
        ),
    )
    repo_gpgcheck = serializers.IntegerField(
        max_value=1,
        min_value=0,
        required=False,
        allow_null=True,
        help_text=_(
            "DEPRECATED: An option specifying whether a client should perform "
            "a GPG signature check on the repodata."
        ),
    )
    sqlite_metadata = serializers.BooleanField(
        default=False,
        required=False,
        help_text=_(
            "REMOVED: An option specifying whether Pulp should generate SQLite metadata. "
            "Not operation since pulp_rpm 3.25.0 release"
        ),
        read_only=True,
    )
    repo_config = CustomJSONField(
        required=False,
        help_text=_("A JSON document describing config.repo file"),
    )

    def validate(self, data):
        """Validate data."""
        for field in ("checksum_type", "metadata_checksum_type", "package_checksum_type"):
            if field in data and data[field]:
                if data[field] not in settings.ALLOWED_CONTENT_CHECKSUMS:
                    raise serializers.ValidationError({field: _(ALLOWED_CHECKSUM_ERROR_MSG)})

                if data[field] not in ALLOWED_PUBLISH_CHECKSUMS:
                    raise serializers.ValidationError(
                        {field: _(ALLOWED_PUBLISH_CHECKSUM_ERROR_MSG)}
                    )

        if data.get("package_checksum_type") or data.get("metadata_checksum_type"):
            logging.getLogger("pulp_rpm.deprecation").info(
                "Support for '*_checksum_type' options will be removed from a future release "
                "of pulp_rpm."
            )
            if data.get("checksum_type"):
                raise serializers.ValidationError(
                    _(
                        "Cannot use '*_checksum_type' options and 'checksum_type' options "
                        "simultaneously. The 'package_checksum_type' and 'metadata_checksum_type' "
                        "options are deprecated, please use 'checksum_type' only."
                    )
                )

        validated_data = super().validate(data)
        if (data.get("gpgcheck") or data.get("repo_gpgcheck")) and data.get("repo_config"):
            raise serializers.ValidationError(
                _(
                    "Cannot use gpg options and 'repo_config' options simultaneously. "
                    "The 'gpgcheck' and 'repo_gpgcheck' options are deprecated, please use "
                    "'repo_config' only."
                )
            )
        return validated_data

    def create(self, validated_data):
        """
        Save the repo and handle gpg options

        Args:
            validated_data (dict): A dict of validated data to create the repo

        Returns:
            repo: the created repo
        """
        # gpg options are deprecated in favour of repo_config
        # acting as shim layer between old and new api
        gpgcheck = validated_data.pop("gpgcheck", None)
        repo_gpgcheck = validated_data.pop("repo_gpgcheck", None)
        gpgcheck_options = {}
        if gpgcheck is not None:
            gpgcheck_options["gpgcheck"] = gpgcheck
        if repo_gpgcheck is not None:
            gpgcheck_options["repo_gpgcheck"] = repo_gpgcheck
        if gpgcheck_options.keys():
            logging.getLogger("pulp_rpm.deprecation").info(
                "Support for gpg options will be removed from a future release of pulp_rpm."
            )
        repo_config = (
            gpgcheck_options if gpgcheck_options else validated_data.get("repo_config", {})
        )
        repo = super().create(validated_data)
        repo.repo_config = repo_config
        return repo

    def update(self, instance, validated_data):
        """
        Update the repo and handle gpg options

        Args:
            validated_data (dict): A dict of validated data to update the repo

        Returns:
            repo: the updated repo
        """
        # gpg options are deprecated in favour of repo_config
        # acting as shim layer between old and new api
        gpgcheck = validated_data.pop("gpgcheck", None)
        repo_gpgcheck = validated_data.pop("repo_gpgcheck", None)
        gpgcheck_options = {}
        if gpgcheck is not None:
            gpgcheck_options["gpgcheck"] = gpgcheck
        if repo_gpgcheck is not None:
            gpgcheck_options["repo_gpgcheck"] = repo_gpgcheck
        if gpgcheck_options.keys():
            logging.getLogger("pulp_rpm.deprecation").info(
                "Support for gpg options will be removed from a future release of pulp_rpm."
            )
        repo_config = (
            gpgcheck_options if gpgcheck_options else validated_data.get("repo_config", {})
        )
        instance.repo_config = repo_config
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        fields = RepositorySerializer.Meta.fields + (
            "autopublish",
            "metadata_signing_service",
            "package_signing_service",
            "package_signing_fingerprint",
            "retain_package_versions",
            "checksum_type",
            "metadata_checksum_type",
            "package_checksum_type",
            "gpgcheck",
            "repo_gpgcheck",
            "sqlite_metadata",
            "repo_config",
            "compression_type",
        )
        model = RpmRepository


class RpmBaseRemoteSerializer(RemoteSerializer):
    """
    A common base serializer for multiple RPM based remotes.
    """

    policy = serializers.ChoiceField(
        help_text=_(
            "The policy to use when downloading content. The possible values include: "
            "'immediate', 'on_demand', and 'streamed'. 'immediate' is the default."
        ),
        choices=Remote.POLICY_CHOICES,
        default=Remote.IMMEDIATE,
    )


class RpmRemoteSerializer(RpmBaseRemoteSerializer):
    """
    A Serializer for RpmRemote.
    """

    sles_auth_token = serializers.CharField(
        help_text=_("Authentication token for SLES repositories."),
        required=False,
        allow_null=True,
    )

    def validate_url(self, value):
        ALLOWED = ("http", "https", "file")
        protocol = urlparse(value).scheme
        if protocol not in ALLOWED:
            raise serializers.ValidationError(
                f"The url {repr(value)} is not valid. It must start with: {ALLOWED}."
            )
        return value

    class Meta:
        fields = RemoteSerializer.Meta.fields + ("sles_auth_token",)
        model = RpmRemote


class UlnRemoteSerializer(RpmBaseRemoteSerializer):
    """
    A Serializer for UlnRemote.
    """

    username = serializers.CharField(
        help_text=_("Your ULN account username."),
        required=True,
        write_only=True,
    )
    password = serializers.CharField(
        help_text=_("Your ULN account password."),
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )

    url = serializers.CharField(
        help_text=_(
            "The ULN repo URL of the remote content source."
            '"This is "uln://" followed by the channel name. E.g.: "uln://ol7_x86_64_oracle"'
        ),
        required=True,
    )

    uln_server_base_url = serializers.CharField(
        help_text=_(
            "Base URL of the ULN server. If the uln_server_base_url is not provided pulp_rpm will"
            "use the contents of the DEFAULT_ULN_SERVER_BASE_URL setting instead."
        ),
        required=False,
        allow_null=True,
    )

    def validate_url(self, value):
        ALLOWED = ("uln",)
        protocol = urlparse(value).scheme
        if protocol not in ALLOWED:
            raise serializers.ValidationError(
                f"The url {repr(value)} is not valid. It must start with: {ALLOWED}."
            )
        return value

    class Meta:
        fields = RemoteSerializer.Meta.fields + ("uln_server_base_url",)
        model = UlnRemote


class RpmPublicationSerializer(PublicationSerializer):
    """
    A Serializer for RpmPublication.
    """

    metadata_checksum_type = serializers.ChoiceField(
        help_text=_("DEPRECATED: The checksum type for metadata."),
        choices=CHECKSUM_CHOICES,
        required=False,
    )
    package_checksum_type = serializers.ChoiceField(
        help_text=_("DEPRECATED: The checksum type for packages."),
        choices=CHECKSUM_CHOICES,
        required=False,
    )
    checksum_type = serializers.ChoiceField(
        help_text=_("The preferred checksum type used during repo publishes."),
        choices=CHECKSUM_CHOICES,
        required=False,
    )
    compression_type = serializers.ChoiceField(
        help_text=_("The compression type to use for metadata files."),
        choices=COMPRESSION_CHOICES,
        required=False,
    )
    gpgcheck = serializers.IntegerField(
        max_value=1,
        min_value=0,
        required=False,
        allow_null=True,
        help_text=_(
            "DEPRECATED: An option specifying whether a client should perform "
            "a GPG signature check on packages."
        ),
    )
    repo_gpgcheck = serializers.IntegerField(
        max_value=1,
        min_value=0,
        required=False,
        allow_null=True,
        help_text=_(
            "DEPRECATED: An option specifying whether a client should perform "
            "a GPG signature check on the repodata."
        ),
    )
    sqlite_metadata = serializers.BooleanField(
        default=False,
        required=False,
        help_text=_(
            "REMOVED: An option specifying whether Pulp should generate SQLite metadata. "
            "Not operation since pulp_rpm 3.25.0 release"
        ),
        read_only=True,
    )
    repo_config = CustomJSONField(
        required=False,
        help_text=_("A JSON document describing config.repo file"),
    )

    def validate(self, data):
        """Validate data."""
        for field in ("checksum_type", "metadata_checksum_type", "package_checksum_type"):
            if field in data and data[field]:
                if data[field] not in settings.ALLOWED_CONTENT_CHECKSUMS:
                    raise serializers.ValidationError({field: _(ALLOWED_CHECKSUM_ERROR_MSG)})

                if data[field] not in ALLOWED_PUBLISH_CHECKSUMS:
                    raise serializers.ValidationError(
                        {field: _(ALLOWED_PUBLISH_CHECKSUM_ERROR_MSG)}
                    )

        if data.get("package_checksum_type") or data.get("metadata_checksum_type"):
            logging.getLogger("pulp_rpm.deprecation").info(
                "Support for '*_checksum_type' options will be removed from a future release "
                "of pulp_rpm."
            )
            if data.get("checksum_type"):
                raise serializers.ValidationError(
                    _(
                        "Cannot use '*_checksum_type' options and 'checksum_type' options "
                        "simultaneously. The 'package_checksum_type' and 'metadata_checksum_type' "
                        "options are deprecated, please use 'checksum_type' only."
                    )
                )

        validated_data = super().validate(data)
        if (data.get("gpgcheck") or data.get("repo_gpgcheck")) and data.get("repo_config"):
            raise serializers.ValidationError(
                _(
                    "Cannot use gpg options and 'repo_config' options simultaneously. "
                    "The 'gpgcheck' and 'repo_gpgcheck' options are deprecated, please use "
                    "'repo_config' only."
                )
            )
        return validated_data

    class Meta:
        fields = PublicationSerializer.Meta.fields + (
            "checksum_type",
            "metadata_checksum_type",
            "package_checksum_type",
            "gpgcheck",
            "repo_gpgcheck",
            "sqlite_metadata",
            "repo_config",
            "compression_type",
        )
        model = RpmPublication


class RpmDistributionSerializer(DistributionSerializer):
    """
    Serializer for RPM Distributions.
    """

    publication = DetailRelatedField(
        required=False,
        help_text=_("Publication to be served"),
        view_name_pattern=r"publications(-.*/.*)?-detail",
        queryset=Publication.objects.exclude(complete=False),
        allow_null=True,
    )
    generate_repo_config = serializers.BooleanField(
        default=False,
        required=False,
        help_text=_("An option specifying whether Pulp should generate *.repo files."),
    )

    class Meta:
        fields = DistributionSerializer.Meta.fields + ("publication", "generate_repo_config")
        model = RpmDistribution


class RpmRepositorySyncURLSerializer(RepositorySyncURLSerializer):
    """
    Serializer for RPM Sync.
    """

    mirror = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text=_(
            "DEPRECATED: If ``True``, ``sync_policy`` will default to 'mirror_complete' "
            "instead of 'additive'."
        ),
    )
    sync_policy = serializers.ChoiceField(
        help_text=_(
            "Options: 'additive', 'mirror_complete', 'mirror_content_only'. Default: 'additive'. "
            "Modifies how the sync is performed. 'mirror_complete' will clone the original "
            "metadata and create an automatic publication from it, but comes with some "
            "limitations and does not work for certain repositories. 'mirror_content_only' will "
            "change the repository contents to match the remote but the metadata will be "
            "regenerated and will not be bit-for-bit identical. 'additive' will retain the "
            "existing contents of the repository and add the contents of the repository being "
            "synced."
        ),
        choices=SYNC_POLICY_CHOICES,
        required=False,
        allow_null=True,
    )
    skip_types = serializers.ListField(
        help_text=_("List of content types to skip during sync."),
        required=False,
        default=[],
        child=serializers.ChoiceField([(skip_type, skip_type) for skip_type in SKIP_TYPES]),
    )
    optimize = serializers.BooleanField(
        help_text=_("Whether or not to optimize sync."), required=False, default=True
    )

    def validate(self, data):
        """
        Validate sync parameters.
        """
        data = super().validate(data)

        if "mirror" in data and "sync_policy" in data:
            raise serializers.ValidationError(
                _(
                    "Cannot use 'mirror' and 'sync_policy' options simultaneously. The 'mirror' "
                    "option is deprecated, please use 'sync_policy' only."
                )
            )

        return data


class CopySerializer(ValidateFieldsMixin, serializers.Serializer):
    """
    A serializer for Content Copy API.
    """

    config = CustomJSONField(
        help_text=_("A JSON document describing sources, destinations, and content to be copied"),
    )

    dependency_solving = serializers.BooleanField(
        help_text=_("Also copy dependencies of the content being copied."), default=True
    )

    def validate(self, data):
        """
        Validate that the Serializer contains valid data.

        Make sure the config-JSON matches the config-schema.
        Check for cross-domain references (if domain-enabled).
        """

        def check_domain(domain, href, name):
            # We're doing just a string-check here rather than checking objects
            # because there can be A LOT of objects, and this is happening in the view-layer
            # where we have strictly-limited timescales to work with
            if href and domain not in href:
                raise serializers.ValidationError(
                    _("{} must be a part of the {} domain.").format(name, domain)
                )

        def check_cross_domain_config(cfg):
            """Check that all config-elts are in 'our' domain."""
            # copy-cfg is a list of dictionaries.
            # source_repo_version and dest_repo are required fields.
            # Insure curr-domain exists in src/dest/dest_base_version/content-list hrefs
            curr_domain_name = get_domain().name
            for entry in cfg:
                check_domain(curr_domain_name, entry["source_repo_version"], "dest_repo")
                check_domain(curr_domain_name, entry["dest_repo"], "dest_repo")
                check_domain(
                    curr_domain_name, entry.get("dest_base_version", None), "dest_base_version"
                )
                for content_href in entry.get("content", []):
                    check_domain(curr_domain_name, content_href, "content")

        super().validate(data)
        if "config" in data:
            # Make sure config is valid JSON
            validator = Draft7Validator(COPY_CONFIG_SCHEMA)

            err = []
            for error in sorted(validator.iter_errors(data["config"]), key=str):
                err.append(error.message)
            if err:
                raise serializers.ValidationError(
                    _("Provided copy criteria is invalid:'{}'".format(err))
                )

            if settings.DOMAIN_ENABLED:
                check_cross_domain_config(data["config"])

        return data
