# -*- coding:utf-8 -*-
import platform

__all__ = ['IS_PY3', 'httplib', 'urllib2']
IS_PY3 = int(platform.python_version_tuple()[0]) == 3

# 不需要用这些方式，可以用 from six.moves import urllib 
# ============================================================
# from baselib.py import httplib
if IS_PY3:
    import http.client as httplib
else:
    import httplib

# ============================================================
# from baselib.py import urllib2
"""
在Python3中，`urllib2`库已经被分拆成`urllib.request`和`urllib.error`等模块。
因此，在Python3中，您应该使用`urllib.request`代替`urllib2`。
"""
if IS_PY3:
    import urllib.request as urllib2
else:
    import urllib2