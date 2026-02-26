"""AI-README.md 生成: ドラフトを最終版に整形"""

import re

from yoken_kun.config import client, MODEL_NAME


def generate_ai_readme(draft: str) -> str:
    """対話で確定したドラフトを元にAI-README.mdを生成"""

    prompt = f"""\
以下は対話で確定したAI-README.mdのドラフトです。
これを最終版として整形してください。

## ルール
- フォーマットは維持すること（セクション構成を変えない）
- 内容は変えず、文章を自然に整える程度
- 箇条書きは `-` で統一
- コードブロック内のパスはバッククォートで囲む
- 空のセクションがあれば削除
- Markdownとして正しい形式にする
- 出力はMarkdown本文のみ（```markdown ブロックで囲まない）

## ドラフト
{draft}
"""

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return _clean_markdown(response.text)


def _clean_markdown(text: str) -> str:
    """LLM出力からMarkdownコードフェンスのラッパーを除去"""
    text = text.strip()

    # ```markdown ... ``` で囲まれていたら除去
    if text.startswith("```markdown"):
        text = text[len("```markdown"):].strip()
    elif text.startswith("```md"):
        text = text[len("```md"):].strip()
    elif text.startswith("```"):
        text = text[3:].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text
