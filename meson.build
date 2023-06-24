# Copyright 2023 Ross J. Duff MSc 
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
project('OZI', version: run_command(
  'python3', # scm_version_snip
  ['-c', 'from setuptools_scm import get_version;print(get_version(normalize=False))'], 
  check:true
 ).stdout().strip(), default_options: ['warning_level=3'],
        license: 'Apache-2.0', license_files: 'LICENSE.txt', meson_version: '>=1.1.0')
pkg_info = {
        '@PYTHON_MAJOR@'       : '3',
        '@PYTHON_SECURITY_OLD@': '3.9',
        '@PYTHON_SECURITY_NEW@': '3.10',
        '@PYTHON_BUGFIX@'      : '3.11',
}
env   = environment()
fs    = import('fs')
pymod = import('python')
# emoji
emoji_no_version       = get_option('emoji-no-version')    
emoji_metadata_version = get_option('emoji-metadata-version')
emoji_directory        = get_option('emoji-directory')
emoji_setup            = get_option('emoji-setup')
emoji_dist             = get_option('emoji-dist')
emoji_docs             = get_option('emoji-docs')
emoji_lint             = get_option('emoji-lint')
emoji_test             = get_option('emoji-test')
# prescript arrays
no_version             = get_option('no-version')
unhashable             = get_option('unhashable')
should_fail            = get_option('should-fail')
module_only            = get_option('module-only')
dist_suite             = get_option('dist-suite')
docs_suite             = get_option('docs-suite')
lint_suite             = get_option('lint-suite')
test_suite             = get_option('test-suite')
dist_exclude_suites    = get_option('dist-exclude-suites')
docs_exclude_suites    = get_option('docs-exclude-suites')
lint_exclude_suites    = get_option('lint-exclude-suites')
test_exclude_suites    = get_option('test-exclude-suites')
# descript arrays   
namespace              = get_option('namespace')
pytest_plugins         = get_option('pytest-plugins')
python_dependencies    = get_option('python-dependencies')
# features   
dev                    = get_option('dev')
source_to_build        = get_option('source-to-build')
docs_source            = get_option('docs-source')
test_source            = get_option('test-source')
# templates
python_readlines       = get_option('python-readline-snip')

# Python 3.9+ setup
python = pymod.find_installation('python3', modules: python_dependencies, required: true, 
                                 disabler: true)
core_metadata          = run_command(python,
['-c', python_readlines.format('ozi'/'scripts'/get_option('core-metadata-template'))],
check: true).stdout()
metadata_version       = run_command(python,
['-c', python_readlines.format('ozi'/'scripts'/get_option('version-metadata-template'))],
check: true).stdout()
# snippets
scm_version_snip       = run_command(python,
['-c', python_readlines.format('ozi'/'scripts'/get_option('scm-version-snip'))],
check: true).stdout()
pip = find_program('pip', required: true, disabler: true)
source_to_build.enable_auto_if(source_to_build.auto())
docs_source.enable_auto_if(docs_source.auto())
test_source.enable_auto_if(test_source.auto())
no_check = {'check': false, 'env': env}
install = ['install']
build_commands = {'dev': []}
test_app_args = {}
pip_repr = pip.full_path()
if get_option('ozi-bootstrap').enabled()
 # BEGIN BOOTSTRAP SCRIPT
 env             = environment()
 source_root     = meson.current_source_dir()
 build_root      = meson.current_build_dir()
 fs              = import('fs')
 pymod           = import('python')
 project_name    = get_option('project-name'   ).auto()? meson.project_name() : 'todo'
 build_dir       = get_option('build-dir'      ).auto()? fs.stem(build_root)  : 'todo'
 source_to_build = get_option('source-to-build').auto()? configuration_data() : 'todo'
 docs_source     = get_option('docs-source'    ).auto()? 'subprojects/docs'   : 'todo'
 test_source     = get_option('test-source'    ).auto()? 'tests'              : 'todo'
 dev  = subproject('dev')
 foreach var : get_option('variables')
 name = var.replace('-', '_')
 set_variable(name, dev.get_variable(name))
 endforeach
 scm_version = run_command(python, ['-c', scm_version_snip], check:true).stdout().strip()
 semantic_version = meson.project_version().split('.')
 maj_version = semantic_version.get(0)
 min_version = semantic_version.get(1)
 pat_version = semantic_version.get(2)
 configure_file(input: 'pyproject.toml', output: 'pyproject.toml', 
 configuration: configuration_data({
  'PROJECT_NAME' : project_name,
  'MESON_DIST_FALLBACK_VERSION' : '.'.join(maj_version, min_version, pat_version),
 }))
 foreach source : ['README.rst', 'CHANGELOG.md', 'LICENSE.txt']
  fs.copyfile(source)
 endforeach
 python_files = []
 stub_files = []
 foreach dir : [project_name]
  subdir(dir.to_lower())
 endforeach
 foreach file : python_files
  python.install_sources(file)
 endforeach
 # TODO: documentation build imports are broken for dist
 # docs = subproject('docs')
 # TODO: stub build imports are broken for dist
 # stubs = custom_target('stubs', install: true, install_dir: get_option('prefix'),
 #  output: stub_files,
 #  command: [find_program('pyright', required: true), '--createstub', project_name])
 foreach dir : [
  'prefix',
  'bindir',
  'libdir',
  'datadir',
  'localedir',
  'python.install_env', 
  'python.platlibdir', 
  'python.purelibdir'
 ]
  summary({'📁 '+dir : get_option(dir)}, section: '〽️ meson install -C @0@'.format(build_dir))
 endforeach
 # END BOOTSTRAP SCRIPT
endif
foreach name: namespace
 command_names = get_option(name+'-suite')
 summary({get_variable('emoji_'+name)+' @0@=auto'.format(name): '[auto|enabled|disabled]'}, 
  section: '🧪 meson setup --reconfigure -D[option]')
 foreach command: command_names
  flag = command in module_only? disabler() : find_program(command, required: false, disabler: true)
  set_variable(command.replace('-', '_'), flag)
  if not flag.found() and command not in module_only
   requirements = ['-vvv', '-r', 'scripts'/name/command/'requirements.txt']
   install += requirements
   build_commands += {name: ['install'] + requirements}
  endif
  set_variable(name, get_option(name).enable_auto_if(get_option('dev').enabled()))
  set_variable(name+'_kwargs', {'suite': name, 'env': env})
  _args = get_option('args-'+command)
  command_args = []
  foreach arg : _args
   if arg.startswith('@') and arg.endswith('@')
    arg = arg.strip('@')
    arg = is_variable(arg)? get_variable(arg) : arg
   endif
   command_args += arg
  endforeach
  if command not in pytest_plugins
   test_app_args += {command: command_args}
  endif
 endforeach
endforeach
if install == ['install']
 install = ['--help']
endif
build_commands += {'dev': install}
foreach suite, command_arr : build_commands
 if get_option('dev').auto() or get_option(suite).enabled()
  debug(run_command(pip, command_arr, check: true).stdout())
 endif
 if suite in 'dev'
  break
 endif
endforeach
foreach pytest_plugin : pytest_plugins
 plugin_found = run_command(pip, 'check', pytest_plugin, kwargs: no_check).returncode() == 0
 plugin_found? true : warning('missing plugin @0@'.format(pytest_plugin))
endforeach
done = []
foreach name : namespace
 foreach suite : get_option(name+'-exclude-suites')
  foreach app : get_option(suite+'-suite')
   if app in done
    continue
   endif
   emoji = get_variable('emoji_'+suite)
   header = [emoji, 'meson', 'test', '--setup=@0@'.format(suite)]
   feature = get_variable(suite)
   if app not in no_version
    summary({'📦 '+app: get_variable(app.replace('-', '_')).version()}, section: ' '.join(header))
   endif
   packaged_version = run_command(python, ['-c', metadata_version.format(app)], 
   kwargs: no_check).stdout().strip()
   if app == 'semantic-release'  # HACK: we should take care of python- and pytest- names here
    fallback_version = run_command(pip, ['show', 'python-'+app], kwargs: no_check).stdout().split('\n')
   else
    fallback_version = run_command(pip, ['show', app], kwargs: no_check).stdout().split('\n')
   endif
   fallback_version = fallback_version.length() > 2? fallback_version[1].split(':')[1].strip(
   ) : 'unknown'
   if app in no_version
    if packaged_version == ''
     app = '📡 '+app
     version = fallback_version
    else
     app = '📦 '+app
     version = packaged_version
    endif
    if app not in done
     summary({app : version}, section: ' '.join(header))
    endif
   endif
   done += app
  endforeach
 endforeach
endforeach
foreach pytest_plugin : pytest_plugins
 packaged_version = run_command(python, ['-c', metadata_version.format(pytest_plugin)], 
 kwargs: no_check).stdout().strip()
 fallback_version = run_command(pip, ['show', pytest_plugin], kwargs: no_check).stdout(
 ).split('\n')
 fallback_version = fallback_version.length() > 2? fallback_version[1].split(':')[1].strip():\
 'unknown'
 if pytest_plugin in no_version
  summary({emoji_metadata_version+' '+pytest_plugin: fallback_version}, 
          section: '✅ meson test --setup=test')
 else
  summary({'📡 '+pytest_plugin: packaged_version}, section: '✅ meson test --setup=test')
 endif
endforeach
summary({
 emoji_no_version       : 'non-standard PyPA version metadata',
 emoji_metadata_version : 'standard PyPA version metadata',
 emoji_directory        : 'install directory',
 emoji_setup            : 'developer setup invocations (dev)',
 emoji_dist             : 'distribution               (dist)',
 emoji_docs             : 'documentation              (docs)',
 emoji_lint             : 'linting & typechecking     (lint)',
 emoji_test             : 'testing & checkpointing    (test)',
}, section: '〽️ Configuration Legend')
