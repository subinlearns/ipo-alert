# IPO Alert

A simple Python-based IPO monitoring tool for Nepal.

The script periodically fetches IPO information from [Nepali Paisa](https://nepalipaisa.com/), compares it with previously seen IPOs, and sends a mobile notification through **ntfy** whenever a new IPO opening is detected.

## How It Works

```text
Nepali Paisa API
       ↓
Fetch current IPOs
       ↓
Compare with previous state
       ↓
New IPO detected?
       ↓
   Yes → Send ntfy notification 📱
       ↓
Update state
```

The project is designed to run automatically using **GitHub Actions**, so no VPS or separate server is required.

## Features

* Fetches IPO data from Nepali Paisa
* Detects newly added IPOs
* Sends instant mobile notifications using ntfy
* Stores previous IPO state in `state.json`
* Runs automatically using GitHub Actions
* Can also be triggered manually from GitHub Actions

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/subinlearns/ipo-alert.git
cd ipo-alert
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up ntfy

This project uses **ntfy** to send notifications to your phone.

You need to set up ntfy yourself:

1. Install the ntfy app on your phone.
2. Choose a topic name that is unique to you.
3. Subscribe to that topic in the ntfy app. (Its free)
4. Use the same topic URL for this project.

Learn more about ntfy at https://ntfy.sh/

> **Note:** Keep your ntfy topic private. Anyone who knows the topic name may be able to publish notifications to it.

### 4. Configure GitHub Secret

If you're running the project through GitHub Actions, add your ntfy URL as a repository secret.

Go to:

**Repository → Settings → Secrets and variables → Actions → New repository secret**

Create:

```text
Name: NTFY_URL
Value: https://ntfy.sh/your-topic
```

The workflow passes this secret to the Python script as an environment variable.

## Running Locally

Set the environment variable:

```bash
export NTFY_URL="https://ntfy.sh/your-topic"
```

Then run:

```bash
python main.py
```

## GitHub Actions

The project can run automatically using GitHub Actions.

The workflow can be configured to run periodically, for example:

```yaml
on:
  schedule:
    - cron: "0 6,18 * * *"

  workflow_dispatch:
```

This runs the monitor approximately twice a day.

You can also manually trigger it from:

**GitHub → Actions → IPO Monitor → Run workflow**

## State Management

The project uses `state.json` to remember previously seen IPOs.

Example:

```json
{
  "seen": [
    "Company A",
    "Company B",
    "Company C"
  ]
}
```

When the script runs, it compares the current IPO list with this stored state.

If a new IPO is found:

```text
Current IPOs
     ↓
Compare with state.json
     ↓
New IPO found
     ↓
Send notification
     ↓
Update state.json
```

GitHub Actions commits the updated `state.json` back to the repository, allowing the state to persist between workflow runs.

## Disclaimer

This project is for personal use and educational purposes. IPO information is fetched from a third-party source, so the data may occasionally be delayed, changed, or unavailable.

Always verify IPO information from official sources before making investment decisions.

## License

MIT
