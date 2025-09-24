import os
import re
import pdfplumber

# 「ご請求額： ¥ 4,155」を検出する正規表現
pattern = r"ご請求額：\s*¥\s*([\d,]+)"


def _extract_amount_from_pdf(pdf_path: str) -> str | None:
    """PDFの最初のページから請求額を抽出（カンマ付き数字を返す）"""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        if text:
            for line in text.splitlines():
                match = re.search(pattern, line)
                if match:
                    return match.group(1)  # 例: "4,155"
    return None


def rename_pdfs_in_directory(directory: str) -> list[str]:
    """ディレクトリ内のPDFをリネームし、最終的なファイル名リストを返す"""
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):  # 全PDF対象
            old_path = os.path.join(directory, filename)

            # 金額を抽出
            amount = _extract_amount_from_pdf(old_path)
            if not amount:
                print(f"金額が見つかりませんでした: {filename}")
                continue

            # ファイル名を分解
            parts = filename.split("_", 2)  # 例: 20250101_xxxx_yyyy.pdf
            if len(parts) < 3:
                print(f"ファイル名形式が不正です: {filename}")
                continue

            date, rest = parts[0], parts[1:]
            rest_str = "_".join(rest)

            # 新しいファイル名
            new_filename = f"Amazon_{date}_{amount}_{rest_str}"
            new_path = os.path.join(directory, new_filename)

            # リネーム実行
            os.rename(old_path, new_path)
            print(f"{filename} → {new_filename}")

    # リネーム後の全ファイル名リストを返す
    return sorted(os.listdir(directory))


# 20241222_Printable Order Summary_249-6032917-3743854.pdf
if __name__ == "__main__":
    current_dir = os.getcwd()
    print("現在のディレクトリ:", current_dir)
    amount = _extract_amount_from_pdf(
        current_dir
        + "/src/files/20241222_Printable Order Summary_249-6032917-3743854.pdf"
    )
    print(amount)
