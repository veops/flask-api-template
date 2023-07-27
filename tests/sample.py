# -*- coding: utf-8 -*-
"""provide some sample data in database"""
import random
import uuid


def fake_attr_value(attr_dict):
    attr_type = attr_dict["value_type"]
    attr_name = attr_dict["name"]

    if attr_type == "0":
        return {attr_name: random.randint(0, 1000)}
    elif attr_type == "1":
        return {attr_name: random.randint(0, 1000) / 3.0}
    elif attr_type == "2":
        return {attr_name: uuid.uuid4().hex[:8]}
