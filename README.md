# CalVer Creation
Creates a new version based on the current day's date (default of UTC but can specify timezone) and will auto increment the build metadata field (the # after the '+') to ensure that a tag is not overwritten by accident. Having this ability to create unique tags and easily readable allows for fast paced projects to create multiple tags a day, with no overlap, to help trigger other workflows or other items.

## Inputs
- prefix:
  - Allows for setting/reading a prefix, typically 'v', in front of the generated version. By default it is blank to somewhat follow [SemVer](https://semver.org/) standards.
- timezone:
  - Allows for the setting of a custom timezone, instead of the default UTC. Valid timezones are those defined by _pytz_ in Python, examples of such are _America/Chicago_, _Europe/Amsterdam_, _UTC_, etc.
- push_tag:
  - Allows for setting and pushing the generated tag to GitHub. If set to 'true' it requires that the github_token is set and has `contents:write` so it has permission to push.
- github_token
  - The token used for any `git` operations.

## Usage
### Create and push a new tag
```yaml
name: Create and push a new tag

on:
  workflow_dispatch:
permissions:
  contents: write # required for pushing tags

jobs:
  test:
    runs-on: ubuntu-latest
        
    steps:
      - name: Run local action
        uses: MicahWW/CalVer-Creation@v1
        with:
          prefix: 'v'
          timezone: 'America/Chicago'
          push_tag: true
          github_token: ${{ secrets.GITHUB_TOKEN }}
```
If you want to create a new version string and also set & push the tag on the commit that the workflow was run on you can use the above workflow setup.

#### Permissions
The workflow needs to have `contents: write` when trying to push the tag, without the write permissions the workflow would not be able to push the changes up.