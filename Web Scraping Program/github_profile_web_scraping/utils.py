import json


def save_mock_data(data, filename="mock_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_mock_data(filename="mock_data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
