# coding:utf-8
"""
数据库接口
"""
import config

__author__ = 'johhny'

import sqlalchemy

mysql_local_engine = sqlalchemy.create_engine(config.SQLALCHEMY_LOCAL_DATABASE_URI)
#获得连接
local_db_conn = mysql_local_engine.connect()

#事务插入或者更新记录
def INSERT_UPDATE_TRAN(SQL_STR):
    config.logger.info(SQL_STR)
    trans_local=local_db_conn.begin()
    try:
        local_db_conn.execute(SQL_STR)
        trans_local.commit()
    except():
        config.logger.error("error")
        trans_local.rollback()


