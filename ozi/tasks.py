# ozi/tasks.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = [  # noqa: E800, RUF100
#   'OZI.build',
#   'build',
#   'cibuildwheel',
#   'invoke',
#   'meson',
#   'python-semantic-release',
#   'setuptools_scm',
#   'sigstore',
#   'tomli>=2;python_version<="3.11"',  # noqa: E800, RUF100
#   'twine',
# ///
from __future__ import annotations

import inspect
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from invoke.tasks import task

if TYPE_CHECKING:
    from invoke.context import Context
    from invoke.runners import Result


@task
def setup(
    c: Context,
    suite: str = 'dist',
    draft: bool = False,
    ozi: bool = False,
) -> None | Result:
    """Setup a meson build directory for an OZI suite."""
    target = Path(f'.tox/{suite}/tmp').absolute()  # noqa: S108
    env_dir = Path(f'.tox/{suite}').absolute()
    if ozi:
        c.run(
            f'meson setup {target} -D{suite}=enabled -Dtox-env-dir={env_dir} --reconfigure',
        )
    else:
        c.run(
            f'meson setup {target} -Dozi:{suite}=enabled -Dozi:tox-env-dir={env_dir} --reconfigure',
        )
    if draft and suite == 'dist':
        return c.run('psr --strict version')
    return None


@task(setup)
def sign_checkpoint(c: Context, suite: str | None = None) -> None:
    """Sign checkpoint suites with sigstore."""
    banned = './'
    host = f'py{sys.version_info.major}{sys.version_info.minor}'
    if not suite:
        return print('No suite target provided', file=sys.stderr)
    if any(i in suite for i in banned):
        return print(f'Invalid sign target suite: {suite}', file=sys.stderr)
    testlog = Path(f'.tox/{suite}/tmp/meson-logs/testlog-{suite}.txt')  # noqa: S108
    if testlog.exists():
        c.run(f'sigstore sign --output-dir=sig/{host}/{suite} {testlog}')
    else:
        print(f'Test log not found for suite: {suite}.', file=sys.stderr)
    meson_log = Path(f'.tox/{suite}/tmp/meson-logs/meson-log.txt')  # noqa: S108
    if meson_log.exists():
        c.run(f'sigstore sign --output-dir=sig/{host}/{suite} {meson_log}')
    else:
        print(f'Meson log not found for suite: {suite}.', file=sys.stderr)


@task
def checkpoint(c: Context, suite: str, maxfail: int = 1, ozi: bool = False) -> None:
    """Run OZI checkpoint suites with meson test."""
    setup(c, suite=suite, draft=False, ozi=ozi)
    target = Path(f'.tox/{suite}/tmp').absolute()  # noqa: S108
    c.run(
        f'meson test --no-rebuild --maxfail={maxfail} -C {target} --setup={suite}',
    )


@task
def release(
    c: Context,
    sdist: bool = False,
    draft: bool = False,
    cibuildwheel: bool = True,
    sign: bool = False,
    ozi: bool = False,
) -> None:
    """Create releases for the current interpreter."""
    os.environ['CIBW_BUILD'] = f'cp{sys.version_info.major}{sys.version_info.minor}*'
    setup(c, suite='dist', draft=draft, ozi=ozi)
    if sdist:
        c.run('python -m build --sdist')
        if sign:
            c.run('sigstore sign --output-dir=sig dist/*.tar.gz')
    (
        c.run('cibuildwheel --prerelease-pythons --output-dir dist .', warn=True)
        if cibuildwheel
        else None
    )
    c.run('python -m build --wheel')
    if sign:
        c.run('sigstore sign --output-dir=sig dist/*.whl')


@task
def provenance(c: Context) -> None:
    """SLSA provenance currently unavailable in OZI self-hosted CI/CD"""
    print(inspect.getdoc(provenance), file=sys.stderr)


@task
def publish(c: Context, ozi: bool = False) -> None:
    """Publishes a release tag"""
    setup(c, suite='dist', ozi=ozi)
    c.run('psr publish')
    c.run('twine check dist/*')
    c.run('twine upload dist/*')
