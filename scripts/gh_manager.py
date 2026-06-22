#!/usr/bin/env python3
"""GitHub Manager — manage GitHub repos via REST API (no gh CLI needed).

Token resolution order:
  1. env GH_TOKEN / GITHUB_TOKEN
  2. file ~/.config/tt-github/env  (KEY=VALUE lines: GH_TOKEN=..., GITHUB_USER=...)

Never prints the token. Designed for an agent to manage many repos safely.

Subcommands:
  whoami
  list-repos [--limit N]
  create-repo --name N [--desc D] [--private]
  push --path DIR --repo OWNER/NAME [--branch main] [--message MSG] [--create] [--desc D] [--private]
  repo-info --repo OWNER/NAME
  create-issue --repo OWNER/NAME --title T [--body B]
  list-issues --repo OWNER/NAME [--state open|closed|all]
  create-release --repo OWNER/NAME --tag vX --name N [--notes ..]
  delete-repo --repo OWNER/NAME --confirm OWNER/NAME   (guarded)
"""
import argparse, json, os, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

API = "https://api.github.com"
ENV_FILE = Path.home() / ".config" / "tt-github" / "env"


def load_env():
    data = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                data[k.strip()] = v.strip()
    return data


def get_token():
    t = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if t:
        return t
    return load_env().get("GH_TOKEN") or load_env().get("GITHUB_TOKEN")


def get_user():
    return os.environ.get("GITHUB_USER") or load_env().get("GITHUB_USER")


def api(method, path, token, body=None):
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "tt-github-manager")
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            txt = r.read().decode()
            return r.status, (json.loads(txt) if txt else {})
    except urllib.error.HTTPError as e:
        txt = e.read().decode()
        try:
            return e.code, json.loads(txt)
        except Exception:  # noqa
            return e.code, {"message": txt}


def out(o):
    print(json.dumps(o, indent=2, ensure_ascii=False))


def cmd_whoami(a, t):
    s, d = api("GET", "/user", t)
    out({"status": s, "login": d.get("login"), "name": d.get("name"), "public_repos": d.get("public_repos")})


def cmd_list_repos(a, t):
    s, d = api("GET", f"/user/repos?per_page={a.limit}&sort=updated", t)
    if isinstance(d, list):
        out([{"full_name": r["full_name"], "private": r["private"], "url": r["html_url"]} for r in d])
    else:
        out({"status": s, "error": d})


def cmd_create_repo(a, t):
    s, d = api("POST", "/user/repos", t, {
        "name": a.name, "description": a.desc or "", "private": bool(a.private), "has_issues": True})
    out({"status": s, "full_name": d.get("full_name"), "url": d.get("html_url"), "error": d.get("message")})


def cmd_repo_info(a, t):
    s, d = api("GET", f"/repos/{a.repo}", t)
    out({"status": s, "full_name": d.get("full_name"), "url": d.get("html_url"),
         "default_branch": d.get("default_branch"), "stars": d.get("stargazers_count"),
         "open_issues": d.get("open_issues_count"), "error": d.get("message")})


def cmd_push(a, t):
    owner_repo = a.repo
    if a.create:
        name = owner_repo.split("/")[-1]
        api("POST", "/user/repos", t, {"name": name, "description": a.desc or "",
                                       "private": bool(a.private), "has_issues": True})
    token = t
    remote = f"https://x-access-token:{token}@github.com/{owner_repo}.git"
    path = a.path
    cmds = [
        ["git", "-C", path, "init", "-q"],
        ["git", "-C", path, "add", "-A"],
        ["git", "-C", path, "-c", "user.email=tieutam@sendclaw.com", "-c", "user.name=Tieu Tam",
         "commit", "-qm", a.message or "update"],
        ["git", "-C", path, "branch", "-M", a.branch],
    ]
    for c in cmds:
        subprocess.run(c, capture_output=True, text=True)
    subprocess.run(["git", "-C", path, "remote", "remove", "origin"], capture_output=True, text=True)
    subprocess.run(["git", "-C", path, "remote", "add", "origin", remote], capture_output=True, text=True)
    p = subprocess.run(["git", "-C", path, "push", "-u", "origin", a.branch],
                       capture_output=True, text=True)
    # scrub token from remote
    subprocess.run(["git", "-C", path, "remote", "set-url", "origin",
                    f"https://github.com/{owner_repo}.git"], capture_output=True, text=True)
    ok = p.returncode == 0
    out({"pushed": ok, "repo": owner_repo, "branch": a.branch,
         "detail": (p.stderr or p.stdout).strip().splitlines()[-3:] if not ok else "ok"})


def cmd_create_issue(a, t):
    s, d = api("POST", f"/repos/{a.repo}/issues", t, {"title": a.title, "body": a.body or ""})
    out({"status": s, "number": d.get("number"), "url": d.get("html_url"), "error": d.get("message")})


def cmd_list_issues(a, t):
    s, d = api("GET", f"/repos/{a.repo}/issues?state={a.state}&per_page=30", t)
    if isinstance(d, list):
        out([{"number": i["number"], "title": i["title"], "state": i["state"]} for i in d if "pull_request" not in i])
    else:
        out({"status": s, "error": d})


def cmd_create_release(a, t):
    s, d = api("POST", f"/repos/{a.repo}/releases", t,
               {"tag_name": a.tag, "name": a.name, "body": a.notes or ""})
    out({"status": s, "url": d.get("html_url"), "error": d.get("message")})


def cmd_delete_repo(a, t):
    if a.confirm != a.repo:
        out({"ok": False, "error": "confirm must equal --repo exactly"}); return
    s, d = api("DELETE", f"/repos/{a.repo}", t)
    out({"status": s, "deleted": s == 204, "error": d.get("message") if isinstance(d, dict) else None})


def main():
    p = argparse.ArgumentParser(prog="gh_manager")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami").set_defaults(fn=cmd_whoami)
    lr = sub.add_parser("list-repos"); lr.add_argument("--limit", type=int, default=30); lr.set_defaults(fn=cmd_list_repos)
    cr = sub.add_parser("create-repo"); cr.add_argument("--name", required=True); cr.add_argument("--desc", default=""); cr.add_argument("--private", action="store_true"); cr.set_defaults(fn=cmd_create_repo)
    ri = sub.add_parser("repo-info"); ri.add_argument("--repo", required=True); ri.set_defaults(fn=cmd_repo_info)
    pu = sub.add_parser("push"); pu.add_argument("--path", required=True); pu.add_argument("--repo", required=True); pu.add_argument("--branch", default="main"); pu.add_argument("--message", default="update"); pu.add_argument("--create", action="store_true"); pu.add_argument("--desc", default=""); pu.add_argument("--private", action="store_true"); pu.set_defaults(fn=cmd_push)
    ci = sub.add_parser("create-issue"); ci.add_argument("--repo", required=True); ci.add_argument("--title", required=True); ci.add_argument("--body", default=""); ci.set_defaults(fn=cmd_create_issue)
    li = sub.add_parser("list-issues"); li.add_argument("--repo", required=True); li.add_argument("--state", default="open", choices=["open", "closed", "all"]); li.set_defaults(fn=cmd_list_issues)
    rel = sub.add_parser("create-release"); rel.add_argument("--repo", required=True); rel.add_argument("--tag", required=True); rel.add_argument("--name", required=True); rel.add_argument("--notes", default=""); rel.set_defaults(fn=cmd_create_release)
    dr = sub.add_parser("delete-repo"); dr.add_argument("--repo", required=True); dr.add_argument("--confirm", required=True); dr.set_defaults(fn=cmd_delete_repo)

    a = p.parse_args()
    t = get_token()
    if not t:
        out({"error": "no token. Set GH_TOKEN env or ~/.config/tt-github/env"}); sys.exit(1)
    a.fn(a, t)


if __name__ == "__main__":
    main()
