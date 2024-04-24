from lazysdk import lazyrequests
from lazysdk import lazytime
import showlog
import copy
import json


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


def get_ad_report(
        cookie: str,
        media_type: str,
        start_date: str = None,
        end_date: str = None,
        page: int = 1,
        page_size: int = 20,
        sort_field: str = "cost",
        time_dim: str = "sum",
        sort_direction: str = "desc",
        data_dim: str = "ad",
        data_type: str = "list",
        conditions: dict = None,
        kpis: list = None,
        relate_dims: list = None,
):
    """
    报表-广告报表
    :param cookie:
    :param start_date: 数据开始日期，默认为当日
    :param end_date: 数据结束日期，默认为当日
    :param page: 页码
    :param page_size: 每页数量
    :param media_type: 媒体：gdt_new|广点通(新指标体系)，toutiao_upgrade|今日头条2.0，aggregate|不限
    :param sort_field: 排序字段
    :param time_dim: 数据的时间维度汇总方式
    :param sort_direction: 排序方式，desc降序
    :param data_dim: 数据维度，advertiser_id:账户，ad:广告
    :param data_type:
    :param conditions: 搜索条件
    :param kpis: 需要获取的字段
    :param relate_dims: 关联维度，advertiser_id:账户
    :return:
    """
    if not start_date:
        start_date = lazytime.get_date_string(days=0)
    if not end_date:
        end_date = lazytime.get_date_string(days=0)
    url = "https://cli2.mobgi.com/ReportV23/AdReport/getReport"
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "page_size": page_size,
        "media_type": media_type,
        "time_dim": time_dim,
        "data_type": data_type,
        "data_dim": data_dim,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
    }
    if media_type == "baidu":
        if not conditions:
            conditions = {
                    "keyword": "",
                    "advertiser_id": [],
                    "app_id": [],
                    "owner_user_id": [],
                    "media_agent_id": []
                }
        if not kpis:
            kpis = [
                    "cost",
                    "weixinfollowsuccessconversions",
                    "weixinfollowsuccessconversionscost",
                    "payreaduv",
                    "payreaduvcost",
                    "cpc"
                ]
        if not relate_dims:
            relate_dims = ["advertiser_id"]

    elif media_type == "gdt_new":
        if not conditions:
            conditions = {
                    "keyword": "",
                    "advertiser_id": [],
                    "app_id": [],
                    "owner_user_id": [],
                    "media_agent_id": [],
                    "landing_type": [],
                    "time_line": "REPORTING_TIME"
                }
        if not kpis:
            kpis = [
                    "cost",
                    "conversions_count",
                    "from_follow_uv",
                    "cheout_fd",
                    "cheout_fd_reward",
                    "thousand_display_price",
                    "first_pay_count",
                    "conversions_cost",
                    "from_follow_cost",
                    "valid_click_count",
                    "cpc"
                ]
        if not relate_dims:
            relate_dims = ["advertiser_id"]

    elif media_type == "toutiao_upgrade":
        if not conditions:
            conditions = {
                "keyword": "",
                "advertiser_id": [],
                "app_id": [],
                "owner_user_id": [],
                "media_agent_id": [],
                "landing_type": [],
                "cl_create_way": []
            }
        if not kpis:
            kpis = [
                "stat_cost",
                "cpm_platform",
                "convert_cnt",
                "conversion_cost",
                "active",
                "active_cost",
                "click_cnt",
                "cpc_platform",
                "attribution_game_in_app_ltv_1day",
                "attribution_game_in_app_roi_1day",
                "ctr"
            ]
        if not relate_dims:
            relate_dims = ["advertiser_id"]

    else:
        showlog.warning("未知媒体类型")
        return

    headers = copy.deepcopy(default_headers)
    headers["Cookie"] = cookie
    data["conditions"] = conditions
    data["kpis"] = kpis
    data["relate_dims"] = relate_dims
    return lazyrequests.lazy_requests(
        method="POST",
        url=url,
        json=data,
        headers=headers
    )


def get_plan_list(
        cookie: str,
        media_type: str,
        sort_field: str,
        media_account_id: int = None,
        page: int = 1,
        page_size: int = 20,
        start_date: str = None,
        end_date: str = None,
        sort_direction: str = "desc",
        data_type: str = "list",
        conditions: dict = None,
        advertiser_id: int = None,
        cdt_start_date: str = None,
        cdt_end_date: str = None,
        kpis: list = None,
        req_source: str = None
):
    """
    获取推广计划
    :param cookie:
    :param media_type:
    :param media_account_id:
    :param sort_field: 排序字段
    :param page:
    :param page_size:
    :param start_date: 数据开始日期
    :param end_date: 数据结束日期
    :param sort_direction: 排序方式，desc:降序
    :param data_type:
    :param conditions: 搜索条件
    :param advertiser_id: 账户id
    :param cdt_start_date: 创建开始时间
    :param cdt_end_date: 创建结束时间
    :param kpis:
    :param req_source: 腾讯需要的参数
    :return:
    """
    if not start_date:
        start_date = lazytime.get_date_string(days=0)
    if not end_date:
        end_date = lazytime.get_date_string(days=0)
    if not cdt_start_date:
        cdt_start_date = lazytime.get_date_string(days=-365)
    if not cdt_end_date:
        cdt_end_date = lazytime.get_date_string(days=0)
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "page_size": page_size,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
        "data_type": data_type
    }
    if media_type == "baidu":
        url = "https://cli2.mobgi.com/Baidu/Campaign/getList"
        if not conditions:
            conditions = {
                "cl_project_id": [],
                "optimize_user_id": [],
                "media_account_id": [],
                "extension_subject": [],
                "status": "",
                "keyword": "",
                "companys": [],
                "cdt_start_date": f"{cdt_start_date} 00:00:00",
                "cdt_end_date": f"{cdt_end_date} 23:59:59"
            }
            if media_account_id:
                conditions["media_account_id"] = [media_account_id]
        data["conditions"] = json.dumps(conditions)
    elif media_type == "gdt_new":
        url = "https://cli2.mobgi.com/Gdt/MainList/getList"
        if not conditions:
            conditions = {
                "is_deleted": "",
                "project_id": [],
                "advertiser_id": [],
                "user_id": [],
                "configured_status": ["STATUS_NO_DELETED"],  # 所有未删除
                "keyword": "",
                "companys": [],
                "time_line": "REPORTING_TIME",
                "cdt_start_date": f"{cdt_start_date} 00:00:00",
                "cdt_end_date": f"{cdt_end_date} 23:59:59"
            }
            if advertiser_id:
                conditions["advertiser_id"] = [advertiser_id]
        data["conditions"] = json.dumps(conditions)
        if kpis:
            data["kpis"] = kpis
        if req_source:
            data["req_source"] = req_source
    else:
        return
    headers = copy.deepcopy(default_headers)
    headers["Cookie"] = cookie
    return lazyrequests.lazy_requests(
        method="POST",
        url=url,
        json=data,
        headers=headers
    )


def update_ad_batch(
        cookie,
        media_type: str,
        end_point: str,
        adgroup_id: int = None,
        adgroup_ids: list = None,
        advertiser_id: int = None,
        advertiser_ids: list = None,
        campaign_id: int = None,
        campaign_ids: list = None,
        field: str = "disable"
):
    """
    暂停广告
    :return:
    """
    headers = copy.deepcopy(default_headers)
    headers["Cookie"] = cookie
    if media_type == "gdt_new":
        if end_point == 'updateAdGroupBatch':
            url = "https://cli2.mobgi.com/Gdt/MainList/updateAdGroupBatch"
            if not adgroup_ids:
                adgroup_ids = [adgroup_id]
            if not advertiser_ids:
                advertiser_ids = [advertiser_id]
            post_data = {
                "adgroup_ids": adgroup_ids,
                "advertiser_ids": advertiser_ids,
                "value": "",
                "field": field
            }
        elif end_point == 'updateCampaignBatch':
            url = "https://cli2.mobgi.com/Gdt/MainList/updateCampaignBatch"
            if campaign_id and not campaign_ids:
                campaign_ids = [campaign_id]
            if advertiser_id and advertiser_ids:
                advertiser_ids = [advertiser_id]
            post_data = {
                "campaign_ids": campaign_ids,
                "advertiser_ids": advertiser_ids,
                "value": "",
                "field": field
            }
        else:
            return
    else:
        return
    return lazyrequests.lazy_requests(
        method="POST",
        url=url,
        json=post_data,
        headers=headers
    )
