import enum
import hashlib

from pydantic import BaseModel

from ...utils.reviews_engine import get_review

from ...utils.gh_engine import get_files_list
from ...utils.red_engine import RedEngine
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
    
    repo_files_data_hashed = hashlib.md5(str(repo_files_data).encode()).hexdigest()
    red_engine = RedEngine()
    cached_data = await red_engine.get(repo_files_data_hashed)
    if cached_data:
        print('Cache hit!', repo_files_data_hashed)
        return GenerateReviewReponseScheme(review=cached_data.decode())

    total_data_size = sum([x.size for x in repo_files_data])
    if total_data_size > config.REPO_SIZE_LIMIT:
        return GenerateReviewReponseScheme(error='Total repo files size is too big. Max size is 1MB')

    try:
        review = get_review(repo_files_data, data.assignment_description, data.candidate_level)
    except Exception as e:
        return GenerateReviewReponseScheme(error=str(e))
    
    await red_engine.set(repo_files_data_hashed, review, expire=config.REPO_CACHE_TTL)
    print('Cache miss! Created new: ', repo_files_data_hashed)
    return GenerateReviewReponseScheme(review=review)
