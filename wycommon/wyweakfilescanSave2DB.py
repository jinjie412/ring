#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import MySQLdb
import uuid

# 动态配置项
dbHost      = "127.0.0.1"
dbUser      = "root"
dbPassWd    = ""
dbDataBase  = "ring"
dbCharset   = "utf8"

def wyweakfilescan_save2db(taskid, result):

    # 生成该域名的uuid方便查找，因可能对某个域名多次扫描，得到的信息也有所不同
    taskid = str(taskid)

    # 打开数据库连接
    db = MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPassWd,db=dbDataBase,charset=dbCharset)
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    for subdomain in result['dirs']:
      for url in result['dirs'][subdomain]:
        query = "INSERT INTO weakfilescan (`taskid`, `tag`, `subdomain`, `name`, `url`, `time`) VALUES ('%s', 'dirs', '%s', '', '%s', NOW())" % (taskid, subdomain, url)
        try:
           # 执行sql语句
           cursor.execute(query)
           # 提交到数据库执行
           db.commit()
        except:
           # 返回错误消息
           db.rollback()

    for subdomain in result['files']:
      for name in result['files'][subdomain]:
        for url in result['files'][subdomain][name]:
          query = "INSERT INTO weakfilescan (`taskid`, `tag`, `subdomain`, `name`, `url`, `time`) VALUES ('%s', 'files', '%s', '%s', '%s', NOW())" % (taskid, subdomain, name, url)
          try:
             # 执行sql语句
             cursor.execute(query)
             # 提交到数据库执行
             db.commit()
          except:
             # 返回错误消息
             db.rollback()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # 打开文件
        fo = open(str(sys.argv[2]))
        result = fo.read();
        # 关闭打开的文件
        fo.close()
        wyweakfilescan_save2db(sys.argv[1], eval(result))
        sys.exit(0)
    else:
        print ("usage: %s wyweakfilescan_save2db" % sys.argv[0])
        sys.exit(-1)
