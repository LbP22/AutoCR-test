from typing import Optional
from odmantic import Model

from autocr_test.models.RepoFile import RepoFileType

class FileForReview(Model):
    file_name: str
    file_type: RepoFileType

    file_content: Optional[str] = None
    included_files: Optional[str] = None
