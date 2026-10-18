import os

from django.conf import settings

def remove_old_photo(photo):

    '''
        创建软件包utils作为辅助函数包，web/views/utils
        在utils下创建py文件photo.py，实现删除旧头像文件
        特判是否为默认头像，若不是再进行后续操作；
        保存旧头像路径：使用/分隔开操作路径和photo.name路径；
        如果旧路径存在，则删除os.path.exists
    '''

    if photo and photo.name != 'user/photo/default.png':
        old_path = settings.MEDIA_ROOT / photo.name
        if os.path.exists(old_path):
            os.remove(old_path)