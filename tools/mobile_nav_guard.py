#!/usr/bin/env python3
"""Verify mobile navigation survives later design iterations. Stdlib only."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "zhiyuan.html", "moyu.html", "chashi.html", "lianxi.html")
for page in PAGES:
    html = (ROOT / page).read_text(encoding="utf-8")
    menus = re.findall(r'<details class="mobile-nav"[^>]*>(.*?)</details>', html, flags=re.S)
    assert len(menus) == 1, f"{page}: missing or duplicate mobile menu"
    menu = menus[0]
    assert "<summary>菜单</summary>" in menu and 'aria-label="手机站内导航"' in menu, f"{page}: inaccessible menu"
    for target in PAGES:
        assert f'href="{target}"' in menu, f"{page}: missing {target}"
for page in ("index.html", "style.css"):
    source = (ROOT / page).read_text(encoding="utf-8")
    for token in (".mobile-nav{display:none}", "@media(max-width:900px)", ".mast nav{display:none}", ".mobile-nav{display:block"):
        assert token in source, f"{page}: missing responsive CSS {token}"
print("PASS: mobile navigation present on 5/5 pages")
