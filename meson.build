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
            'from setuptools_scm import get_version;print(get_version(normalize=False))',
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

# emoji
emoji_no_version = get_option('emoji-no-version')
emoji_metadata_version = get_option('emoji-metadata-version')
emoji_directory = get_option('emoji-directory')
emoji_generic = get_option('emoji-generic')
emoji_setup = get_option('emoji-setup')
emoji_dist = get_option('emoji-dist')
emoji_docs = get_option('emoji-docs')
emoji_lint = get_option('emoji-lint')
emoji_test = get_option('emoji-test')
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

build_root = meson.current_build_dir()
scripts = 'ozi' / 'scripts'
project_name = meson.project_name()
python = pymod.find_installation(
    'python3',
    modules: python_dependencies,
    required: true,
    disabler: true,
)
pyproject_config.set('PYTHON_VERSION_DIST', 'py'+''.join(python.language_version().split('.')))
pyproject_config.set('VCS_TAG', '@VCS_TAG@')
pre_pyproject = configure_file(input: 'pyproject.toml', output: 'pyproject.toml.pre', configuration: pyproject_config)

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
sync_pkg_readme = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'sync_pkg_readme.py',
        ),
    ],
    check: true,
).stdout()
to_distribution = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'to_distribution_template.py'
        ),
    ],
    check: true,
).stdout()
replace_ruff_target_version = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            scripts / 'replace_ruff_target_version.py'
        ),
    ],
    check: true,
).stdout()
run_command(python, ['-c', replace_ruff_target_version], check: true)
run_command(python, ['-c', sync_pkg_readme], check: true)
pip = find_program('pip', required: true, disabler: true)
pip_compile = find_program('pip-compile', required: true)
vcs_tag(input: pre_pyproject, output: 'pyproject.toml')
custom_target(
    'requirements-ozi',
    input: 'requirements.in',
    output: 'requirements.txt',
    build_always_stale: true,
    build_by_default: true,
    command: ['pip-compile', '--allow-unsafe', '--strip-extras', '-q', '--generate-hashes', '-o', '@OUTPUT@', '@INPUT@']
)
source_to_build.enable_auto_if(source_to_build.auto())
docs_source = 'docs'
test_source = 'tests'
no_check = {'check': false, 'env': env}
install = ['install']
build_commands = {'dev': []}
test_app_args = {}
pip_repr = pip.full_path()
root_files = ['README.rst', 'CHANGELOG.md', 'PKG-INFO', 'LICENSE.txt']
foreach source : root_files
    fs.copyfile(source)
endforeach
if false
    executable('root_files', root_files)
endif
if get_option('ozi-blastpipe').enabled()
    # BEGIN BOOTSTRAP SCRIPT
    subproject('blastpipe')
    # END BOOTSTRAP SCRIPT
endif
subdir('ozi')
subdir('tests')

# BEGIN checkpoint-suite-install
modules = []
foreach name : namespace
    command_names = get_option(name + '-suite')
    summary(
        {
            get_variable('emoji_' + name) + ' @0@=auto'.format(name): '[auto|enabled|disabled]',
        },
        section: ' '.join(emoji_setup, 'meson setup --reconfigure -D[option]'),
    )
    foreach command : command_names
        suite = get_option(name)
        suite.enable_auto_if(dev.enabled())
        set_variable(name, suite)
        if suite.enabled() and command not in plugin_only+module_only
            flag = find_program(
                command,
                required: false,
                disabler: true,
            )
        elif suite.enabled() and command in module_only
            modules += [command]
            flag = disabler()
        else
            flag = disabler()
        endif
        requirements = [
            'install',
            '-r',
            build_root / 'ozi' / name / command / 'requirements.txt',
        ]
        if get_option('dev').enabled() or get_variable(name).enabled() and command not in plugin_only
            run_command(
                pip_compile,  
                [
                    '-q',
                    '--allow-unsafe',
                    '--strip-extras',
                    '--generate-hashes',
                    '-o', build_root / 'ozi' / name / command / 'requirements.txt',
                    'ozi' / name / command / 'requirements.in'
                ],
                check: true,
            )
            run_command(pip, requirements, check: true)
            if not flag.found() and command not in module_only
                flag = find_program(
                    command,
                    required: false,
                    disabler: true,
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
    disabler: true
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
            emoji = get_variable('emoji_' + suite)
            header = [emoji, 'meson', 'test', '--suite=@0@'.format(suite)]
            feature = get_variable(suite)
            if feature.enabled()
                if app not in plugin_only+module_only
                    if app not in no_version
                        summary(
                            {
                                ' '.join(emoji_metadata_version, app): get_variable(
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
                        fallback_version = 'unknown'
                    endif
                    if app in no_version
                        if packaged_version == ''
                            app = ' '.join(emoji_no_version, app)
                            version = fallback_version
                        else
                            app = ' '.join(emoji_metadata_version, app)
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
                            ['show', run_command(python, ['-c', to_distribution.format(app)], kwargs: no_check).stdout()],
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
                        fallback_version = 'unknown'
                    endif
                    if app in no_version
                        summary(
                            {' '.join(emoji_metadata_version, app): fallback_version},
                            section: ' '.join(header),
                        )
                    else
                        summary(
                            {' '.join(emoji_metadata_version, app): packaged_version},
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
add_test_setup('dev', is_default: true, env: env)
env.append('TESTS_BUILDDIR', build_root)
no_check = {'check': false, 'env': env}
opt_cov_eq_project_name = '--cov='+project_name
build_commands = {'dev': []}
foreach name: namespace
    add_test_setup(
        name,
        exclude_suites: get_option(name+'-exclude-suites'),
        timeout_multiplier: get_option(name+'-timeout-multiplier'))
    set_variable(name+'_kwargs', {'suite': name, 'env': env})
    command_names = get_option(name+'-suite')
    foreach command: command_names
        if command not in plugin_only
            _args = get_option('args-'+command)
        else
            _args = []
        endif
        command_args = []
        test_app_args = {}
        foreach arg : _args
            if arg.startswith('@') and (arg.endswith('@') or arg.endswith('@/'))
                arg = arg.strip('@')
                if is_variable(arg)
                    arg = get_variable(arg)
                elif arg.endswith('@/')
                    arg = get_variable(arg.replace('@/', '')) + '/'
                else
                    warning(arg+' unknown')
                endif
            endif
            command_args += arg
        endforeach
        if command in ['pytest']
            test_paths = []
            foreach file: test_files
                test_paths += ['tests' / file]
            endforeach
            command_args = test_paths + command_args
        endif
        if command not in plugin_only
            foreach app, args : {command: command_args}
                if app in module_only
                    args = ['-m', app.replace('-', '_'), args]
                endif
                args = {'args': args, 'env': env, 'priority': get_option(name+'-priority'), 'suite': name}
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

summary(
    {
        emoji_no_version: 'non-standard PyPA version metadata',
        emoji_metadata_version: 'standard PyPA version metadata',
        emoji_directory: 'install directory',
        emoji_setup: 'developer setup invocations (dev)',
        emoji_dist: 'distribution               (dist)',
        emoji_docs: 'documentation              (docs)',
        emoji_lint: 'linting & typechecking     (lint)',
        emoji_test: 'testing & checkpointing    (test)',
    },
    section: ' '.join(emoji_generic, 'Configuration Legend'),
)
display_dirs = [
    'prefix',
    'bindir',
    'libdir',
    'datadir',
    'localedir',
    'python.install_env',
    'python.platlibdir',
    'python.purelibdir',
]
foreach dir : display_dirs
    summary(
        {'📁 ' + dir: get_option(dir)},
        section: '〽️ meson install -C @0@'.format(build_root),
    )
endforeach