import json
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).parent
FIELDS = ["inventory_number", "name", "status"]

class EquipmentTableParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.rows = []
        self._in_td = False
        self._row = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag == "td" and self._row is not None:
            self._in_td = True
            self._row.append("")

    def handle_endtag(self, tag):
        if tag == "td":
            self._in_td = False
        elif tag == "tr":
            if self._row:
                self.rows.append([c.strip() for c in self._row])
            self._row = None

    def handle_data(self, data):
        if self._in_td:
            self._row[-1] += data

def parse_equipment(html: str) -> list[dict]:
    parser = EquipmentTableParser()
    parser.feed(html)
    return [dict(zip(FIELDS, row)) for row in parser.rows if len(row) == len(FIELDS)]

def main():
    html = (BASE / "equipment.html").read_text(encoding="utf-8")
    items = parse_equipment(html)
    out = BASE / "parsed_equipment.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Извлечено записей: {len(items)} -> {out.name}")

if __name__ == "__main__":
    main()
