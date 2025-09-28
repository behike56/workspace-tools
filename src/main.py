# src/main.py
import argparse
import os

from files.dir_compare import compare_filenames
from files.pdf_file_rename import rename_pdfs_in_directory
# ★ Kivy を使う可能性があるが、ここでは import しない（後で条件付き import）


def main() -> None:
    print("=== workspace-tools v0.1 ===")

    parser = argparse.ArgumentParser(description="ファイル名リネームツール")
    parser.add_argument(
        "--rename-pdf", action="store_true", help="PDF を Amazon 形式でリネーム"
    )
    parser.add_argument("--gui", action="store_true", help="GUI を起動")
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("DIR_A", "DIR_B"),
        help="2つのディレクトリで同名ファイルを比較",
    )
    args = parser.parse_args()
    print(f"選択されたオプション: {args}")

    # CLI: PDF リネームのみ
    if args.rename_pdf:
        print("|> 対象のディレクトリをフルパスで入力してください: ")
        pdf_path: str = input().strip()
        result = rename_pdfs_in_directory(pdf_path)
        print("リネーム後のファイル一覧:")
        for f in result:
            print(f)
        return

    if args.compare:
        res = compare_filenames(args.compare[0], args.compare[1])
        print("== 共通 ==")
        print("\n".join(res["common"]))
        print("== Aのみ ==")
        print("\n".join(res["only_a"]))
        print("== Bのみ ==")
        print("\n".join(res["only_b"]))
        return

    # GUI 起動（デフォルト or --gui）
    # ★ ここで Kivy の引数処理を無効化してから import するのがポイント
    os.environ.setdefault("KIVY_NO_ARGS", "1")

    from gui.ui_app import RenameApp  # 遅延 import（ここで初めて Kivy が読み込まれる）

    RenameApp().run()


if __name__ == "__main__":
    main()
