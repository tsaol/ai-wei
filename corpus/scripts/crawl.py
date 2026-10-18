#!/usr/bin/env python3
"""
抓取技术写作样例（阮一峰、酷壳、美团技术团队），存成带元数据的 Markdown。
礼貌抓取：每次请求间隔 >= 3 秒；酷壳原站文章页报"数据库错误"，改用 Internet Archive 存档。

用法:
    python crawl.py --source ruanyifeng|coolshell|meituan --urls lists/xxx.txt --out corpus --n 60
"""

import argparse
import json
import os
import re
import time
import urllib.request

import lxml.html
import trafilatura
from markdownify import markdownify

# 每个站点的正文容器。找到就用 markdownify 转换（保留代码块和标题），找不到再退回 trafilatura
CONTAINERS = {
    "ruanyifeng": ['//*[@id="main-content"]'],
    "meituan": ['//*[contains(@class,"vp-page-content")]'],
    "coolshell": ['//*[contains(@class,"entry-content")]'],
}
DROP = ['.//script', './/style', './/*[contains(@class,"vp-post-header")]', './/*[contains(@class,"vp-post-meta")]',
        './/*[contains(@class,"vp-post-cover")]', './/*[contains(@class,"asset-meta")]', './/*[contains(@class,"share")]',
        './/*[contains(@class,"wumii")]', './/*[contains(@class,"post-views")]', './/*[contains(@id,"jp-relatedposts")]']


def extract(source: str, html: str, url: str) -> tuple:
    tree = lxml.html.fromstring(html)
    title = (tree.findtext(".//title") or "").split(" | ")[0].split(" - 阮一峰")[0].strip()
    for xp in CONTAINERS[source]:
        found = tree.xpath(xp)
        if found:
            el = found[0]
            for d in DROP:
                for x in el.xpath(d):
                    x.getparent().remove(x)
            body = markdownify(lxml.html.tostring(el, encoding="unicode"), heading_style="ATX", bullets="-",
                               code_language="", strip=["img"])
            body = re.sub(r"(?m)^(#+)\s*\[([^\]]+)\]\(#[^)]*\)\s*$", r"\1 \2", body)  # 去掉标题上的锚点链接
            body = re.sub(r"\n{3,}", "\n\n", body).strip()
            return title, body, "markdownify"
    body = trafilatura.extract(html, url=url, output_format="markdown", include_comments=False,
                               include_tables=True, include_formatting=True, favor_precision=True)
    return title, body or "", "trafilatura"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36 (ai-wei research; github.com/tsaol/ai-wei)"

SOURCES = {
    "ruanyifeng": dict(author="阮一峰", site="阮一峰的网络日志",
                       license="自由转载-非商用-非衍生-保持署名（CC BY-NC-ND 3.0），见原文页面的版权声明"),
    "coolshell": dict(author="陈皓", site="酷壳 CoolShell",
                      license="未见开放许可，默认保留所有权利；仅供私人研究，不得公开转载"),
    "meituan": dict(author="美团技术团队", site="美团技术团队博客",
                    license="未见开放许可，默认保留所有权利；仅供私人研究，不得公开转载"),
}


def get(url: str, tries: int = 3) -> str:
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(10 * (i + 1))


def date_of(url: str) -> str:
    m = re.search(r"/(20\d{2})/(\d{2})(?:/(\d{2}))?/", url)
    return f"{m.group(1)}-{m.group(2)}" + (f"-{m.group(3)}" if m.group(3) else "") if m else ""


def even_sample(urls: list, n: int) -> list:
    """按日期排序后均匀抽样，让各个时期都有代表。"""
    urls = sorted(set(urls), key=lambda u: (date_of(u), u))
    if len(urls) <= n:
        return urls
    step = len(urls) / n
    return [urls[int(i * step)] for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, choices=SOURCES)
    ap.add_argument("--urls", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--delay", type=float, default=3.0)
    ap.add_argument("--exclude", default="", help="跳过标题里含这些词的文章，逗号分隔")
    ap.add_argument("--wayback-ts", default="2023", help="酷壳从 Internet Archive 取最接近这个时间的存档（原站后来出现数据库错误）")
    a = ap.parse_args()
    meta = SOURCES[a.source]
    out_dir = os.path.join(a.out, a.source)
    os.makedirs(out_dir, exist_ok=True)
    with open(a.urls, encoding="utf-8") as f:
        urls = [l.strip() for l in f if l.strip()]
    excl = [w for w in a.exclude.split(",") if w]
    picked = even_sample(urls, a.n + 15)  # 多取一些，失败或被排除的可以补上
    done, index = 0, []
    for u in picked:
        if done >= a.n:
            break
        fetch = f"https://web.archive.org/web/{a.wayback_ts}id_/{u}" if a.source == "coolshell" else u
        try:
            html = get(fetch)
            title, body, how = extract(a.source, html, u)
            raw_dir = os.path.join(a.out, "_raw_html", a.source)
            os.makedirs(raw_dir, exist_ok=True)
            with open(os.path.join(raw_dir, re.sub(r"[^A-Za-z0-9_.-]+", "_", u.split("://", 1)[1])), "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            print(json.dumps({"url": u, "ok": False, "err": str(e)[:120]}, ensure_ascii=False), flush=True)
            time.sleep(a.delay)
            continue
        date = date_of(u)
        if not date:
            m = re.search(r'(20\d{2})[-年/](\d{1,2})[-月/](\d{1,2})', html)
            date = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else ""
        if not body or len(body) < 800 or any(w in title for w in excl):
            print(json.dumps({"url": u, "ok": False, "err": f"skipped (len={len(body or '')}, title={title[:20]})"}, ensure_ascii=False), flush=True)
            time.sleep(a.delay)
            continue
        slug = re.sub(r"[^A-Za-z0-9_-]+", "-", u.rstrip("/").rsplit("/", 1)[-1].replace(".html", ""))[:60]
        name = f"{date or 'nodate'}-{slug}.md"
        front = {"title": title, "author": meta["author"], "site": meta["site"], "date": date, "url": u,
                 "fetched_from": fetch, "fetched_at": time.strftime("%Y-%m-%d"), "license": meta["license"],
                 "extractor": how, "note": "正文从网页的正文容器提取并转成 Markdown（保留代码块和标题，去掉图片），文字未改动"}
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write("---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()) + "\n---\n\n" + body + "\n")
        index.append(dict(front, file=f"{a.source}/{name}", chars=len(body)))
        done += 1
        print(json.dumps({"url": u, "ok": True, "title": title[:30], "chars": len(body), "how": how, "fences": body.count("```") // 2}, ensure_ascii=False), flush=True)
        time.sleep(a.delay)
    with open(os.path.join(out_dir, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    print(f"[crawl] {a.source}: {done} saved")


if __name__ == "__main__":
    main()
