import os
from hivemind.utils import get_logger

logger = get_logger(__name__)

import boto3
import requests
from requests_aws4auth import AWS4Auth


async def dispense_bonus(self, bonus_dict, server_total):
    if not os.getenv("WANDB_MODE", ""):
        return
    if not self.prefix.split("_") or len(self.prefix.split("_")[0]) != 36:
        return
    real_target = server_total
    percent_map = {}
    for size in bonus_dict.values():
        real_target += size
    percent = {p2pid.to_string(): round(data_size / real_target, 3) for p2pid, data_size in bonus_dict.items() if
               data_size > 0}
    percent_map["action"] = "dispense"
    percent_map["standard_data_size"] = server_total
    percent_map["job_id"] = self.prefix.split("_")[0]
    percent_map["percent"] = percent
    stage = os.getenv("stage", "dev")
    if stage == "dev":
        api_id = "g30ih92s42"
    elif stage == "test":
        api_id = "ky87e6eagk"
    else:
        api_id = "ya5b7jtid2"
    session = boto3.Session()
    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, 'us-west-2', "execute-api")
    url = f"https://{api_id}.execute-api.us-west-2.amazonaws.com/{stage}/vc_dispense"
    response = requests.post(url, json=percent_map, auth=awsauth)
    logger.info(f"dispense response,{response.json()}")
    # todo aiohttp only support BasicAuth, do self-design method for signing the URLs in Lambda server
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, json=percent_map,auth=awsauth) as response:
    #         print("debug: dispense response", await response.json())
    return