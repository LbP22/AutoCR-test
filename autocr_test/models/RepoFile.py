import enum
from typing import Optional
from odmantic import Model

class RepoFileType(str, enum.Enum):
    FILE = 'file'
    DIRECTORY = 'dir'

class RepoFileModel(Model):
    name: str
    path: str
    sha: str
    size: int
    url: str
    html_url: str
    git_url: str
    type: RepoFileType
    download_url: Optional[str]

    files: Optional[list] = None
    content: Optional[str] = None