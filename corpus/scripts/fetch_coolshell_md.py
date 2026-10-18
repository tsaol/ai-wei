#!/usr/bin/env python3
"""
从 GitHub 上的酷壳 Markdown 存档（slan-ning/coolshell-markdown）取样，转成语料格式。
先按长度筛（>= 1500 中文字，主要是原创长文），再按年份轮流取，让每年都有代表。

用法:
    python fetch_coolshell_md.py --paths lists/cs_md_paths.json --out corpus/coolshell --n 60
"""

import argparse
import json
import os
import re
import time
import urllib.parse
import urllib.request

RAW = "https://raw.githubusercontent.com/slan-ning/coolshell-markdown/main/"
CJK = re.compile(r"[一-鿿]")


def get(path: str) -> str:
    u = RAW + urllib.parse.quote(path)
    req = urllib.request.Request(u, headers={"User-Agent": "ai-wei research (github.com/tsaol/ai-wei)"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--min-chars", type=int, default=1500)
    a = ap.parse_args()
    with open(a.paths, encoding="utf-8") as f:
        paths = json.load(f)

    # 第一步：下载全部，按长度筛（raw.githubusercontent.com 是静态文件，间隔 0.5 秒足够）
    docs = []
    for p in paths:
        try:
            raw = get(p)
        except Exception as e:
            print("ERR", p, e)
            continue
        m = re.match(r"#\s*(.+?)\n>date:\s*(\S+)", raw)
        if not m:
            continue
        body = raw[m.end():].strip()
        if len(CJK.findall(body)) >= a.min_chars:
            docs.append(dict(path=p, title=m.group(1).strip(), date=m.group(2)[:10], body=body))
        time.sleep(0.5)
    print(f"[coolshell-md] {len(docs)} / {len(paths)} articles have >= {a.min_chars} CJK chars")

    # 第二步：按年份轮流取
    by_year = {}
    for d in sorted(docs, key=lambda d: d["date"]):
        by_year.setdefault(d["date"][:4], []).append(d)
    picked, i = [], 0
    while len(picked) < a.n and any(by_year.values()):
        for y in sorted(by_year):
            if by_year[y] and len(picked) < a.n:
                lst = by_year[y]
                picked.append(lst.pop(len(lst) // 2 if i % 2 else 0))
        i += 1

    os.makedirs(a.out, exist_ok=True)
    for d in picked:
        slug = re.sub(r"[^\w-]+", "-", d["title"])[:40].strip("-")
        front = {"title": d["title"], "author": "陈皓", "site": "酷壳 CoolShell", "date": d["date"],
                 "url": "https://coolshell.cn/", "fetched_from": RAW + d["path"], "fetched_at": time.strftime("%Y-%m-%d"),
                 "license": "未见开放许可，默认保留所有权利；仅供私人研究，不得公开转载",
                 "extractor": "github:slan-ning/coolshell-markdown",
                 "note": "原站文章页现在报数据库错误；取自 GitHub 上的 Markdown 存档，文字未改动"}
        with open(os.path.join(a.out, f"{d['date']}-{slug}.md"), "w", encoding="utf-8") as f:
            f.write("---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()) + "\n---\n\n" + d["body"] + "\n")
    years = {}
    for d in picked:
        years[d["date"][:4]] = years.get(d["date"][:4], 0) + 1
    print(f"[coolshell-md] picked {len(picked)}: {dict(sorted(years.items()))}")


if __name__ == "__main__":
    main()
