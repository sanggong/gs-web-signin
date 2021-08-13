import sys
import os
from PyQt5.QtWidgets import *
from Appins import Appins
from Appexe import Appexe
import gutil


def main():
    config_path = os.path.join(os.path.dirname(sys.argv[0]), gutil.CONFIG)
    if len(sys.argv) != 1 and sys.argv[1] == '-startup':
        gutil.Genshin().signin()
        print('sign in success..')
    elif os.path.exists(config_path):  exeGui(state='exe')
    else:  exeGui(state='ins')


def exeGui(state='exe'):
    app = QApplication(sys.argv)
    if state == 'exe':   appexe = Appexe()
    elif state == 'ins': appins = Appins()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
