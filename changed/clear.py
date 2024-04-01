# чистить папку added
from pathlib import Path
from shutil import rmtree


for path in Path('D:\\Codes\\bot\\changed\\added\\').glob('*'):
    if path.is_dir():
        rmtree(path)
    else:
        path.unlink()
