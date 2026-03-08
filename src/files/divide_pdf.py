from pathlib import Path

from pypdf import PdfReader, PdfWriter

# 1. パスの設定
# プロジェクトのルートディレクトリからの相対パスで指定します
input_path = Path(
    "data/input/Web-API開発実践ガイド-――REST-gRPC-GraphQLからテスト、セキュリティまで_00.pdf"
)
output_path = Path(
    "data/output/subset-2.pdf"
)  # 出力するファイル名はお好みで変更してください

# (任意) もし output ディレクトリが存在しない場合、自動的に作成する
output_path.parent.mkdir(parents=True, exist_ok=True)

# 2. PDFの読み込みと抽出
try:
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # 例：2ページ目から4ページ目まで（インデックスは0から始まるので 1:4 と指定）を抽出
    # 抽出したいページ数に合わせて変更してください
    for page in reader.pages[106:]:
        writer.add_page(page)

    # 3. ファイルの書き出し
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"抽出が完了しました。保存先: {output_path}")

except FileNotFoundError:
    print(
        f"エラー: 入力ファイルが見つかりません。パスを確認してください。\n指定されたパス: {input_path}"
    )
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
