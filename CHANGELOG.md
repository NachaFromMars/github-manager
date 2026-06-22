# Changelog

## v1.1.0 — Auto repo polish
- Added one-shot `publish` (ensure repo -> push via Contents API -> set description -> set topics -> optional release).
- Added `set-topics` and `set-meta` for discoverability.
- Push uses the REST Contents API (robust vs restricted git-over-HTTPS auth).
- Professional README: hero, why, features, quickstart, commands, safety model, workflows, install, roadmap.


## v0.2.0 — 2026-06-22

### Added
- `update-repo` command for description, homepage, topics, and library sync.
- My Repo Library commands: `library-list`, `library-add`, `library-remove`.
- Automatic library save after `create-repo`, `push`, and `update-repo`.
- Optional visual polish workflow: ask before generating banner/logo/screenshot assets.

## v0.1.0 — 2026-06-22

### Added
- First public-ready packaging for `github-manager`.
- Premium README with quickstart, workflows, safety model, and roadmap.
- Security notes and repository polish metadata.

### Existing core features
- Account verification via `whoami`.
- Repository listing, creation, and inspection.
- Folder push with optional repo creation.
- Issue creation/listing.
- Release creation.
- Guarded repository deletion.
