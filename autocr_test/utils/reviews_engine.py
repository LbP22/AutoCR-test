    
import json
from autocr_test.models.Review import FileForReview
from ..models.RepoFile import RepoFileModel, RepoFileType
from ..utils.config import config
from ..utils.constants import PROMPT

from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

def convert_from_repo_file_to_file_for_review(file: RepoFileModel) -> FileForReview:
    return FileForReview(
        file_name=file.name,
        file_type=file.type,
        file_content=file.content,
        included_files=[convert_from_repo_file_to_file_for_review(x) for x in file.files] if file.files else None
    )

def get_review(repo_files_data: list[RepoFileModel], assignment_description : str, candidate_level: RepoFileType) -> str:
    code_data_to_send = [convert_from_repo_file_to_file_for_review(x) for x in repo_files_data]
    code_data_to_send_json = [x.model_dump_json(exclude_none=True) for x in code_data_to_send] # exclude none values to save tokens
    code_data_to_send_dump = json.dumps(code_data_to_send_json)

    stream = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                CANDIDATE_LEVEL=candidate_level, ASSIGNMENT_DESCRIPTION=assignment_description , 
                REPO_DUMP=code_data_to_send_dump
            )
        }],
        stream=True,  # stream to not block the event loop
    )

    review = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            review += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")

    return review