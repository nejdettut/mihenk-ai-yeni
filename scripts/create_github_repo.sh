#!/usr/bin/env bash
# Usage: ./scripts/create_github_repo.sh <owner/repo> "repo description"
if [ -z "$1" ]; then
  echo "Usage: $0 owner/repo \"description\""
  exit 1
fi
REPO=$1
DESC=$2
# Requires GitHub CLI (gh)
gh repo create "$REPO" --public --description "$DESC" --source=. --remote=origin --push
echo "Created and pushed to https://github.com/$REPO"
