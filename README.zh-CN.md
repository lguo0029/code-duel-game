# CodeDuel 自动反馈游戏

[English documentation](README.md)

需要 Python 3.11+ 和 Tkinter。在本目录运行 `python main.py`。
首页语言菜单可选 English 或简体中文；开始后保持所选语言。

固定四位，输入自己的秘密数字，默认隐藏。双方每轮各猜一次，系统自动评分，同轮猜中判平局。本版按原规则重建，并非找回的原始快照。

三档 AI 都遵守全部历史，只计算同位置同数字。允许重复与前导零。

安装及测试：

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
python -m tests.gui_smoke
```

详细算法、真实测试规模、局限及求职说明见英文 README。两个项目必须使用不同虚拟环境。
