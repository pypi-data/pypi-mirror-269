#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/4/22 10:11
# Author:Zhang HongTao
# @File:gen_key.py


import pyotp

key = '3UJX4IAYEJSRXXQIN7DY7CJ6I64N7UCF'
totp = pyotp.TOTP(key)
print(totp.now())