import sys
from os.path import abspath, dirname

dir_above = dirname(dirname(abspath(__file__)))
sys.path.insert(0, dir_above)
from npgsm import NPGSM

if __name__ == "__main__":
    PROJECT_ID = "scbpt-349407"
    SA_PATH = "./tests/scbpt-data-admin.json"
    SECRET_NAME = "nptest"
    gsm = NPGSM(project_id=PROJECT_ID, gcp_service_account_path=SA_PATH)
    print(gsm.create_secret(SECRET_NAME))
    print(gsm.add_secret_version(SECRET_NAME, {"mykey": {"mykey2": "myvalue2"}}))
    x = gsm.access_secret_version(SECRET_NAME)
    print(x)
    gsm.delete_secret(SECRET_NAME)
