#
# ! Class for getting product price

import requests
from bs4 import BeautifulSoup


class GetProductPrice:
    """
    A class to fetch the product price and product name from any online shopping product page.
    """

    def __init__(self, product_url: str):
        self.product_url = product_url

    def get_price_and_product(self):
        """
        Retrieves the product price and product name from the online shopping page.
        Returns:
        1. int: The product price as an integer.
        2. str: The product name as an string.
        """

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        response = requests.get(self.product_url, headers=header)

        # ? you can use both either .content or .text, I prefer what I learnt
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())

        product_price = soup.find("span", class_="a-price-whole").getText()

        if "," in product_price and "." in product_price:
            product_price = product_price.replace(",", "")
            product_price = product_price.replace(".", "")
            product_price = int(product_price)
        elif "." in product_price:
            product_price = product_price.replace(".", "")
            product_price = int(product_price)

        product_name = (
            soup.find("span", class_="a-size-large product-title-word-break")
            .getText()
            .strip()
        )

        return product_price, product_name
