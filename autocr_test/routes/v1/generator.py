import asyncio
import enum
import json

from pydantic import BaseModel

from ...utils.reviews_engine import get_review

from ...utils.gh_engine import get_files_list
from ...utils.red_engine import RedEngine
from ...utils.router_helper import ApiRouterHelper
import httpx
from ...utils.config import config
from ...models.RepoFile import RepoFileModel, RepoFileType

router = ApiRouterHelper(path='generator', tags=['generator'])

class CandidateLevel(str, enum.Enum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'

class GenerateReviewRequestScheme(BaseModel):
    assignement_description: str
    github_repo_url: str
    candidate_level: CandidateLevel

class GenerateReviewReponseScheme(BaseModel):
    review: str

@router.version(1).post("/generate_review")
async def generate_review(data: GenerateReviewRequestScheme) -> GenerateReviewReponseScheme:
    repo_url_parts = data.github_repo_url.split('github.com/')
    repo =  repo_url_parts[1]
    url = f"https://api.github.com/repos/{repo}/contents"

    repo_files_data = await get_files_list(url)

    print('Total repo size:', sum([x.size for x in repo_files_data])/1024, 'kb')
    return GenerateReviewReponseScheme(review=get_review(repo_files_data, data.assignement_description, data.candidate_level))
