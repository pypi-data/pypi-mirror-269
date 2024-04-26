import os
import sys
import ctypes
import platform
import argparse
from qtpy import QtWidgets, QtGui, QtCore

from libreflow_launcher.model import Servers, Projects, Settings
from libreflow_launcher.controller import Controller
from libreflow_launcher.view import MainWindow


class App(QtWidgets.QApplication):

    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.setApplicationName("Libreflow Launcher")

        self.parse_command_line_args(argv)

        QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+'/ui/fonts/Asap-VariableFont_wdth,wght.ttf')
        self.setFont(QtGui.QFont('Asap', 9))

        QtCore.QDir.addSearchPath('icons.gui', os.path.dirname(__file__)+'/ui/icons/gui')

        css_file = os.path.dirname(__file__)+'/ui/styles/default/default_style.css'
        with open(css_file, 'r') as r:
            self.setStyleSheet(r.read())

        # Connect everything together
        self.servers_model = Servers()
        self.projects_model = Projects()
        self.settings_model = Settings()

        self.ctrl = Controller(self.servers_model, self.projects_model, self.settings_model)
        self.view = MainWindow(self.ctrl)
        
        self.view.show()
    
    def parse_command_line_args(self, args):
        parser = argparse.ArgumentParser(
            description='Libreflow Launcher Arguments'
        )

        parser.add_argument(
            '-S', '--site', default='LFS', dest='site', help='Site Name to use'
        )

        values, _ = parser.parse_known_args(args)

        if values.site:
            os.environ['LF_LAUNCHER_SITE_NAME'] = values.site


if __name__ == '__main__':
    if platform.system() == "Windows":
        myappid = 'lfscoop.libreflow_launcher'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = App(sys.argv)
    sys.exit(app.exec_())