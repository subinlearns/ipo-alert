import json
import requests
import os

NTFY_URL = os.environ["NTFY_URL"]

API_URL = 'https://nepalipaisa.com/api/GetIpos?stockSymbol=&pageNo=1&itemsPerPage=30&pagePerDisplay=5'
STATE_FILE = "state.json"

def get_data():
    try:
        res = requests.get(API_URL, timeout=10)
        res.raise_for_status()
        return res.json()["result"]["data"]
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Failed to fetch IPO data: {e}")
        return None

def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file, indent=2)

def load_state():
    try:
        with open(STATE_FILE) as file:
            content = file.read().strip()
            if not content:
                return {"seen":[]}
            return json.load(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"seen":[]}

def send_notification(ipos):
    if not ipos:
        return

    message = "🚨 New IPO opened:\n" + "\n".join(ipos)
    try:
        response = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Notification failed: {e}")
        return False

def main():
    data = get_data()
    if data is None:
        return

    current_ipos = [
        ipo["companyName"]
        for ipo in data
        if ipo.get("companyName")
    ]

    state = load_state()
    seen = set(state["seen"])

    new_ipos = [
        ipo for ipo in current_ipos
        if ipo not in seen
    ]

    if new_ipos:
        print("New IPOs:")
        print("\n".join(new_ipos))
        if send_notification(new_ipos):
            state["seen"] = current_ipos
            save_state(state)
        else:
            print("Keeping old state because notification failed.")
    else:
        print("No new IPOs.")
        state["seen"] = current_ipos
        save_state(state)

if __name__ == "__main__":
    main()
