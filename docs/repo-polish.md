# Repo Polish Notes

A useful automation repo should communicate value in the first 10 seconds.

## Minimum polish

1. Clear tagline
2. Problem statement
3. 30-second quickstart
4. Real commands
5. Safety model
6. License
7. Changelog
8. Roadmap

## Recommended GitHub topics

- openclaw
- ai-agent
- github-api
- automation
- developer-tools
- python

## Optional visual upgrade flow

When a repo is code-complete but visually plain, the agent should ask before creating media:

> “Repo is publish-ready. Do you want me to generate a banner/logo/screenshot package before release?”

Only create images after human approval. Suggested assets:

- `assets/banner.png` — README hero banner
- `assets/logo.png` — square social/avatar asset
- `assets/demo-terminal.png` — command output screenshot

## My Repo Library

`github-manager` keeps a local repo library at:

```text
~/.config/tt-github/repos.json
```

This library helps the agent remember which repos have been published, their topics, descriptions, and notes.
