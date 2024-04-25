#!/usr/bin/env python3

# Bundle class, pylint: disable=too-few-public-methods
class Bundle:

    # Names
    NAME: str = 'gitlab-projects-settings'

    # Details
    DESCRIPTION: str = 'Configure GitLab groups and projects settings automatically'

    # Sources
    REPOSITORY: str = 'https://gitlab.com/AdrianDC/gitlab-projects-settings'

    # Environment
    ENV_GITLAB_TOKEN: str = 'GITLAB_TOKEN'
