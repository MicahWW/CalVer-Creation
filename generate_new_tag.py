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
    prefix = os.getenv('INPUT_PREFIX', '')
    set_build_metadata = os.getenv('INPUT_SET_BUILD_METADATA')

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

    if (not set_build_metadata):
        print('::error::Default set_build_metadata not set via actions.yml')
        exit(1)

    if (set_build_metadata not in ['true', 'false']):
        print(f'::error::Unexpected input for set_build_metadata of "{set_build_metadata}"')
        exit(1)
    # endregion

    today = datetime.now(pytz.timezone(timezone)).strftime("%Y.%m.%d")
    latest_tag = get_latest_tag()

    # if set_build_metadata find & generate a tag with metadata appended
    if (set_build_metadata == 'true'):
        # Check if latest tag matches today's date and with the given prefix
        pattern = re.compile(rf"^{prefix}{today}\+(\d+)$")
        match = pattern.match(latest_tag)

        if match:
            next_build = int(match.group(1)) + 1
        else:
            next_build = 0

        new_version = f"{prefix}{today}+{next_build}"
    # if not set_build_metadata don't find & generate a tag with metadata 
    else:
        # Check if latest tag matches today's date and with the given prefix
        pattern = re.compile(rf"^{prefix}{today}$")
        match = pattern.match(latest_tag)

        # if it matches then the tag exists and shouldn't be overwritten
        if match:
            print(f"::error::Tag {latest_tag} already exists.")
            exit(1)
        # if it doesn't match then it is good to create a new tag
        else:
            new_version = today

    # display and output new version
    print(f'new_version: {new_version}')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_output:
        gh_output.write(f'new_version={new_version}')


if __name__ == "__main__":
    print("::group::Generate tag")
    main()
    print("::endgroup::")
