import os
import tkinter as tk
from configparser import ConfigParser
from platform import system
from subprocess import run
from tkinter import filedialog


class IconChanger():
    """
        mode = 1, Change folder icon

        mode = 2, Reset folder and .ini attributes, delete .ini
    """
    def __init__(self, mode=1):
        self.base_path = None
        self.mode = mode

    def start(self):
        self.get_base_path()
        self.get_directory_list()
        self.get_settings()

        if not self.settings:
            print('>>> Settings file is empty or format error')
            return

        for element in self.settings:
            if mode == 1:
                self.generate_desktop_ini(element)
                self.set_attributes(element)
            else:
                self.clear_attributes(element)
                self.remove_desktop_ini(element)

    def get_base_path(self):
        root = tk.Tk()
        root.withdraw()

        print('>>> Select the target path...')
        base_path = ''
        while base_path == '':
            base_path = (filedialog.askdirectory()).replace('/', os.sep)

        self.base_path = base_path

        print('>>> Base Path: ', self.base_path)

    def get_directory_list(self):
        file_and_directory = os.listdir(self.base_path)
        directory_list = [item for item in file_and_directory if os.path.isdir(self.base_path + os.sep + item)]

        self.directory_list = directory_list

        print('>>> Directories: ', self.directory_list)

    def get_settings(self):
        file_path = self.select_settings_file_path()

        print('>>> Settings file Path: ', file_path)

        config = ConfigParser()
        config.read(file_path)

        config_sections = config.sections()
        self.settings = []
        for program_name in config_sections:
            program_abs_path = str(self.base_path) + os.sep + program_name
            program_icon_abs_path = program_abs_path + config[program_name]['iconresource']
            if os.path.isfile(program_icon_abs_path) and os.path.isdir(program_abs_path):
                self.settings.append([program_abs_path, program_icon_abs_path])
            else:
                print('>>> Program dir or icon DO NOT EXIST: ', program_abs_path, program_icon_abs_path)

    def select_settings_file_path(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(filetypes=(("組態設定檔", "*.ini"), ("所有檔案", "*.*")))

        if file_path.endswith(r'.ini'):
            return file_path.replace('/', os.sep)
        else:
            raise TypeError('<<< Must be INI file. >>>')

    def generate_desktop_ini(self, settings):
        config = ConfigParser()
        config.read(settings[0] + os.sep + 'desktop.ini')

        if '.ShellClassInfo' in config:
            if config['.ShellClassInfo'].get('IconResource') is not None:
                print('Reset origin value: ', config['.ShellClassInfo']['IconResource'])
        else:
            config['.ShellClassInfo'] = {}

        config['.ShellClassInfo']['IconResource'] = settings[1] + ',0'

        try:
            with open(settings[0] + os.sep + 'desktop.ini', 'w') as configfile:
                config.write(configfile)
                print('Generated: ' + settings[0] + os.sep + 'desktop.ini')
        except Exception as e:
            print(e)

    def set_attributes(self, settings):
        dir_path = settings[0]
        ini_path = dir_path + os.sep + 'desktop.ini'

        run(['attrib', '+a', '+s', '+h', ini_path], shell=True)
        print('Set attributes: Archive, System, Hidden ->', ini_path)

        run(['attrib', '+r', dir_path], shell=True)
        print('Set attribute: Read-only ->', dir_path)
        print()

    def clear_attributes(self, settings):
        dir_path = settings[0]
        ini_path = dir_path + os.sep + 'desktop.ini'

        if os.path.isfile(ini_path):
            run(['attrib', '-a', '-s', '-h', ini_path], shell=True)
            print('Clear attributes: Archive, System, Hidden ->', ini_path)
        else:
            print('DO NOT EXIST: ', ini_path)

        run(['attrib', '-r', dir_path], shell=True)
        print('Clear attribute: Read-only ->', dir_path)

    def remove_desktop_ini(self, settings):
        ini_path = settings[0] + os.sep + 'desktop.ini'

        if os.path.isfile(ini_path):
            os.remove(ini_path)
            print('Removed: ', ini_path)
        else:
            print('DO NOT EXIST: ', ini_path)
        print()


if __name__ == "__main__":
    if system() != 'Windows':
        print('<<< Must be Windows system. >>>')
        print('<<< Must be Windows system. >>>')
        print('<<< Must be Windows system. >>>')
        os.system('pause')
    else:
        while True:
            print(
                '--------------------------------------------------\n'
                '(1) Change folder icon\t'
                '(2) Reset folder and .ini attributes, delete .ini'
            )
            mode = input('Please select mode: ')
            if mode.isdigit():
                mode = int(mode)
                if mode >= 1 and mode <= 2:
                    break
        handler = IconChanger()
        handler.start()

        print('FINISHED')
        os.system('pause')
