from bs4 import BeautifulSoup
import lxml
import requests


class Product:
    ids = ["#price_inside_buybox_badge", "#newBuyBoxPrice", "#price_inside_buybox", "#price"]

    def __init__(self, url):
        self.prices = []
        self.url = url
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
        }

        response = requests.get(self.url, headers=header)
        contents = response.text
        self.soup = BeautifulSoup(contents, "lxml")

    def get_product_title(self):
        item_name = self.soup.find(name='span', id="productTitle")
        item=item_name.getText().replace(u'\xa0', u'').replace('\n', '').replace(u'\xe9', u'').replace(u"\xe0", u"")
        # print(item)
        return item

    def define_price(self):
        for i in self.ids:
            try:
                price_item = self.soup.select_one(i)
                #print(f"item: {price_item}")
            except ValueError:
                print('not found')
            else:
                if price_item is not None:
                    try:
                        price = float(price_item.getText().strip().replace("$", "").replace(" ", "").replace('\n', '').replace(u'\xa0', u'').replace("'", "").replace(",", ".").replace(u'\xe9', u'').replace(u"\xe0", u""))
                    except ValueError as e:
                        print("can not convert", e)
                    else:
                        if price > 0:
                            self.prices.append(price)
                        min_price = min(self.prices)
                        print(f"min price = {min_price}")
                        return min_price
