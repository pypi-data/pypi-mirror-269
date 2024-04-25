from ikarus import dataverse_github


def test_download_from_repo():
    icon_svg = "docs/img/icon.svg"
    path_on_disk = dataverse_github.download(icon_svg)

    assert path_on_disk.exists() and path_on_disk.is_file()
