#!/usr/bin/env python3
"""
Sync GitHub repositories for codefl0w into _data/projects.yml.
Usage:
    python scripts/sync_repos.py [--dry-run]
"""

import sys
import os
import json
import urllib.request
import yaml

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "projects.yml")
GITHUB_API = "https://api.github.com/users/codefl0w/repos?per_page=100"
IGNORED_REPOS = {"codefl0w", "codefl0w.github.io"}


def fetch_github_repos():
    headers = {"User-Agent": "codefl0w-site-updater", "Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(GITHUB_API, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_current_projects():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data if isinstance(data, list) else []


def main():
    dry_run = "--dry-run" in sys.argv
    print(f"Fetching public repositories for user 'codefl0w'...")
    repos = fetch_github_repos()

    current_projects = load_current_projects()
    projects_by_name = {p["name"].lower(): p for p in current_projects}

    updated_count = 0
    added_count = 0

    for r in repos:
        name = r.get("name")
        if not name or r.get("fork") or name in IGNORED_REPOS:
            continue

        stars = r.get("stargazers_count", 0)
        language = r.get("language") or "Other"
        gh_url = r.get("html_url")
        topics = r.get("topics", [])
        gh_desc = r.get("description") or ""

        existing = projects_by_name.get(name.lower())
        if existing:
            # Update live stats
            if existing.get("stars") != stars:
                existing["stars"] = stars
                updated_count += 1
            if not existing.get("github"):
                existing["github"] = gh_url
            if not existing.get("language") and language != "Other":
                existing["language"] = language
        else:
            # New repo discovered
            slug = name.lower().replace("_", "-")
            new_item = {
                "name": name,
                "slug": slug,
                "description": gh_desc or f"Tool by codefl0w ({name}).",
                "language": language,
                "stars": stars,
                "category": "Android Tools" if "android" in topics or "android" in name.lower() else "Automation",
                "featured": False,
                "github": gh_url,
                "page": f"/archive/projects/{slug}.html",
                "demo": r.get("homepage") or "",
                "topics": topics,
            }
            current_projects.append(new_item)
            projects_by_name[name.lower()] = new_item
            added_count += 1
            print(f"  + Discovered new project: {name}")

    if dry_run:
        print(f"[Dry Run] Would update {updated_count} projects and add {added_count} projects.")
        return

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        yaml.dump(current_projects, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"Successfully synced _data/projects.yml! Updated stats for {updated_count} projects, added {added_count} new.")


if __name__ == "__main__":
    main()
