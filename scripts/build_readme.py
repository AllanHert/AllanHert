"""Renders README.md from profile.yaml.

    python scripts/build_readme.py                 # render
    python scripts/build_readme.py --check-links   # also hide live links that do not answer
                                                   # and case links whose repo is not public yet

Exit code 0 always; prints what it hid so the workflow log explains the diff.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (profile-readme link check; +https://github.com/AllanHert)"


def url_ok(url: str) -> bool:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status < 400:
                    return True
        except urllib.error.HTTPError as e:
            if e.code < 400:
                return True
        except Exception:
            pass
    return False


def repo_public(owner: str, repo: str) -> bool:
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return not json.load(r).get("private", True)
    except Exception:
        return False


class Links:
    """Decides which links survive. Without --check-links everything does."""

    def __init__(self, owner: str, check: bool):
        self.owner, self.check, self.hidden = owner, check, []

    def live(self, url: str | None) -> str | None:
        if not url:
            return None
        if self.check and not url_ok(url):
            self.hidden.append(f"live link down: {url}")
            return None
        return url

    def case(self, repo: str | None) -> str | None:
        if not repo:
            return None
        if self.check and not repo_public(self.owner, repo):
            self.hidden.append(f"case repo not public: {self.owner}/{repo}")
            return None
        return f"https://github.com/{self.owner}/{repo}"


def featured(items, links: Links) -> list[str]:
    out = []
    for it in items:
        live, case = links.live(it.get("live")), links.case(it.get("case"))
        target = live or case
        out.append(f"### {it['name']}\n")
        if it.get("image"):
            img = f'<img src="./{it["image"]}" alt="{it["name"]} preview" width="100%" />'
            out.append(f'<p>\n  <a href="{target}">{img}</a>\n</p>\n' if target else f"<p>\n  {img}\n</p>\n")
        out.append(it["text"].strip() + "\n")
        out.append(f"**Focus:** {it['focus']}  \n**Stack:** {it['stack']}\n")
        actions = []
        if live:
            actions.append(f'<a href="{live}"><strong>Live product →</strong></a>')
        if case:
            actions.append(f'<a href="{case}"><strong>Case study →</strong></a>')
        if actions:
            out.append(" &nbsp;·&nbsp; ".join(actions) + "\n")
        out.append("")
    return out


def icon_table(items, links: Links, case_key: str = "case") -> list[str]:
    rows = []
    for it in items:
        repo = it.get(case_key) or it["name"]
        href = links.case(repo) if case_key == "case" else f"https://github.com/{links.owner}/{repo}"
        name = f'<a href="{href}"><strong>{it["name"]}</strong></a>' if href else f"<strong>{it['name']}</strong>"
        rows.append(
            "  <tr>\n"
            f'    <td width="56" align="center"><img src="./{it["icon"]}" width="40" alt="" /></td>\n'
            f"    <td>{name}<br/>{it['text']}<br/><sub>{it['stack']}</sub></td>\n"
            "  </tr>"
        )
    return ["<table>", *rows, "</table>", ""]


def web_table(items, links: Links) -> list[str]:
    out = ["| Site | What it shows |", "|---|---|"]
    for it in items:
        url = links.live(it["url"])
        name = f"[{it['name']}]({url})" if url else it["name"]
        out.append(f"| {name} | {it['text']} |")
    return out + [""]


def render(p: dict, links: Links) -> str:
    out = [
        "<!-- Generated from profile.yaml by scripts/build_readme.py. Edit profile.yaml, not this file. -->",
        "",
        f'<img src="./{p["banner"]}" alt="{p["banner_alt"]}" width="100%" />',
        "",
        '<p align="center">',
        "  " + "\n  ·\n  ".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in p["links"]),
        "</p>",
        "",
        "## About",
        "",
        p["about"].strip(),
        "",
        "---",
        "",
        "## Selected products",
        "",
        *featured(p["featured"], links),
        "---",
        "",
        f"## {p['systems']['title']}",
        "",
        *icon_table(p["systems"]["items"], links),
        f"## {p['web']['title']}",
        "",
        *web_table(p["web"]["items"], links),
        f"## {p['open_source']['title']}",
        "",
        *icon_table(p["open_source"]["items"], links, case_key="repo"),
        "---",
        "",
        "## Toolkit",
        "",
        "<p>",
        f'  <img src="https://skillicons.dev/icons?i={p["toolkit"]["icons"]}&theme=dark" alt="Main technologies" />',
        "</p>",
        "",
        *[line + "  " for line in p["toolkit"]["lines"]],
        "",
        "## How I work",
        "",
        *[f"- {line}" for line in p["how_i_work"]],
        "",
        "---",
        "",
        f"<sub>{p['footer']}</sub>",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-links", action="store_true")
    args = ap.parse_args()
    profile = yaml.safe_load((ROOT / "profile.yaml").read_text(encoding="utf-8"))
    links = Links(profile["owner"], args.check_links)
    text = render(profile, links)
    if "—" in text or "–" in text:
        print("error: em/en dash in the rendered README; fix profile.yaml", file=sys.stderr)
        return 1
    (ROOT / "README.md").write_text(text, encoding="utf-8", newline="\n")
    for h in links.hidden:
        print("hidden:", h)
    print("README.md written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
