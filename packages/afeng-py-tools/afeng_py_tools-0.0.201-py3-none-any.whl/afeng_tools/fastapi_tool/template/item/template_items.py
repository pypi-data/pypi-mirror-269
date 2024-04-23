from typing import Optional, Any

from afeng_tools.pydantic_tool.model.common_models import LinkItem, EnumItem
from pydantic import BaseModel, Field

from afeng_tools.fastapi_tool.template.item import CalendarDataItem, AppinfoDataItem, Error501DataItem, \
    Error500DataItem, Error404DataItem


class TemplateBaseData(BaseModel):
    """模板基础数据"""
    # 是否是移动端
    is_mobile: Optional[bool] = False
    # 附加的数据字典
    data_dict: Optional[dict[str, Any]] = None


class TemplateHtmlHeadData(TemplateBaseData):
    """模板head信息"""
    # 标题
    title: str
    # 描述
    description: Optional[str] = None
    # 关键字
    keyword_list: Optional[list[str]] = []
    # 作者
    author: Optional[str] = Field(default='chentiefeng')
    # favicon图标
    favicon: Optional[str] = Field(default='/favicon.ico')
    # 域信息
    origin: Optional[str] = None


class TemplateBreadCrumbData(TemplateBaseData):
    """面包屑信息"""
    # 标题
    page_title: Optional[str] = None
    # 面包屑列表
    bread_crumb_list: Optional[list[LinkItem]] = None


class TemplateLeftNavData(TemplateBaseData):
    """左侧链接信息"""
    # 链接列表
    link_list: Optional[list[LinkItem]] = None


class TemplatePaginationAreaData(TemplateBaseData):
    """分页信息"""
    # 上一页按钮
    pre_btn: Optional[LinkItem] = None
    # 下一页按钮
    next_btn: Optional[LinkItem] = None
    # 中间数据按钮
    data_list: Optional[list[LinkItem]] = []
    # 总数量
    total_count: Optional[int] = 0
    # 总页数
    total_page: Optional[int] = 0
    # 跳转到某页的地址
    jump_href: Optional[str] = None
    # 跳转页面时附加的数据数据字典
    jump_data_dict: Optional[dict[str, Any]] = None


class TemplatePageFooterData(TemplateBaseData):
    """页面底部链息"""
    # 友情链接标题
    friendly_link_title: Optional[LinkItem] = LinkItem(title='友情链接', href='/article/help/friendly_link')
    # 联系信息，如：QQ: 1640125562， 邮箱：imafengbook@aliyun.com
    contact_info: Optional[str] = None
    # 友情链接列表
    friendly_link_list: Optional[list[LinkItem]] = None
    # 底部链接列表
    footer_link_list: Optional[list[LinkItem]] = None
    # 版权链接
    copyright_link: Optional[LinkItem] = LinkItem(title='阿锋', href='/')
    # ICP备案信息，如：京ICP备2023032898号-1 京公网安备xxxx号
    icp_record_info: Optional[str] = None
    # 公安备案信息，如：京公网安备11000002000001号
    police_record_info: Optional[str] = None
    # 公安备案号：11000002000001
    police_record_code: Optional[str] = None


class TemplateTopBarData(TemplateBaseData):
    """页面顶部top bar链息"""
    # 应用链接列表
    app_link_list: Optional[list[LinkItem]] = None
    # 微信公众号图片
    weixin_qr_code_image: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 快捷链接列表
    quick_link_list: Optional[list[LinkItem]] = None


class TemplateLogoSearchData(TemplateBaseData):
    """页面顶部logo search链息"""
    # logo图片
    logo_image: Optional[str] = '/image/logo/logo.png'
    # 应用标题, 如：阿锋书屋
    app_title: Optional[str] = None
    # 查询表单提交url
    search_form_submit_url: Optional[str] = '/search'
    # 查询选项名称， 如：search_type
    search_select_type_name: Optional[str] = 'search_type'
    # 查询选项列表
    search_select_option_list: Optional[list[EnumItem]] = None


class TemplateFixNavData(TemplateBaseData):
    """页面顶部fix nav链息"""
    # 类型链接列表
    type_link_list: Optional[list[LinkItem]] = None
    # 热点链接列表
    hotspot_link_list: Optional[list[LinkItem]] = None


class TemplatePageHeaderData(TemplateBaseData):
    """页面顶部链息"""
    # topbar数据
    topbar_data: TemplateTopBarData = TemplateTopBarData()
    # logo search数据
    logo_search_data: TemplateLogoSearchData = TemplateLogoSearchData()
    # fix nav数据
    fix_nav_data: TemplateFixNavData = TemplateFixNavData()


class TemplateIndexPageHeaderData(TemplateBaseData):
    """页面顶部链息"""
    # 应用链接列表
    app_link_list: Optional[list[LinkItem]] = None
    # 微信公众号图片
    weixin_qr_code_image: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 快捷链接列表
    quick_link_list: Optional[list[LinkItem]] = None
    # 全部类型列表
    all_type_list: Optional[list[LinkItem]] = None


class TemplatePageSearchHeaderData(TemplateBaseData):
    """页面搜索顶部链息"""
    # 微信公众号图片
    weixin_qr_code_image: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 快捷链接列表
    quick_link_list: Optional[list[LinkItem]] = None
    # 查询关键字
    keyword: Optional[str] = None
    # 搜索模式
    search_model_list: Optional[list[EnumItem]] = None
    # 搜索类型
    search_type_list: Optional[list[EnumItem]] = None


class TemplateResultListData(TemplateBaseData):
    """页面结果列表链息"""
    # 结果值列表
    data_list: Optional[list[Any]] = None
    # 没有数据时的html代码
    none_html_code: Optional[str] = '暂无数据！'


class TemplateGroupListData(TemplateBaseData):
    # 查询提交url
    search_url: Optional[str] = None
    # 查询输入框placeholder
    search_placeholder: Optional[str] = None
    # 搜索值
    search_value: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateTagListData(TemplateBaseData):
    # 查询提交url
    search_url: Optional[str] = None
    # 查询输入框placeholder
    search_placeholder: Optional[str] = None
    # 搜索值
    search_value: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateFilterTypeAreaData(TemplateBaseData):
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateDayCalendarData(TemplateBaseData):
    # 标题
    title: Optional[str] = None
    # 初始日期
    init_date: Optional[str] = None
    # 数据列表
    data_list: Optional[list[CalendarDataItem]] = None


class TemplateTabPanelItem(BaseModel):
    # 是否激活
    is_active: Optional[bool] = False
    # 编码
    code: Optional[str] = None
    # 标题
    title: Optional[str] = None
    # html内容
    html: Optional[str] = None


class TemplateTabPanelData(TemplateBaseData):
    # 查看更多的按钮
    more_btn: Optional[LinkItem] = None
    # 子项列表
    item_list: Optional[list[TemplateTabPanelItem]] = None


class TemplateTopRankingData(TemplateBaseData):
    # 标题
    title: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateRedirectDownloadAreaData(TemplateBaseData):
    """下载区域数据"""
    # 应用信息
    app_info: Optional[AppinfoDataItem] = None
    # 文件名
    file_name: Optional[str] = None
    # 广告列表
    ad_list: Optional[list[LinkItem]] = None
    # 下载链接
    download_url: Optional[str] = None
    # 返回链接
    back_url: Optional[str] = '/'


class TemplateRedirectAreaData(TemplateBaseData):
    """重定向区域数据"""
    # 应用信息
    app_info: Optional[AppinfoDataItem] = None
    # 广告列表
    ad_list: Optional[list[LinkItem]] = None
    # 跳转链接
    redirect_url: Optional[str] = None
    # 返回链接
    back_url: Optional[str] = '/'


class TemplateInfoAreaData(TemplateBaseData):
    """信息区域数据"""
    # 应用信息
    app_info: Optional[AppinfoDataItem] = None
    # 广告列表
    ad_list: Optional[list[LinkItem]] = None
    # 标题
    title: Optional[str] = None
    # 数据列表
    data_list: Optional[list[LinkItem]] = None


class TemplateShowQrcodeAreaData(TemplateBaseData):
    """显示二维码区域数据"""
    # 二维码图片地址
    qrcode_image_url: Optional[str] = '/static/image/qrcode/wx_of_qrcode.jpg'
    # 二维码图片标题
    qrcode_image_title: Optional[str] = None
    # 提示信息列表
    message_list: Optional[list[str]] = None


class TemplateAlertInfoAreaData(TemplateBaseData):
    """重定向区域数据"""
    # 警告图标前端代码
    alert_logo_url: Optional[str] = 'data:image/svg+xml;base64,PHN2ZyB0PSIxNzEzODEyMTM3ODI1IiBjbGFzcz0iaWNvbiIgdmlld0JveD0iMCAwIDEwNzIgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjY0MjciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIj48cGF0aCBkPSJNMTAzMy4wNDY0OTYgNDkyLjI1MTQyOWgtNzkuNDgxOTA1YTM5LjY0MzQyOSAzOS42NDM0MjkgMCAwIDEtMzkuNzQwOTUzLTM5LjM1MDg1OGMwLTIxLjY5OTA0OCAxNy44OTU2MTktMzkuNDQ4MzgxIDM5Ljc0MDk1My0zOS40NDgzODFoNzkuNDgxOTA1YzIxLjg0NTMzMyAwIDM5Ljc0MDk1MiAxNy43NDkzMzMgMzkuNzQwOTUyIDM5LjQ0ODM4MWEzOS42NDM0MjkgMzkuNjQzNDI5IDAgMCAxLTM5Ljc0MDk1MiAzOS4zNTA4NTh6IG0tMTk0LjcwNjI4Ni0yNTQuMDQ5NTI0Yy0xMy44OTcxNDMgMTUuNzk4ODU3LTM5Ljc0MDk1MiAxNS43OTg4NTctNTUuNjM3MzM0IDBhMzcuNzkwNDc2IDM3Ljc5MDQ3NiAwIDAgMSAwLTU1LjEwMDk1M2w1NS42MzczMzQtNTUuMTQ5NzE0YTM4LjY2ODE5IDM4LjY2ODE5IDAgMCAxIDU1LjYzNzMzMyAwIDM3LjkzNjc2MiAzNy45MzY3NjIgMCAwIDEgMCA1NS4xNDk3MTRsLTU1LjYzNzMzMyA1NS4xMDA5NTN6IG0xNS44OTYzODEgNzA2Ljk5ODg1N2gxNzguODA5OTA1YzIxLjg0NTMzMyAwIDM5Ljc0MDk1MiAxNy43MDA1NzEgMzkuNzQwOTUyIDM5LjM5OTYxOWEzOS42NDM0MjkgMzkuNjQzNDI5IDAgMCAxLTM5Ljc0MDk1MiAzOS4zNTA4NTdIMzkuNzE3NzM0YTM5LjY0MzQyOSAzOS42NDM0MjkgMCAwIDEtMzkuNzQwOTUzLTM5LjM1MDg1N2MwLTIxLjY5OTA0OCAxNy44OTU2MTktMzkuMzk5NjE5IDM5Ljc0MDk1My0zOS4zOTk2MTloMTc4LjgwOTkwNHYtMzkzLjg0OTkwNWMwLTE3My4yOTk4MSAxNDMuMDE4NjY3LTMxNS4wOTk0MjkgMzE3LjgzMDA5Ni0zMTUuMDk5NDI4czMxNy44Nzg4NTcgMTQxLjc5OTYxOSAzMTcuODc4ODU3IDMxNS4wOTk0Mjh2MzkzLjg0OTkwNXogbS0zOTcuMzEyLTM1NC40OTkwNDhhMzkuNjQzNDI5IDM5LjY0MzQyOSAwIDAgMC0zOS43NDA5NTMtMzkuMzUwODU3IDM5LjY0MzQyOSAzOS42NDM0MjkgMCAwIDAtMzkuNzQwOTUyIDM5LjM1MDg1N3YyMzYuMzQ4OTUzYzAgMjEuNjUwMjg2IDE3Ljg5NTYxOSAzOS4zNTA4NTcgMzkuNzQwOTUyIDM5LjM1MDg1N2EzOS42NDM0MjkgMzkuNjQzNDI5IDAgMCAwIDM5Ljc0MDk1My0zOS4zNTA4NTd2LTIzNi4zNDg5NTN6IG03OS40MzMxNDMtNDMzLjIwMDc2MmEzOS42NDM0MjkgMzkuNjQzNDI5IDAgMCAxLTM5LjY5MjE5MS0zOS4zOTk2MTlWMzkuMzAyMDk1YzAtMjEuNjUwMjg2IDE3Ljg0Njg1Ny0zOS4zNTA4NTcgMzkuNjkyMTkxLTM5LjM1MDg1NyAyMS44OTQwOTUgMCAzOS43NDA5NTIgMTcuNzAwNTcxIDM5Ljc0MDk1MiAzOS4zNTA4NTd2NzguNzk5MjM4YTM5LjY5MjE5IDM5LjY5MjE5IDAgMCAxLTM5Ljc0MDk1MiAzOS4zOTk2MTl6TTI0Mi4zNzIyMSAyMzguMjAxOTA1bC01NS42MzczMzQtNTUuMTAwOTUzYTM3LjgzOTIzOCAzNy44MzkyMzggMCAwIDEgMC01NS4xNDk3MTQgMzguNjY4MTkgMzguNjY4MTkgMCAwIDEgNTUuNjM3MzM0IDBsNTUuNjM3MzMzIDU1LjE0OTcxNGEzNy43OTA0NzYgMzcuNzkwNDc2IDAgMCAxIDAgNTUuMTAwOTUzIDM4LjU3MDY2NyAzOC41NzA2NjcgMCAwIDEtNTUuNjM3MzMzIDB6IG0tMTIzLjE3MjU3MiAyNTQuMDQ5NTI0SDM5LjcxNzczNGEzOS42NDM0MjkgMzkuNjQzNDI5IDAgMCAxLTM5Ljc0MDk1My0zOS4zNTA4NThjMC0yMS42OTkwNDggMTcuODk1NjE5LTM5LjQ0ODM4MSAzOS43NDA5NTMtMzkuNDQ4MzgxaDc5LjQ4MTkwNGMyMS44NDUzMzMgMCAzOS42OTIxOSAxNy43NDkzMzMgMzkuNjkyMTkxIDM5LjQ0ODM4MWEzOS42NDM0MjkgMzkuNjQzNDI5IDAgMCAxLTM5LjY5MjE5MSAzOS4zNTA4NTh6IiBmaWxsPSIjRTA1QjU2IiBwLWlkPSI2NDI4Ij48L3BhdGg+PC9zdmc+'
    # 警告标题
    alert_title: Optional[str] = '警告'
    # 提示信息列表
    alert_message_list: list[str]


class TemplateError404AreaData(TemplateBaseData, Error404DataItem):
    """错误404数据"""
    pass


class TemplateError500AreaData(TemplateBaseData, Error500DataItem):
    """错误500数据"""
    pass


class TemplateError501AreaData(TemplateBaseData, Error501DataItem):
    """错误501数据"""
    pass
