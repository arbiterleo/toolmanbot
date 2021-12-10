# VScode 輸出時出現亂碼

# -*-coding:utf-8 -*-
import io
import sys


# 改變標準輸出的預設編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
