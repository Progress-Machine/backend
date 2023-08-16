import json
import time
import jwt
import requests
from sqlalchemy.orm import Session

from ml_analytics.full_pipeline import get_product_by_link
from ml_analytics.get_analytics import get_analytics
from product.constants import *
from product.crud import create_product
from product.models import Product, ProductCreate
from storage_functions import upload_file


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


def product_analytics(product: Product) -> dict:
    dict_product = product.dict()
    dict_product.pop("id")
    dict_product.pop("created_datetime")
    dict_product["text_params"] = dict_product["text_params"].split("~")
    return get_analytics(dict_product)


async def get_product_from_wb(product_url: str, session: Session) -> Product:
    product_json = get_product_by_link(product_url)
    if product_json["text_params"] is not None:
        product_json["text_params"] = '~'.join(product_json["text_params"])
    product = ProductCreate(**product_json)
    product = create_product(product_create=product, session=session)
    data = product_analytics(product)
    with open(f"{product.id}.json", 'w') as f:
        json.dump(data, f)
    file = open(f"{product.id}.json", "rb")
    await upload_file(f"product_analytic/{product.id}.json", file.read())
    os.remove(f"{product.id}.json")
    return product
