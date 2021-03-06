#! usr/bin/env python
#coding:utf8

__author__ = 'fenton-fd.zhu'
'''
上传器,负责文件上传，初始化需要设置文件保存地址、可接受文件类型、最大size
'''
from django.http import HttpRequest
import hashlib
import os, stat
from os.path import getsize
from modernLamps import settings

class Uploader(object):


    def __init__(self, diskPath='upload/static/myAllUpload/', fileType=('jpeg', 'jpg', 'png'), max_size=1024*100):
        self.__maxSize = max_size;
        self.__diskPath = diskPath;
        self.__fileType = [];
        for type in fileType:
            self.__fileType.append('.'+type);

    #文件校验
    def fileCheck(self, fileMemItem):
        #check type
        name, extension = os.path.splitext(fileMemItem.name);  #分解文件名和扩展名
        if extension not in self.__fileType:
            return 'fileType fail';

        # #路径
        if not os.path.exists(self.__diskPath):
            result = os.makedirs(self.__diskPath);   #新建文件夹,成功返回None
            if not result:
                os.chmod(self.__diskPath, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO);  # mode:777  无返回值
            else:
                return result;
        return True;


    def uploadFile(self, fileMemItem):
        if fileMemItem:
            #文件检验

            result = self.fileCheck(fileMemItem);
            if result != True:
                return '';

            name, extension = os.path.splitext(fileMemItem.name);  #分解文件名和扩展名
            hash_md5 = hashlib.md5();
            hash_md5.update(name);
            fileName = hash_md5.hexdigest() + extension;  #先对名字部分摘要，在拼接
            try:
                with open(os.path.join(self.__diskPath, fileName), 'wb') as descFile:  #新建一个空文件
                    for chunk in fileMemItem.chunks():
                        descFile.write(chunk);
                descFile.close();

                if settings.DEBUG == False:
                    path = settings.BASE_URL+'media'+self.__diskPath.split('media')[-1];
                    # path = os.path.join(os.path.join(settings.BASE_URL,'media'), self.__diskPath.split('media')[-1]);
                    # return os.path.join(path, fileName);
                    return path + '/' + fileName;  #返回路径,这个路径是要求服务器来识别的
                else:
                    return self.__diskPath + "\\" + fileName;  #只是为了本地文件调试
            except Exception, e:
                return '';
        else:
            return '';

