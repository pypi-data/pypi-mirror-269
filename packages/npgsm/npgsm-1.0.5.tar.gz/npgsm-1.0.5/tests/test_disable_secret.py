import sys
from os.path import abspath, dirname

dir_above = dirname(dirname(abspath(__file__)))
sys.path.insert(0, dir_above)
from npgsm import NPGSM

if __name__ == "__main__":
    project_id = "central-cto-ssp-data-hub-prod"
    npgsm = NPGSM(project_id)
    secrets = npgsm.access_secret_version("shopee_295338991")
    print(secrets)
    # npgsm.disable_secret_version('shopee_295338991',1)
    versions = npgsm.get_versions("shopee_295338991")
    print(versions)
