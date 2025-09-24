import os
from typing import List


def rename_files_with_prefix(directory: str, prefix: str = "Amazon_") -> List[str]:
    """
    指定したディレクトリ内のファイル名の先頭にプレフィックスを付けてリネームする関数。

    Args:
        directory (str): 対象ディレクトリのパス
        prefix (str): ファイル名の先頭に付与する文字列 (デフォルト: "Amazon_")

    Returns:
        List[str]: ディレクトリ内のすべてのファイル名（変更後の状態）
    """
    all_files: List[str] = []

    for filename in os.listdir(directory):
        old_path: str = os.path.join(directory, filename)

        # ディレクトリはスキップ
        if os.path.isdir(old_path):
            continue

        # 新しいファイル名を作成
        if filename.startswith(prefix):
            new_filename: str = filename
        else:
            new_filename: str = prefix + filename
            new_path: str = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"{filename} -> {new_filename}")

        all_files.append(new_filename)

    return all_files


if __name__ == "__main__":
    target_directory: str = "/Users/behike56/Desktop/領収書_第3期/enginerring/Amazon/購入明細書_from_2024-10-01_to_2025-09-23"  # 変更したいディレクトリを指定
    result: List[str] = rename_files_with_prefix(target_directory)
    print("変更後のファイル名リスト:", result)
