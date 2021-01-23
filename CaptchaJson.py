#Quebra de Captcha utilizando o AntiCaptcha
def __ini__():
    pass


def create_task_json(img_64):

    task_json = {"clientKey":"bce67d58082ef2657cc434be18904d95",
                 "task": {"type": "ImageToTextTask",
                          "body": img_64,
                          "phrase": "false",
                          "case": "false",
                          "numeric": "0",
                          "math": "0",
                          "minLength": "0",
                          "maxLength": "0"
                        }
                }
    return task_json

def task_json_status(task_data):
    json_status = {"clientKey": "bce67d58082ef2657cc434be18904d95",
                   "taskId": task_data['taskId']
                  }
    return json_status

link_anticaptcha = 'https://api.anti-captcha.com/createTask'

link_anticaptcha_result = 'https://api.anti-captcha.com/getTaskResult'