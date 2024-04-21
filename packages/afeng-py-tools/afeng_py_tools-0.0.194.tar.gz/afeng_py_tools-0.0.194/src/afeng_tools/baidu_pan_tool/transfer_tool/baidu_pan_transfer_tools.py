import os
from typing import Callable

from afeng_tools.aliyun_pan_tool import aliyun_pan_tools, aliyun_pan_share_tools
from afeng_tools.baidu_pan_tool.core.baidu_pan_models import UploadCreateResult
from afeng_tools.baidu_pan_tool.tools.baidu_pan_file_path_tools import format_pan_path
from afeng_tools.baidu_pan_tool.transfer_tool.core.alipan_transfer_to_baidupan import alipan_file_save
from afeng_tools.file_tool import tmp_file_tools, file_tools
from afeng_tools.log_tool import loguru_tools
from aligo import BaseShareFile

logger = loguru_tools.get_logger()


def alipan_share_transfer_to_baidupan(baidupan_access_token: str, alipan_share_msg: str,
                                      alipan_file_filter_func: Callable[[str, BaseShareFile], bool] = lambda x, y: True,
                                      baidupan_save_path_func: Callable[[str, str], str] = lambda x, y: f'{x}/{y}',
                                      baidupan_save_after_handle_func: Callable[
                                          [str, UploadCreateResult], None] = None):
    """
    阿里云盘的分享转存道百度网盘
    :param baidupan_access_token:百度网盘access_token
    :param alipan_share_msg: 阿里云盘分享信息
     :param alipan_file_filter_func: 阿里云盘文件过滤函数，只有满足条件的文件才会进行转存，参数：(阿里云盘的路径(包含文件名): alipan_path, 阿里云盘的文件: alipan_file)-> True或False
    :param baidupan_save_path_func: 百度网盘路径函数：(阿里云盘的路径(不包含文件名，根路径为/): alipan_path, 阿里云盘的文件名: alipan_file_name)-> 百度网盘的路径
      :param baidupan_save_after_handle_func:  百度网盘保存后的处理函数，参数：(百度网盘保存路径（包含文件名）,上传保存结果)
    :return:
    """
    logger.info(alipan_share_msg)
    # 获取阿里云盘中要上传的文件
    alipan_api = aliyun_pan_tools.get_ali_api()
    share_info_result = aliyun_pan_share_tools.get_share_info_by_link(alipan_api, share_msg=alipan_share_msg)

    transfer_list_file = os.path.join(tmp_file_tools.get_user_tmp_dir(),
                                      f'.alipan_transfer_list-{share_info_result.share_id}')
    exist_file_list = []
    if os.path.exists(transfer_list_file):
        exist_file_list = file_tools.read_file_lines(transfer_list_file)
    alipan_share_token = aliyun_pan_share_tools.get_share_token(alipan_api, share_info_result.share_id,
                                                                share_info_result.share_pwd)
    aliyun_pan_share_tools.list_share_all_file(alipan_api, alipan_share_token,
                                               callback_func=lambda _, pan_path, pan_file: alipan_file_save(
                                                   baidupan_access_token=baidupan_access_token,
                                                   alipan_api=alipan_api,
                                                   alipan_path=pan_path,
                                                   alipan_file=pan_file,
                                                   transfer_list_file=transfer_list_file,
                                                   exist_file_list=exist_file_list,
                                                   alipan_file_filter_func=alipan_file_filter_func,
                                                   baidupan_save_path_func=baidupan_save_path_func,
                                                   baidupan_save_after_handle_func=baidupan_save_after_handle_func))

    if os.path.exists(transfer_list_file):
        os.remove(transfer_list_file)


if __name__ == '__main__':
    alipan_share_transfer_to_baidupan(baidupan_access_token='',
                                      alipan_share_msg='https://www.alipan.com/s/oqCriKvJDig',
                                      alipan_file_filter_func=lambda x, y: True,
                                      baidupan_save_path_func=lambda x,
                                                                     y: f'/apps/阿里云转存{format_pan_path(x)}/{format_pan_path(y)}')
