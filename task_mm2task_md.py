import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter import Tk, filedialog


def get_attr(node, name):
    for attr in node.findall("attribute"):
        if attr.get("NAME") == name:
            return attr.get("VALUE")
    return None


def node_text(node):
    return node.get("TEXT", "").strip()


def format_due(due):
    """Freeplaneの日付 2026/09/21 → Obsidian Tasks用 2026-09-21"""
    if due:
        return due.replace("/", "-")
    return None


def convert_node(node, level, lines):
    text = node_text(node)
    task = get_attr(node, "task")
    due = format_due(get_attr(node, "due"))

    # task=yes のノードは、階層に関係なくタスクとして出力
    if task == "yes":
        indent = "  " * max(level - 1, 0)

        line = f"{indent}- [ ] {text}"

        if due:
            line += f" 📅 {due}"

        lines.append(line)

    else:
        # 通常ノードは見出しにする
        if level == 1 and text:
            lines.append(f"## {text}")
            lines.append("")

        elif level == 2 and text:
            lines.append(f"### {text}")
            lines.append("")

        elif level >= 3 and text:
            indent = "  " * (level - 3)
            lines.append(f"{indent}- {text}")

    # 子ノード
    for child in node.findall("node"):
        convert_node(child, level + 1, lines)


def main():
    root = Tk()
    root.withdraw()

    mm_path = filedialog.askopenfilename(
        title="Freeplaneのmmファイルを選んでください",
        filetypes=[("Freeplane files", "*.mm")]
    )

    if not mm_path:
        print("キャンセルしました")
        return

    mm_path = Path(mm_path)

    tree = ET.parse(mm_path)
    map_root = tree.getroot()
    root_node = map_root.find("node")

    lines = []

    # H1はファイル名
    lines.append(f"# {mm_path.stem}")
    lines.append("")

    for child in root_node.findall("node"):
        convert_node(child, 1, lines)

    md_path = mm_path.with_suffix(".md")

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("変換完了！")
    print(md_path)


if __name__ == "__main__":
    main()