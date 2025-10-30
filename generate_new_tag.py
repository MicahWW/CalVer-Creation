import re
from datetime import datetime
import pytz
import os
import subprocess


def get_latest_tag():
    # requires to be run in Linux
    cmd = "git tag --list --sort=-committerdate | sort -V | tail -n 1"

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True, check=True)
    return result.stdout.strip()


def main():
    timezone = os.getenv('INPUT_TIMEZONE')

    # region Checks
    # TZ check should've already been run via pre_check.py
    # But running redundant checks to ensure
    if (not timezone):
        print('::error::Default timezone not set via actions.yml')
        exit(1)

    try:
        pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        print(f'::error::Unknown timezone: {timezone}')
        exit(1)
    # endregion

    today = datetime.now(pytz.timezone(timezone)).strftime("%Y.%m.%d")
    latest_tag = get_latest_tag()

    # Check if latest tag matches today's date
    pattern = re.compile(rf"^{today}\+(\d+)$")
    match = pattern.match(latest_tag)

    if match:
        next_build = int(match.group(1)) + 1
        print("matched")
    else:
        next_build = 0
        print("not matched")

    new_version = f"{today}+{next_build}"
    print(f"::set-output name=new_version::{new_version}")


if __name__ == "__main__":
    main()
