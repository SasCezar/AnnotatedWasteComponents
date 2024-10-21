from typing import List, Tuple, Dict

import requests
from loguru import logger

from entities import Project
from finder import ProjectFinder


class GitHubFinder(ProjectFinder):
    """
    Uses GitHub REST API to get GitHub repositories deemed abandoned.
    """

    def __init__(self, min_stars: int, last_pushed_date: str, language: str = "java",
                 only_archived: bool = True):
        """
        Initializes the GitHubFinder instance.

        Args:
            min_stars (int): The minimum number of stars a repository should have to be considered.
            last_pushed_date (str): The date until which repositories are considered for abandonment.
            language (str, optional): The programming language of the repositories (default is "java").
            only_archived (bool, optional): Flag to use only archived repositories (default is True).
        """
        self.base_url = "https://api.github.com/search/repositories"
        self.min_stars = min_stars
        self.last_pushed_date = last_pushed_date
        self.language = language
        self.only_archived = only_archived

        logger.info(f"Initialized GitHubFinder")

    def find_projects(self, amount: int = 10) -> List[Project]:
        """
        Retrieves abandoned projects.

        Args:
            amount (int): The number of abandoned projects to retrieve (default is 10).

        Returns:
            List[Dict]: A list of dictionaries representing abandoned projects.
        """
        projects = []
        page = 1
        per_page = min(amount, 100)  # GitHub API allows max 100 results per page

        while len(projects) < amount:
            params, headers = self._create_request(per_page, page)
            response = requests.get(self.base_url, params=params, headers=headers)

            if response.status_code == 200:
                res = response.json().get("items", [])
                for repo in res:
                    projects.append(Project(
                        name=repo["full_name"].replace("/", "|"),
                        remote=repo["html_url"],
                        description=repo["description"],
                        stargazers_count=repo["stargazers_count"],
                        language=repo["language"],
                        archived=repo["archived"],
                        pushed_at=repo["pushed_at"]
                    ))

                if len(res) < per_page:
                    # If the response contains fewer items than `per_page`, we've reached the last page
                    break
            else:
                response.raise_for_status()

            page += 1

        return projects[:amount]

    def _create_request(self, per_page: int, page: int) -> Tuple[Dict, Dict]:
        """
        Create request parameters and headers for GitHub repository search.

        Args:
            per_page (int): The number of results to retrieve per page.
            page (int): The current page number to fetch.

        Returns:
            Tuple[Dict, Dict]: A tuple containing request parameters and headers.
        """
        query = f"language:{self.language} stars:>={self.min_stars} pushed:<{self.last_pushed_date}"
        if self.only_archived:
            query += " archived:true"

        params = {"q": query, "per_page": per_page, "page": page}
        headers = {"Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2022-11-28"}

        return params, headers
