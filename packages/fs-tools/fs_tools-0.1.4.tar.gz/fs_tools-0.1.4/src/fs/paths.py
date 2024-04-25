from typing import Iterable
import os
from pathlib import Path

def ensure_path(file: str | Path):
  """Creates the path to `file`'s folder if it didn't exist
  - E.g. `ensure('path/to/file.txt')` will create `'path/to'` if needed
  """
  dir = os.path.dirname(file)
  if dir != '':
    os.makedirs(dir, exist_ok=True)

def filenames(base_path: str | Path) -> Iterable[str]:
  """Returns all files inside `base_path`, recursively, relative to `base_path`"""
  base = Path(base_path)
  for file_path in base.rglob('*'):
    if file_path.is_file():
      yield file_path.relative_to(base).as_posix()