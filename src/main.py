import argparse
from files.pdf_file_rename import rename_pdfs_in_directory


def main():
    print("=== workspace-tools v0,1 ===")
    print("")
    # ArgumentParserの生成
    parser = argparse.ArgumentParser(description="")

    # オプション引数（--付きで指定可能）
    parser.add_argument("--rename-pdf", action="store_true", help="PDFファイルリネーム")

    # 引数を解析
    args = parser.parse_args()
    print(f"選択されたオプション: {args}")

    if args.rename_pdf:
        print("|> 対象のディレクトリをフルパスで入力してください: ")
        pdf_path: str = input()
        result = rename_pdfs_in_directory(pdf_path)
        print("リネーム後のファイル一覧:")
        for f in result:
            print(f)


if __name__ == "__main__":
    main()
