project('os-installer',  
          version: '0.3.0',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
  license: 'GPL-3.0-or-later',
)

i18n = import('i18n')

application_id = 'com.github.p3732.OS-Installer'

subdir('.build_files')
subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('.build_files/postinstall.py')
