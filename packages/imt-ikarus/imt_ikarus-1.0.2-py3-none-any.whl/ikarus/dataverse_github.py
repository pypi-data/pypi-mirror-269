from functools import cache
from pathlib import Path
from typing import NamedTuple, Optional

import requests


def listdir(
    filter_prefix: Optional[str] = None,
    filter_suffix: Optional[str] = None,
    backend: str = "github",
) -> list[str]:

    if backend == "github":
        files = _listdir_github()
    elif backend == "dataverse":
        files = _listdir_dataverse()
    else:
        raise NotImplementedError

    if filter_prefix is not None:
        files = [file for file in files if file[: len(filter_prefix)] == filter_prefix]

    if filter_suffix is not None:
        files = [
            file
            for file in files
            if file[-len(filter_suffix) :] == filter_suffix  # noqa: E203
        ]

    return files


def download(
    path_in_repo: str, path_to_cache: str = "~/.ikarus_cache", backend: str = "github"
) -> Path:
    "Download file from Github repo. Returns path on disk."
    path_on_disk = Path(path_to_cache).expanduser().joinpath(path_in_repo)
    if not path_on_disk.exists():
        path_on_disk.parent.mkdir(parents=True, exist_ok=True)

        if backend == "github":
            url = _url_github(path_in_repo)
        elif backend == "dataverse":
            url = _url_dataverse(path_in_repo)
        else:
            raise NotImplementedError

        print(f"Downloading file from url {url}.. (this might take a moment)")
        _wget(url, out=str(path_on_disk))
        print(
            f"Downloading finished. Saved to location {path_on_disk}. "
            f"All downloaded files can be deleted by removing folder {path_to_cache}."
        )
    return path_on_disk


class DataverseFile(NamedTuple):
    path: str
    id: int


_dataverse_url = "https://dataverse.harvard.edu/api"
_dataset_doi = "doi:10.7910/DVN/M0NKN9"


@cache
def _dataverse_files() -> list[DataverseFile]:

    url = f"{_dataverse_url}/datasets/:persistentId/versions/:latest/files?persistentId={_dataset_doi}"  # noqa: E501
    response = requests.get(url)
    data = response.json().get("data", [])

    files: list[DataverseFile] = []
    for ele in data:
        filepath = ele["dataFile"]["filename"]
        if "directoryLabel" in ele:
            filepath = ele["directoryLabel"] + "/" + filepath
        files.append(DataverseFile(filepath, ele["dataFile"]["id"]))

    files.sort(key=lambda ele: ele.path)

    return files


def _listdir_dataverse() -> list[str]:
    return [ele.path for ele in _dataverse_files()]


def _url_dataverse(path_in_repo: str) -> str:
    for file in _dataverse_files():
        if file.path == path_in_repo:
            break
    else:
        raise Exception(f"Path `{path_in_repo}` was not found in dataverse repo.")
    return f"{_dataverse_url}/access/datafile/{file.id}"


_github_user = "SimiPixel"
_github_repo = "ikarus"
_github_branch = "main"


def _listdir_github() -> list[str]:

    recursive: bool = True

    url = (
        f"https://api.github.com/repos/{_github_user}/{_github_repo}/"
        f"git/trees/{_github_branch}?recursive={int(recursive)}"
    )
    resp = requests.get(url).json()
    files = [ele["path"] for ele in resp["tree"]]
    return files


def _url_github(
    path_in_repo: str,
) -> str:
    url = f"https://raw.githubusercontent.com/{_github_user}/{_github_repo}/{_github_branch}/{path_in_repo}"  # noqa: E501
    return url


def _wget(url: str, out: str):
    download_response = requests.get(url)
    with open(out, "wb") as f:
        f.write(download_response.content)
