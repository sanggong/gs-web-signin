import genshinstats as gs
import os
import sys

REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
REG_NAME = 'GenshinSignIn'
CONFIG = 'gs_signin.ini'

class Genshin():
    def __init__(self):
        config_path = os.path.join(os.path.dirname(sys.argv[0]), CONFIG)
        try:
            with open(config_path, 'r') as f:
                ltuid = int(f.readline())
                ltoken = f.readline()
                gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
        except:
            exit()

    def signin(self):
        return gs.sign_in()

    def get_signin_info(self):
        return gs.get_daily_reward_info()