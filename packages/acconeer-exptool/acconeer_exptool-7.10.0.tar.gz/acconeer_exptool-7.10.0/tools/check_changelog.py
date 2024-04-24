# Copyright (c) Acconeer AB, 2022-2023
# All rights reserved

"""This script checks whether CHANGELOG refers to the same version as the current git tag."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Optional

from packaging.version import Version


VERSION_PATTERN = r"v?\d+\.\d+\.\d+"
EMPTY_UNRELEASED_CHANGELOG = """# Unreleased Changelog

## Unreleased

### Added

### Changed

### Fixed

### Removed
"""


def utf8_subprocess_output(*args: str) -> str:
    return subprocess.check_output(args, encoding="utf-8").strip()


def get_commit_sha_of_git_tag(git_tag: str) -> str:
    return utf8_subprocess_output("git", "rev-list", "-n", "1", git_tag)


def get_current_commit_sha() -> str:
    return utf8_subprocess_output("git", "rev-parse", "--verify", "HEAD")


def get_current_commit_prepare_release_version() -> Optional[str]:
    commit_title = utf8_subprocess_output("git", "log", "-n1", "--pretty=format:%s")
    match = re.match(rf"Prepare release ({VERSION_PATTERN})", commit_title)
    return None if match is None else match.groups()[0]


def get_most_recent_git_tag() -> str:
    return utf8_subprocess_output("git", "describe", "--abbrev=0", "--tags")


def get_current_commit_tag() -> Optional[str]:
    recent_tag = get_most_recent_git_tag()
    return (
        recent_tag if get_current_commit_sha() == get_commit_sha_of_git_tag(recent_tag) else None
    )


def get_first_match_in_string(pattern: str, string: str, *, group: int = 0) -> Optional[str]:
    """
    Searches for the first match of `pattern` in `string`. Returns `group`:th group (default 0)
    """
    valid_group_numbers = range(0, re.compile(pattern).groups + 1)

    if group not in valid_group_numbers:
        raise ValueError(
            f"`group` is out-of range. group={group} should be "
            + f"in [{valid_group_numbers[0]}, {valid_group_numbers[-1]}]"
        )

    match = re.search(pattern, string)
    return None if (match is None) else match.group(group)


def get_number_of_matches_in_string(pattern: str, string: str) -> int:
    match = re.findall(pattern, string)

    return len(match)


def main() -> None:
    FILE_PATH = "CHANGELOG.md"
    UNRELEASED_FILE_PATH = "UNRELEASED_CHANGELOG.md"

    changelog = Path(FILE_PATH)
    unreleased_changelog = Path(UNRELEASED_FILE_PATH)

    status = True

    if get_number_of_matches_in_string(r"## Unreleased", changelog.read_text()) > 0:
        print("Changelog contains illegal 'Unreleased' headline")
        status = False

    if (
        get_number_of_matches_in_string(r"## " + VERSION_PATTERN, unreleased_changelog.read_text())
        > 0
    ):
        print("Unreleased Changelog contains illegal version tag headline")
        status = False

    # The version if this is a "Prepare release" commit.
    prepare_release_version = get_current_commit_prepare_release_version()

    # The current git tag
    git_tag = get_current_commit_tag()

    version_tag = prepare_release_version or git_tag

    if version_tag is None or Version(version_tag).is_prerelease:
        exit(0 if status else 1)

    if prepare_release_version is not None:
        print(f"Current commit is a prepare commit for {prepare_release_version}.")
    elif git_tag is not None:
        print(f"Current commit is tagged ({git_tag}).")
    else:
        assert False

    first_match = get_first_match_in_string(VERSION_PATTERN, changelog.read_text())
    print(f'Found "{first_match}" in {FILE_PATH}', end=" ... ")

    if first_match == version_tag:
        print(f"Which matches {version_tag} exactly.")
    else:
        print(f'Which does not match "{version_tag}".')
        status = False

    if unreleased_changelog.read_text() != EMPTY_UNRELEASED_CHANGELOG:
        print("Unreleased changelog is not cleared")
        status = False

    exit(0 if status else 1)


if __name__ == "__main__":
    main()
