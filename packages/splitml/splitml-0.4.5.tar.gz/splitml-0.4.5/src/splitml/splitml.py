from pathlib import Path
from typing import Union

from tclogger import logger

from .stats import stat_tokens
from .groupers import NodesGrouper
from .html_splitter import HTMLSplitter


def split_html_str(html_str: str, format=None):
    return HTMLSplitter().split_html_str(html_str, format=format)


def split_html_file(html_path: Union[Path, str], format=None):
    return HTMLSplitter().split_html_file(html_path, format=format)


def chunk_html_str(html_str: str, format=None):
    nodes = HTMLSplitter().split_html_str(html_str, format=format)
    grouped_nodes = NodesGrouper().group_nodes(nodes)
    return grouped_nodes


def chunk_html_file(html_path: Union[Path, str], format=None):
    nodes = HTMLSplitter().split_html_file(html_path, format=format)
    grouped_nodes = NodesGrouper().group_nodes(nodes)
    return grouped_nodes


if __name__ == "__main__":
    html_root = Path(__file__).parent / "samples"

    file_pattern = "*.html.md"
    html_paths = sorted(
        list(html_root.glob(file_pattern)),
        key=lambda x: str(x).lower(),
    )[:2]
    splitter = HTMLSplitter()
    grouper = NodesGrouper()
    for html_path in html_paths:
        logger.note(f"> Processing: {html_path.name}")
        nodes = splitter.split_html_file(html_path)
        logger.success(f"  - {len(nodes)} nodes.")
        stat_tokens(nodes)
        grouped_nodes = grouper.group_nodes(nodes)
        logger.success(f"  - {len(grouped_nodes)} grouped nodes.")
        stat_tokens(grouped_nodes)

    # [**/src]
    # python -m splitml.splitml
