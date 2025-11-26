from typing import List

import requests
from bs4 import BeautifulSoup
from mcp.server import FastMCP


# FastMCP instance used to expose tools to MCP-compatible AI agents.
mcp = FastMCP("gia-vang-giao-thuy-mcp")


def _parse_gia_vang_html(html: str) -> str:
    """
    Phân tích HTML từ https://cccsonline.click/gia-vang-giao-thuy
    và trả về tóm tắt dạng văn bản/markdown **bằng tiếng Việt** cho AI agent.
    """
    soup = BeautifulSoup(html, "html.parser")

    parts: List[str] = []

    # Main page title (if present)
    title = soup.find("h1")
    if title:
        parts.append(title.get_text(strip=True))

    # Tables section:
    #   - first table is usually "Giá vàng Hiệp hội vàng bạc Giao Thủy Hải Hậu"
    #   - second table is usually the SJC price table
    tables = soup.find_all("table")
    if not tables:
        return "Không tìm thấy bảng giá vàng nào trong nội dung trang."

    def table_to_markdown(table, heading: str | None = None) -> str:
        rows = table.find_all("tr")
        if not rows:
            return ""

        md_lines: List[str] = []
        if heading:
            md_lines.append(f"## {heading}")

        # Header row
        headers = [
            " ".join(col.stripped_strings)
            for col in rows[0].find_all(["th", "td"])
        ]
        if headers:
            md_lines.append("| " + " | ".join(headers) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        # Data rows
        for row in rows[1:]:
            # Join all text fragments inside each cell so that `<br>` and
            # nested <font> like "▲50K" become a single readable string,
            # e.g. "15.140.000 ▲50K".
            cols = [
                " ".join(col.stripped_strings)
                for col in row.find_all("td")
            ]
            if cols:
                md_lines.append("| " + " | ".join(cols) + " |")

        return "\n".join(md_lines)

    # Assumption: table[0] = local association (Giao Thủy / Hải Hậu),
    #             table[1] = SJC price table
    if len(tables) >= 1:
        parts.append(
            table_to_markdown(
                tables[0], "Giá vàng Hiệp hội vàng bạc Giao Thủy Hải Hậu"
            )
        )
    if len(tables) >= 2:
        parts.append(table_to_markdown(tables[1], "Bảng giá vàng SJC"))

    # Time / last update note if present in raw text
    time_note = soup.find(string=lambda t: isinstance(t, str) and "cập nhật" in t.lower())
    if time_note:
        parts.append(f"Thông tin bổ sung từ trang (tiếng Việt): {time_note.strip()}")

    # Filter out any empty sections
    parts = [p for p in parts if p]
    if not parts:
        return "Không trích xuất được dữ liệu giá vàng từ trang."

    body = "\n\n".join(parts)

    # Gợi ý nhẹ cho AI agent: nên trả lời người dùng bằng tiếng Việt.
    hint = (
        "\n\nGợi ý cho AI agent: Hãy dùng dữ liệu bảng giá vàng ở trên và "
        "giải thích / so sánh cho người dùng **bằng tiếng Việt dễ hiểu**."
    )

    return body + hint


@mcp.tool()
async def fetch_gia_vang_giao_thuy() -> str:
    """
    MCP tool: lấy bảng giá vàng từ
    https://cccsonline.click/gia-vang-giao-thuy và trả về tóm tắt
    dạng markdown **bằng tiếng Việt**.
    """
    url = "https://cccsonline.click/gia-vang-giao-thuy"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Lỗi khi tải dữ liệu từ {url}: {e}"

    parsed_text = _parse_gia_vang_html(response.text)

    return parsed_text


if __name__ == "__main__":
    mcp.run()


