from PIL import Image
import requests

from ml_analytics.wb_parser import parse_link
from ml_analytics.get_regressor_predict_by_product import get_predict
from ml_analytics.get_analytics import get_analytics


def get_float_or_none(num):
    if num is None:
        return 0
    return float(num)


def get_product_by_link(link):
    dct_product_data = parse_link(link)
    dct_product_data["price"] = get_float_or_none(dct_product_data["price"])
    dct_product_data["old_price"] = get_float_or_none(dct_product_data["old_price"])
    dct_product_data["order_count"] = get_float_or_none(dct_product_data["order_count"])
    return dct_product_data


# def get_predict_by_link(link):
#     """получает ссылку - парсит данные, делает аналитику и получает предикт выручки"""
#
#     analys_data = get_analytics(dct_product_data)
#     revenue_predict = get_predict(dct_product_data, img)  # предикт выручки
#
#     return dct_product_data, revenue_predict, analys_data


def get_predict_for_new_product(dct_product_data):
    """для измененного товара делает аналитику и получает предикт выручки"""
    img_link = dct_product_data["img_link"]

    img_data = requests.get(img_link).content
    with open('cur_img.jpg', 'wb') as handler:
        handler.write(img_data)
    img = Image.open("cur_img.jpg")

    revenue_predict = get_predict(dct_product_data, img)  # предикт выручки
    analys_data = get_analytics(dct_product_data)

    return dct_product_data, revenue_predict, analys_data


if __name__ == '__main__':
    json_data_product, revenue, analys = get_predict_by_link(
        "https://www.wildberries.ru/catalog/26299102/detail.aspx")
    print(json_data_product)
    print(revenue)
    print(analys)
