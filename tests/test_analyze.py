import json
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from aiflavor import analyze, detect_lang  # noqa: E402
from aiflavor.analyze import load_lexicon  # noqa: E402

AI_ZH = """在数字化浪潮的背景下，人工智能正在深刻改变我们的生活。首先，人工智能赋能千行百业，发挥着不可或缺的作用。其次，它不仅提升了效率，更推动了创新。值得注意的是，人工智能也带来了新的挑战。一方面，它创造了新的机会；另一方面，它也引发了就业的担忧。随着技术的不断发展，我们需要全方位地看待这一问题。总之，人工智能具有重要意义。展望未来，让我们携手共进，共同迎接智能时代的到来。"""

HUMAN_ZH = """上周三我去城西那家修车铺，老板老周正蹲在地上拆一个变速箱。他说今年生意少了三成，来的大多是开了十年的老车。"新车都在 4S 店，坏了也不来我这儿。"他抬头看了我一眼。我问那怎么办。他没说话，把一颗螺丝扔进铁盒，叮的一声。铺子门口那棵梧桐，去年还在，今年被修路的砍了。"""

AI_EN = """In today's fast-paced world, artificial intelligence plays a crucial role in shaping our future. It's not just a tool — it's a transformative force. Moreover, it fosters innovation and unlocks new possibilities. Furthermore, it is important to note that we must navigate the complexities of this ever-evolving landscape. In conclusion, AI is a testament to human ingenuity, and its pivotal impact will continue to delve into every realm of society."""

HUMAN_EN = """My grandfather fixed radios in a shop on Fulton Street until 1987. He kept the tubes in cigar boxes, sorted by a code nobody else understood. When the shop closed he took one box home. It sat on the fridge for twenty years. After he died, my mother opened it: three tubes, a ticket stub from a 1962 Giants game, and a note that said only "ask Ray"."""


class TestAnalyze(unittest.TestCase):
    def test_lexicons_compile_and_have_fields(self):
        for lang in ("zh", "en"):
            items = load_lexicon(lang)
            self.assertGreater(len(items), 10)
            for it in items:
                for k in ("pattern", "label", "type", "evidence"):
                    self.assertIn(k, it)
                self.assertIn(it["evidence"], ("research", "multi", "single"))

    def test_detect_lang(self):
        self.assertEqual(detect_lang(AI_ZH), "zh")
        self.assertEqual(detect_lang(AI_EN), "en")

    def test_zh_ai_scores_higher_than_human(self):
        ai, hu = analyze(AI_ZH), analyze(HUMAN_ZH)
        self.assertGreater(ai.score, hu.score + 20, (ai.score, hu.score))
        labels = {h.label for h in ai.hits}
        for want in ("首先……其次", "总之（句首）", "值得注意的是", "具有重要意义", "一方面……另一方面"):
            self.assertIn(want, labels)
        self.assertLess(len(hu.hits), 2)

    def test_en_ai_scores_higher_than_human(self):
        ai, hu = analyze(AI_EN), analyze(HUMAN_EN)
        self.assertGreater(ai.score, hu.score + 20, (ai.score, hu.score))
        labels = {h.label for h in ai.hits}
        for want in ("in today's fast-paced world", "It's not X, it's Y", "Moreover / Furthermore", "In conclusion"):
            self.assertIn(want, labels)
        self.assertEqual(hu.hits, [])

    def test_uniform_sentences_raise_uniformity(self):
        uniform = "这件事很重要。我们必须认真对待。大家应该一起努力。结果一定会更好。机会总是留给有准备的人。"
        varied = "下雨了。我站在公交站等了四十分钟，车一辆都没来，旁边卖煎饼的大姐收了摊，把伞借给了一个穿校服的孩子。冷。"
        self.assertGreater(analyze(uniform).parts["uniformity"], analyze(varied).parts["uniformity"])

    def test_concrete_details_lower_vagueness(self):
        self.assertGreater(analyze(AI_ZH).parts["vagueness"], analyze(HUMAN_ZH).parts["vagueness"])

    def test_template_structure(self):
        listy = "# 三个要点\n\n**要点一：**效率提升\n\n1. 降低成本\n2. 提高质量\n3. 加快速度\n\n总之，意义重大。"
        prose = "我原本以为降低成本最难，后来发现最难的是让大家愿意改流程。这个过程花了两年。"
        self.assertGreater(analyze(listy).parts["template"], analyze(prose).parts["template"] + 0.3)

    def test_ordinary_text_does_not_trigger_markers(self):
        ordinary = "他首先打开窗户，然后坐下来吃早饭。今天的牛奶有点酸，他皱了一下眉。"
        labels = {h.label for h in analyze(ordinary).hits}
        self.assertNotIn("首先……其次", labels)

    def test_score_bounds(self):
        for t in (AI_ZH, HUMAN_ZH, AI_EN, HUMAN_EN, "短。", ""):
            r = analyze(t)
            self.assertGreaterEqual(r.score, 0)
            self.assertLessEqual(r.score, 100)


class TestCLI(unittest.TestCase):
    def run_cli(self, *args, stdin=None):
        env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "tools"))
        return subprocess.run([sys.executable, "-m", "aiflavor", *args], input=stdin, capture_output=True,
                              text=True, env=env, cwd=ROOT)

    def test_stdin_text_output(self):
        p = self.run_cli("-", stdin=AI_ZH)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("AI 味指数", p.stdout)
        self.assertIn("建议", p.stdout)

    def test_json_and_html(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            a, b, h = os.path.join(d, "a.txt"), os.path.join(d, "b.txt"), os.path.join(d, "r.html")
            for path, body in ((a, AI_ZH), (b, HUMAN_ZH)):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(body)
            p = self.run_cli(a, b, "--json")
            self.assertEqual(p.returncode, 0, p.stderr)
            data = json.loads(p.stdout)
            self.assertEqual(len(data), 2)
            self.assertGreater(data[0]["score"], data[1]["score"])
            p = self.run_cli(a, "--html", h)
            self.assertEqual(p.returncode, 0, p.stderr)
            with open(h, encoding="utf-8") as f:
                page = f.read()
            self.assertGreaterEqual(len(re.findall("<mark", page)), 5)


if __name__ == "__main__":
    unittest.main()
