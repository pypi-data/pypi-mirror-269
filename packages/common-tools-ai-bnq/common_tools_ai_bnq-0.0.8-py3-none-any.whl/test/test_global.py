#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/4/22 15:19
# Author:Zhang HongTao
# @File:test_global.py

import os

global_var = "host_dev"


def get_env(env):
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(base_path, "base_path")
    return base_path


def modify_global_var():
    global global_var
    global_var = "host_test"

    print(global_var)


get_env_1 = get_env(global_var)

if __name__ == '__main__':
    modify_global_var()
