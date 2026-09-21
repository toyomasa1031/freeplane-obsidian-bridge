![Workflow](images/workflow.png)
# Freeplane → Obsidian Bridge

Freeplaneで整理したマインドマップを、Obsidian Tasksで管理できるMarkdownへ変換するPythonツールです。

## 概要

このツールは、Freeplaneの `.mm` ファイルを読み込み、

- task 属性
- due 属性

を検出して、

Obsidian Tasks形式のMarkdownへ変換します。

```
Freeplane
      ↓
Python
      ↓
Obsidian Tasks
```

## 特徴

- Freeplaneの属性をそのまま利用
- task=yes を Obsidian Tasksへ変換
- due を期限日へ変換
- H1はファイル名
- シンプルなルールで運用可能

## Freeplane側の設定

タスクにしたいノードへ

```
task = yes
due = 2026-09-30
```

という属性を追加します。

## 変換例

### Freeplane

```
task = yes
due = 2026-09-30
TEXT = Python変換ツールを作成する
```

↓

### Obsidian

```markdown
- [ ] Python変換ツールを作成する 📅 2026-09-30
```

## 使い方

1. Pythonを起動
2. `freeplane_to_obsidian.py` を実行
3. Freeplaneの `.mm` を選択
4. 同じフォルダへ `.md` が生成されます。

## 動作環境

- Python 3.x
- Freeplane
- Obsidian + Tasks Plugin

## 今後の予定

- タグ変換
- カテゴリー変換
- 一括変換
- Markdown → Freeplane変換
- Obsidian Properties対応

## ライセンス

MIT License

## 作者

紗月堂主人

https://satsukidou.com
