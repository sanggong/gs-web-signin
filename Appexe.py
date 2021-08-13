import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import gutil
import winreg

class Appexe(QWidget):
    def __init__(self):
        super().__init__()
        self.gs = gutil.Genshin()
        self.lbl1 = QLabel('금일 보상 :', self)
        self.te1 = QTextEdit(self)
        self.delete_btn = QPushButton('레지스트리/파일 삭제', self)
        self.reward_btn = QPushButton('보상 수령', self)
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.delete_btn)
        hbox.addWidget(self.reward_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.te1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.delete_btn.clicked.connect(self.delete_registry)
        self.reward_btn.clicked.connect(self.sign_in)

        self.show_reward_text()
        self.setWindowIcon(QIcon('icon_1.png'))
        self.setWindowTitle('gs_signin')
        self.setGeometry(200, 200, 400, 300)
        self.show()

    def delete_registry(self):
        reply = QMessageBox.question(self, 'delete',
                                     "레지스트리와 gs_signin.ini를 삭제하시겠습니까?\n"
                                     "삭제 후 프로그램을 재실행하면 다시 설치할 수 있습니다.",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            try:
                config_path = os.path.join(os.path.dirname(sys.argv[0]), gutil.CONFIG)
                os.remove(config_path)
                file_msg = 'gs_signin.ini 삭제 완료\n'
            except:
                file_msg = 'gs_signin.ini 삭제 실패, 직접 삭제해주세요.\n'

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, gutil.REG_PATH, 0, winreg.KEY_WRITE) as reg:
                try:
                    winreg.DeleteValue(reg, gutil.REG_NAME)
                    winreg.CloseKey(reg)
                    reg_msg = "레지스트리 삭제 완료"
                except:
                    reg_msg = "레지스트리 삭제 실패\n"\
                              "레지스트리 편집기의 '컴퓨터\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'에서"\
                              "GenshinSignIn을 직접 지워주세요."
            QMessageBox.information(self, 'delete', file_msg + reg_msg)

    def sign_in(self):
        self.gs.signin()
        self.show_reward_text()

    def show_reward_text(self):
        info = self.gs.get_signin_info()
        text = '일차 보상 수령 '
        if info['is_sign'] is True:
            cnt = str(info['total_sign_day'])
            result = '성공'
        else:
            cnt = str(info['total_sign_day'] + 1)
            result = '실패'
        self.te1.setText(info['today'] + '\n' + cnt + text + result)

