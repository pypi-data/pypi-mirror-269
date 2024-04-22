#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from tempfile import NamedTemporaryFile

# Components
from ..features.gitlab import GitLabFeature
from ..system.platform import Platform

# MigrationFeature class, pylint: disable=too-few-public-methods
class MigrationFeature:

    # GitLab projects migrate
    @staticmethod
    def gitlab_projects_migrate(options: Namespace) -> bool:

        # Input client
        input_gitlab = GitLabFeature(options.input_gitlab, options.input_token)
        print(f' - GitLab input: {input_gitlab.url}')
        Platform.flush()

        # Output client
        output_gitlab = GitLabFeature(options.output_gitlab, options.output_token)
        print(f' - GitLab output: {output_gitlab.url}')
        Platform.flush()
        print('')

        # Input group
        input_group = input_gitlab.group(options.input_group)
        print(f' - GitLab input group: {input_group.path} ({input_group.description})')
        Platform.flush()

        # Output group
        output_group = output_gitlab.group(options.output_group)
        print(f' - GitLab output group: {output_group.path} ({output_group.description})')
        Platform.flush()
        print('')

        # Iterate through projects
        for input_project in input_group.projects.list(get_all=True):

            # Show project details
            print(
                f' - GitLab input project: {input_project.path} ({input_project.description})'
            )

            # Ignore existing projects
            if input_project.path in [
                    output_project.path
                    for output_project in output_group.projects.list(get_all=True)
            ]:
                output_group_project = output_gitlab.project(
                    f'{output_group.full_path}/{input_project.path}')
                print(
                    '   - Already exists in GitLab output:'
                    f' {output_group_project.path} ({output_group_project.description})')
                print('')
                continue

            # Export project
            print(f'   - Exporting project from: {options.input_group}')
            with NamedTemporaryFile(suffix='.tar.gz') as file_export:
                input_gitlab.project_export(file_export.name, input_project.id,
                                            options.keep_members)

                # Import project
                print(f'   - Importing project to: {options.output_group}')
                imported_project = output_gitlab.project_import(
                    file_export.name, options.output_group, input_project.path,
                    input_project.name)
                output_project = output_gitlab.project(imported_project.id)

                # Configure project description
                if options.update_description:
                    description = f'{output_project.name[:1].capitalize()}{output_project.name[1:]}'
                    output_project.description = f'{description} - {output_group.description}'
                    output_project.save()
                    print(
                        f'   - Updated project description: {output_project.description}')

                # Configure project members
                if not options.keep_members:
                    for member in output_project.members.list():
                        output_project.members.delete(member.id)
                    output_project.save()
                    print('   - Updated project members: Successfully reset')

                # Configure project avatar
                if options.set_avatar:
                    with open(options.set_avatar, 'rb') as project_avatar:
                        output_project.avatar = project_avatar
                    output_project.save()
                    print(f'   - Updated project avatar: {options.set_avatar}')

            # Show project result
            print('   - Migrated project: Successfully')
            print('')

        # Result
        return True
