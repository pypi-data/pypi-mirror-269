from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
                 'excludes': ['tkinter',
                              'PyQt5.QtQml',
                              'PyQt5.QtBluetooth',
                              'PyQt5.QtQuickWidgets',
                              'PyQt5.QtSensors',
                              'PyQt5.QtSerialPort',
                              'PyQt5.QtSql'
                              ]}


import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('audiometry_trainer\\__main__.py',
               base=base,
               target_name = 'audiometry_trainer',
               icon='icons/audiometry_trainer_icon.ico'
               )
]

setup(name='audiometry_trainer',
    version="0.1.9",
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
