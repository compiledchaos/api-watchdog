# 📡 API Watchdog

A Python tool that periodically monitors one or more public APIs (like weather, stocks, GitHub) and logs when their response changes.

## Features

- Fetch any JSON API on a schedule
- Compare and detect differences between responses
- Save change logs
- View changes via CLI (GUI coming soon)
- Installable as a package or CLI tool

## Example

```bash
api-watchdog --url https://api.github.com/repos/psf/requests/releases/latest