# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  middleware-help-python
# FileName:     mysql.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from mysql.connector import connect
from mysql.connector.cursor_cext import CMySQLCursor


class Mysql(object):

    def __init__(self, **mysql_params_map):
        self.conn = connect(
            host=mysql_params_map.get("host"),
            user=mysql_params_map.get("user"),
            port=mysql_params_map.get("port"),
            charset=mysql_params_map.get("charset"),
            password=mysql_params_map.get("password"),
            database=mysql_params_map.get("database")
        )

    @classmethod
    def convert_tuple_to_dict(cls, records: list, column_names: tuple) -> list:
        # 将元组列表转换为字典列表
        result_list = []
        for row in records:
            row_dict = {}
            for index, value in enumerate(row):
                column_name = column_names[index]
                row_dict[column_name] = value
            result_list.append(row_dict)
        return result_list

    @classmethod
    def cursor_query_data(cls, cursor: CMySQLCursor, sql: str) -> list:
        # 执行 SQL 查询语句
        cursor.execute(sql)
        # 获取查询结果
        records = cursor.fetchall()
        # 获取列名
        column_names = cursor.column_names
        result_list = cls.convert_tuple_to_dict(records=records, column_names=column_names)
        return result_list

    def execute_sql(self, sql: str, action: str):
        results = None
        if self.conn.is_connected():
            cursor: CMySQLCursor = self.conn.cursor()
            if action in ("insert", "update", "delete"):
                try:
                    cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()
            elif action == "select":
                try:
                    # 获取查询结果
                    results = self.cursor_query_data(sql=sql, cursor=cursor)
                except Exception as e:
                    print(e)
            else:
                pass
            cursor.close()
            self.conn.close()
        else:
            print("当前连接不正常.")
        return results

    @classmethod
    def convert_key_value_str(cls, **kwargs) -> tuple:
        field_list, value_list = list(), list()
        for key, value in kwargs.items():
            field_list.append("`{}`".format(key))
            if isinstance(value, str):
                value = "'{}'".format(value)
            else:
                value = str(value)
            value_list.append(value)
        field_str = "(" + ", ".join(field_list) + ")"
        value_str = "(" + ", ".join(value_list) + ")"
        return field_str, value_str

    def insert_order_sql(self, data_info: dict, table_name: str) -> None:
        field_str, value_str = self.convert_key_value_str(**data_info)
        sql = "insert into " + "`{}` {} values {};".format(table_name, field_str, value_str)
        return self.execute_sql(sql=sql, action="insert")
