import asyncio
import httpx
from autocr_test.models.RepoFile import RepoFileModel, RepoFileType
from ..utils.config import config

async def get_files_list(url: str) -> list[RepoFileModel]:
    repo_files_data_raw = []
    async with httpx.AsyncClient() as client:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {config.GITHUB_TOKEN}'
        }
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Error fetching github repo files. Status code: {response.status_code}\nMessage: '+response.text)
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

async def get_file_content(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            print('Error fetching file content: '+response.text)
            return ''
        return response.text