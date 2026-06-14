from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")
html = html.replace(">ソース1欄</button>", ">View source</button>")
html = html.replace("<h2>ソース1欄</h2>", "<h2>View source</h2>")
path.write_text(html, encoding="utf-8")
