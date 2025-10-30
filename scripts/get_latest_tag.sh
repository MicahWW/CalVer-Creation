#!/bin/bash

latest_tag=$(git describe --tags --abbrev=0)
echo "Latest tag: $latest_tag"