# CalVer Creation
Creates a new version based on the current day's date (default of UTC but can specify timezone) and will auto increment the build metadata field (the # after the '+') to ensure that a tag is not overwritten by accident. Having this ability to create unique tags and easily readable allows for fast paced projects to create multiple tags a day, with no overlap, to help trigger other workflows or other items.

## Inputs
- prefix:
  - Allows for setting/reading a prefix, typically 'v', in front of the generated version. By default it is blank to somewhat follow [SemVer](https://semver.org/) standards.
- timezone:
  - Allows for the setting of a custom timezone, instead of the default UTC. Valid timezones are those defined by _pytz_ in Python, examples of such are _America/Chicago_, _Europe/Amsterdam_, _UTC_, etc.
- push_tag:
  - Allows for setting and pushing the generated tag to GitHub. If set to 'true' it requires that the github_token is set and has `contents:write` so it has permission to push.
- publish_release:
  - Allows for the publishing of a new GitHub release. If set to 'true' it requires that push_tag is set to true and github_token is set and has `contents:write` so it can publish.
- github_token:
  - The token used for any `git` operations.
- set_build_metadata:
  - Toggles the feature of appending build metadata to the end of the version. If this is set to 'false' after the first run for a calendar day, all subsequent runs will fail as it would attempt to create/overwrite a tag that was created on the first run.

## Workflow permissions
Both pushing a new tag and publishing a new release require the `contents: write` permission to be set. You can see an example of how this is set at the [Create and push a new tag usage example](#create-and-push-a-new-tag).

## Usage
### Create and push a new tag
Use this example workflow if you want to:
1. generate a new version string
1. tag the commit the workflow was run on then push that tag to GitHub

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
      - name: Create and push tag
        uses: MicahWW/CalVer-Creation@v1
        with:
          prefix: 'v'
          timezone: 'America/Chicago'
          push_tag: 'true'
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Create and push a new tag _without build metadata_
Use this example workflow if you want to:
1. generate a new version string _without build metadata_
1. tag the commit the workflow was run on then push that tag to GitHub

```yaml
name: Create and push a new tag without build metadata

on:
  workflow_dispatch:
permissions:
  contents: write # required for pushing tags

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Create and push tag
        uses: MicahWW/CalVer-Creation@v1
        with:
          set_build_metadata: 'false'
          prefix: 'v'
          timezone: 'America/Chicago'
          push_tag: 'true'
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Publish a new release & tag
Use this example workflow if you want to:
1. generate a new version string
1. tag the commit the workflow was run on then push that tag to GitHub
1. generate a release based on the new tag pushed

```yaml
name: Publish a new release & tag

on:
  workflow_dispatch:
permissions:
  contents: write # required for pushing tags & publishing releases

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Publish release and tag
        uses: MicahWW/CalVer-Creation@v1
        with:
          prefix: 'v'
          timezone: 'America/Chicago'
          push_tag: 'true'
          publish_release: 'true'
          github_token: ${{ secrets.GITHUB_TOKEN }}
```
