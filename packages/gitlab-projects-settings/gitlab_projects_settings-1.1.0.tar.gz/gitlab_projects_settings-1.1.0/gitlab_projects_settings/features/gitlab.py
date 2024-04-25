#!/usr/bin/env python3

# Standard libraries
from typing import List

# Modules libraries
from gitlab import Gitlab
from gitlab.exceptions import GitlabListError
from gitlab.v4.objects import Group, Project

# GitLabFeature class
class GitLabFeature:

    # Members
    __dry_run: bool = False
    __gitlab: Gitlab

    # Constructor
    def __init__(self, url: str, token: str, dry_run: bool = False) -> None:
        self.__dry_run = dry_run
        self.__gitlab = Gitlab(url, private_token=token)
        self.__gitlab.auth()

    # Group
    def group(self, criteria: str) -> Group:
        return self.__gitlab.groups.get(criteria)

    # Group reset members
    def group_reset_members(self, criteria: str) -> None:

        # Remove group members
        group = self.group(criteria)
        for member in group.members.list():
            if not self.__dry_run:
                group.members.delete(member.id)

        # Save group
        if not self.__dry_run:
            group.save()

    # Group set avatar
    def group_set_avatar(self, criteria: str, file: str) -> None:

        # Set group avatar
        group = self.group(criteria)
        with open(file, 'rb') as avatar:
            group.avatar = avatar

            # Save group
            if not self.__dry_run:
                group.save()

    # Group set description
    def group_set_description(self, criteria: str, description: str) -> None:

        # Set group description
        group = self.group(criteria)
        group.description = description

        # Save group
        if not self.__dry_run:
            group.save()

    # Project
    def project(self, criteria: str) -> Project:
        return self.__gitlab.projects.get(criteria)

    # Project protect branches
    def project_protect_branches(self, criteria: str) -> List[str]:

        # Validate project feature
        result: List[str] = []
        project = self.project(criteria)
        try:
            assert project.branches.list()
        except (AssertionError, GitlabListError):
            return result

        # Acquire project, branches and protected branches
        branches = [branch.name for branch in project.branches.list()]
        protectedbranches = [
            protectedbranch.name for protectedbranch in project.protectedbranches.list()
        ]

        # Protect main/master
        for branch in ['main', 'master']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 40,
                        'push_access_level': 40,
                        'allow_force_push': False
                    })
                result += [branch]

        # Protect develop
        for branch in ['develop']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 40,
                        'push_access_level': 40,
                        'allow_force_push': True
                    })
                result += [branch]

        # Protect staging
        for branch in ['staging']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 30,
                        'push_access_level': 30,
                        'allow_force_push': True
                    })
                result += [branch]

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project protect tags, pylint: disable=too-many-branches
    def project_protect_tags(self, criteria: str, protect_level: str) -> List[str]:

        # Validate project feature
        result: List[str] = []
        project = self.project(criteria)
        try:
            assert project.tags.list()
        except (AssertionError, GitlabListError):
            return result

        # Prepare access level
        access_level: int
        if protect_level == 'no-one':
            access_level = 0
        elif protect_level == 'admins':
            access_level = 60
        elif protect_level == 'maintainers':
            access_level = 40
        elif protect_level == 'developers':
            access_level = 30
        else:
            raise SyntaxError(f'Unknown protection level: {access_level}')

        # Acquire protected tags
        protectedtags = [
            protectedtag.name for protectedtag in project.protectedtags.list()
        ]

        # Update protected tags
        for protectedtag in project.protectedtags.list():
            protectedtag_level = protectedtag.create_access_levels[0]['access_level']
            if protectedtag_level != 0 and (access_level == 0
                                            or protectedtag_level < access_level):
                name = protectedtag.name
                if not self.__dry_run:
                    protectedtag.delete()
                    project.protectedtags.create({
                        'name': name,
                        'create_access_level': access_level
                    })
                result += [name]

        # Protect unprotected tags
        for tag in project.tags.list():
            if tag.name not in protectedtags:
                if not self.__dry_run:
                    project.protectedtags.create({
                        'name': tag.name,
                        'create_access_level': access_level
                    })
                result += [tag.name]

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        result.sort()
        return result

    # Project reset features, pylint: disable=too-many-branches,too-many-statements
    def project_reset_features(self, criteria: str) -> List[str]:

        # Variables
        result: List[str] = []
        project = self.__gitlab.projects.get(criteria, statistics=True)

        # Disable unused features
        if project.issues_enabled and not project.issues.list(get_all=False):
            project.issues_enabled = False
            result += ['Issues']
        try:
            assert project.commits.list(get_all=False)
        except (AssertionError, GitlabListError):
            if project.repository_access_level != 'disabled':
                project.repository_access_level = 'disabled'
                result += ['Repository']
        if project.merge_requests_enabled and not project.mergerequests.list(
                get_all=False):
            project.merge_requests_enabled = False
            result += ['Merge requests']
        if project.forking_access_level != 'disabled' and not project.forks.list(
                get_all=False):
            project.forking_access_level = 'disabled'
            result += ['Forks']
        if project.lfs_enabled and project.statistics['lfs_objects_size'] == 0:
            project.lfs_enabled = False
            result += ['Git LFS']
        if project.jobs_enabled and not project.jobs.list(get_all=False):
            project.jobs_enabled = False
            result += ['CI/CD']
        if project.container_registry_enabled and not project.repositories.list(
                get_all=False):
            project.container_registry_enabled = False
            result += ['Container registry']
        if project.analytics_access_level != 'disabled':
            project.analytics_access_level = 'disabled'
            result += ['Analytics']
        if project.security_and_compliance_access_level != 'disabled':
            project.security_and_compliance_access_level = 'disabled'
            result += ['Security and Compliance']
        if project.wiki_enabled and not project.wikis.list(get_all=False):
            project.wiki_enabled = False
            result += ['Wiki']
        if project.snippets_enabled and not project.snippets.list(get_all=False):
            project.snippets_enabled = False
            result += ['Snippets']
        if project.packages_enabled and not project.packages.list(get_all=False):
            project.packages_enabled = False
            result += ['Package registry']
        if project.model_experiments_access_level != 'disabled':
            project.model_experiments_access_level = 'disabled'
            result += ['Model experiments']
        if project.model_registry_access_level != 'disabled':
            project.model_registry_access_level = 'disabled'
            result += ['Model registry']
        if project.pages_access_level != 'disabled':
            project.pages_access_level = 'disabled'
            result += ['Pages']
        if project.monitor_access_level != 'disabled':
            project.monitor_access_level = 'disabled'
            result += ['Monitor']
        try:
            assert project.environments.list(get_all=False)
        except (AssertionError, GitlabListError):
            if project.environments_access_level != 'disabled':
                project.environments_access_level = 'disabled'
                result += ['Environments']
        if project.feature_flags_access_level != 'disabled':
            project.feature_flags_access_level = 'disabled'
            result += ['Feature flags']
        if project.infrastructure_access_level != 'disabled':
            project.infrastructure_access_level = 'disabled'
            result += ['Infrastructure']
        if project.releases_access_level != 'disabled' and not project.releases.list(
                get_all=False):
            project.releases_access_level = 'disabled'
            result += ['Releases']
        if project.service_desk_enabled:
            project.service_desk_enabled = False
            result += ['Service Desk']
        if project.auto_devops_enabled:
            project.auto_devops_enabled = False
            result += ['Auto DevOps']

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project reset members
    def project_reset_members(self, criteria: str) -> None:

        # Remove project members
        project = self.project(criteria)
        for member in project.members.list():
            if not self.__dry_run:
                project.members.delete(member.id)

        # Save project
        if not self.__dry_run:
            project.save()

    # Project set avatar
    def project_set_avatar(self, criteria: str, file: str) -> None:

        # Set project avatar
        project = self.project(criteria)
        with open(file, 'rb') as avatar:
            project.avatar = avatar
            if not self.__dry_run:
                project.save()

    # Project set description
    def project_set_description(self, criteria: str, description: str) -> None:
        project = self.project(criteria)
        project.description = description
        if not self.__dry_run:
            project.save()

    # URL
    @property
    def url(self) -> str:
        return str(self.__gitlab.api_url)
