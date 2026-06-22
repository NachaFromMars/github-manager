# Changelog

## v0.2.3 — 2026-06-22

### Fixed
- `publish` now explicitly saves the repo into My Repo Library after successful publish metadata sync.

## v0.2.2 — 2026-06-22

### Changed
- `push` now defaults to Contents API via `--method api`.
- Legacy git-over-HTTPS push is explicitly gated behind `--method git` and warns about token exposure risk.
- README now recommends `publish` as the normal polished shipping path.
- `repo-info` now syncs successful lookups into My Repo Library.

### Added
- `docs/library.md` for My Repo Library behavior.
- `docs/metadata.md` for public metadata vs local-only notes.
- SKILL.md command docs for `update-repo` and library commands.
- Clear docs that `--note` is local-only and never public on GitHub.

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
