import os
from pathlib import Path

def py_gzcompress(input: str | Path, output: str | Path | None = None):
  import shutil
  import gzip
  output = output or f'{input}.gz'
  with open(input, 'rb') as f_in:
    with gzip.open(output, 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)

def bash_gzcompress(input: str | Path, output: str | Path | None = None, *, keep: bool = True):
  output = output or f'{input}.gz'
  k = '-k' if keep else ''
  os.system(f'gzip {k} {input} -c > {output}')

def gzcompress(input: str | Path, output: str | Path | None = None, *, keep: bool = True):
  """Compress `input` to `output`.
  - Tries to use bash's `gzip`, otherwise defaults to python's `gzip`
  - Outputs to `f'{input}.gz'` if `output is None`
  - `keep`: whether to keep the `input` file
  """
  try:
    bash_gzcompress(input, output, keep=keep)
  except:
    py_gzcompress(input, output)
    if not keep:
      os.remove(input)