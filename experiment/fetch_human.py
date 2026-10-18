#!/usr/bin/env python3
"""
从维基文库下载实验用的人写散文（作者都已去世 50 年以上，在中国属于公有领域），
转成简体，在段落处截到约 1500 字。原文不放进仓库，需要时用这个脚本下载。

用法:
    pip install opencc-python-reimplemented
    python experiment/fetch_human.py --out data/human_s
"""

import argparse
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

PAGES = {
    "一件小事": "一件小事",
    "从百草园到三味书屋": "从百草园到三味书屋",
    "匆匆": "匆匆",
    "好的故事": "好的故事",
    "孔乙己": "孔乙己",
    "我所知道的康桥": "我所知道的康橋",
    "春": "春 (朱自清)",
    "桨声灯影里的秦淮河": "槳聲燈影裏的秦淮河",
    "社戏": "社戏",
    "背影": "背影",
    "荷塘月色": "荷塘月色",
    "藤野先生": "藤野先生",
    "阿长与《山海经》": "阿長與《山海經》"
}


def fetch(page: str) -> str:
    u = "https://zh.wikisource.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "parse", "page": page, "prop": "text", "format": "json", "redirects": 1})
    req = urllib.request.Request(u, headers={"User-Agent": "ai-wei-research/0.1 (https://github.com/tsaol/ai-wei)"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    h = re.sub(r"<(table|style|script|sup)[\s\S]*?</\1>", "", d["parse"]["text"]["*"])
    paras = [html.unescape(re.sub("<[^>]+>", "", p)).strip() for p in re.findall(r"<p>([\s\S]*?)</p>", h)]
    return "\n".join(p for p in paras if len(p) > 1).replace("\u200b", "")


def main():
    import opencc
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--chars", type=int, default=1500)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cc = opencc.OpenCC("t2s")
    for title, page in PAGES.items():
        text, out, n = cc.convert(fetch(page)), [], 0
        for p in text.split("\n"):
            out.append(p)
            n += len(p)
            if n >= a.chars:
                break
        with open(os.path.join(a.out, f"{title}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print(title, n)
        time.sleep(6)  # 维基文库会对频繁请求返回 429


if __name__ == "__main__":
    main()
