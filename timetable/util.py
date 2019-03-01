import json
import pathlib

this = pathlib.Path(__file__).parent


def save_json(data, filename, package_data=True):
    data = json.dumps(data, indent=2, ensure_ascii=False)
    (this / filename).parent.mkdir(parents=True, exist_ok=True)
    return (this / filename).write_text(data, encoding='utf-8')


def load_json(filename, package_data=False) -> dict:
    if package_data:
        filename = this / filename
    filepath = pathlib.Path(filename)
    if not filepath.exists():
        data = {}
    text = filepath.read_text(encoding='utf-8')
    data = json.loads(text)
    return data
