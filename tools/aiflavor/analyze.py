"""
AI 味诊断：把一段文字里可能让人觉得「像 AI 写的」地方找出来，并说明原因。

这不是 AI 检测器。研究表明，自动检测器在改写后很容易失效，还会误判非母语作者
（Liang et al., 2023）。这里的每一项都只是写作上的信号，分数只用来对比同一作者的
不同版本，不能用来判断一段文字是不是 AI 写的。
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from dataclasses import dataclass, field, asdict

LEXICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexicons")

# 各项信号在总分里的权重（总和 100）。权重是经验设定，见 docs/05-tool.md。
WEIGHTS = {
    "markers": 35,      # AI 爱用的词、套话、套路句式
    "uniformity": 20,   # 句子长短太均匀
    "template": 15,     # 分点、列表、小标题、总结段
    "punctuation": 10,  # 破折号、冒号、emoji 过多
    "repetition": 10,   # 句子之间重复的说法
    "vagueness": 10,    # 缺少具体的东西（数字、引语、名字）
}

CJK = re.compile(r"[一-鿿]")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


@dataclass
class Hit:
    label: str
    type: str
    evidence: str
    note: str
    start: int
    end: int
    text: str


@dataclass
class Report:
    lang: str
    chars: int
    sentences: int
    score: float
    parts: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    hits: list = field(default_factory=list)
    advice: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["hits"] = [asdict(h) if isinstance(h, Hit) else h for h in self.hits]
        return d


def detect_lang(text: str) -> str:
    cjk = len(CJK.findall(text))
    letters = len(re.findall(r"[A-Za-z]", text))
    return "zh" if cjk >= letters * 0.3 else "en"


def load_lexicon(lang: str, extra: str | None = None) -> list[dict]:
    with open(os.path.join(LEXICON_DIR, f"{lang}.json"), encoding="utf-8") as f:
        items = json.load(f)
    if extra:
        with open(extra, encoding="utf-8") as f:
            items += json.load(f)
    flags = re.MULTILINE | (re.IGNORECASE if lang == "en" else 0)
    for it in items:
        it["re"] = re.compile(it["pattern"], flags)
    return items


def split_sentences(text: str, lang: str) -> list[str]:
    if lang == "zh":
        parts = re.split(r"(?<=[。！？!?；;])|\n+", text)
    else:
        parts = re.split(r"(?<=[.!?;])\s+|\n+", text)
    return [p.strip() for p in parts if p and p.strip()]


def sent_len(s: str, lang: str) -> int:
    if lang == "zh":
        return len(CJK.findall(s)) + len(re.findall(r"[A-Za-z0-9]+", s))
    return len(re.findall(r"\b[\w'-]+\b", s))


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


def analyze(text: str, lang: str = "auto", extra_lexicon: str | None = None) -> Report:
    lang = detect_lang(text) if lang == "auto" else lang
    sents = split_sentences(text, lang)
    lens = [sent_len(s, lang) for s in sents if sent_len(s, lang) > 0]
    size = max(len(CJK.findall(text)) if lang == "zh" else len(re.findall(r"\b\w+\b", text)), 1)
    # 每千字（中文）或每千词（英文）。设一个最小篇幅，免得短文本里一个冒号就把分数打满
    per_k = 1000 / max(size, 300 if lang == "zh" else 200)

    # 1. 标记词和套路句式
    hits: list[Hit] = []
    for it in load_lexicon(lang, extra_lexicon):
        for m in it["re"].finditer(text):
            hits.append(Hit(it["label"], it["type"], it["evidence"], it.get("note", ""),
                            m.start(), m.end(), m.group(0)[:60]))
    hits.sort(key=lambda h: h.start)
    weight = {"research": 1.0, "multi": 0.8, "single": 0.4}
    marker_density = sum(weight.get(h.evidence, 0.5) for h in hits) * per_k
    # 中文每千字约 6 个、英文每千词约 8 个时打满
    markers = _clip(marker_density / (6 if lang == "zh" else 8))

    # 2. 句长均匀度：变异系数越低越均匀。人写的文字通常 CV 在 0.5 以上
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        sd = math.sqrt(sum((x - mean) ** 2 for x in lens) / len(lens))
        cv = sd / mean if mean else 0.0
        uniformity = _clip((0.6 - cv) / 0.35)
    else:
        mean, cv, uniformity = (sum(lens) / len(lens) if lens else 0.0), None, 0.0
    short_cut, long_cut = (8, 50) if lang == "zh" else (6, 35)
    short_share = sum(1 for x in lens if x <= short_cut) / len(lens) if lens else 0.0
    long_share = sum(1 for x in lens if x >= long_cut) / len(lens) if lens else 0.0

    # 3. 模板化结构
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    list_lines = sum(1 for l in lines if re.match(r"^([-*•·]|\d+[.、)）]|[一二三四五六七八九十]+[、.]|（[一二三四五六七八九十]）)", l))
    heading_lines = sum(1 for l in lines if re.match(r"^(#+\s|\*\*[^*]{1,30}\*\*[:：]?$)", l) or (len(l) <= 20 and l.endswith(("：", ":"))))
    bold_spans = len(re.findall(r"\*\*[^*]{1,40}\*\*", text))
    struct_hits = sum(1 for h in hits if h.type == "structure")
    template = _clip((list_lines + heading_lines) / max(len(lines), 1) * 1.5 + bold_spans * per_k / 20 + struct_hits * 0.15)

    # 4. 标点
    dashes = text.count("——") + (len(re.findall(r"\s[—–]\s|\w—\w", text)) if lang == "en" else 0)
    colons = text.count("：") + (text.count(":") if lang == "en" else 0)
    emojis = len(EMOJI.findall(text))
    punctuation = _clip(dashes * per_k / 10 + colons * per_k / 20 + emojis * per_k / 4)

    # 5. 重复：句子之间共享的 n-gram。中文按字取 6-gram，英文按词取 4-gram，
    #    这样只抓重复的说法，不会把反复出现的话题词（如「人工智能」）算进去
    n = 6 if lang == "zh" else 4
    def grams(s: str) -> set:
        toks = CJK.findall(s) if lang == "zh" else re.findall(r"\b\w+\b", s.lower())
        return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}
    seen: Counter = Counter()
    for s in sents:
        seen.update(grams(s))
    repeated = sum(c - 1 for c in seen.values() if c > 1)
    repetition = _clip(repeated * per_k / 25)

    # 6. 空泛：具体的东西越少，越像 AI。数字、引语、专有名词、具体时间都算具体
    numbers = len(re.findall(r"\d+(\.\d+)?%?|[一二三四五六七八九十百千万]+(个|年|天|次|岁|块|元|人)", text))
    quotes = len(re.findall(r"[“「\"][^”」\"]{2,80}[”」\"]", text))
    if lang == "en":
        # 只算句子中间的大写词，句首的 In / Moreover 不算专有名词
        names = len(re.findall(r"(?<![.!?]\s)(?<!^)(?<=\s)[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", text, re.M))
    else:
        names = len(re.findall(r"[A-Za-z]{2,}", text))
    concrete = (numbers + quotes * 2 + names * 0.5) * per_k
    vagueness = _clip(1 - concrete / 12) if size >= (80 if lang == "zh" else 50) else 0.0

    parts = {"markers": markers, "uniformity": uniformity, "template": template,
             "punctuation": punctuation, "repetition": repetition, "vagueness": vagueness}
    score = round(sum(WEIGHTS[k] * v for k, v in parts.items()), 1)

    advice = []
    if markers > 0.3:
        top = Counter(h.label for h in hits).most_common(3)
        advice.append("删掉或换掉这些套话：" + "、".join(f"「{k}」×{n}" for k, n in top))
    if uniformity > 0.4:
        advice.append(f"句子长短太平均（变异系数 {cv:.2f}）。加几个很短的句子，或者把一个判断写长、写透")
    if template > 0.4:
        advice.append("结构太像提纲：减少分点、小标题和加粗，把要点写成连贯的段落")
    if punctuation > 0.4:
        advice.append("破折号、冒号或 emoji 太多，换成句号和普通的连接词")
    if repetition > 0.4:
        advice.append("同样的说法反复出现，删掉重复的那几句")
    if vagueness > 0.5:
        advice.append("太空泛：加一个具体的数字、名字、场景或别人说过的原话")

    metrics = {
        "markers_per_k": round(marker_density, 2), "sentence_len_mean": round(mean, 1),
        "sentence_len_cv": None if cv is None else round(cv, 3),
        "short_sentence_share": round(short_share, 3), "long_sentence_share": round(long_share, 3),
        "list_or_heading_lines": list_lines + heading_lines, "bold_spans": bold_spans,
        "dashes": dashes, "colons": colons, "emojis": emojis, "repeated_ngrams": repeated,
        "numbers": numbers, "quotes": quotes,
    }
    return Report(lang, len(text), len(sents), score, {k: round(v, 3) for k, v in parts.items()},
                  metrics, hits, advice)
