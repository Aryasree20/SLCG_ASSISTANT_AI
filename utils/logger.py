from datetime import datetime
from pathlib import Path

# Create logs folder automatically
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "agent.log"


def log_event(event, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = f"[{timestamp}] {event}: {details}"

    # Show in Terminal
    print(log_message)

    # Save to log file
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_message + "\n")