import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


OUTPUT_DIR = Path(
    "/Users/toyomasa/Library/Mobile Documents/"
    "iCloud~md~obsidian/Documents/iVault/FreePlane"
)


def get_attr(node, name):
    """Freeplaneノードから指定した属性を取得する。"""
    for attr in node.findall("attribute"):
        if attr.get("NAME") == name:
            return attr.get("VALUE")
    return None


def node_text(node):
    """Freeplaneノードのテキストを取得する。"""
    return node.get("TEXT", "").strip()


def format_due(due):
    """Freeplaneの日付をObsidian Tasks形式へ変換する。"""
    if due:
        return due.strip().replace("/", "-")
    return None


def is_task(node):
    """ノードのtask属性がyesか確認する。"""
    task_value = get_attr(node, "task")
    if task_value is None:
        return False
    return task_value.strip().lower() == "yes"


def convert_node(node, level, lines):
    """FreeplaneのノードをMarkdownへ変換する。"""
    text = node_text(node)
    due = format_due(get_attr(node, "due"))

    if text:
        if is_task(node):
            indent = "  " * max(level - 1, 0)
            line = f"{indent}- [ ] {text}"
            if due:
                line += f" 📅 {due}"
            lines.append(line)
        else:
            lines.append(text)
            lines.append("")

    for child in node.findall("node"):
        convert_node(child, level + 1, lines)


def select_mm_file():
    """macOS標準のファイル選択画面を表示する。"""
    apple_script = '''
        try
            set selectedFile to choose file with prompt "Freeplaneのmmファイルを選んでください"
            return POSIX path of selectedFile
        on error number -128
            return ""
        end try
    '''

    result = subprocess.run(
        ["osascript", "-e", apple_script],
        capture_output=True,
        text=True,
        check=False,
    )
    selected_path = result.stdout.strip()

    if not selected_path:
        return None

    mm_path = Path(selected_path)
    if mm_path.suffix.lower() != ".mm":
        raise ValueError("選択したファイルはFreeplaneのmmファイルではありません。")
    return mm_path


def show_dialog(title, message, error=False):
    """macOS標準のダイアログを表示する。"""
    icon_name = "stop" if error else "note"
    apple_script = '''
        on run argv
            set dialogTitle to item 1 of argv
            set dialogMessage to item 2 of argv
            set iconName to item 3 of argv

            if iconName is "stop" then
                display dialog dialogMessage with title dialogTitle buttons {"OK"} default button "OK" with icon stop
            else
                display dialog dialogMessage with title dialogTitle buttons {"OK"} default button "OK" with icon note
            end if
        end run
    '''

    subprocess.run(
        ["osascript", "-e", apple_script, title, message, icon_name],
        check=False,
    )


def convert_mm_to_markdown(mm_path):
    """mmファイルをMarkdownへ変換してObsidianに保存する。"""
    tree = ET.parse(mm_path)
    map_root = tree.getroot()
    root_node = map_root.find("node")

    if root_node is None:
        raise ValueError("Freeplaneのルートノードが見つかりません。")

    lines = []
    for child in root_node.findall("node"):
        convert_node(child, 1, lines)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    md_path = OUTPUT_DIR / f"{mm_path.stem}.md"
    markdown_text = "\n".join(lines).rstrip() + "\n"
    md_path.write_text(markdown_text, encoding="utf-8")
    return md_path


def main():
    try:
        mm_path = select_mm_file()
        if mm_path is None:
            print("キャンセルしました。")
            return

        md_path = convert_mm_to_markdown(mm_path)
    except ET.ParseError as error:
        message = f"mmファイルを読み込めませんでした。\n\n詳細: {error}"
        print(message)
        show_dialog("変換エラー", message, error=True)
        return
    except Exception as error:
        message = f"変換中にエラーが発生しました。\n\n詳細: {error}"
        print(message)
        show_dialog("変換エラー", message, error=True)
        return

    message = f"変換が完了しました。\n\n保存先:\n{md_path}"
    print("変換完了！")
    print(md_path)
    show_dialog("変換完了", message)


if __name__ == "__main__":
    main()
