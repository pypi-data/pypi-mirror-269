import os
import re
import shutil
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Set


def create_directory(directory: str):
    create_directories([directory])


def create_directories(directories: List[str]):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def _should_consider_file(
    file_name: str,
    extension: Optional[str] = None,
    extensions_to_not_consider: Optional[Set[str]] = None,
    pattern: Optional[re.Pattern] = None,
) -> bool:
    # If file is of type extension, return True
    if extension:
        return file_name.endswith(extension)

    # If file extension is in the blacklist, return False
    if extensions_to_not_consider:
        for ext in extensions_to_not_consider:
            if file_name.endswith(ext):
                return False

    # if file extension is in the pattern, return True
    if pattern:
        return pattern.match(file_name) is not None

    return True


def get_input_files_batch(
    directory,
    batch_size: Optional[int] = None,
    extension: Optional[str] = None,
    filter_extensions: Optional[Set[str]] = None,
    glob_pattern: Optional[str] = None,
):
    pattern: re.Pattern = re.compile(glob_pattern) if glob_pattern else None
    file_list = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if not _should_consider_file(
                file_name=filename,
                extension=extension,
                extensions_to_not_consider=filter_extensions,
                pattern=pattern,
            ):
                continue

            file_path = Path(root).joinpath(filename)
            file_list.append(file_path)

    file_list.sort(key=lambda k: str(k))

    if batch_size:
        yield from get_files_in_batches(file_list=file_list, batch_size=batch_size)
    else:
        yield file_list


def get_files_in_batches(file_list: List[Any], batch_size: int):
    for i in range(0, len(file_list), batch_size):
        yield file_list[i : i + batch_size]


def get_input_files_dir(
    directory,
    extension: Optional[str] = None,
    filter_extensions: Optional[Set[str]] = None,
) -> List[Path]:
    try:
        return next(
            get_input_files_batch(
                directory=directory,
                extension=extension,
                filter_extensions=filter_extensions,
            )
        )
    except StopIteration:
        return []


def get_dest_file_path(
    file_path: Path, src_dir, dst_dir, extn: Optional[str] = None
) -> Path:
    src_dir = src_dir.rstrip("/")
    rel_file_path = Path(str(file_path)[len(src_dir) + 1 :])
    if extn:
        rel_file_path = f"{rel_file_path}{extn}"

    return Path(dst_dir).joinpath(rel_file_path)


def create_parent_directory(path: Path):
    create_directory(str(path.parent))


def copy_file(src_path, dst_path: Path):
    create_parent_directory(dst_path)

    shutil.copyfile(src_path, dst_path)
