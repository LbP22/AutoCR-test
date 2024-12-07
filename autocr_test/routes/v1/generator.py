import enum

from pydantic import BaseModel
from ...utils.red_engine import RedEngine
from ...utils.router_helper import ApiRouterHelper

router = ApiRouterHelper(path='generator', tags=['generator'])

class CandidateLevel(str, enum.Enum):
    JUNIOR = 'j'
    MIDDLE = 'm'
    SENIOR = 's'

class GenerateReviewRequestScheme(BaseModel):
    assignement_description: str
    github_repo_url: str
    candidate_level: CandidateLevel

class GenerateReviewReponseScheme(BaseModel):
    review: str

@router.version(1).post("/generate_review")
async def generate_review(data: GenerateReviewRequestScheme) -> GenerateReviewReponseScheme:
    return GenerateReviewReponseScheme(review='Good job!')