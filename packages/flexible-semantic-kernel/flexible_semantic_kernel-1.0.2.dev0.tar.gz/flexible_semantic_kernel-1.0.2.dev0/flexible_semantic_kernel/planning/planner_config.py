# !/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2022 baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
Action Planner配置

Authors: caoyitong
Date: 2024/03/06
"""
import json
from typing import List, Dict


class PlannerConfig:
    """
    Planner配置
    """
    def __init__(
        self,
        excluded_plugins: List[str] = None,
        excluded_functions: List[str] = None,
        extension_data: Dict = None
    ):
        self.excluded_plugins: List[str] = excluded_plugins or []
        self.excluded_functions: List[str] = excluded_functions or []
        self.extension_data: Dict = extension_data or {}

    @classmethod
    def from_json(cls, json_str: str):
        """
        json转换
        """
        data = json.loads(json_str)
        config = {
            key: value for key, value in data.items() if key in ["excluded_plugins", "excluded_functions"]
        }
        config = cls._process_execution_settings(config, data)

        return cls(**config)

    @classmethod
    def _process_execution_settings(cls, config: dict, data: dict) -> dict:
        exec_settings = data.get("execution_settings", {})

        for service_id, settings in exec_settings.items():
            # Copy settings to avoid modifying the original data
            settings = settings.copy()

            # Initialize the concrete type with the service_id and remaining settings
            config["extension_data"] = settings

        return config
