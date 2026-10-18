#!/usr/bin/env python3
"""
统计技术写作样例的写作特征，按来源汇总。输出只有数字和标题，不含正文，可以公开。

用法:
    python analyze_corpus.py --corpus corpus --out stats [--aiflavor path/to/ai-wei/tools]
"""

import argparse
import json
import os
import re
import sys
from statistics import mean, median

CJK = re.compile(r"[一-鿿]")


def load(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"---\n(.*?)\n---\n\n(.*)", raw, re.S)
    meta = {k: json.loads(v) for k, v in (l.split(": ", 1) for l in m.group(1).splitlines())}
    return meta, m.group(2)


def features(text, analyze):
    # 只分析正文：去掉作者自己附在文末的广告段和"（完）"之后的内容（公开的全文不做任何删改）
    text = re.split(r"\n（完）|\n以下为广告部分", text)[0]
    code_blocks = re.findall(r"```.*?```", text, re.S)
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    prose = re.sub(r"`[^`\n]+`", "X", prose)
    # 链接地址里的 ? 和数字不算（比如图片地址的参数），只保留链接文字
    prose = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", prose)
    prose = re.sub(r"https?://\S+", "", prose)
    zh = len(CJK.findall(prose)) or 1
    k = 1000 / zh
    lines = [l.strip() for l in prose.splitlines() if l.strip()]
    paras = [l for l in lines if not re.match(r"^(#|[-*+]\s|\d+[.、)]\s?|\|)", l)]
    sents = [s for s in re.split(r"(?<=[。！？!?])", prose) if len(CJK.findall(s)) >= 2]
    slen = [len(CJK.findall(s)) for s in sents]
    first = paras[0] if paras else ""
    r = analyze(text, "zh")
    return {
        "chars_zh": zh,
        "code_blocks": len(code_blocks),
        "code_share": round(sum(len(c) for c in code_blocks) / max(len(text), 1), 3),
        "inline_code_per_k": round(len(re.findall(r"`[^`\n]+`", text)) * k, 2),
        "numbers_per_k": round(len(re.findall(r"\d+(?:\.\d+)?%?", prose)) * k, 2),
        "headings_per_k": round(sum(1 for l in lines if l.startswith("#")) * k, 2),
        "list_line_share": round(sum(1 for l in lines if re.match(r"^([-*+]\s|\d+[.、)]\s?)", l)) / max(len(lines), 1), 3),
        "i_per_k": round(len(re.findall(r"我(?!们)", prose)) * k, 2),
        "we_per_k": round(len(re.findall(r"我们", prose)) * k, 2),
        "questions_per_k": round(len(re.findall(r"[？?]", prose)) * k, 2),
        "judgment_per_k": round(len(re.findall(r"我(认为|觉得|建议|的看法|个人)|建议|不要|千万|其实|说白了|坦率|问题在于|关键是", prose)) * k, 2),
        "hedge_per_k": round(len(re.findall(r"可能|也许|或许|大概|似乎|不一定|未必", prose)) * k, 2),
        "links_per_k": round(len(re.findall(r"\]\(http", text)) * k, 2),
        "opens_with_benwen": bool(re.match(r"^(本文|这篇文章|今天我们|今天|本篇)", first)),
        "opens_with_question": "？" in first[:80] or "?" in first[:80],
        "has_summary_section": bool(re.search(r"^#+\s*(总结|小结|结语|结论)", text, re.M)),
        "sent_len_median": median(slen) if slen else 0,
        "sent_len_cv": round((sum((x - mean(slen)) ** 2 for x in slen) / len(slen)) ** 0.5 / mean(slen), 3) if len(slen) > 3 else None,
        "para_len_median": median(len(CJK.findall(p)) for p in paras) if paras else 0,
        "aiflavor_score": r.score,
        "aiflavor_hits_per_k": round(len(r.hits) * 1000 / max(zh, 300), 2),
        "aiflavor_labels": [h.label for h in r.hits],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--aiflavor", default=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools"),
                    help="ai-wei 仓库里 tools/ 的路径（默认按 corpus/scripts/ 的位置推算）")
    a = ap.parse_args()
    sys.path.insert(0, a.aiflavor)
    from aiflavor import analyze

    os.makedirs(a.out, exist_ok=True)
    rows = []
    for src in sorted(os.listdir(a.corpus)):
        d = os.path.join(a.corpus, src)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                meta, text = load(os.path.join(d, f))
                rows.append(dict(source=src, title=meta["title"], date=meta["date"], url=meta["url"], **features(text, analyze)))
    with open(os.path.join(a.out, "per_article.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    num = [k for k, v in rows[0].items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    boo = [k for k, v in rows[0].items() if isinstance(v, bool)]
    summary = {}
    for src in sorted({r["source"] for r in rows}):
        rs = [r for r in rows if r["source"] == src]
        s = {"n": len(rs), "years": f"{min(r['date'] for r in rs)[:4]}–{max(r['date'] for r in rs)[:4]}"}
        for k in num:
            vals = [r[k] for r in rs if r[k] is not None]
            s[k] = round(median(vals), 3) if vals else None
        for k in boo:
            s[k] = round(sum(r[k] for r in rs) / len(rs), 3)
        labels = {}
        for r in rs:
            for l in r["aiflavor_labels"]:
                labels[l] = labels.get(l, 0) + 1
        s["top_aiflavor_labels"] = sorted(labels.items(), key=lambda x: -x[1])[:8]
        summary[src] = s
    with open(os.path.join(a.out, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
