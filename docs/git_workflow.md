# Git Workflow

## Basic commands

The command git init creates a repository. The command git add stages changes and git commit saves them as a snapshot with a message. The command git status shows changed files and git log shows the history. The command git push sends commits to a remote repository such as GitHub, and git pull downloads and merges new commits.

## Branches

A branch is a separate line of development. The main branch holds the stable version. A new feature is developed on its own branch, for example feature/login, created with git checkout -b feature/login. When the work is finished, the branch is merged into main.

## Pull requests

A pull request asks the team to review and merge a branch. Reviewers comment on the code, and the branch is merged after approval. Small pull requests are easier to review than large ones.

## Commit messages

A good commit message is short and describes what changed, for example "add login endpoint". One commit should contain one logical change.

## The .gitignore file

The file .gitignore lists files that Git must not track: dependencies such as node_modules, virtual environments, build output, and secrets such as .env files. Secrets committed by mistake stay in the history even after deletion, so the key must be replaced.
