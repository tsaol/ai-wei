#!/usr/bin/env python3
"""
同题对照实验：给每篇人写散文的题目，让 3 个模型各写两篇（普通提示 / 去 AI 味提示）。

用法:
    python experiment/generate.py --human data/human_s --out data/ai [--models opus,kimi,gpt] [--workers 6]

需要 AWS 凭证和 Bedrock 上这些模型的权限。模型 ID 可以用环境变量覆盖：
    OPUS_MODEL_ID / OPUS_REGION, KIMI_MODEL_ID, GPT_MODEL_ID, BEDROCK_REGION
"""

import argparse
import concurrent.futures as cf
import json
import os
import time

import boto3
from botocore.config import Config

MODELS = {
    "opus": (os.environ.get("OPUS_MODEL_ID", "jp.anthropic.claude-opus-5-5"), os.environ.get("OPUS_REGION", "ap-northeast-1")),
    "kimi": (os.environ.get("KIMI_MODEL_ID", "us.moonshotai.kimi-k3"), os.environ.get("BEDROCK_REGION", "us-east-1")),
    "gpt": (os.environ.get("GPT_MODEL_ID", "us.openai.gpt-6-astra"), os.environ.get("BEDROCK_REGION", "us-east-1")),
}

PLAIN = "请以《{title}》为题写一篇中文散文，约{n}字。不要模仿已经存在的同名作品。直接输出正文，不要标题。"

DEAI = PLAIN + """

写的时候注意：
- 写一件具体的事：有时间、地点、人名或物件，有人说过的原话。
- 句子长短要有变化：有很短的句子，也有一口气说下来的长句。
- 不用"首先、其次、总之、综上、值得注意的是、由此可见、具有重要意义、展望未来"这类连接和收尾套话。
- 不要分点、小标题、加粗，不要堆砌排比和对仗。
- 结尾不要升华，也不要总结道理，停在一个具体的画面或动作上。
- 可以有个人的偏见、犹豫和不确定，不必面面俱到。"""

PROMPTS = {"plain": PLAIN, "deai": DEAI}


def call(key: str, prompt: str) -> tuple[str, dict]:
    model_id, region = MODELS[key]
    client = boto3.client("bedrock-runtime", region_name=region,
                          config=Config(read_timeout=600, retries={"max_attempts": 3}))
    msgs = [{"role": "user", "content": [{"text": prompt}]}]
    t = time.time()
    if key == "opus":
        # Opus 5.5 不支持 temperature；用流式接口，输出长时更稳
        r = client.converse_stream(modelId=model_id, messages=msgs, inferenceConfig={"maxTokens": 16000})
        text, usage = [], {}
        for ev in r["stream"]:
            if "contentBlockDelta" in ev:
                text.append(ev["contentBlockDelta"]["delta"].get("text", ""))
            elif "metadata" in ev:
                usage = ev["metadata"].get("usage", {})
        out = "".join(text)
    else:
        r = client.converse(modelId=model_id, messages=msgs, inferenceConfig={"maxTokens": 16000})
        out = "".join(c.get("text", "") for c in r["output"]["message"]["content"])
        usage = r.get("usage", {})
    return out.strip(), {"sec": round(time.time() - t, 1), "tokens": usage.get("totalTokens")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", default="opus,kimi,gpt")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    for f in sorted(os.listdir(a.human)):
        title = f[:-4]
        with open(os.path.join(a.human, f), encoding="utf-8") as fh:
            n = round(len(fh.read()), -2)
        for m in a.models.split(","):
            for p in PROMPTS:
                path = os.path.join(a.out, f"{title}__{m}__{p}.txt")
                if not os.path.exists(path):
                    jobs.append((title, n, m, p, path))
    print(f"[generate] {len(jobs)} jobs")

    def run(job):
        title, n, m, p, path = job
        try:
            text, info = call(m, PROMPTS[p].format(title=title, n=n))
            if not text:
                raise RuntimeError("empty output")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
            return dict(title=title, model=m, prompt=p, ok=True, chars=len(text), **info)
        except Exception as e:  # 一个失败不影响其他
            return dict(title=title, model=m, prompt=p, ok=False, err=str(e)[:200])

    with cf.ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(run, jobs):
            print(json.dumps(r, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
