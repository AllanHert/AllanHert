"""Keeps GitHub metadata (profile, descriptions, topics, sites) in line with the manifests.

    uv run --with ruamel.yaml python scripts/polish_repos.py                       # dry run, public account
    uv run --with ruamel.yaml python scripts/polish_repos.py --portfolio PATH      # + private repos from the registry
    uv run --with ruamel.yaml python scripts/polish_repos.py ... --apply           # write

Each account is used through its own gh login (`gh auth token --user LOGIN`), so the active gh account does
not matter. Nothing is created, deleted or made public here: only metadata of repos that already exist.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent
PRIVATE_OWNER = "Hertwave"


def load(path: Path):
    return YAML(typ="safe").load(path.read_text(encoding="utf-8"))


class Gh:
    def __init__(self, login: str):
        r = subprocess.run(["gh", "auth", "token", "--user", login], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"gh has no login for {login}. Run: gh auth login (and pick {login})")
        self.env = {**os.environ, "GH_TOKEN": r.stdout.strip()}

    def api(self, *args: str, body: dict | None = None):
        cmd = ["gh", "api", *args]
        if body is not None:
            cmd += ["--input", "-"]
        r = subprocess.run(cmd, input=json.dumps(body) if body is not None else None,
                           capture_output=True, text=True, env=self.env, encoding="utf-8")
        if r.returncode != 0:
            raise RuntimeError(f"gh api {' '.join(args)}: {r.stderr.strip()}")
        return json.loads(r.stdout) if r.stdout.strip() else None


def diff(current: dict, wanted: dict) -> dict:
    return {k: v for k, v in wanted.items() if current.get(k) != v}


def show(label: str, changes: dict, current: dict):
    for k, v in changes.items():
        print(f"  {label}.{k}: {current.get(k)!r} -> {v!r}")


def polish_public(manifest: dict, apply: bool) -> int:
    acct = manifest["account"]
    owner = acct["login"]
    gh = Gh(owner)
    n = 0

    me = gh.api("user")
    wanted = {k: v for k, v in acct.items() if k != "login"}
    changes = diff(me, wanted)
    print(f"[{owner}] profile: {len(changes)} change(s)")
    show("profile", changes, me)
    if changes and apply:
        gh.api("-X", "PATCH", "user", body=changes)
    n += len(changes)

    for name, spec in manifest["repos"].items():
        try:
            repo = gh.api(f"repos/{owner}/{name}")
        except RuntimeError:
            print(f"[{owner}/{name}] not on GitHub yet, skipped")
            continue
        if repo.get("archived") and spec.get("archived"):
            print(f"[{owner}/{name}] archived, left as is")
            continue
        wanted = {k: spec[k] for k in ("description", "homepage", "archived") if k in spec}
        if spec.get("case"):
            wanted.update(manifest.get("case_defaults", {}))
        changes = diff(repo, wanted)
        topics = sorted(spec.get("topics", []))
        topics_change = topics and sorted(repo.get("topics", [])) != topics
        print(f"[{owner}/{name}] {len(changes) + bool(topics_change)} change(s)")
        show(name, changes, repo)
        if topics_change:
            print(f"  {name}.topics: {sorted(repo.get('topics', []))} -> {topics}")
        if apply and changes:
            gh.api("-X", "PATCH", f"repos/{owner}/{name}", body=changes)
        if apply and topics_change:
            gh.api("-X", "PUT", f"repos/{owner}/{name}/topics", body={"names": topics})
        n += len(changes) + bool(topics_change)
    return n


def pick_projects(projects: list[dict]) -> dict[str, dict]:
    """One registry project per repo. Several projects can live in one repo (the jarvis repo holds the voice
    assistant, the remote control and a routine); the one whose slug is the repo name wins, else the repo is
    skipped rather than guessed."""
    by_repo: dict[str, list[dict]] = {}
    for p in projects:
        full = p.get("github") or ""
        if full.startswith(f"{PRIVATE_OWNER}/"):
            by_repo.setdefault(full, []).append(p)
    chosen = {}
    for full, ps in by_repo.items():
        name = full.split("/", 1)[1]
        match = [p for p in ps if p.get("slug") == name]
        if len(ps) == 1 or match:
            chosen[full] = (match or ps)[0]
        else:
            print(f"[{full}] {len(ps)} projects share it ({', '.join(p['slug'] for p in ps)}), skipped")
    return chosen


def polish_private(portfolio: Path, apply: bool, overwrite: bool) -> int:
    """Private repos: description = registry summary (only when empty, unless overwrite), homepage = live URL."""
    gh = Gh(PRIVATE_OWNER)
    n = 0
    for full, p in pick_projects(load(portfolio)["projetos"]).items():
        name = full.split("/", 1)[1]
        try:
            repo = gh.api(f"repos/{full}")
        except RuntimeError:
            print(f"[{full}] not found, skipped")
            continue
        if not repo["private"]:
            print(f"[{full}] is public, left to repos.yaml")
            continue
        wanted = {}
        if overwrite or not repo.get("description"):
            wanted["description"] = (p.get("resumo") or "").strip()[:350]
        if p.get("url") and p.get("status") == "no-ar":
            wanted["homepage"] = p["url"]
        changes = diff(repo, wanted)
        if changes:
            print(f"[{full}] {len(changes)} change(s)")
            show(name, changes, repo)
            if apply:
                gh.api("-X", "PATCH", f"repos/{full}", body=changes)
        n += len(changes)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the changes (default is a dry run)")
    ap.add_argument("--portfolio", type=Path, help="local project registry (_portfolio.yaml) for private repos")
    ap.add_argument("--overwrite", action="store_true", help="replace private descriptions that already exist")
    ap.add_argument("--skip-public", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    total = 0
    if not args.skip_public:
        total += polish_public(load(ROOT / "repos.yaml"), args.apply)
    if args.portfolio:
        total += polish_private(args.portfolio, args.apply, args.overwrite)
    print(f"{total} change(s) {'applied' if args.apply else 'pending (dry run, use --apply)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
