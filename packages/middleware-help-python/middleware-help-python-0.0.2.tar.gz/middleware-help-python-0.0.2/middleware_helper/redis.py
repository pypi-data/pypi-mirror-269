# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  middleware-help-python
# FileName:     redis.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from redis import ConnectionPool, Redis


def get_redis_pool(**redis_params_map) -> ConnectionPool:
    return ConnectionPool(
        host=redis_params_map.get("host"),
        password=redis_params_map.get("password"),
        port=redis_params_map.get("port"),
        db=redis_params_map.get("db"),
        max_connections=redis_params_map.get("max_connections")
    )


def get_redis_connection(**redis_params_map) -> Redis:
    # 使用连接池创建 Redis 客户端
    return Redis(connection_pool=get_redis_pool(**redis_params_map))
