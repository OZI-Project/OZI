from pathlib import Path
from warnings import warn

from git import InvalidGitRepositoryError
from git import Repo
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import TemplateNotFound
from jinja2 import select_autoescape

from ozi.filter import current_date
from ozi.filter import sha256sum
from ozi.filter import to_distribution
from ozi.filter import underscorify
from ozi.filter import wheel_repr
from ozi.spec import Metadata

metadata = Metadata()
env = Environment(
    loader=PackageLoader('ozi'),
    autoescape=select_autoescape(),
    enable_async=True,
)
env.filters['to_distribution'] = to_distribution
env.filters['underscorify'] = underscorify
env.filters['zip'] = zip
env.filters['sha256sum'] = sha256sum
env.filters['wheel_repr'] = wheel_repr
env.filters['current_date'] = current_date
env.globals = env.globals | metadata.asdict()


def render_ci_files_set_user(env: Environment, target: Path, ci_provider: str) -> str:
    """Render CI files based on the ci_provider for target in env.
    Return the ci_user of the target repository.
    """
    match ci_provider:
        case 'github':
            try:
                ci_user = Repo(target).config_reader().get('user', 'name')
            except InvalidGitRepositoryError:
                ci_user = ''
            Path(target, '.github', 'workflows').mkdir(parents=True)
            template = env.get_template('github_workflows/ozi.yml.j2')
            with open(Path(target, '.github', 'workflows', 'ozi.yml'), 'w') as f:
                f.write(template.render())
        case _:
            warn(
                f'--ci-provider "{ci_provider}" unrecognized. ci_user could not be set.',
                RuntimeWarning,
            )
            ci_user = ''
    return ci_user


def render_project_files(env: Environment, target: Path, name: str) -> None:
    """Render the primary new project files(excluding CI)."""
    Path(target, underscorify(name)).mkdir()
    Path(target, 'subprojects').mkdir()
    Path(target, 'tests').mkdir()
    templates = metadata.spec.python.src.template
    for filename in templates.root:
        template = env.get_template(f'{filename}.j2')
        try:
            content = template.render(filename=filename)
        except TemplateNotFound:  # pragma: defer to good-first-issue
            content = f'template "{filename}" failed to render.'
            warn(content, RuntimeWarning, stacklevel=0)
        with open(target / filename, 'w') as f:
            f.write(content)

    for filename in templates.source:
        template = env.get_template(f'{filename}.j2')
        filename = filename.replace('project.name', underscorify(name).lower())
        with open(target / filename, 'w') as f:
            f.write(template.render())

    for filename in templates.test:
        template = env.get_template(f'{filename}.j2')
        with open(target / filename, 'w') as f:
            f.write(template.render())

    template = env.get_template('project.ozi.wrap.j2')
    with open(target / 'subprojects' / 'ozi.wrap', 'w') as f:
        f.write(template.render())
