"""対話エンジン: 3フェーズで要件定義を行う"""

import re

from yoken_kun.config import client, MODEL_NAME
from yoken_kun.dialogue.prompts import SYSTEM_PROMPT


def run_dialogue(notes_text: str | None = None) -> str:
    """対話ループを実行し、確定したドラフトを返す"""

    system = SYSTEM_PROMPT.format(
        notes_text=notes_text or "（事前メモなし）"
    )

    # 初回メッセージ
    first_msg = "要件定義を始めてください。「何を作りたいですか？」から始めてください。"
    if notes_text:
        first_msg += f"\n\nユーザーからの事前メモ:\n```\n{notes_text}\n```"

    history = []

    # system promptを最初のユーザーメッセージに含める
    full_first = system + "\n\n---\n\n" + first_msg

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=_build_contents(history, full_first),
    )
    ai_text = response.text
    history.append({"role": "user", "text": full_first})
    history.append({"role": "model", "text": ai_text})

    print(f"\n{ai_text}\n")

    # 対話ループ
    confirmed_draft = None

    while True:
        draft = _extract_draft(ai_text)
        summary = _extract_summary(ai_text)

        if draft:
            # フェーズ3: ドラフトレビュー
            print("\n--- ドラフト確認 ---")
            print("修正したい点があれば入力してください。OKならそのままEnterを押してください。")
            user_input = input("\n> ").strip()

            if not user_input:
                confirmed_draft = draft
                print("\nドラフト確定!")
                break
            else:
                msg = f"以下の修正を反映してドラフトを再提示してください:\n{user_input}"

        elif summary:
            # フェーズ1→2 遷移: 要約確認
            print("\n--- 要約確認 ---")
            print("方向性は合っていますか？修正や補足があれば入力してください。OKならそのままEnterを押してください。")
            user_input = input("\n> ").strip()

            if not user_input:
                msg = "方向性OKです。不足している情報を質問して、AI-READMEのドラフトを完成させてください。"
            else:
                msg = user_input

        else:
            # フェーズ1 or 2: 通常対話
            user_input = input("\n> ").strip()
            if not user_input:
                msg = "ここまでの情報でまとめてください。"
            else:
                msg = user_input

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=_build_contents(history, msg),
        )
        ai_text = response.text
        history.append({"role": "user", "text": msg})
        history.append({"role": "model", "text": ai_text})
        print(f"\n{ai_text}\n")

    return confirmed_draft


def _build_contents(history: list[dict], new_msg: str) -> list[dict]:
    """履歴 + 新メッセージをGemini API形式に変換"""
    contents = []
    for h in history:
        contents.append({
            "role": h["role"],
            "parts": [{"text": h["text"]}],
        })
    contents.append({
        "role": "user",
        "parts": [{"text": new_msg}],
    })
    return contents


def _extract_draft(text: str) -> str | None:
    """[DRAFT]...[/DRAFT] ブロックを抽出"""
    start = text.find("[DRAFT]")
    end = text.find("[/DRAFT]")

    if start != -1 and end != -1:
        return text[start + len("[DRAFT]"):end].strip()

    if start != -1:
        return text[start + len("[DRAFT]"):].strip()

    return None


def _extract_summary(text: str) -> str | None:
    """[SUMMARY]...[/SUMMARY] ブロックを抽出"""
    start = text.find("[SUMMARY]")
    end = text.find("[/SUMMARY]")

    if start != -1 and end != -1:
        return text[start + len("[SUMMARY]"):end].strip()

    if start != -1:
        return text[start + len("[SUMMARY]"):].strip()

    return None
