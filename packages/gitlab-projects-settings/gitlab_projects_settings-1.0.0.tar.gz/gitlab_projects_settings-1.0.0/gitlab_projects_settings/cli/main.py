#!/usr/bin/env python3

# Standard libraries
from argparse import (_ArgumentGroup, ArgumentParser, Namespace, RawTextHelpFormatter)
from os import environ
from sys import exit as sys_exit

# Components
from ..features.settings import SettingsFeature
from ..package.bundle import Bundle
from ..package.version import Version
from ..prints.colors import Colors
from ..system.platform import Platform

# Main, pylint: disable=too-many-statements
def main() -> None:

    # Variables
    group: _ArgumentGroup
    result: bool = False

    # Arguments creation
    parser: ArgumentParser = ArgumentParser(
        prog=Bundle.NAME,
        description=f'{Bundle.NAME}: {Bundle.DESCRIPTION}',
        add_help=False,
        formatter_class=RawTextHelpFormatter,
    )

    # Arguments internal definitions
    group = parser.add_argument_group('internal arguments')
    group.add_argument(
        '-h',
        '--help',
        dest='help',
        action='store_true',
        help='Show this help message',
    )
    group.add_argument(
        '--version',
        dest='version',
        action='store_true',
        help='Show the current version',
    )

    # Arguments credentials definitions
    group = parser.add_argument_group('credentials arguments')
    group.add_argument(
        '-t',
        dest='token',
        default=environ.get(Bundle.ENV_GITLAB_TOKEN, ''), #
        help=f'GitLab API token (default: {Bundle.ENV_GITLAB_TOKEN} environment)',
    )

    # Arguments common settings definitions
    group = parser.add_argument_group('common settings arguments')
    group.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        help='Enable dry run mode to check without saving',
    )
    group.add_argument(
        '--avoid-group',
        dest='avoid_group',
        action='store_true',
        help='Avoid affecting parent group settings',
    )
    group.add_argument(
        '--avoid-subgroups',
        dest='avoid_subgroups',
        action='store_true',
        help='Avoid affecting children subgroups settings',
    )
    group.add_argument(
        '--avoid-projects',
        dest='avoid_projects',
        action='store_true',
        help='Avoid affecting children projects settings',
    )

    # Arguments general settings definitions
    group = parser.add_argument_group('general settings arguments')
    group.add_argument(
        '--reset-features',
        dest='reset_features',
        action='store_true',
        help='Reset features of GitLab projects based on usage',
    )
    group.add_argument(
        '--reset-members',
        dest='reset_members',
        action='store_true',
        help='Reset members of GitLab projects and groups',
    )
    group.add_argument(
        '--set-avatar',
        dest='set_avatar',
        action='store',
        metavar='FILE',
        help='Set avatar of GitLab projects and groups',
    )
    group.add_argument(
        '--set-description',
        dest='set_description',
        action='store',
        metavar='DESCRIPTION',
        help='Set description of GitLab projects and groups',
    )
    group.add_argument(
        '--update-description',
        dest='update_description',
        action='store_true',
        help='Update description of GitLab projects and groups automatically',
    )

    # Arguments repository settings definitions
    group = parser.add_argument_group('repository settings arguments')
    group.add_argument(
        '--protect-branches',
        dest='protect_branches',
        action='store_true',
        help='Protect branches with default master/main, develop and staging',
    )
    group.add_argument(
        '--protect-tags',
        dest='protect_tags',
        action='store',
        metavar='LEVEL',
        help='Protect tags at level [no-one,admins,maintainers,developers]',
    )

    # Arguments positional definitions
    group = parser.add_argument_group('positional arguments')
    group.add_argument(
        dest='gitlab',
        action='store',
        nargs='?',
        default='https://gitlab.com',
        help='GitLab URL (default: https://gitlab.com)',
    )
    group.add_argument(
        dest='path',
        action='store',
        nargs='?',
        help='GitLab group or project path',
    )

    # Arguments parser
    options: Namespace = parser.parse_args()

    # Help informations
    if options.help:
        print(' ')
        parser.print_help()
        print(' ')
        Platform.flush()
        sys_exit(0)

    # Prepare colors
    Colors.prepare()

    # Version informations
    if options.version:
        print(
            f'{Bundle.NAME} {Version.get()} from {Version.path()} (python {Version.python()})'
        )
        Platform.flush()
        sys_exit(0)

    # Arguments validation
    if not options.token or not options.gitlab or not options.path:
        print(' ')
        parser.print_help()
        print(' ')
        Platform.flush()
        sys_exit(1)

    # Header
    print(' ')
    Platform.flush()

    # Configure GitLab projects
    result = SettingsFeature.entrypoint(options)

    # Footer
    print(' ')
    Platform.flush()

    # Result
    if result:
        sys_exit(0)
    else:
        sys_exit(1)

# Entrypoint
if __name__ == '__main__': # pragma: no cover
    main()
