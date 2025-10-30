#!/bin/bash

latest_tag=$(git tag --sort=-creatordate | head -n 1)
echo "Latest tag: $latest_tag"
echo "$GITHUB_OUTPUT"
