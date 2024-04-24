# Create secret for the first time, after it was created we can keep update it.
import datetime
import json
import logging
from pathlib import Path

from google.cloud import secretmanager, secretmanager_v1
from pytz import timezone

from npgsm import NPGSM

LOG_DIR = "./log"
Path(LOG_DIR).mkdir(exist_ok=True, parents=True)
LOG_PATH = str(Path(LOG_DIR).joinpath(Path(__file__).stem)) + ".log"

logger = logging.getLogger(__name__)
logger.propagate = False  # remove duplicated log
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8", delay=False)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
SHOPS = [
    (100028015, "G2000"),
    (100033120, "S'fare"),
    (32324, "Casio Calaulator"),
    (100021544, "Clarins"),
    (35627, "Dyson"),
    (33173, "Lee"),
    (32136, "Tanita"),
    (100027987, "Casio Watch"),
    (33304, "Jockey"),
    (1000238172, "The Body Shop"),
    (33176, "Hush Puppies"),
    (100033111, "John Henry"),
    (33174, "Wrangler"),
    (100194532, "Lululun"),
    (1000054781, "Fitflop"),
    (1000072357, "Banila Co"),
    (1000168152, "Calvin Klein"),
    (1000189930, "Casio Music"),
    (1000253034, "Inglot"),
    (1000267133, "3INA"),
    (1000333324, "Tommy Hilfiger"),
    (100179015261, "Guess"),
    (100179114397, "Three"),
    (100179966199, "Nautica"),
    (100180275229, "Superga"),
    (100181028364, "Watch Station"),
    (100187688056, "Polo Ralph Lauren"),
    (100187838703, "MLB"),
    (100190637842, "Clarks"),
    (100191876166, "Kiko"),
    (100196160969, "Shaper"),
    (100181100372, "D1 Milano"),
    (100204074030, "Neocal"),
]

project_id_prd = "central-cto-cmg-data-prod"
gsm_prd = NPGSM(project_id=project_id_prd)

if __name__ == "__main__":
    # clone the secret from the dev environments
    parent = f"projects/{project_id_prd}"
    request = secretmanager_v1.ListSecretsRequest(
        parent=parent,
    )
    secret_names = gsm_prd.client.list_secrets(request)
    for secret_name in secret_names:
        print(secret_name.name)
        secret_name = secret_name.name.split("/")[-1]
        logger.info(f"working on {secret_name}")
        # get secret data
        data = gsm_prd.access_secret_version(secret_name)
        item = json.loads(data)
        # backup in log
        logger.info(f"{secret_name} {item}")
        # delete and re-create
        gsm_prd.delete_secret(secret_name)
        gsm_prd.create_secret(secret_name)
        now_th = datetime.datetime.now(timezone("Asia/Bangkok"))
        item["updated_at"] = now_th.strftime("%Y-%m-%d %H:%M:%S")
        gsm_prd.add_secret_version(secret_name, item)
        print(f"Created & Updated secret {secret_name}")
        if secret_name.startswith("test"):
            gsm_prd.delete_secret(secret_name)
    print("job is done")
