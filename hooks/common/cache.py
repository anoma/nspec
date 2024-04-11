import hashlib
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional


def compute_sha_over_folder(_folder_path: Path) -> str:
    """Compute the sha with respect to the structure of a folder."""

    folder_path = _folder_path.absolute().as_posix()
    sha_hash: hashlib._Hash = hashlib.sha256()
    for root, dirs, files in os.walk(folder_path):
        for names in sorted(dirs):
            sha_hash.update(names.encode("utf-8"))
        for filename in sorted(files):
            file_path = os.path.join(root, filename)
            sha_hash.update(file_path.encode("utf-8"))
            hash_file_hash_obj(sha_hash, Path(file_path))
    return sha_hash.hexdigest()


def hash_file_hash_obj(hash_obj, filepath: Path):
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hash_obj.update(chunk)


def hash_file(_filepath: Path):
    filepath = _filepath.absolute()
    _hash_obj = hashlib.sha256()
    hash_file_hash_obj(_hash_obj, filepath)
    return _hash_obj.hexdigest()


@lru_cache(maxsize=128)
def compute_hash_filepath(_filepath: Path, hash_dir: Optional[Path] = None) -> Path:
    """
    Computes the hash file path location for the given file path.
    """
    hash_obj = hashlib.sha256()
    filepath = _filepath.absolute()
    hash_obj.update(filepath.as_posix().encode("utf8"))
    hash_filename = hash_obj.hexdigest()
    if hash_dir is None:
        return Path(hash_filename)
    return hash_dir.joinpath(hash_filename)
