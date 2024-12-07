import asyncio
import backoff
import httpx
from autocr_test.models.RepoFile import RepoFileModel, RepoFileType
from ..utils.config import config

class GithubRateLimitException(Exception):
    pass

class GithubRepoNotFoundException(Exception):
    pass

class GithubBadCredentialsException(Exception):
    pass

exceptions = {
    401: GithubBadCredentialsException,
    404: GithubRepoNotFoundException,
    403: GithubRateLimitException,
    429: GithubRateLimitException
}

def get_github_exception(status_code):
    return exceptions.get(status_code, Exception)

def get_github_exception_status_code(exception):
    for status_code, exception_type in exceptions.items():
        if isinstance(exception, exception_type):
            return status_code
    return 500

@backoff.on_exception(backoff.constant, ValueError, interval=1, max_tries=5)
async def get_files_list(url: str) -> list[RepoFileModel]:
    """Get files list from github repo"""
    repo_files_data_raw = []
    async with httpx.AsyncClient() as client:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {config.GITHUB_TOKEN}'
        }
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise get_github_exception(response.status_code)(response.text)
        repo_files_data_raw = response.json()

    repo_files_data = [RepoFileModel(**x) for x in repo_files_data_raw]

    files_jobs = {}
    for file in repo_files_data:
        if file.type == RepoFileType.DIRECTORY:
            files_jobs["file_"+file.url] = get_files_list(file.url)
        else:
            files_jobs["file_content_"+file.download_url] = get_file_content(file.download_url)

    files_jobs_results = await asyncio.gather(*files_jobs.values())
    for i, file in enumerate(repo_files_data):
        if file.type == RepoFileType.DIRECTORY:
            file.files = files_jobs_results[i]
        else:
            file.content = files_jobs_results[i]

    return repo_files_data


@backoff.on_exception(backoff.constant, ValueError, interval=1, max_tries=5)
async def get_file_content(url: str) -> str:
    """Get file content from github repo"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise get_github_exception(response.status_code)(response.text)
        return response.text