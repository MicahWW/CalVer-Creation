"""
pre_check.py

This module performs a set of early runtime validations for a GitHub Action that
relies on environment inputs. It ensures required environment variables are
present, and validates the given values as allowed. When a validation fails, the
module writes an error message to stdout in the GitHub Actions error format and
exits the process with a non-zero status.

Behavior and checks performed:
- Validates that INPUT_TIMEZONE corresponds to a known pytz timezone.
- Validates that INPUT_PUSH_TAG is either "true" or "false".
- Validates that INPUT_PUBLISH_RELEASE is either "true" or "false".
- If pushing tags is requested (INPUT_PUSH_TAG == 'true'), verifies that
  INPUT_GITHUB_TOKEN is present and non-empty.
- If publishing a release is request (INPUT_PUBLISH_RELEASE == 'true'), verifies
  that INPUT_PUSH_TAG is set to true.

Exit behavior:
- On any validation failure, the module prints an error line prefixed with
  "::error::" (so it surfaces in GitHub Actions logs) and exits the process with
  exit code 1.

Notes on redundancy:
- Some of the checks here may appear redundant with checks performed elsewhere
  They are intentionally duplicated here to provide a single, early, and
  explicit fail-fast validation. Primary this is for when in some parts
  validation is not as easy to do.

Usage:
- This module is intended to be executed at process start to fail fast on bad
  inputs. No return value is provided; successful completion simply means the
  checks passed and the program may continue.
"""
import os
import pytz


def main():
    timezone = os.getenv('INPUT_TIMEZONE')
    push_tag = os.getenv('INPUT_PUSH_TAG')
    github_token = os.getenv('INPUT_GITHUB_TOKEN')
    publish_release = os.getenv('INPUT_PUBLISH_RELEASE')

    # region Check values are set
    if (not timezone):
        print('::error::Default timezone not set via actions.yml')
        exit(1)

    if (not push_tag):
        print('::error::Default push_tag not set via actions.yml')
        exit(1)

    if (not publish_release):
        print('::error::Default publish_release not set via actions.yml')
        exit(1)

    # endregion

    # region Check timezone
    try:
        pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        print(f'::error::Unknown timezone: {timezone}')
        exit(1)
    # endregion

    # region Check input allowed values
    if (push_tag not in ['true', 'false']):
        print(f'::error::Unexpected input for push_tag of "{push_tag}"')
        exit(1)

    if (publish_release not in ['true', 'false']):
        print(f'::error::Unexpected input for publish_release of "{publish_release}"')
        exit(1)

    # endregion

    # region Check github token
    if (not push_tag and push_tag == 'true'):
        if (not github_token or not github_token.strip()):
            print('::error::github_token is required ')
            exit(1)
    # endregion

if __name__ == "__main__":
    print("::group::Pre Checks")
    main()
    print("::endgroup::")
