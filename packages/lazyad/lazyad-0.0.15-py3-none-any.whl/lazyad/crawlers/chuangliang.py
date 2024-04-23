from lazysdk import lazyrequests
import copy

default_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Host": "cli2.mobgi.com",
        "Origin": "https://cl.mobgi.com",
        "Referer": "https://cl.mobgi.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0",
    }


def get_media_account(
        media_type: str,
        cookie: str = None,
        page: int = 1,
        page_size: int = 20,
        total_count: int = 0
):
    """
    获取 推广-账户管理下的账户列表
    :param media_type: 媒体类型
    :param cookie:
    :param page:
    :param page_size:
    :param total_count:
    :return:
    """

    url = 'https://cli2.mobgi.com/Media/Account/getList'
    data = {
        "media_type": media_type,
        "advertiser_type": "1",
        "page": page,
        "page_size": page_size,
        "total_count": total_count
    }
    headers = copy.deepcopy(default_headers)
    headers["Cookie"] = cookie

    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=data,
        headers=headers,
        return_json=True
    )
