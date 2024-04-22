#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from tempfile import NamedTemporaryFile

# Components
from ..features.gitlab import GitLabFeature
from ..prints.colors import Colors
from ..system.platform import Platform

# MigrationFeature class, pylint: disable=too-few-public-methods
class MigrationFeature:

    # GitLab projects migrate
    @staticmethod
    def gitlab_projects_migrate(options: Namespace) -> bool:

        # Header
        print(' ')

        # Input client
        input_gitlab = GitLabFeature(options.input_gitlab, options.input_token)
        print(f'{Colors.BOLD} - GitLab input: '
              f'{Colors.GREEN}{input_gitlab.url}'
              f'{Colors.RESET}')
        Platform.flush()

        # Output client
        output_gitlab = GitLabFeature(options.output_gitlab, options.output_token)
        print(f'{Colors.BOLD} - GitLab output: '
              f'{Colors.GREEN}{output_gitlab.url}'
              f'{Colors.RESET}')
        print(' ')
        Platform.flush()

        # Input group
        input_group = input_gitlab.group(options.input_group)
        print(f'{Colors.BOLD} - GitLab input group: '
              f'{Colors.GREEN}{input_group.path} ({input_group.description})'
              f'{Colors.RESET}')
        Platform.flush()

        # Output group
        output_group = output_gitlab.group(options.output_group)
        print(f'{Colors.BOLD} - GitLab output group: '
              f'{Colors.GREEN}{output_group.path} ({output_group.description})'
              f'{Colors.RESET}')
        print(' ')
        Platform.flush()

        # Iterate through projects
        for input_project in input_group.projects.list(get_all=True):

            # Show project details
            print(f'{Colors.BOLD} - GitLab input project: '
                  f'{Colors.YELLOW_LIGHT}{input_project.path} '
                  f'{Colors.CYAN}({input_project.description})'
                  f'{Colors.RESET}')

            # Ignore existing projects
            if not options.overwrite and input_project.path in [
                    output_project.path
                    for output_project in output_group.projects.list(get_all=True)
            ]:
                output_group_project = output_gitlab.project(
                    f'{output_group.full_path}/{input_project.path}')
                print(
                    f'{Colors.BOLD}   - Already exists in GitLab output: '
                    f'{Colors.CYAN}{output_group_project.path} ({output_group_project.description})'
                    f'{Colors.RESET}')
                print(' ')
                continue

            # Export project
            print(f'{Colors.BOLD}   - Exporting from: '
                  f'{Colors.GREEN}{options.input_group}'
                  f'{Colors.RESET}')
            with NamedTemporaryFile(suffix='.tar.gz') as file_export:
                input_gitlab.project_export(
                    file_export.name,
                    input_project.id,
                    options.keep_members,
                )

                # Existing project removal
                if options.overwrite:
                    output_gitlab.project_delete(
                        f'{output_group.full_path}/{input_project.path}')

                # Import project
                print(f'{Colors.BOLD}   - Importing to: '
                      f'{Colors.GREEN}{options.output_group}'
                      f'{Colors.RESET}')
                imported_project = output_gitlab.project_import(
                    file_export.name,
                    options.output_group,
                    input_project.path,
                    input_project.name,
                    options.overwrite,
                )
                output_project = output_gitlab.project(imported_project.id)

                # Configure project description
                if options.update_description:
                    description = f'{output_project.name[:1].capitalize()}{output_project.name[1:]}'
                    output_project.description = f'{description} - {output_group.description}'
                    output_project.save()
                    print(f'{Colors.BOLD}   - Updated description: '
                          f'{Colors.CYAN}{output_project.description}'
                          f'{Colors.RESET}')

                # Configure project members
                if not options.keep_members:
                    for member in output_project.members.list():
                        output_project.members.delete(member.id)
                    output_project.save()
                    print(f'{Colors.BOLD}   - Updated members: '
                          f'{Colors.GREEN}Success'
                          f'{Colors.RESET}')

                # Configure project avatar
                if options.set_avatar:
                    with open(options.set_avatar, 'rb') as project_avatar:
                        output_project.avatar = project_avatar
                        output_project.save()
                    print(f'{Colors.BOLD}   - Updated avatar: '
                          f'{Colors.CYAN}{options.set_avatar}'
                          f'{Colors.RESET}')

            # Show project result
            print(f'{Colors.BOLD}   - Migrated project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()

        # Result
        return True
