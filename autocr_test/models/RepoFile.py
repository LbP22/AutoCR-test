import enum
from typing import Union
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
    download_url: Union[str, None]

    files: Union[list, None] = None
    content: Union[str, None] = None
