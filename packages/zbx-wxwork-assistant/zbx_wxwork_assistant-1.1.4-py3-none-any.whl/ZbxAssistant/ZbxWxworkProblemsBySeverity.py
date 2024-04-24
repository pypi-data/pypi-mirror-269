#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from collections import Counter
from zabbix_api import ZabbixAPIException
from .ZbxApis import ZabbixAPIS
from .ZbxConfigs import SEVERITY


class ZabbixProblemsBySeverity(ZabbixAPIS):
    def __init__(self, login_user: str = ""):
        super().__init__(login_user)
        self._login_user = login_user.strip()

    def count_priority(self, hostgroup: dict, **kwargs):
        """
            统计用户有权查看的各个主机组的所有主机【按照严重性分类】(
            即类似于 Zabbix 页面的 "Problems by severity")的告警数量：
        :param hostgroup:
        :return:
        """
        try:
            if self.user_zbxapi:
                # 根据问题的严重性（severity）计算每种严重性级别的问题数量
                priorities_count = Counter(
                    item.get("severity")
                    for host in hostgroup.get("hosts", [])
                    for item in self.user_zbxapi.problem.get(
                        {
                            "hostids": host.get("hostid"),
                            "recent": False,
                            "output": "extend",
                            **{
                                k: v
                                for k, v in kwargs.items()
                                if kwargs
                            }
                        }
                    )
                    if item.get("severity") is not None
                )
                # 获取 Zabbix 各个告警等级的基础统计字典
                # {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
                prioritized_count = {
                    str(sev): 0
                    for sev in sorted(SEVERITY.keys(), reverse=True)
                }
                prioritized_count.update(priorities_count)
                return {hostgroup.get("name"): prioritized_count}
        except ZabbixAPIException as err:
            logging.error(str(err))
