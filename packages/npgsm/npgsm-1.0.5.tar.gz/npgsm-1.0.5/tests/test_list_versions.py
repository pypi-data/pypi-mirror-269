import sys
from os.path import abspath, dirname

dir_above = dirname(dirname(abspath(__file__)))
sys.path.insert(0, dir_above)
from npgsm import NPGSM

if __name__ == "__main__":
    project_id = "central-cto-cmg-data-prod"
    secret_name ='shopee_273122043'
    npgsm = NPGSM(project_id)
    versions = npgsm.get_versions(secret_name)
    print(versions)
