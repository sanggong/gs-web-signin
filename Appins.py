from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import gutil
import sys
import os
import winreg

class Appins(QWidget):
    def __init__(self):
        super().__init__()
        self.make_text()
        self.app_lbl = QLabel(self.app_desc, self)
        self.chk_box = QCheckBox('위 내용을 인지했습니다.', self)
        self.how_lbl = QLabel(self.how_desc, self)
        self.ltuid_lbl = QLabel('ltuid :', self)
        self.ltuid_le = QLineEdit(self)
        self.ltoken_lbl = QLabel('ltoken :', self)
        self.ltoken_le = QLineEdit(self)
        self.install_btn = QPushButton('레지스트리 및 파일 생성', self)
        self.init_ui()

    def init_ui(self):
        self.chk_box.stateChanged.connect(self.activateInstall)
        self.ltuid_le.textChanged.connect(self.activateInstall)
        self.ltoken_le.textChanged.connect(self.activateInstall)
        self.install_btn.clicked.connect(self.install)

        self.ltuid_le.setEnabled(False)
        self.ltoken_le.setEnabled(False)
        self.install_btn.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.app_lbl)
        vbox.addWidget(self.chk_box)
        vbox.addWidget(self.how_lbl)
        vbox.addWidget(self.ltuid_lbl)
        vbox.addWidget(self.ltuid_le)
        vbox.addWidget(self.ltoken_lbl)
        vbox.addWidget(self.ltoken_le)
        vbox.addWidget(self.install_btn)

        self.setLayout(vbox)
        self.setWindowIcon(QIcon('icon_1.png'))
        self.setWindowTitle('gs_signin_install')
        self.setGeometry(200, 200, 400, 400)
        self.show()

    def activateInstall(self):
        if self.chk_box.isChecked():
            self.ltuid_le.setEnabled(True)
            self.ltoken_le.setEnabled(True)
            if self.ltuid_le.text() != '' and self.ltoken_le.text() != '':
                self.install_btn.setEnabled(True)
            else:
                self.install_btn.setEnabled(False)
        else:
            self.ltuid_le.setEnabled(False)
            self.ltoken_le.setEnabled(False)
            self.install_btn.setEnabled(False)

    def make_text(self):
        self.app_desc = "● 이 프로그램은 원신 웹 자동 출석을 지원하는 프로그램입니다.\n\n"\
                        "● 레지스트리에 등록되어 PC 부팅 시 마다 프로그램이 시작됩니다.\n\n"\
                        "● 로그인에는 ltuid와 ltoken이 필요하며 이는 첫 입력 후 " \
                        "이 프로그램과 동일 폴더에 gs_signin.ini 파일로 저장됩니다.\n\n"\
                        "● 파일 및 레지스트리가 저장된 후 이 프로그램을 재실행하면 당월 보상 횟수와 여부를 확인할 수 있고"\
                        "레지스트리 및 파일을 삭제할 수 있습니다.\n\n"\
                        "● 해당 파일의 위치를 바꾸고 싶은 경우 반드시 파일 및 레지스트리 삭제 후 위치 이동해주세요."
        self.how_desc = "ltuid, ltoken 확인하는 방법\n"\
                        "1. https://www.hoyolab.com/genshin/ 접속 후 로그인\n"\
                        "2. <F12>를 누른 후 상단의 [응용프로그램] > "\
                        "좌측의 [쿠키] 내 [https://webstatic-sea.mihoyo....] 클릭 > "\
                        "표의 'ltuid'와 'ltoken'의 값 확인\n"\
                        "3. 아래 텍스트창에 각각 입력 (스페이스가 없어야 합니다.)"

    def install(self):
        config_path = os.path.join(os.path.dirname(sys.argv[0]), gutil.CONFIG)
        with open(config_path, 'w') as f:
            f.write(self.ltuid_le.text() + '\n')
            f.write(self.ltoken_le.text())

        value = r'"' + os.getcwd() + r'\gs_signin.exe" -startup'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, gutil.REG_PATH, 0, winreg.KEY_WRITE) as reg:
            try:
                winreg.SetValueEx(reg, gutil.REG_NAME, 0, winreg.REG_SZ, value)
                winreg.CloseKey(reg)
                reg_msg = "레지스트리 생성 성공\n"
            except:
                reg_msg = "레지스트리 생성 실패\n"

        try:
            gs = gutil.Genshin()
            gs.signin()
            msg = '금일 출석 성공\n'
        except:
            msg = '금일 출석 실패\ngs_signin.ini 파일을 열어 ltuid, ltoken을 제대로 입력해주세요.'
        QMessageBox.about(self, 'install', reg_msg + msg)
        sys.exit()