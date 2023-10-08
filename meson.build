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
python_readlines = get_option('python-readline-snip')

# Python 3.9+ setup
python = pymod.find_installation(
    'python3',
    modules: python_dependencies,
    required: true,
    disabler: true,
)
core_metadata = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            'ozi' / 'scripts' / get_option('core-metadata-template'),
        ),
    ],
    check: true,
).stdout()
metadata_version = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            'ozi' / 'scripts' / get_option('version-metadata-template'),
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
            'ozi' / 'scripts' / get_option('scm-version-snip'),
        ),
    ],
    check: true,
).stdout()
sync_pkg_readme = run_command(
    python,
    [
        '-c',
        python_readlines.format(
            'ozi' / 'scripts' / get_option('sync-pkg-readme'),
        ),
    ],
    check: true,
).stdout()
run_command(python, ['-c', sync_pkg_readme], check: true).stdout()
pip = find_program('pip', required: true, disabler: true)
pip_compile = find_program('pip-compile', required: true)
custom_target(
    'requirements-ozi',
    input: 'requirements.in',
    output: 'requirements.txt',
    build_always_stale: true,
    build_by_default: true,
    command: ['pip-compile',  '--generate-hashes', '-o', '@OUTPUT@', '@INPUT@']
)
source_to_build.enable_auto_if(source_to_build.auto())
docs_source.enable_auto_if(docs_source.auto())
test_source.enable_auto_if(test_source.auto())
no_check = {'check': false, 'env': env}
install = ['install']
build_commands = {'dev': []}
test_app_args = {}
pip_repr = pip.full_path()
if get_option('ozi-blastpipe').enabled()
    # BEGIN BOOTSTRAP SCRIPT
    subproject('blastpipe')
    # END BOOTSTRAP SCRIPT
endif
subdir('ozi')
subdir('tests')
foreach name : namespace
    command_names = get_option(name + '-suite')
    summary(
        {
            get_variable('emoji_' + name) + ' @0@=auto'.format(name): '[auto|enabled|disabled]',
        },
        section: ' '.join(emoji_setup, 'meson setup --reconfigure -D[option]'),
    )
    foreach command : command_names
        flag = (
            command in module_only ? disabler() : find_program(
                command,
                required: false,
                disabler: true,
            )
        )
        set_variable(command.replace('-', '_'), flag)
        set_variable(
            name,
            get_option(name).enable_auto_if(get_option('dev').enabled()),
        )
        requirements = [
            'install',
            '-vvv',
            '-r',
            'ozi' / 'scripts' / name / command / 'requirements.txt',
        ]
        if get_option('dev').enabled() or get_variable(name).enabled()
            debug(run_command(pip, requirements, check: true).stdout())
        endif
        set_variable(name + '_kwargs', {'suite': name, 'env': env})
        _args = get_option('args-' + command)
        command_args = []
        foreach arg : _args
            if arg.startswith('@') and arg.endswith('@')
                arg = arg.strip('@')
                arg = is_variable(arg) ? get_variable(arg) : arg
            endif
            command_args += arg
        endforeach
        if command not in plugin_only
            test_app_args += {command: command_args}
        endif
    endforeach
endforeach
done = []
foreach name : namespace
    foreach suite : get_option(name + '-exclude-suites')
        foreach app : get_option(suite + '-suite')
            if app in done
                continue
            endif
            emoji = get_variable('emoji_' + suite)
            header = [emoji, 'meson', 'test', '--setup=@0@'.format(suite)]
            feature = get_variable(suite)
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
            if (
                app == 'semantic-release' # HACK: we should take care of python- and pytest- names here
            )
                fallback_version = run_command(
                    pip,
                    ['show', 'python-' + app],
                    kwargs: no_check,
                ).stdout().split('\n')
            else
                fallback_version = run_command(
                    pip,
                    ['show', app],
                    kwargs: no_check,
                ).stdout().split('\n')
            endif
            fallback_version = (
                fallback_version.length() > 2 ? fallback_version[1].split(':')[1].strip() : 'unknown'
            )
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
            done += app
        endforeach
    endforeach
endforeach
foreach plugin : plugin_only
    packaged_version = run_command(
        python,
        ['-c', metadata_version.format(plugin)],
        kwargs: no_check,
    ).stdout().strip()
    fallback_version = run_command(
        pip,
        ['show', plugin],
        kwargs: no_check,
    ).stdout().split('\n')
    fallback_version = (
        fallback_version.length() > 2 ? fallback_version[1].split(':')[1].strip() : 'unknown'
    )
    if plugin in no_version
        summary(
            {' '.join(emoji_metadata_version, plugin): fallback_version},
            section: ' '.join(emoji_test, 'meson test --setup=test'),
        )
    else
        summary(
            {' '.join(emoji_metadata_version, plugin): packaged_version},
            section: ' '.join(emoji_test, 'meson test --setup=test'),
        )
    endif
endforeach
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
# foreach dir : display_dirs
#     summary(
#         {'📁 ' + dir: get_option(dir)},
#         section: '〽️ meson install -C @0@'.format(build_dir),
#     )
# endforeach