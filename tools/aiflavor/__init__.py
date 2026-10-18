"""写作 AI 味诊断工具。见 docs/05-tool.md。"""

from .analyze import Report, analyze, detect_lang

__all__ = ["analyze", "detect_lang", "Report"]
__version__ = "0.1.0"
