# noqa: INP001
import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml


if __name__ == '__main__':
    source = '/' / Path(
        os.path.relpath(
            os.path.join('/', os.environ.get('MESON_BUILD_ROOT', os.path.relpath('..'))),
            '/',
        ),
    )
    dist = '/' / Path(
        os.path.relpath(
            os.path.join('/', os.environ.get('MESON_DIST_ROOT', os.path.relpath('..'))),
            '/',
        ),
    )
    with (source / 'pyproject.toml').open('rb') as project_file:
        pyproject_toml = toml.load(project_file)
    dependencies = pyproject_toml.get('project', {}).get('dependencies', [])
    print('$$'.join(dependencies))
