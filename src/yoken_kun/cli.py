"""yoken-kun CLI: 対話で要件定義してAI-README.mdを生成"""

import os
from pathlib import Path

import click

from yoken_kun.dialogue.engine import run_dialogue
from yoken_kun.generator.ai_readme import generate_ai_readme


@click.command()
@click.option("--output", "-o", default=".", help="AI-README.md の出力先ディレクトリ")
@click.option("--notes", type=click.Path(exists=True), help="事前メモファイル（箇条書きでもOK）")
@click.version_option()
def main(output: str, notes: str | None):
    """曖昧なアイデアから対話でAI-README.mdを生成する"""

    click.echo()
    click.secho("╔══════════════════════════════════════╗", fg="cyan")
    click.secho("║       よけんくん v0.1.0              ║", fg="cyan")
    click.secho("║   対話ベースの要件定義ツール         ║", fg="cyan")
    click.secho("╚══════════════════════════════════════╝", fg="cyan")
    click.echo()
    click.echo("アイデアを聞かせてください。対話を通じてAI-README.mdを作成します。")
    click.echo("技術的なことがわからなくても大丈夫です。「おまかせ」でOK。")
    click.echo()

    # 事前メモ読み込み
    notes_text = None
    if notes:
        notes_text = Path(notes).read_text(encoding="utf-8")
        click.secho(f"事前メモを読み込みました: {notes}", fg="green")
        click.echo()

    # 対話実行
    try:
        draft = run_dialogue(notes_text)
    except KeyboardInterrupt:
        click.echo("\n\n中断されました。")
        raise SystemExit(0)

    if not draft:
        click.secho("ドラフトが生成されませんでした。", fg="red")
        raise SystemExit(1)

    # 最終整形
    click.echo()
    click.secho("AI-README.md を生成中...", fg="yellow")
    final = generate_ai_readme(draft)

    # 出力
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "AI-README.md"
    output_path.write_text(final, encoding="utf-8")

    click.echo()
    click.secho(f"✅ AI-README.md を生成しました: {output_path}", fg="green", bold=True)
    click.echo()
    click.secho("次のステップ:", fg="cyan")
    click.echo(f"  repo-readme-stage2 {output_path} -o {output_dir}")
    click.echo("  → GEMINI.md, CLAUDE.md, hookファイルが生成されます")
    click.echo()


if __name__ == "__main__":
    main()
