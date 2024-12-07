import enum
from typing import Union
from odmantic import Model

from autocr_test.models.RepoFile import RepoFileType

class FileForReview(Model):
    file_name: str
    file_type: RepoFileType

    file_content: Union[str, None] = None
    included_files: Union[list, None] = None
