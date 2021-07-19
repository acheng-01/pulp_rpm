"""Constants for Pulp RPM plugin tests."""

from urllib.parse import urljoin

from pulp_smash import config
from pulp_smash.pulp3.constants import (
    BASE_CONTENT_PATH,
    BASE_DISTRIBUTION_PATH,
    BASE_REPO_PATH,
    BASE_PATH,
    BASE_PUBLICATION_PATH,
    BASE_REMOTE_PATH,
)

RPM_COPY_PATH = urljoin(BASE_PATH, "rpm/copy/")
"""The URL used for copying RPM content between repos."""

PULP_FIXTURES_BASE_URL = config.get_config().get_fixtures_url()

DOWNLOAD_POLICIES = ["immediate", "on_demand", "streamed"]

DRPM_UNSIGNED_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "drpm-unsigned/")
"""The URL to a repository with unsigned DRPM packages."""

RPM_PACKAGE_CONTENT_NAME = "rpm.package"

RPM_PACKAGECATEGORY_CONTENT_NAME = "rpm.packagecategory"

RPM_PACKAGEENVIRONMENT_CONTENT_NAME = "rpm.packageenvironment"

RPM_PACKAGEGROUP_CONTENT_NAME = "rpm.packagegroup"

RPM_PACKAGELANGPACKS_CONTENT_NAME = "rpm.packagelangpacks"

RPM_ADVISORY_CONTENT_NAME = "rpm.advisory"

RPM_ALT_LAYOUT_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-alt-layout/")
"""The URL to a signed RPM repository. See :data:`RPM_SIGNED_FIXTURE_URL`."""

RPM_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "rpm/packages/")
"""The location of RPM packages on the content endpoint."""

RPM_NAMESPACES = {
    "metadata/common": "http://linux.duke.edu/metadata/common",
    "metadata/filelists": "http://linux.duke.edu/metadata/filelists",
    "metadata/other": "http://linux.duke.edu/metadata/other",
    "metadata/repo": "http://linux.duke.edu/metadata/repo",
    "metadata/rpm": "http://linux.duke.edu/metadata/rpm",
}
"""Namespaces used by XML-based RPM metadata.

Many of the XML files generated by the ``createrepo`` utility make use of these
namespaces. Some of the files that use these namespaces are listed below:

metadata/common
    Used by ``repodata/primary.xml``.

metadata/filelists
    Used by ``repodata/filelists.xml``.

metadata/other
    Used by ``repodata/other.xml``.

metadata/repo
    Used by ``repodata/repomd.xml``.

metadata/rpm
    Used by ``repodata/repomd.xml``.
"""

RPM_DISTRIBUTION_PATH = urljoin(BASE_DISTRIBUTION_PATH, "rpm/rpm/")

RPM_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, "rpm/rpm/")

RPM_REPO_PATH = urljoin(BASE_REPO_PATH, "rpm/rpm/")

RPM_PUBLICATION_PATH = urljoin(BASE_PUBLICATION_PATH, "rpm/rpm/")

RPM_SHA512_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-with-sha-512/")
"""The URL to an RPM repository with sha512 checksum."""

RPM_SIGNED_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-signed/")
"""The URL to a repository with signed RPM packages."""

RPM_COMPLEX_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-complex-pkg/")

RPM_SINGLE_REQUEST_UPLOAD = urljoin(BASE_PATH, "content/rpm/packages/")

RPM_UNSIGNED_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-unsigned/")
"""The URL to a repository with unsigned RPM packages."""

RPM_INVALID_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-missing-filelists/")

RPM_MIRROR_LIST_GOOD_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-mirrorlist-good")
RPM_MIRROR_LIST_BAD_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-mirrorlist-bad")

RPM_PACKAGE_COUNT = 35
"""The number of packages available at
:data:`RPM_SIGNED_FIXTURE_URL` and :data:`RPM_UNSIGNED_FIXTURE_URL`
"""

RPM_PACKAGECATEGORY_COUNT = 1
"""The number of packagecategories."""

RPM_PACKAGEGROUP_COUNT = 2
"""The number of packagegroups."""

RPM_PACKAGELANGPACKS_COUNT = 1
"""The number of packagelangpacks."""

RPM_ADVISORY_COUNT = 4
"""The number of updated record units."""

RPM_FIXTURE_SUMMARY = {
    RPM_PACKAGE_CONTENT_NAME: RPM_PACKAGE_COUNT,
    RPM_ADVISORY_CONTENT_NAME: RPM_ADVISORY_COUNT,
    RPM_PACKAGECATEGORY_CONTENT_NAME: RPM_PACKAGECATEGORY_COUNT,
    RPM_PACKAGEGROUP_CONTENT_NAME: RPM_PACKAGEGROUP_COUNT,
    RPM_PACKAGELANGPACKS_CONTENT_NAME: RPM_PACKAGELANGPACKS_COUNT,
}
"""The breakdown of how many of each type of content unit are present in the
standard repositories, i.e. :data:`RPM_SIGNED_FIXTURE_URL` and
:data:`RPM_UNSIGNED_FIXTURE_URL`.  This matches the format output by the
"content_summary" field on "../repositories/../versions/../".
"""

RPM_EPEL_URL = "https://dl.fedoraproject.org/pub/epel/7Server/x86_64/"
"""The URL to large repository. EPEL7.

.. NOTE:: This repository is not generated by pulp-fixtures.
"""

FEDORA_MIRRORLIST_BASE = "https://mirrors.fedoraproject.org/mirrorlist"
FEDORA_MIRRORLIST_PARAMS = "?repo=epel-modular-8&arch=x86_64&infra=stock&content=centos"
RPM_EPEL_MIRROR_URL = FEDORA_MIRRORLIST_BASE + FEDORA_MIRRORLIST_PARAMS
"""The URL to retrieve a mirrorlist for the EPEL-8-MODULAR repo.

.. NOTE:: This repository is not generated by pulp-fixtures.
"""

RPM_LONG_UPDATEINFO_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-long-updateinfo/")
"""The URL to RPM with a long updateinfo.xml."""

RPM_MODULAR_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-with-modules/")
"""The URL to a modular RPM repository."""

RPM_MODULES_COUNT = 10
"""The number of modules present on `RPM_MODULAR_FIXTURE_URL`."""

RPM_MODULES_DEFAULTS_COUNT = 3
"""The number of modules-default present on `RPM_MODULAR_FIXTURE_URL`."""

RPM_MODULES_CONTENT_NAME = "rpm.modulemd"

RPM_MODULES_DEFAULTS_CONTENT_NAME = "rpm.modulemd_defaults"

RPM_ADVISORY_MODULAR_COUNT = 6

RPM_MODULAR_FIXTURE_SUMMARY = {
    RPM_PACKAGE_CONTENT_NAME: RPM_PACKAGE_COUNT,
    RPM_ADVISORY_CONTENT_NAME: RPM_ADVISORY_MODULAR_COUNT,
    RPM_MODULES_CONTENT_NAME: RPM_MODULES_COUNT,
    RPM_MODULES_DEFAULTS_CONTENT_NAME: RPM_MODULES_DEFAULTS_COUNT,
    RPM_PACKAGECATEGORY_CONTENT_NAME: RPM_PACKAGECATEGORY_COUNT,
    RPM_PACKAGEGROUP_CONTENT_NAME: RPM_PACKAGEGROUP_COUNT,
    RPM_PACKAGELANGPACKS_CONTENT_NAME: RPM_PACKAGELANGPACKS_COUNT,
}

RPM_MODULES_STATIC_CONTEXT_FIXTURE_URL = urljoin(
    PULP_FIXTURES_BASE_URL, "rpm-modules-static-context/"
)
"""The URL to a modular RPM repository that uses the static_context field."""

# static-context test fixture doesn't add the 2 'modular' advisories
RPM_MODULAR_STATIC_FIXTURE_SUMMARY = {
    RPM_PACKAGE_CONTENT_NAME: RPM_PACKAGE_COUNT,
    RPM_ADVISORY_CONTENT_NAME: RPM_ADVISORY_COUNT,
    RPM_MODULES_CONTENT_NAME: RPM_MODULES_COUNT,
    RPM_MODULES_DEFAULTS_CONTENT_NAME: RPM_MODULES_DEFAULTS_COUNT,
    RPM_PACKAGECATEGORY_CONTENT_NAME: RPM_PACKAGECATEGORY_COUNT,
    RPM_PACKAGEGROUP_CONTENT_NAME: RPM_PACKAGEGROUP_COUNT,
    RPM_PACKAGELANGPACKS_CONTENT_NAME: RPM_PACKAGELANGPACKS_COUNT,
}

"""The breakdown of how many of each type of content unit are present in the
i.e. :data:`RPM_MODULAR_FIXTURE_URL`."""

RPM_PACKAGE_DATA = {
    "name": "kangaroo",
    "epoch": "0",
    "version": "0.3",
    "release": "1",
    "arch": "noarch",
    "description": "A modular RPM fixture for testing Pulp.",
    "summary": "hop like a kangaroo in Australia",
    "rpm_license": "Public Domain",
    "rpm_group": "Unspecified",
    "rpm_vendor": "",
    # TODO: Complete this information once we figure out how to serialize
    # everything nicely
}
"""The metadata for one RPM package."""


RPM_COMPLEX_PACKAGE_DATA = {
    "arch": "x86_64",
    "artifact": None,
    "changelogs": [
        [
            "Lucille Bluth <lucille@bluthcompany.com> - 1.1.1-1",
            1617192000,
            "- It's a banana, Michael. How much could it cost, $10?",
        ],
        [
            "Job Bluth <job@alliance-of-magicians.com> - 2.2.2-2",
            1619352000,
            "- I've made a huge mistake",
        ],
        [
            "George Bluth <george@federalprison.gov> - 3.3.3-3",
            1623672000,
            "- There’s always money in the banana stand",
        ],
    ],
    "checksum_type": "sha256",
    "conflicts": [["foxnetwork", "GT", "0", "5555", None, False]],
    "description": "Complex package",
    "enhances": [["(bananas or magic)", None, None, None, None, False]],
    "epoch": "1",
    "files": [
        [None, "/etc/complex/", "pkg.cfg"],
        [None, "/usr/bin/", "complex_a"],
        ["dir", "/usr/share/doc/", "complex-package"],
        [None, "/usr/share/doc/complex-package/", "README"],
        ["dir", "/var/lib/", "complex"],
        ["ghost", "/var/log/", "complex.log"],
    ],
    "is_modular": False,
    "location_base": "",
    "location_href": "complex-package-2.3.4-5.el8.x86_64.rpm",
    "md5": None,
    "name": "complex-package",
    "obsoletes": [
        ["bluemangroup", "LT", "0", "32.1", "0", False],
        ["cornballer", "LT", "0", "444", None, False],
    ],
    "pkg_id": "bbb7b0e9350a0f75b923bdd0ef4f9af39765c668a3e70bfd3486ea9f0f618aaf",
    "provides": [
        ["/usr/bin/ls", None, None, None, None, False],
        ["complex-package", "EQ", "1", "2.3.4", "5.el8", False],
        ["complex-package(x86-64)", "EQ", "1", "2.3.4", "5.el8", False],
        ["laughter", "EQ", "0", "33", None, False],
        ["narration(ronhoward)", None, None, None, None, False],
    ],
    "recommends": [
        ["((hiding and attic) if light-treason)", None, None, None, None, False],
        ["GeneParmesan(PI)", None, None, None, None, False],
        ["yacht", "GT", "9", "11.0", "0", False],
    ],
    "release": "5.el8",
    "requires": [
        ["/usr/bin/bash", None, None, None, None, False],
        ["/usr/sbin/useradd", None, None, None, None, True],
        ["arson", "GE", "0", "1.0.0", "1", False],
        ["fur", "LE", "0", "2", None, False],
        ["staircar", "LE", "0", "99.1", "3", False],
    ],
    "rpm_buildhost": "localhost",
    "rpm_group": "Development/Tools",
    "rpm_header_end": 8413,
    "rpm_header_start": 4504,
    "rpm_license": "MPLv2",
    "rpm_packager": "Michael Bluth",
    "rpm_sourcerpm": "complex-package-2.3.4-5.el8.src.rpm",
    "rpm_vendor": "Bluth Company",
    "sha1": None,
    "sha224": None,
    "sha256": None,
    "sha384": None,
    "sha512": None,
    "size_archive": 932,
    "size_installed": 117,
    "size_package": 8680,
    "suggests": [
        ["(bobloblaw >= 1.1 if maritimelaw else anyone < 0.5.1-2)", None, None, None, None, False],
        ["(dove and return)", None, None, None, None, False],
        ["(job or money > 9000)", None, None, None, None, False],
    ],
    "summary": "A package for exercising many different features of RPM metadata",
    "supplements": [
        ["((hiding and illusion) unless alliance-of-magicians)", None, None, None, None, False],
        ["comedy", "EQ", "0", "11.1", "4", False],
    ],
    "time_build": 1627052743,
    "time_file": 1627056000,
    "url": "http://bobloblaw.com",
    "version": "2.3.4",
}


RPM_PACKAGE_DATA2 = {
    "name": "duck",
    "epoch": "0",
    "version": "0.7",
    "release": "1",
    "arch": "noarch",
    "description": "A dummy package of duck",
    "summary": "A dummy package of duck",
    "rpm_license": "GPLv2",
    "rpm_group": "Internet/Applications",
    "rpm_vendor": "",
    # TODO: Complete this information once we figure out how to serialize
    # everything nicely
}
"""The metadata for one RPM package."""

RPM_PACKAGE_NAME = "{}".format(RPM_PACKAGE_DATA["name"])
"""The name of one RPM package."""

RPM_PACKAGE_FILENAME = "{}-{}-{}.{}.rpm".format(
    RPM_PACKAGE_DATA["name"],
    RPM_PACKAGE_DATA["version"],
    RPM_PACKAGE_DATA["release"],
    RPM_PACKAGE_DATA["arch"],
)
"""The filename of one RPM package."""

RPM_PACKAGE_FILENAME2 = "{}-{}-{}.{}.rpm".format(
    RPM_PACKAGE_DATA2["name"],
    RPM_PACKAGE_DATA2["version"],
    RPM_PACKAGE_DATA2["release"],
    RPM_PACKAGE_DATA2["arch"],
)
"""The filename of one RPM package."""

RPM_REFERENCES_UPDATEINFO_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-references-updateinfo/")
"""The URL to a repository with ``updateinfo.xml`` containing references.

This repository includes advisory with reference element (0, 1 or 2 references)
and without it.
"""

RPM_RICH_WEAK_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-richnweak-deps/")
"""The URL to an RPM repository with weak and rich dependencies."""

RPM_SIGNED_URL = urljoin(RPM_SIGNED_FIXTURE_URL, RPM_PACKAGE_FILENAME)
"""The path to a single signed RPM package."""

RPM_SIGNED_URL2 = urljoin(RPM_SIGNED_FIXTURE_URL, RPM_PACKAGE_FILENAME2)
"""The path to a single signed RPM package."""

RPM_UNSIGNED_URL = urljoin(RPM_UNSIGNED_FIXTURE_URL, RPM_PACKAGE_FILENAME)
"""The path to a single unsigned RPM package."""

RPM_UPDATED_UPDATEINFO_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-updated-updateinfo/")
"""The URL to a repository containing UpdateRecords (Advisory) with the same IDs
as the ones in the standard repositories, but with different metadata.

Note: This repository uses unsigned RPMs.
"""

RPM_ADVISORY_UPDATED_VERSION_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-updated-updateversion")
"""The URL to a repository containing Advisories with same ID as the ones in the standard
unsigned rpm repository, but with updated Advisory version.
"""

RPM_ADVISORY_DIFFERENT_PKGLIST_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-advisory-diffpkgs")
"""The URL to a repository containing Advisories with same ID and version as the ones in the
standard unsigned rpm repository, but with different pkglist.
"""

RPM_ADVISORY_DIFFERENT_REPO_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-advisory-diff-repo")
"""The URL to a repository containing Advisories with same ID and version as the ones in the
standard unsigned rpm repository, but with different update_date and packages intersection.
"""

RPM_ADVISORY_INCOMPLETE_PKG_LIST_URL = urljoin(
    PULP_FIXTURES_BASE_URL, "rpm-advisory-incomplete-package-list"
)
"""The URL to a repository containing Advisories with same update_date and version as the ones
in the standard unsigned rpm repository, but pkglist intersection is non-empty and not equal
to either pkglist.
"""

RPM_ADVISORY_NO_DATES = urljoin(PULP_FIXTURES_BASE_URL, "rpm-advisory-no-dates")
"""The URL to a repository containing Advisories with same id and version as the ones
in the standard unsigned rpm repository, but no update_date or issue_date.
"""

RPM_ADVISORY_TEST_ID = "RHEA-2012:0056"
RPM_ADVISORY_TEST_ID_NEW = "RHEA-2012:0058"
"""The ID of an UpdateRecord (advisory/erratum).

The package contained on this advisory is defined by
:data:`RPM_UPDATERECORD_RPM_NAME` and the advisory is present in the standard
repositories, i.e. :data:`RPM_SIGNED_FIXTURE_URL` and
:data:`RPM_UNSIGNED_FIXTURE_URL`.
"""
RPM_ADVISORY_TEST_REMOVE_COUNT = 3
RPM_ADVISORY_TEST_ADDED_COUNT = 6


RPM_REPO_METADATA_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-repo-metadata/")
"""The URL to RPM repository with custom repository metadata."""

RPM_UPDATERECORD_RPM_NAME = "gorilla"
"""The name of the RPM named by :data:`RPM_UPDATERECORD_ID`."""

RPM_WITH_NON_ASCII_NAME = "rpm-with-non-ascii"

RPM_WITH_NON_ASCII_URL = urljoin(
    PULP_FIXTURES_BASE_URL,
    "rpm-with-non-ascii/{}-1-1.fc25.noarch.rpm".format(RPM_WITH_NON_ASCII_NAME),
)
"""The URL to an RPM with non-ascii metadata in its header."""

RPM_WITH_NON_UTF_8_NAME = "rpm-with-non-utf-8"

RPM_WITH_NON_UTF_8_URL = urljoin(
    PULP_FIXTURES_BASE_URL,
    "rpm-with-non-utf-8/{}-1-1.fc25.noarch.rpm".format(RPM_WITH_NON_UTF_8_NAME),
)
"""The URL to an RPM with non-UTF-8 metadata in its header."""

SRPM_UNSIGNED_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "srpm-unsigned/")
"""The URL to a repository with unsigned SRPM packages."""

SRPM_UNSIGNED_FIXTURE_ADVISORY_COUNT = 2
"""Count of advisories in the repository."""

SRPM_UNSIGNED_FIXTURE_PACKAGE_COUNT = 3
"""Count of packages in the repository."""

UPDATERECORD_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "rpm/advisories/")
"""The location of RPM UpdateRecords on the content endpoint."""

KICKSTART_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "rpm/distribution_trees/")
"""The location of RPM Distribution Trees on the content endpoint."""

RPM_KICKSTART_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-distribution-tree/")
RPM_DISTRIBUTION_TREE_CHANGED_ADDON_URL = urljoin(
    PULP_FIXTURES_BASE_URL, "rpm-distribution-tree-changed-addon/"
)
RPM_DISTRIBUTION_TREE_CHANGED_MAIN_URL = urljoin(
    PULP_FIXTURES_BASE_URL, "rpm-distribution-tree-changed-main/"
)
RPM_DISTRIBUTION_TREE_CHANGED_VARIANT_URL = urljoin(
    PULP_FIXTURES_BASE_URL, "rpm-distribution-tree-changed-variant/"
)

RPM_KICKSTART_CONTENT_NAME = "rpm.distribution_tree"

RPM_KICKSTART_COUNT = 1

RPM_KICKSTART_FIXTURE_SUMMARY = {
    RPM_KICKSTART_CONTENT_NAME: RPM_KICKSTART_COUNT,
    RPM_PACKAGE_CONTENT_NAME: 1,
    RPM_PACKAGECATEGORY_CONTENT_NAME: 1,
    RPM_PACKAGEENVIRONMENT_CONTENT_NAME: 1,
    RPM_PACKAGEGROUP_CONTENT_NAME: 1,
    RPM_PACKAGELANGPACKS_CONTENT_NAME: 1,
}

RPM_KICKSTART_REPOSITORY_ROOT_CONTENT = [
    ".treeinfo",
    "Dolphin/",
    "External/",
    "Land/",
    "LiveOS/",
    "Packages/",
    "Whale/",
    "images/",
]

PULP_FIXTURES_COMMON_URL = "https://github.com/pulp/pulp-fixtures/raw/master/common/"
PUBLIC_GPG_KEY_URL = urljoin(PULP_FIXTURES_COMMON_URL, "GPG-KEY-pulp-qe")
PRIVATE_GPG_KEY_URL = urljoin(PULP_FIXTURES_COMMON_URL, "GPG-PRIVATE-KEY-pulp-qe")

RPM_CUSTOM_REPO_METADATA_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-repo-metadata/")
RPM_CUSTOM_REPO_METADATA_CHANGED_FIXTURE_URL = urljoin(
    PULP_FIXTURES_BASE_URL, "rpm-repo-metadata-changed/"
)

RPM_MD5_REPO_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "rpm-with-md5/")

CENTOS6_URL = "http://mirror.centos.org/centos-6/6.10/os/x86_64/"
CENTOS7_URL = "http://mirror.centos.org/centos-7/7/os/x86_64/"
CENTOS8_KICKSTART_APP_URL = "http://mirror.centos.org/centos-8/8/AppStream/x86_64/kickstart/"
CENTOS8_KICKSTART_BASEOS_URL = "http://mirror.centos.org/centos-8/8/BaseOS/x86_64/kickstart/"
CENTOS8_APPSTREAM_URL = "http://mirror.centos.org/centos-8/8/AppStream/x86_64/os/"
CENTOS8_BASEOS_URL = "http://mirror.centos.org/centos-8/8/BaseOS/x86_64/os/"
EPEL7_URL = "https://dl.fedoraproject.org/pub/epel/7/x86_64/"
RPM_CDN_APPSTREAM_URL = "https://cdn.redhat.com/content/dist/rhel8/8.2/x86_64/appstream/os/"
RPM_CDN_BASEOS_URL = "https://cdn.redhat.com/content/dist/rhel8/8.2/x86_64/baseos/os/"
EPEL8_MIRRORLIST_URL = "https://mirrors.fedoraproject.org/mirrorlist?repo=epel-8&arch=x86_64"
EPEL8_PLAYGROUND_KICKSTART_URL = "http://mirrors.sonic.net/epel/playground/8/Everything/x86_64/os/"

PULP_TYPE_ADVISORY = "rpm.advisory"
PULP_TYPE_DISTRIBUTION_TREE = "rpm.distribution_tree"
PULP_TYPE_PACKAGE = "rpm.package"
PULP_TYPE_PACKAGE_CATEGORY = "rpm.packagecategory"
PULP_TYPE_PACKAGE_GROUP = "rpm.packagegroup"
PULP_TYPE_REPOMETADATA = "rpm.repo_metadata_file"
PULP_TYPE_MODULEMD = "rpm.modulemd"
PULP_TYPE_MODULEMD_DEFAULTS = "rpm.modulemd_defaults"
