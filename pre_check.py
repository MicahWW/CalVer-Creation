import os
import pytz

timezone = os.getenv('INPUT_TIMEZONE')
push_tag = os.getenv('INPUT_PUSH_TAG')
github_token = os.getenv('INPUT_GITHUB_TOKEN')

# region Check values are set
if (not timezone):
    print('::error::Default timezone not set via actions.yml')
    exit(1)

if (not push_tag):
    print('::error::Default push_tag not set via actions.yml')
    exit(1)
# endregion

# region Check timezone
try:
    pytz.timezone(timezone)
except pytz.UnknownTimeZoneError:
    print(f'::error::Unknown timezone: {timezone}')
    exit(1)
# endregion

# region Check github_token
if (push_tag not in ['true', 'false']):
    print(f'::error::Unexpected input for push_tag of "{push_tag}"')
    exit(1)

if (not push_tag and push_tag == 'true'):
    if (not github_token or not github_token.strip()):
        print('::error::github_token is required ')
        exit(1)
# endregion
