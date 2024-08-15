from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from invoke.tasks import call
from invoke.tasks import task

if TYPE_CHECKING:
    from invoke.context import Context


@task
def sign_log(c: Context, suite: str | None = None) -> None:
    banned = './'
    if not suite:
        return print('No suite target provided', file=sys.stderr)
    if any(i in suite for i in banned):
        return print(f'Invalid sign target suite: {suite}', file=sys.stderr)
    log = Path(f'.tox/{suite}/tmp/meson-logs/testlog-{suite}.txt')  # noqa: S108
    if log.exists():
        c.run(f'sigstore sign --output-dir=sig {log}')
    else:
        print(f'Log not found for {suite}.', file=sys.stderr)


@task(
    pre=[
        call(sign_log, suite='dist'),  # type: ignore
        call(sign_log, suite='test'),  # type: ignore
        call(sign_log, suite='lint'),  # type: ignore
    ],
)
def release(c: Context, sdist: bool = False) -> None:
    """Create release wheels for the current interpreter.

    :param c: invoke context
    :type c: Context
    :param sdist: create source distribution tarball, defaults to False
    :type sdist: bool, optional
    """
    draft = c.run('psr --noop version')
    if draft and draft.exited != 0:
        return print('No release drafted.', file=sys.stderr)
    if sdist:
        c.run('python -m build --sdist')
        c.run('sigstore sign dist/*.tar.gz')
    ext_wheel = c.run('cibuildwheel --output-dir dist .')
    if ext_wheel and ext_wheel.exited != 0:
        c.run('python -m build --wheel')
    c.run('sigstore sign --output-dir=sig dist/*.whl')


@task(release)
def provenance(c: Context) -> None:
    print('SLSA provenance currently unavailable in OZI self-hosted CI/CD', file=sys.stderr)


@task(provenance)
def publish(c: Context) -> None:
    """Publishes a release tag"""
    c.run('psr publish')
    c.run('twine upload dist/*')
