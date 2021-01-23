import CaptchaJson as anti
import time
from requests import Session

import json


def __ini__():
    pass


def get_captcha(img_64,timeout):

    dhbegin = time.time()
    browser= Session()

    task_json = anti.create_task_json(img_64)

    browser.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    task_post = browser.post(anti.link_anticaptcha, data=json.dumps(task_json), timeout=10)

    task_data = json.loads(task_post.content.strip())

    task_json_status = anti.task_json_status(task_data)

    time.sleep(5)

    while True:
        if time.time() - dhbegin > timeout:
            return {}
        try:
            result = browser.post(anti.link_anticaptcha_result, data=json.dumps(task_json_status), timeout=3)
            data = json.loads(result.content.strip())
            if data['status'] == 'processing':
                time.sleep(2)
                continue
            return data.get('solution').get('text')
        except:
            time.sleep(2)
            continue
    return