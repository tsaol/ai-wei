"""
用法:
    python -m aiflavor 文件.txt                 # 终端输出
    python -m aiflavor 文件.txt --json          # JSON
    python -m aiflavor 文件.txt --html out.html # 高亮报告
    cat 文件.txt | python -m aiflavor -         # 从标准输入读
    python -m aiflavor a.txt b.txt              # 多个文件对比
"""

import argparse
import html
import json
import sys

from .analyze import WEIGHTS, analyze

PART_NAMES = {"markers": "套话和套路句式", "uniformity": "句长太均匀", "template": "模板化结构",
              "punctuation": "破折号/冒号/emoji", "repetition": "重复", "vagueness": "空泛"}


def bar(v: float, width: int = 20) -> str:
    n = round(v * width)
    return "█" * n + "·" * (width - n)


def render_text(name: str, r) -> str:
    out = [f"== {name}  [{r.lang}] {r.chars} 字符, {r.sentences} 句",
           f"AI 味指数: {r.score} / 100（只适合对比同一作者的不同版本，不能用来判断是不是 AI 写的）"]
    for k, v in r.parts.items():
        out.append(f"  {PART_NAMES[k]:<14} {bar(v)} {v:.2f} × {WEIGHTS[k]}")
    m = r.metrics
    out.append(f"  句长均值 {m['sentence_len_mean']}，变异系数 {m['sentence_len_cv']}，"
               f"短句 {m['short_sentence_share']:.0%}，长句 {m['long_sentence_share']:.0%}")
    if r.hits:
        out.append("  命中:")
        for h in r.hits[:30]:
            out.append(f"    - 「{h.text}」 {h.label}（{h.note or h.type}）")
        if len(r.hits) > 30:
            out.append(f"    … 另有 {len(r.hits) - 30} 处")
    if r.advice:
        out.append("  建议:")
        out += [f"    * {a}" for a in r.advice]
    return "\n".join(out)


def render_html(text: str, r) -> str:
    spans, pos = [], 0
    for h in sorted(r.hits, key=lambda h: h.start):
        if h.start < pos:
            continue
        spans.append(html.escape(text[pos:h.start]))
        spans.append(f'<mark title="{html.escape(h.label + "：" + (h.note or h.type))}">'
                     f'{html.escape(text[h.start:h.end])}</mark>')
        pos = h.end
    spans.append(html.escape(text[pos:]))
    rows = "".join(f"<tr><td>{PART_NAMES[k]}</td><td>{v:.2f}</td><td>{WEIGHTS[k]}</td></tr>"
                   for k, v in r.parts.items())
    adv = "".join(f"<li>{html.escape(a)}</li>" for a in r.advice) or "<li>没有明显问题</li>"
    return f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>AI 味报告</title>
<style>body{{font:16px/1.8 -apple-system,"PingFang SC","Noto Sans CJK SC",sans-serif;max-width:860px;margin:30px auto;padding:0 16px}}
mark{{background:#fde68a;border-radius:3px;padding:0 2px}}pre{{white-space:pre-wrap;font:inherit;background:#fafafa;padding:16px;border:1px solid #eee}}
td,th{{border:1px solid #ddd;padding:4px 10px}}table{{border-collapse:collapse}}</style>
<h1>AI 味指数 {r.score} / 100</h1><p>只适合对比同一作者的不同版本，不能用来判断一段文字是不是 AI 写的。把鼠标放在黄色部分上可以看到原因。</p>
<table><tr><th>信号</th><th>强度 0–1</th><th>权重</th></tr>{rows}</table><h2>建议</h2><ul>{adv}</ul><h2>原文</h2><pre>{''.join(spans)}</pre></html>"""


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="aiflavor", description="写作 AI 味诊断（不是 AI 检测器）")
    p.add_argument("files", nargs="+", help="文本文件，- 表示标准输入")
    p.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    p.add_argument("--lexicon", help="额外的词表 JSON，格式同 lexicons/zh.json")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.add_argument("--html", help="把第一个文件的高亮报告写到这个路径")
    a = p.parse_args(argv)

    results = []
    for f in a.files:
        if f == "-":
            text = sys.stdin.read()
        else:
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
        r = analyze(text, a.lang, a.lexicon)
        results.append((f, text, r))

    if a.json:
        print(json.dumps([dict(file=f, **r.to_dict()) for f, _, r in results], ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render_text(f, r) for f, _, r in results))
        if len(results) > 1:
            print("\n对比: " + " | ".join(f"{f}: {r.score}" for f, _, r in results))
    if a.html:
        with open(a.html, "w", encoding="utf-8") as fh:
            fh.write(render_html(results[0][1], results[0][2]))
        print(f"\n[html] {a.html}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
