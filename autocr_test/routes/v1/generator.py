import enum

import backoff
from fastapi import Response
from pydantic import BaseModel, Field

from autocr_test.utils.cache_engine import get_cache, set_cache

from ...utils.reviews_engine import get_review

from ...utils.gh_engine import get_files_list, get_github_exception_status_code
from ...utils.router_helper import ApiRouterHelper
from ...utils.config import config

router = ApiRouterHelper(path='generator', tags=['generator'])

class CandidateLevel(str, enum.Enum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'

class GenerateReviewRequestScheme(BaseModel):
    assignment_description: str
    github_repo_url: str = Field(pattern=r'^https://github.com/.*')
    candidate_level: CandidateLevel

class GenerateReviewReponseScheme(BaseModel):
    review: str = None
    error: str = None
    cache_hit: bool = False

@router.version(1).post("/generate_review")
@backoff.on_exception(backoff.constant, ValueError, interval=1, max_tries=5)
async def generate_review(data: GenerateReviewRequestScheme, resp: Response) -> GenerateReviewReponseScheme:
    """Analyze repo and provide the review"""
    repo_url_parts = data.github_repo_url.split('https://github.com/')
    repo =  repo_url_parts[1]
    url = f"https://api.github.com/repos/{repo}/contents"

    try:
        repo_files_data = await get_files_list(url)
    except Exception as e:
        resp.status_code = get_github_exception_status_code(e)
        return GenerateReviewReponseScheme(error=str(e))

    if len(str(repo_files_data)) > config.REPO_SIZE_LIMIT:
        resp.status_code = 413
        return GenerateReviewReponseScheme(error="Repo is too large")

    cached_data = await get_cache(repo_files_data, assignment=data.assignment_description)
    if cached_data:
        return GenerateReviewReponseScheme(review=cached_data, cache_hit=True)

    try:
        review = get_review(repo_files_data, data.assignment_description, data.candidate_level)
    except Exception as e:
        return GenerateReviewReponseScheme(error=str(e))
    
    await set_cache(repo_files_data, data.assignment_description, review)
    return GenerateReviewReponseScheme(review=review)
