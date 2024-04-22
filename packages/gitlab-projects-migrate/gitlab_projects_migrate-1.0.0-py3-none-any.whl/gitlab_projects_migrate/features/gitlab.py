#!/usr/bin/env python3

# Standard libraries
from os import remove
from os.path import join
from shutil import make_archive, unpack_archive
from tempfile import TemporaryDirectory
from time import sleep

# Modules libraries
from gitlab import Gitlab
from gitlab.v4.objects import Group, Project

# GitLabFeature class
class GitLabFeature:

    # Members
    __gitlab: Gitlab

    # Constructor
    def __init__(self, url: str, token: str) -> None:
        self.__gitlab = Gitlab(url, private_token=token)
        self.__gitlab.auth()

    # Group
    def group(self, criteria: str) -> Group:
        return self.__gitlab.groups.get(criteria)

    # Project
    def project(self, criteria: str) -> Project:
        return self.__gitlab.projects.get(criteria)

    # Project export
    def project_export(self, archive: str, criteria: str,
                       keep_members: bool = False) -> None:

        # Create project export
        project = self.project(criteria)
        project_export = project.exports.create()
        project_export.refresh()
        while project_export.export_status not in ['finished', 'failed']:
            sleep(1)
            project_export.refresh()

        # Failed project export
        if project_export.export_status == 'failed':
            raise RuntimeError(project_export)

        # Download project export
        with open(archive, 'wb') as file:
            project_export.download(streamed=True, action=file.write)

        # Reset project members
        if not keep_members:
            with TemporaryDirectory() as temp_directory:
                stem = archive
                if stem.endswith('.tar.gz'):
                    stem = stem[:-len('.tar.gz')]
                unpack_archive(archive, temp_directory, 'gztar')
                remove(join(temp_directory, 'tree', 'project', 'project_members.ndjson'))
                remove(archive)
                make_archive(stem, 'gztar', temp_directory)

    # Project import
    def project_import(self, archive: str, group: str, path: str, name: str) -> Project:
        with open(archive, 'rb') as file:
            project_imported = self.__gitlab.projects.import_project(
                file,
                path=path,
                name=name,
                namespace=group,
                overwrite=False,
            )

        # Upload project import
        project_import = self.__gitlab.projects.get(project_imported['id'],
                                                    lazy=True).imports.get()
        while project_import.import_status not in ['finished', 'failed']:
            sleep(1)
            project_import.refresh()

        # Result
        return project_import

    # URL
    @property
    def url(self) -> str:
        return str(self.__gitlab.api_url)
