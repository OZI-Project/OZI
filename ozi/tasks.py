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
"""Invoke tasks for OZI CI."""
from __future__ import annotations

import inspect
import os
import runpy
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from invoke.tasks import task

if TYPE_CHECKING:
    from invoke.context import Context
    from invoke.runners import Result


_IS_OZI = str(Path(__file__).parent.parent.parent.name) != 'subprojects'


def __build(c: Context, sdist: bool, wheel_sign_token: str | None = None) -> None:
    kind = '--sdist' if sdist else '--wheel'
    env = {'WHEEL_SIGN_TOKEN': wheel_sign_token} if wheel_sign_token else {}
    build = c.run('python -m build {}'.format(kind), warn=True, env=env)
    if build is not None and build.exited != 0:
        c.run('uv build {}'.format(kind), env=env)


def build_sdist(c: Context, sdist: bool, sign: bool) -> None:
    if sdist:
        __build(c, sdist=sdist)
    if sign:
        c.run(f'sigstore sign --output-dir=sig dist{os.sep}*.tar.gz')


def build_wheel(
    c: Context,
    wheel: bool,
    cibuildwheel: bool,
    sign: bool,
    wheel_sign_token: str | None = None,
) -> None:
    if cibuildwheel:
        os.environ['CIBW_BUILD'] = f'cp{sys.version_info.major}{sys.version_info.minor}*'
        res = c.run('cibuildwheel --prerelease-pythons --output-dir dist .', warn=True)
        if res is not None and res.exited != 0 and wheel:
            __build(c, sdist=not wheel, wheel_sign_token=wheel_sign_token)
    elif wheel:
        __build(c, sdist=not wheel, wheel_sign_token=wheel_sign_token)

    if sign and (wheel or cibuildwheel):
        c.run(f'sigstore sign --output-dir=sig dist{os.sep}*.whl')


@task
def setup(
    c: Context,
    suite: str = 'dist',
    draft: bool = False,
    ozi: bool = _IS_OZI,
) -> None | Result:
    """Setup a meson build directory for an OZI suite."""
    runpy.run_path('.tox/invoke/bin/activate_this.py')
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
    banned = '.' + os.sep
    host = f'py{sys.version_info.major}{sys.version_info.minor}'
    if not suite:
        return print('No suite target provided', file=sys.stderr)
    if any(i in suite for i in banned):
        return print(f'Invalid sign target suite: {suite}', file=sys.stderr)
    testlog = Path(f'.tox/{suite}/tmp/meson-logs/testlog-{suite}.txt')  # noqa: S108
    meson_log = Path(f'.tox/{suite}/tmp/meson-logs/meson-log.txt')  # noqa: S108
    sigdir = Path(f'sig/{host}/{suite}')
    if testlog.exists():
        c.run(f'sigstore sign --output-dir={sigdir} {testlog}')
    else:
        print(f'Test log not found for suite: {suite}.', file=sys.stderr)
    if meson_log.exists():
        c.run(f'sigstore sign --output-dir={sigdir} {meson_log}')
    else:
        print(f'Meson log not found for suite: {suite}.', file=sys.stderr)


@task
def checkpoint(c: Context, suite: str, maxfail: int = 1, ozi: bool = _IS_OZI) -> None:
    """Run OZI checkpoint suites with meson test."""
    setup(c, suite=suite, draft=False, ozi=ozi)
    target = Path(f'.tox/{suite}/tmp').absolute()  # noqa: S108
    testlog = Path(f'.tox/{suite}/tmp/meson-logs/testlog-{suite}.txt')
    meson_log = Path(f'.tox/{suite}/tmp/meson-logs/meson-log.txt')  # noqa: S108
    c.run(
        f'meson test --no-rebuild --maxfail={maxfail} -C {target} --setup={suite}',
    )
    if meson_log.exists():
        print(meson_log.read_text())
    if testlog.exists():
        print(testlog.read_text())


@task
def release(  # noqa:
    c: Context,
    sdist: bool = False,
    draft: bool = False,
    cibuildwheel: bool = True,
    wheel: bool = True,
    sign: bool = False,
    wheel_sign_token: str | None = None,
    ozi: bool = _IS_OZI,
) -> None:
    """Create releases for the current interpreter."""
    setup(c, suite='dist', draft=draft, ozi=ozi)
    build_sdist(c, sdist, sign)
    build_wheel(c, wheel, cibuildwheel, sign, wheel_sign_token)


@task
def provenance(c: Context) -> None:
    """SLSA provenance currently unavailable in OZI self-hosted CI/CD"""
    print(inspect.getdoc(provenance), file=sys.stderr)


@task
def publish(c: Context, ozi: bool = _IS_OZI) -> None:
    """Publishes a release tag"""
    setup(c, suite='dist', ozi=ozi)
    c.run('psr publish')
    c.run(f'twine check dist{os.sep}*')
    c.run(f'twine upload dist{os.sep}*')


@task
def rewrite(c: Context, command: str) -> None:
    """Interactive mode entrypoint for meson rewrite."""
    c.run(f"meson rewrite command '{command}'")
