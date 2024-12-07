from ..utils.red_engine import RedEngine
from ..utils.config import config
from ..models.RepoFile import RepoFileModel, RepoFileType

# probably github has some kind of hash for the whole repo, but I've realised it too late
# and I dont want to check if its true to not disappoint myself for wasting time on this

def sort_files_by_sha(repo_files_data: list[RepoFileModel]) -> list[RepoFileModel]:
    for repo_file in repo_files_data:
        if repo_file.type == RepoFileType.DIRECTORY:
            repo_file.files = sort_files_by_sha(repo_file.files)
    
    return sorted(repo_files_data, key=lambda x: x.sha)

def get_hashes_from_files(repo_files_data: list[RepoFileModel]) -> list[str]:
    hashes = []
    for repo_file in repo_files_data:
        if repo_file.type == RepoFileType.DIRECTORY:
            hashes.append(repo_file.sha)
            hashes.extend(get_hashes_from_files(repo_file.files))
        else:
            hashes.append(repo_file.sha)
    
    return hashes

def get_hashed_data(repo_files_data: list[RepoFileModel], assignment: str) -> str:
    repo_files_data = sort_files_by_sha(repo_files_data) # need to sort files by sha to avoid different order of files got from github
    repo_files_data_raw = []
    for repo_file in repo_files_data:
        repo_file_raw = repo_file.model_dump(exclude_none=True)
        repo_file_raw.pop('id', None)  # id is not needed for hashing, bc it's not a part of the data and generated randomly
        repo_files_data_raw.append(repo_file_raw)

    return str(hash(assignment+str(get_hashes_from_files(repo_files_data))))  # using generated by github hashes per file to hash the data per repo


async def get_cache(repo_files_data: list[RepoFileModel], assignment: str) -> str:
    repo_files_data_hashed = get_hashed_data(repo_files_data, assignment)

    cached_data = await RedEngine().get(repo_files_data_hashed)
    if cached_data:
        print('Cache hit!', repo_files_data_hashed)
        return cached_data
    else:
        print('Cache miss!', repo_files_data_hashed)
        return ''
    

async def set_cache(repo_files_data: list[RepoFileModel], assignment: str, review: str) -> None:
    repo_files_data_hashed = get_hashed_data(repo_files_data, assignment)
    await RedEngine().set(repo_files_data_hashed, review, expire=config.REPO_CACHE_TTL)
    print('Cache set!', repo_files_data_hashed)