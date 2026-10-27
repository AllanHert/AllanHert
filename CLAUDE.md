# AllanHert (profile repository)

Public GitHub profile of Allan Hert, written for recruiters hiring remote full-stack / AI engineers. English only.

## How it works

- `profile.yaml` is the source. `README.md` is generated: never edit it by hand.
- `python scripts/build_readme.py` renders it (`--check-links` hides live links that are down and case-study links whose repo is not public).
- `.github/workflows/refresh.yml` runs every Monday and on changes to `profile.yaml`; when the README changes it opens a PR, never pushes to `main`.
- `repos.yaml` + `scripts/polish_repos.py`: profile bio and metadata of the public repos. With `--portfolio <vault>/02-projetos/_portfolio.yaml` it also fills description and site of the private repos on the Hertwave account (empty descriptions only, unless `--overwrite`). Dry run by default; `--apply` writes. Run with `uv run --with ruamel.yaml python scripts/polish_repos.py ...`.
- `scripts/render_banner.ps1` re-renders `assets/banner.png` from `assets/src/banner.html` (same look as allanhert.com: #05070c, #36dede, Geist).
- Case studies live in their own public repos on this account , with no source code.

## Never

- No em dash or en dash as punctuation (the build fails on them).
- No private repo names, client personal data, paths of the PC or numbers without a source.
- Nothing goes public (new repo, visibility change, push to main) without Allan's ok in the moment.
