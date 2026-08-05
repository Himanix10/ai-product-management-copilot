from pathlib import Path

path = Path("requirements.txt")
text = path.read_text(encoding="utf-16")
if "openpyxl" not in text:
    if not text.endswith("\n"):
        text += "\r\n"
    text += "openpyxl\r\n"
    path.write_text(text, encoding="utf-16")
    print("added openpyxl")
else:
    print("openpyxl already present")
