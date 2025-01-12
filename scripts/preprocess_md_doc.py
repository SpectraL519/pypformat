import argparse
import re
from pathlib import Path


def preprocess_md_doc(input_file: Path, output_file: Path, repo_url: str):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = re.sub(
        r"\[([^\]]+)\]\((?!http)(.*?)\)",
        lambda match: f"[{match.group(1)}]({repo_url}/{match.group(2).lstrip('./')})",
        content,
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(updated_content)


def parse_args():
    parser = argparse.ArgumentParser(description="Preprocess README file for PyPI.")
    parser.add_argument(
        "-i", "--input-file", type=Path, default="README.md", help="Path to the input README file."
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=Path,
        default="README_preprocessed.md",
        help="Path to the output README file.",
    )
    parser.add_argument(
        "-r",
        "--repo-url",
        type=str,
        default="https://github.com/SpectraL519/repo/blob/master",
        help="Base URL of the repository.",
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    preprocess_md_doc(**parse_args())
