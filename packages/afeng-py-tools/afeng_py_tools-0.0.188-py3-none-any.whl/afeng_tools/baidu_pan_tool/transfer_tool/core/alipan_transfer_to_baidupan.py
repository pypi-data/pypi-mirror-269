import os
from typing import Callable

from afeng_tools.aliyun_pan_tool import aliyun_pan_tools
from afeng_tools.baidu_pan_tool.core.baidu_pan_models import UploadCreateResult
from afeng_tools.baidu_pan_tool.tools import baidu_pan_file_upload_tools
from afeng_tools.file_tool import tmp_file_tools
from afeng_tools.log_tool.loguru_tools import get_logger, log_error
from aligo import Aligo, BaseShareFile

logger = get_logger()


def get_baidupan_save_path(alipan_path: str, baidupan_save_path_func: Callable[[str, str], str]) -> str:
    """获取百度网盘保存路径"""
    if '/' in alipan_path:
        alipan_path_info_arr = alipan_path.rsplit('/', maxsplit=1)
        alipan_parent_path, alipan_file_name = '/' + alipan_path_info_arr[0], alipan_path_info_arr[1]
    else:
        alipan_parent_path, alipan_file_name = '/', alipan_path
    return baidupan_save_path_func(alipan_parent_path, alipan_file_name)


def alipan_file_save(baidupan_access_token: str, alipan_api: Aligo, alipan_path: str, alipan_file: BaseShareFile,
                     transfer_list_file: str,
                     exist_file_list: list[str],
                     alipan_file_filter_func: Callable[[str, BaseShareFile], bool] = lambda x, y: True,
                     baidupan_save_path_func: Callable[[str, str], str] =
                     lambda x, y: f'{x}/{y}',
                     baidupan_save_after_handle_func: Callable[[str, UploadCreateResult], None] = None):
    """
    阿里云盘文件保存
    :param baidupan_access_token:百度网盘access_token
    :param alipan_api:
    :param alipan_path:
    :param alipan_file:
    :param transfer_list_file:
    :param exist_file_list:
    :param alipan_file_filter_func: 阿里云盘文件过滤函数，只有满足条件的文件才会进行转存，参数：(阿里云盘的路径(包含文件名): alipan_path, 阿里云盘的文件: alipan_file)-> True或False
    :param baidupan_save_path_func: 百度网盘路径函数：(阿里云盘的路径(不包含文件名，根路径为/): alipan_path, 阿里云盘的文件名: alipan_file_name)-> 百度网盘的路径
    :param baidupan_save_after_handle_func: 百度网盘保存后的处理函数，参数：(百度网盘保存路径（包含文件名）,上传保存结果)
    :return:
    """
    if alipan_file.file_id in exist_file_list or not alipan_file_filter_func(alipan_path, alipan_file):
        return
    baidupan_save_path = get_baidupan_save_path(alipan_path, baidupan_save_path_func)
    try:
        tmp_local_save_path = os.path.join(tmp_file_tools.get_user_tmp_dir(), f'ali_tmp_file-{alipan_file.share_id}')
        os.makedirs(tmp_local_save_path, exist_ok=True)
        tmp_local_file = aliyun_pan_tools.download_file(alipan_api, pan_file=alipan_file,
                                                        local_path=tmp_local_save_path)
        if tmp_local_file:
            result = baidu_pan_file_upload_tools.upload_file(baidupan_access_token,
                                                             local_file=tmp_local_file,
                                                             pan_path=baidupan_save_path)
            if result and result.errno == 0:
                os.remove(tmp_local_file)
                with open(transfer_list_file, 'a+', encoding='utf-8') as f:
                    f.write(f'{alipan_file.file_id}\n')
            if baidupan_save_after_handle_func and isinstance(baidupan_save_after_handle_func, Callable):
                baidupan_save_after_handle_func(baidupan_save_path, result)
    except Exception as e:
        log_error(logger,

                  f'[alipan_share_to_baidupan]阿里云文件[{alipan_path}]转存到百度云[{baidupan_save_path}]出现异常', e)
