#!/bin/bash

latest_tag=$(git tag --list --merged HEAD --sort=-committerdate | sort -V | tail -n 1)
echo "Latest tag: $latest_tag"
echo "$GITHUB_OUTPUT"
