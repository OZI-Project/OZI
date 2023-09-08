tests_templates = [
    'meson.build.j2',
    'new_test.py.j2',
]
foreach file: tests_templates
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates')
endforeach