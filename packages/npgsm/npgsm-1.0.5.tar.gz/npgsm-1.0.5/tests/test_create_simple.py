import sys
from os.path import abspath, dirname

dir_above = dirname(dirname(abspath(__file__)))
sys.path.insert(0, dir_above)
from npgsm import NPGSM

if __name__ == "__main__":
    PROJECT_ID = "central-cto-cmg-data-prod"
    SECRET_NAME = "nptest"
    gsm = NPGSM(project_id=PROJECT_ID)
    gsm.create_secret(SECRET_NAME, "asia-southeast1")
