import enum

from pydantic import BaseModel

from autocr_test.utils.cache_engine import get_cache, set_cache

from ...utils.reviews_engine import get_review

from ...utils.gh_engine import get_files_list
from ...utils.router_helper import ApiRouterHelper
from ...utils.config import config

router = ApiRouterHelper(path='generator', tags=['generator'])

class CandidateLevel(str, enum.Enum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'

class GenerateReviewRequestScheme(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: CandidateLevel

class GenerateReviewReponseScheme(BaseModel):
    review: str = None
    error: str = None

@router.version(1).post("/generate_review")
async def generate_review(data: GenerateReviewRequestScheme) -> GenerateReviewReponseScheme:
    """Analyze repo and provide the review"""
    repo_url_parts = data.github_repo_url.split('github.com/')
    repo =  repo_url_parts[1]
    url = f"https://api.github.com/repos/{repo}/contents"

    try:
        repo_files_data = await get_files_list(url)
    except Exception as e:
        return GenerateReviewReponseScheme(error=str(e))
    
    cached_data = await get_cache(repo_files_data)
    if cached_data:
        return GenerateReviewReponseScheme(review=cached_data)

    try:
        review = get_review(repo_files_data, data.assignment_description, data.candidate_level)
    except Exception as e:
        return GenerateReviewReponseScheme(error=str(e))
    
    await set_cache(repo_files_data, review)
    return GenerateReviewReponseScheme(review=review)
