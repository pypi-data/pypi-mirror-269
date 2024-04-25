import requests

def 取服务器列表及链接():
    page = 1
    titles_links_dict = {}
    while True:
        url = f"https://sls.g2g.com/offer/search?page={page}&seo_term=wow-classic-gold&page_size=48&currency=USD&country=HK"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 如果请求失败将会抛出异常
        except requests.exceptions.RequestException as e:
            print("网络异常:", e)
            return {}  # 返回空字典

        data = response.json()
        results_value = data["payload"]["results"]

        if not results_value:  # 如果结果为空，说明已经到达最后一页
            break

        for result in results_value:
            title = result["title"]
            service_id = result["service_id"]
            brand_id = result["brand_id"]
            filter_attribute = result["filter_attributes"]
            key = next(iter(filter_attribute.keys()))  # 获取字典的键
            value = filter_attribute[key][0]  # 获取字典对应键的值
            filter_attribute = key + ":" + value

            link = f"https://www.g2g.com/offer/{title.replace('] - ', '----').replace(' [', '--')}?service_id={service_id}&brand_id={brand_id}&fa={filter_attribute}"

            titles_links_dict[title] = link

        page += 1  # 继续下一页

    return titles_links_dict


# # 调用函数
# result = 取服务器列表及链接()
# ic(len(result), result)
