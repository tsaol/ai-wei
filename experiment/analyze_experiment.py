#!/usr/bin/env python3
"""
分析同题对照实验：用 aiflavor 给人写和模型写的文章打分，汇总成表格。

用法:
    python experiment/analyze_experiment.py --human data/human_s --ai data/ai --out results
输出: results/scores.csv, results/summary.json, results/summary.md
"""

import argparse
import csv
import json
import os
import re
from collections import Counter, defaultdict
from statistics import mean, median

import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from aiflavor import analyze  # noqa: E402

CJK = re.compile(r"[一-鿿]")
PARTS = ["markers", "uniformity", "template", "punctuation", "repetition", "vagueness"]


def auc(pos, neg):
    """pos 组得分高于 neg 组的概率（Mann-Whitney U / AUC），平局算一半。"""
    if not pos or not neg:
        return None
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def overlap(a: str, b: str, n: int = 8) -> float:
    """a 里有多少比例的 8 字片段也出现在 b 里，用来检查模型有没有背原文。"""
    ca, cb = "".join(CJK.findall(a)), "".join(CJK.findall(b))
    ga = {ca[i:i + n] for i in range(len(ca) - n + 1)}
    gb = {cb[i:i + n] for i in range(len(cb) - n + 1)}
    return len(ga & gb) / len(ga) if ga else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", required=True)
    ap.add_argument("--ai", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    rows, texts, human = [], {}, {}
    for f in sorted(os.listdir(a.human)):
        title = f[:-4]
        with open(os.path.join(a.human, f), encoding="utf-8") as fh:
            human[title] = fh.read()
        texts[(title, "human", "-")] = human[title]
    for f in sorted(os.listdir(a.ai)):
        title, model, prompt = f[:-4].split("__")
        with open(os.path.join(a.ai, f), encoding="utf-8") as fh:
            texts[(title, model, prompt)] = fh.read()

    marker_counts = defaultdict(Counter)
    for (title, model, prompt), t in texts.items():
        r = analyze(t, "zh")
        group = "human" if model == "human" else f"{model}/{prompt}"
        row = dict(title=title, model=model, prompt=prompt, group=group, chars=len(CJK.findall(t)),
                   score=r.score, hits=len(r.hits), cv=r.metrics["sentence_len_cv"],
                   short=r.metrics["short_sentence_share"], long=r.metrics["long_sentence_share"],
                   copy_of_original=round(overlap(t, human[title]), 3) if model != "human" else None,
                   **{p: r.parts[p] for p in PARTS})
        rows.append(row)
        kind = "human" if model == "human" else prompt
        for h in r.hits:
            marker_counts[kind][h.label] += 1

    with open(os.path.join(a.out, "scores.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    groups = defaultdict(list)
    for r in rows:
        groups[r["group"]].append(r)
        if r["model"] != "human":
            groups[f"all/{r['prompt']}"].append(r)

    def stat(rs):
        return dict(n=len(rs), score_mean=round(mean(x["score"] for x in rs), 1),
                    score_median=round(median(x["score"] for x in rs), 1),
                    chars_median=median(x["chars"] for x in rs),
                    hits_per_k=round(mean(1000 * x["hits"] / max(x["chars"], 300) for x in rs), 2),
                    cv_mean=round(mean(x["cv"] for x in rs if x["cv"] is not None), 3),
                    short_share=round(mean(x["short"] for x in rs), 3),
                    long_share=round(mean(x["long"] for x in rs), 3),
                    **{p: round(mean(x[p] for x in rs), 3) for p in PARTS},
                    copy_max=max((x["copy_of_original"] or 0) for x in rs))

    order = ["human", "all/plain", "all/deai"] + sorted(k for k in groups if k.count("/") == 1 and not k.startswith("all"))
    summary = {g: stat(groups[g]) for g in order if g in groups}
    hs = [r["score"] for r in groups["human"]]
    summary["auc"] = {g: round(auc([r["score"] for r in groups[g]], hs), 3) for g in order if g != "human" and g in groups}
    # 每个信号单独的区分度：plain 组 vs 人写
    summary["auc_by_signal_plain"] = {p: round(auc([r[p] for r in groups["all/plain"]], [r[p] for r in groups["human"]]), 3)
                                      for p in PARTS + ["hits"]}
    summary["auc_by_signal_plain"]["low_cv"] = round(auc([-r["cv"] for r in groups["all/plain"]], [-r["cv"] for r in groups["human"]]), 3)
    # 去 AI 味提示：同一题目、同一模型配对比较
    paired = []
    for r in rows:
        if r["prompt"] == "plain":
            d = next((x for x in rows if x["title"] == r["title"] and x["model"] == r["model"] and x["prompt"] == "deai"), None)
            if d:
                paired.append(d["score"] - r["score"])
    summary["deai_paired"] = dict(n=len(paired), mean_delta=round(mean(paired), 1), lower_in=sum(1 for x in paired if x < 0))
    summary["top_markers"] = {k: v.most_common(12) for k, v in marker_counts.items()}
    with open(os.path.join(a.out, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)

    names = {"human": "人写（公有领域散文）", "all/plain": "模型 · 普通提示（合计）", "all/deai": "模型 · 去 AI 味提示（合计）"}
    md = ["| 组 | 篇数 | AI 味指数（均值 / 中位数） | 命中 / 千字 | 句长 CV | 短句 | 长句 | 区分度 AUC（vs 人写） | 和原文 8 字重合（最高） |",
          "|---|---|---|---|---|---|---|---|---|"]
    for g in order:
        if g not in summary:
            continue
        s = summary[g]
        au = "—" if g == "human" else summary["auc"][g]
        cp = "—" if g == "human" else f"{s['copy_max']:.1%}"
        md.append(f"| {names.get(g, g)} | {s['n']} | {s['score_mean']} / {s['score_median']} | {s['hits_per_k']} | {s['cv_mean']} | "
                  f"{s['short_share']:.0%} | {s['long_share']:.0%} | {au} | {cp} |")
    md += ["", "| 信号 | 人写 | 普通提示 | 去 AI 味提示 | 区分度 AUC（普通 vs 人写） |", "|---|---|---|---|---|"]
    for p in PARTS:
        md.append(f"| {p} | {summary['human'][p]} | {summary['all/plain'][p]} | {summary['all/deai'][p]} | {summary['auc_by_signal_plain'][p]} |")
    with open(os.path.join(a.out, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))
    print(json.dumps({k: summary[k] for k in ("auc", "auc_by_signal_plain", "deai_paired")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
