#!/usr/bin/env python3

# Standard libraries
from argparse import (_ArgumentGroup, ArgumentParser, Namespace, RawTextHelpFormatter)
from os import environ
from sys import exit as sys_exit

# Components
from ..features.migration import MigrationFeature
from ..package.bundle import Bundle
from ..package.version import Version
from ..system.platform import Platform

# Main
def main() -> None:

    # Variables
    group: _ArgumentGroup
    result: bool = False

    # Arguments creation
    parser: ArgumentParser = ArgumentParser(
        prog=Bundle.NAME,
        description=f'{Bundle.NAME}: Synchronize issues from a GitLab project to another',
        add_help=False, formatter_class=RawTextHelpFormatter)

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

    # Arguments migration definitions
    group = parser.add_argument_group('migration arguments')
    group.add_argument(
        '-I',
        dest='input_token',
        default=environ.get(Bundle.ENV_GITLAB_INPUT_TOKEN, ''), #
        help=
        f'Input GitLab API token (default: {Bundle.ENV_GITLAB_INPUT_TOKEN} environment)')
    group.add_argument(
        '-O',
        dest='output_token',
        action='store',
        default=environ.get(Bundle.ENV_GITLAB_OUTPUT_TOKEN, ''), #
        help=
        f'Output GitLab API token (default: {Bundle.ENV_GITLAB_OUTPUT_TOKEN} environment'
        ' or input_token)')
    group.add_argument(
        '--keep-members',
        dest='keep_members',
        action='store_true',
        help='Keep input members after importing on output GitLab',
    )
    group.add_argument(
        '--set-avatar',
        dest='set_avatar',
        action='store',
        metavar='FILE',
        help='Set imported projects\' avatar to a specific image file',
    )
    group.add_argument(
        '--update-description',
        dest='update_description',
        action='store_true',
        help='Update project description automatically inside output group',
    )

    # Arguments positional definitions
    group = parser.add_argument_group('positional arguments')
    group.add_argument(
        dest='input_gitlab',
        action='store',
        nargs='?',
        default='https://gitlab.com',
        help='Input GitLab URL (default: https://gitlab.com)',
    )
    group.add_argument(
        dest='input_group',
        action='store',
        nargs='?',
        help='Input GitLab group',
    )
    group.add_argument(
        dest='output_gitlab',
        action='store',
        nargs='?',
        default='https://gitlab.com',
        help='Output GitLab URL (default: https://gitlab.com)',
    )
    group.add_argument(
        dest='output_group',
        action='store',
        nargs='?',
        default='',
        help='Output GitLab group (default: input_group)',
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

    # Version informations
    if options.version:
        print(
            f'{Bundle.NAME} {Version.get()} from {Version.path()} (python {Version.python()})'
        )
        Platform.flush()
        sys_exit(0)

    # Arguments validation
    if not options.input_gitlab or not options.input_group or not options.output_gitlab:
        print(' ')
        parser.print_help()
        print(' ')
        Platform.flush()
        sys_exit(1)

    # Arguments adaptations
    if not options.output_token:
        options.output_token = options.input_token
    if not options.output_group:
        options.output_group = options.input_group

    # Header
    print(' ')
    Platform.flush()

    # Migrate GitLab projects
    result = MigrationFeature.gitlab_projects_migrate(options)

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
