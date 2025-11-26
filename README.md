## Gold Price MCP Server (Giao Thủy)

This project provides an **MCP server** that exposes a tool for AI agents
to fetch gold price tables from  
`https://cccsonline.click/gia-vang-giao-thuy`  
(source: [`cccsonline.click`](https://cccsonline.click/gia-vang-giao-thuy)).

The tool is designed so that **all returned content is in Vietnamese**,  
making it easy for AI agents to answer user questions naturally in Vietnamese.

### Project Structure

- **Main entry file**: `mcp_server.py`
- **MCP tool**:
  - `fetch_gia_vang_giao_thuy`: performs an HTTP request to the website above
    and returns the gold price tables as human‑readable **Vietnamese** text/markdown.

### Installation & Local Run

```bash
cd /Users/duypt/Documents/Coding/gold-price-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the MCP server over stdio
python mcp_server.py
```

### Using with an MCP‑compatible AI Agent

This MCP server communicates via **stdio**, so you can configure any
MCP‑compatible AI agent (for example, Claude Desktop / Claude Server or
another MCP‑aware system) to run the command:

```bash
python /Users/duypt/Documents/Coding/gold-price-mcp/mcp_server.py
```

and register the tool `fetch_gia_vang_giao_thuy`.

When the agent calls this tool, it will receive **Vietnamese** text that includes:

- the article/page title
- the **“Giá vàng Hiệp hội vàng bạc Giao Thủy Hải Hậu”** table
- the **“Giá vàng SJC”** table
- any “last updated” note found in the HTML (also in Vietnamese)
- a short suggestion for the AI to **answer the user in Vietnamese**.

AI agents can then use this Vietnamese content directly to explain or compare
gold prices for end users without needing additional translation.

### Example MCP configuration (Claude Desktop)

Below is an example of how you might configure this server in a
`claude_desktop_config.json` (or similar MCP config file):

```json
{
  "mcpServers": {
    "gia-vang-giao-thuy": {
      "command": "python",
      "args": [
        "/Users/duypt/Documents/Coding/gold-price-mcp/mcp_server.py"
      ]
    }
  }
}
```

After this, restart Claude Desktop and you should see the MCP server
`gia-vang-giao-thuy` available, exposing the tool
`fetch_gia_vang_giao_thuy` for use in your chats.


