    
import json
from autocr_test.models.Review import FileForReview
from ..models.RepoFile import RepoFileModel, RepoFileType
from ..utils.config import config
from ..utils.constants import PROMPT

from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

def get_file_for_review(file: RepoFileModel) -> FileForReview:
    return FileForReview(
        file_name=file.name,
        file_type=file.type,
        file_content=file.content,
        included_files=[get_file_for_review(x) for x in file.files] if file.files else None
    )

def get_review(repo_files_data: list[RepoFileModel], assignement_description: str, candidate_level: RepoFileType) -> str:
    code_data_to_send: list[FileForReview] = []

    for file in repo_files_data:
        code_data_to_send.append(get_file_for_review(file))
    
    code_data_to_send_raw = [x.model_dump_json(exclude_none=True) for x in code_data_to_send]
    code_data_to_send_raw = json.dumps(code_data_to_send_raw)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                CANDIDATE_LEVEL=candidate_level, ASSIGNEMENT_DESCRIPTION=assignement_description, 
                REPO_DUMP=code_data_to_send_raw
            )
        }],
        stream=True,
    )

    review = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            review += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")

    return review