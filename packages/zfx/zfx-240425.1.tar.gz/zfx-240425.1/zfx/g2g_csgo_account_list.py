import requests


def g2g_csgo_account_list(页码):
    """
    #传递一个页码作为参数，只获取这一页的产品ID
    """
    字典 = {}
    url = "https://sls.g2g.com/offer/search"

    try:
        params = {
            "seo_term": "counter-strike-global-offensive-accounts",
            "sort": "highest_price",
            "page_size": "100",
            "currency": "usd",
            "country": "us",
            "page": str(页码),
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            results_value = data["payload"]["results"]
            for result in results_value:
                total_offer = result["total_offer"]
                if total_offer == 1:
                    offer_id = result["offer_id"]
                    display_price = result["display_price"]
                    字典[offer_id] = display_price
    except requests.exceptions.RequestException as e:
        print("网络请求错误:", e)

    return 字典
