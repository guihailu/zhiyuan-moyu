#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""无本地电脑依赖的官网基础静态回归；不上传资料、不发布、不修改任何站点文件。"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import sys

root = Path(__file__).resolve().parents[1]
pages = ["index.html", "zhiyuan.html", "moyu.html", "chashi.html", "lianxi.html"]
errors = []
for page in pages:
    source = root / page
    if not source.is_file():
        errors.append(f"{page}: HTML 不存在")
        continue
    html = source.read_text(encoding="utf-8")
    if html.count('<details class="mobile-nav">') != 1:
        errors.append(f"{page}: 手机菜单个数不是 1")
    if 'href="lianxi.html"' not in html:
        errors.append(f"{page}: 官方联系页入口不存在")
    if '<main id="main"' not in html:
        errors.append(f"{page}: 无 main 地标")
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', html):
        u = urlsplit(url)
        if u.scheme or u.netloc or url.startswith(("#", "//", "data:")):
            continue
        if u.path and not (root / unquote(u.path).lstrip("/")).is_file():
            errors.append(f"{page}: {attr} -> {url} 对应站内文件不存在")
if errors:
    print("FAIL: " + str(len(errors)) + " 个错误")
    for e in errors:
        print(" - " + e)
    sys.exit(1)
print("PASS: 5 页导航、联系入口、站内静态路径和地标检查")
print("注意：手机真实点击、夜色对比度、页面渲染、部署状态仍需要浏览器验收")
