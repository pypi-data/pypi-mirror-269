'''Utility functions for the API.'''

from typing import Tuple, Literal
from re import compile


class SemanticVersion:
    RE = compile(r'^(\d+)\.(\d+)\.(\d+)\.*(\d*)')

    @staticmethod
    def parse(version: str) -> Tuple[int, ...]:
        ''' 'Parse a three-dot or four-dot semantic version into four parts.

        version

        - `three-dot`: <major>.<minor>.<patch>
            - will be auto converted to a four dot version with build set to 0
        - `four-dot`: <major>.<minor>.<patch>.<build>
        '''

        match = SemanticVersion.RE.match(version)
        if not match:
            raise ValueError(f'Invalid {version}, expecting format <major>.<minor>.<patch>.[build]')

        major, minor, patch = map(int, match.group(1, 2, 3))

        build: int = 0
        if match.group(4):
            build = int(match.group(4))

        return (major, minor, patch, build)

    @staticmethod
    def compare(v1: str, v2: str) -> Literal[-1, 0, 1]:
        '''Compare three-dot semantic versions.

        return
        - -1 if v1 is less than v2
        -  0 if v1 is equal to v2
        -  1 if v1 is greater than v2
        '''

        v1_parts = SemanticVersion.parse(v1)
        v2_parts = SemanticVersion.parse(v2)

        if v1_parts < v2_parts:
            return -1
        elif v1_parts > v2_parts:
            return 1

        return 0
