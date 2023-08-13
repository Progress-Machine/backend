import time
import jwt
import requests
from product.constants import *


def _login_gpt() -> str:
    now = int(time.time())
    payload = {'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens', 'iss': SERVICE_ACCOUNT_ID,
               'iat': now, 'exp': now + 360}
    # JWT generation
    encoded_token = jwt.encode(payload, PRIVATE_KEY, algorithm='PS256', headers={'kid': KEY_ID})
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    x = requests.post(url, headers={'Content-Type': 'application/json'},
                      json={'jwt': encoded_token}).json()
    token = x['iamToken']
    return token


def get_text_from_gpt(mode: str, description: str):
    token = _login_gpt()
    url = 'https://api.ml.yandexcloud.net/llm/v1alpha/instruct'

    # Building a prompt
    data = {"model": "general"}

    # Specify an instruction for YandexGPT
    if mode == 'comment':
        data['instruction_text'] = 'Ты купил товар. Теперь ты должен написать отзыв о нем.'
    else:
        data['instruction_text'] = 'Ты должен придумать описание товара, которое поможет продать ' \
                                   'товар в интернет магазине.'
    # Set up advanced model parameters
    data['generation_options'] = {'max_tokens': 1500,
                                  'temperature': 0.5}
    # Enter the request text
    if mode == 'comment':
        data['request_text'] = "Придумай реалистичный отзыв о " + description + '.'
    else:
        data['request_text'] = "Придумай описание " + description + '.'

    # Get the model's response
    response = requests.post(url, headers={'Authorization': 'Bearer ' + token}, json=data).json()
    print(response)
    response_text = response['result']['alternatives'][0]['text']
    return response_text


if __name__ == '__main__':
    get_text_from_gpt("comment", "Футболка с тяночкой")
