# чистить папку added
from pathlib import Path
from shutil import rmtree
from DATA.data import changed

for path in Path(f'{changed.directory}\\added\\').glob('*'):
    if path.is_dir():
        rmtree(path)
    else:
        path.unlink()
