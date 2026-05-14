#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Record Assistant Reply Skill

This script saves assistant replies into a single Markdown file,
grouped by date and appended with timestamps.

Usage:

python scripts/record_reply.py \
  --content "这里是需要记录的机器人回复" \
  --title "可选标题"

Example:

python scripts/record_reply.py \
  --content "这是上一条机器人回复内容。" \
  --title "产品方案记录"
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


DEFAULT_RECORD_DIR = "records"
DEFAULT_RECORD_FILE = "assistant_reply_records.md"


def ensure_record_file(file_path: Path) -> None:
    """
    Ensure the record file and its parent directory exist.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text(
            "# Assistant Reply Records\n\n"
            "This file stores assistant replies recorded during conversations.\n\n",
            encoding="utf-8"
        )


def build_record_block(content: str, title: Optional[str] = None) -> str:
    """
    Build a Markdown block for one record.
    """
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")

    safe_title = title.strip() if title and title.strip() else "未命名记录"

    return (
        f"\n### {time_str}｜{safe_title}\n\n"
        f"{content.strip()}\n\n"
        "---\n"
    )


def append_record_by_date(file_path: Path, content: str, title: Optional[str] = None) -> None:
    """
    Append a record under today's date section.

    If today's section exists, append the new record under it.
    If not, create a new date section at the end of the file.
    """
    ensure_record_file(file_path)

    today = datetime.now().strftime("%Y-%m-%d")
    date_heading = f"## {today}"
    record_block = build_record_block(content, title)

    existing = file_path.read_text(encoding="utf-8")

    if date_heading in existing:
        updated = existing.rstrip() + record_block
    else:
        updated = existing.rstrip() + f"\n\n{date_heading}\n" + record_block

    file_path.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record assistant reply into a date-grouped Markdown file."
    )

    parser.add_argument(
        "--content",
        required=True,
        help="The assistant reply content to record."
    )

    parser.add_argument(
        "--title",
        required=False,
        default=None,
        help="Optional title for this record."
    )

    parser.add_argument(
        "--output",
        required=False,
        default=os.path.join(DEFAULT_RECORD_DIR, DEFAULT_RECORD_FILE),
        help="Output Markdown file path."
    )

    args = parser.parse_args()

    content = args.content.strip()

    if not content:
        result = {
            "success": False,
            "file_path": args.output,
            "message": "Content is empty. Nothing was recorded."
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    file_path = Path(args.output)

    try:
        append_record_by_date(
            file_path=file_path,
            content=content,
            title=args.title
        )

        result = {
            "success": True,
            "file_path": str(file_path),
            "message": "Recorded successfully."
        }

    except Exception as error:
        result = {
            "success": False,
            "file_path": str(file_path),
            "message": f"Failed to record content: {error}"
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
