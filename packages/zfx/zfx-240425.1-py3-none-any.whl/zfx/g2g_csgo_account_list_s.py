import requests


def g2g_csgo_account_list_s():
    """
        #无需传递任何参数，自动获取所有的产品ID，等待时间较久，根据网络情况决定
    """
    字典 = {}
    url = "https://sls.g2g.com/offer/search"
    page = 1

    try:
        while True:
            params = {
                "seo_term": "counter-strike-global-offensive-accounts",
                "sort": "highest_price",
                "page_size": "100",
                "currency": "usd",
                "country": "us",
                "page": str(page),
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                results_value = data["payload"]["results"]
                if not results_value:
                    break
                for result in results_value:
                    total_offer = result["total_offer"]
                    if total_offer == 1:
                        offer_id = result["offer_id"]
                        display_price = result["display_price"]
                        字典[offer_id] = display_price
                page += 1
            else:
                #print("请求失败，状态码:", response.status_code)
                break
    except requests.exceptions.RequestException as e:
        print("网络请求错误:", e)

    return 字典
