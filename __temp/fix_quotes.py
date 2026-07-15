# -*- coding: utf-8 -*-
"""Fix Chinese quotes in script"""
import sys;sys.stdout.reconfigure(encoding='utf-8')
with open(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py','r',encoding='utf-8') as f:
    content=f.read()
content=content.replace('“','「').replace('”','」')
with open(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py','w',encoding='utf-8') as f:
    f.write(content)
print('Fixed')
# Verify syntax
try:
    compile(content,'gen_zgxw_calligraphy.py','exec')
    print('Syntax OK')
except SyntaxError as e:
    print(f'Syntax error: {e}')