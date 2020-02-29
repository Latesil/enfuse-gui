project('enfuse-gui',  
          version: '0.4.0',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

appname = 'com.gitlab.Latesil.enfuse-gui'

i18n = import('i18n')


subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
