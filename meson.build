# meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
project(
    'OZI',
    version: run_command(
        'python3', # scm_version_snip
        [
            '-c',
'''from setuptools_scm import get_version
from packaging.version import Version
v = get_version(normalize=False)
if Version(v) < Version("0.1"):
    print("0.4")
else:
    print(v)
''',
        ],
        check: true,
    ).stdout().strip(),
    default_options: ['warning_level=3'],
    license: 'Apache-2.0 WITH LLVM-exception',
    license_files: 'LICENSE.txt',
    meson_version: '>=1.1.0',
)
env = environment()
fs = import('fs')
pymod = import('python')
pyproject_config = configuration_data()

# prescript arrays
no_version = get_option('no-version')
unhashable = get_option('unhashable')
should_fail = get_option('should-fail')
module_only = get_option('module-only')
dist_suite = get_option('dist-suite')
docs_suite = get_option('docs-suite')
lint_suite = get_option('lint-suite')
test_suite = get_option('test-suite')
dist_exclude_suites = get_option('dist-exclude-suites')
docs_exclude_suites = get_option('docs-exclude-suites')
lint_exclude_suites = get_option('lint-exclude-suites')
test_exclude_suites = get_option('test-exclude-suites')
# descript arrays   
namespace = get_option('namespace')
plugin_only = get_option('plugin-only')
python_dependencies = get_option('python-dependencies')
# features   
dev = get_option('dev')
source_to_build = get_option('source-to-build')
docs_source = get_option('docs-source')
test_source = get_option('test-source')
# templates
python_readlines = 'f=open("@0@","r");print(*f.readlines(),sep="",end="");f.close();'

build_root = meson.global_build_root()
scripts = 'ozi' / 'scripts'
project_name = meson.project_name()
python = pymod.find_installation(
    'python3',
    modules: python_dependencies,
    required: true,
    disabler: true,
)
render_requirements = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'render_requirements.py',
        ),
    ],
    check: true,
).stdout()
pyproject_config.set(
    'PYTHON_VERSION_DIST',
    'py' + ''.join(python.language_version().split('.')),
)
pyproject_config.set('SCM_VERSION', meson.project_version())
pyproject_config.set('VCS_TAG', '@VCS_TAG@')
pyproject_config.set('README_TEXT', fs.read('README'))
pyproject_config.set(
    'REQUIREMENTS_IN',
    run_command(
        python,
        ['-c', render_requirements],
        check: true,
    ).stdout().strip(),
)
pyproject_config.set('PROJECT_NAME', project_name)
pyproject_config.set('LICENSE', meson.project_license()[0])
root_files = ['README', 'CHANGELOG.md', 'LICENSE.txt', 'requirements.in', 'pyproject.toml', '.gitignore']
configure_file(
    input: root_files[4],
    output: root_files[4],
    configuration: pyproject_config,
)
meson_setuptools_scm = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'meson_setuptools_scm.py',
        ),
    ],
    check: true,
).stdout()
meson_dist_setuptools_scm = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'meson_dist_setuptools_scm.py',
        ),
    ],
    check: true,
).stdout()
core_metadata = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'core_metadata_template.py',
        ),
    ],
    check: true,
).stdout()
metadata_version = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'version_metadata_template.py',
        ),
    ],
    check: true,
).stdout()
# snippets
scm_version_snip = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'scm_version_snip.py',
        ),
    ],
    check: true,
).stdout()
to_distribution = run_command(
    python,
    [
        '-c',
        python_readlines.format(scripts / 'to_distribution_template.py'),
    ],
    check: true,
).stdout()
replace_ruff_target_version = run_command(
    python,
    [
        '-c',
        python_readlines.format(scripts / 'replace_ruff_target_version.py'),
    ],
    check: true,
).stdout()
run_command(python, ['-c', replace_ruff_target_version], check: true)
pip = find_program('pip', required: true, disabler: true)
pipx = find_program('pipx', required: true, disabler: true)
pip_compile = find_program('pip-compile', required: true)
if not meson.is_subproject()
    custom_target(
        'requirements.txt',
        input: root_files[3],
        output: 'requirements.txt',
        build_always_stale: true,
        build_by_default: true,
        command: [
            'pip-compile',
            '--allow-unsafe',
            '--strip-extras',
            '-q',
            '--generate-hashes',
            '-o', '@OUTPUT@',
            '@INPUT@',
        ],
    )
endif
source_to_build.enable_auto_if(source_to_build.auto())
docs_source = 'docs'
test_source = 'tests'
no_check = {'check': false, 'env': env}
install = ['install']
build_commands = {'dev': []}
test_app_args = {}
pip_repr = pip.full_path()
configure_file(
    command: [python, '-c', meson_setuptools_scm],
    output: 'PKG-INFO',
)
meson.add_dist_script(pip, 'install', 'tomli>=2.0.0')
meson.add_dist_script(python, '-c', meson_dist_setuptools_scm)
vcs_tag(input: 'pyproject.toml', output: 'pyproject.orig.toml')
message('backed up pyproject.toml as pyproject.orig.toml')
foreach source : root_files
    if source not in ['.gitignore', 'pyproject.toml', 'README', 'CHANGELOG.md']
        fs.copyfile(source)
    elif source == 'README'
        fs.copyfile(source, 'README.rst')
    endif
endforeach
if get_option('ozi-blastpipe').enabled()
    # BEGIN BOOTSTRAP SCRIPT
    subproject('blastpipe')
    # END BOOTSTRAP SCRIPT
endif
root_children = ['ozi', 'tests']
foreach child : root_children
    subdir(child)
endforeach
if false
    executable('root_files', root_files)
    executable('source_files', source_files)
    executable('source_children', source_children)
    executable('test_files', test_files)
    executable('test_children', test_children)
endif

# BEGIN checkpoint-suite-install
modules = []
foreach name : namespace
    command_names = get_option(name + '-suite')
    summary(
        name,
        get_option(name),
        section: ' '.join('$', 'meson setup --reconfigure -D[option]'),
    )
    suite = get_option(name)
    suite.enable_auto_if(dev.enabled())
    set_variable(name, suite)
    foreach command : command_names
        if suite.enabled() and command in module_only
            modules += [command.underscorify()]  # we should collapse repeated `_`
        endif
        flag = disabler()
        if (
            (get_option('dev').enabled() or suite.enabled())
            and command not in plugin_only
        )
            if command not in module_only and get_option('tox-env-dir') != ''
                message('install', command, 'with pipx')
                run_command(
                    pipx,
                    [
                        'runpip',
                        'meson',
                        '--python', python,
                        'install',
                        get_option('install-args-'+command),
                        '-r',
                        meson.project_build_root() / 'ozi' / name / command / 'requirements.txt',
                    ],
                    check: true
                )
            else
                message('install', command, 'with pip')
                run_command(
                    pip,
                    [
                        'install',
                        get_option('install-args-'+command),
                        '-r',
                        meson.project_build_root() / 'ozi' / name / command / 'requirements.txt',
                    ],
                    check: true
                )
            endif
            if not flag.found() and command not in module_only
                flag = find_program(
                    command,
                    required: false,
                    disabler: true,
                    dirs: [get_option('tox-env-dir') / 'bin']
                )
            elif command in module_only
                command = command.replace('-', '_')
                flag = command
            endif
        endif
        if command not in plugin_only
            set_variable(command.replace('-', '_'), flag)
        endif
        set_variable(name + '_kwargs', {'suite': name, 'env': env})
    endforeach
endforeach
pymod.find_installation(
    'python3',
    modules: modules,
    required: false,
    disabler: true,
)
# END checkpoint-suite-install

# BEGIN checkpoint-suite-version-check
done = []
foreach name : namespace
    foreach suite : get_option(name + '-exclude-suites')
        foreach app : get_option(suite + '-suite')
            if app in done
                continue
            endif
            header = ['$', 'meson', 'test', '--suite=@0@'.format(suite)]
            feature = get_variable(suite)
            if feature.enabled()
                if app not in plugin_only + module_only
                    if app not in no_version
                        summary(
                            {
                                app: get_variable(
                                    app.replace('-', '_'),
                                ).version(),
                            },
                            section: ' '.join(header),
                        )
                    endif
                    packaged_version = run_command(
                        python,
                        ['-c', metadata_version.format(app)],
                        kwargs: no_check,
                    ).stdout().strip()
                    fallback_version = run_command(
                        pip,
                        ['show', app],
                        kwargs: no_check,
                    ).stdout().split('\n')
                    if fallback_version.length() > 2
                        fallback_version = fallback_version[1].split(':')[1].strip()
                    else
                        fallback_version = 'unknown (see Python packages)' 
                    endif
                    if app in no_version
                        if packaged_version == ''
                            version = fallback_version
                        else
                            version = packaged_version
                        endif
                        if app not in done
                            summary({app: version}, section: ' '.join(header))
                        endif
                    endif
                else
                    packaged_version = run_command(
                        python,
                        ['-c', metadata_version.format(app)],
                        kwargs: no_check,
                    ).stdout().strip()
                    if app in module_only
                        fallback_version = run_command(
                            pip,
                            [
                                'show',
                                run_command(
                                    python,
                                    ['-c', to_distribution.format(app)],
                                    kwargs: no_check,
                                ).stdout(),
                            ],
                            kwargs: no_check,
                        ).stdout().split('\n')
                    else
                        fallback_version = run_command(
                            pip,
                            ['show', app],
                            kwargs: no_check,
                        ).stdout().split('\n')
                    endif
                    if fallback_version.length() > 2
                        fallback_version = fallback_version[1].split(':')[1].strip()
                    else
                        fallback_version = 'unknown (see Python packages)'
                    endif
                    if app in no_version
                        summary(
                            {
                                app: fallback_version,
                            },
                            section: ' '.join(header),
                        )
                    else
                        summary(
                            {
                                app: packaged_version,
                            },
                            section: ' '.join(header),
                        )
                    endif
                endif
            endif
            done += app
        endforeach
    endforeach
endforeach
# END checkpoint-suite-version-check

# BEGIN checkpoint-suite-invocation
add_test_setup('dev', is_default: not meson.is_subproject(), env: env)
env.append('TESTS_BUILDDIR', build_root)
no_check = {'check': false, 'env': env}
opt_cov_eq_project_name = '--cov=' + project_name
build_commands = {'dev': []}
foreach name : namespace
    add_test_setup(
        name,
        exclude_suites: get_option(name + '-exclude-suites'),
        timeout_multiplier: get_option(name + '-timeout-multiplier'),
    )
    set_variable(name + '_kwargs', {'suite': name, 'env': env})
    command_names = get_option(name + '-suite')
    foreach command : command_names
        if command not in plugin_only
            _args = get_option('args-' + command)
        else
            _args = []
        endif
        command_args = []
        test_app_args = {}
        foreach arg : _args
            if (
                arg.startswith('@')
                and (
                    arg.endswith('@')
                    or arg.endswith('@/')
                    or arg.endswith('@/test')
                )
            )
                arg = arg.strip('@')
                if is_variable(arg)
                    arg = get_variable(arg)
                elif arg.endswith('@/')
                    arg = get_variable(arg.replace('@/', '')) + '/'
                elif arg.endswith('@/test')
                    arg = get_variable(arg.replace('@/test', '')) + '/tests'
                else
                    warning(arg + ' unknown')
                endif
            endif
            command_args += arg
        endforeach
        if command in ['pytest'] and not meson.is_subproject()
            test_paths = []
            foreach file : test_files
                test_paths += ['tests' / file]
            endforeach
            command_args = test_paths + command_args
        endif
        if command not in plugin_only
            foreach app, args : {command: command_args}
                if app in module_only
                    args = ['-m', app.replace('-', '_'), args]
                endif
                args = {
                    'args': args,
                    'env': env,
                    'priority': get_option(name + '-priority'),
                    'suite': name,
                }
                if app in should_fail
                    args += {'should_fail': true}
                endif
                feature = get_variable(name)
                if feature.enabled() and app not in module_only
                    test_app = get_variable(app.replace('-', '_'))
                else
                    test_app = disabler()
                endif
                if test_app.found() and app not in module_only
                    test(app, test_app, kwargs: args)
                elif app in ['bandit']
                    args += {'workdir': meson.global_source_root()}
                    test(app, python, kwargs: args)
                else
                    test(app, python, kwargs: args)
                endif
            endforeach
        endif
    endforeach
endforeach
# END checkpoint-suite-invocation

display_dirs = [
    'bindir',
    'datadir',
    'libdir',
    'localedir',
    'prefix',
]
foreach dir : display_dirs
    summary(
        {dir: get_option(dir)},
        section: '$ meson install -C @0@'.format(build_root),
    )
endforeach
summary('install_dir', python.get_install_dir(), section: 'Python')
summary('install_env', get_option('python.install_env'), section: 'Python')
summary('path', python.full_path(), section: 'Python')
summary('version', python.language_version(), section: 'Python')

installed_packages = []
foreach line : run_command('pip', 'freeze', check: true).stdout().split('\n')
    if line == ''
        continue
    endif
    if not line.contains('@')
        package = line.split('==')
    else
        package = line.split('@')
    endif
    if (
        package[0] not in get_option('test-suite')
        and package[0] not in get_option('lint-suite')
        and package[0] not in get_option('dist-suite')
    )
        installed_packages += package[0]
        summary(package[0], package[1].strip(), section: 'Python packages')
    endif
endforeach

# Prior to Python 3.12 these would not be included in pip freeze
# See: https://github.com/pypa/pip/pull/12032
foreach legacy_package: ['wheel', 'setuptools', 'distribute']
    if legacy_package not in installed_packages
        legacy_package_version = run_command(
            python,
            ['-c', metadata_version.format(legacy_package)],
            kwargs: no_check,
        ).stdout().strip()
        if legacy_package_version != ''
            summary(legacy_package, legacy_package_version, section: 'Python packages')
        endif
    endif
endforeach
pip_version = run_command(pip, '-V', check: true).stdout().split()
summary(pip_version[0], pip_version[1], section: 'Python packages')
