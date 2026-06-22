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
  update-repo --repo OWNER/NAME [--desc D] [--topics a,b] [--homepage URL]
  library-list [--query Q] [--limit N]
  library-add --repo OWNER/NAME [--url URL] [--desc D] [--topics a,b] [--note N]
  library-remove --repo OWNER/NAME
  delete-repo --repo OWNER/NAME --confirm OWNER/NAME   (guarded)
"""
import argparse, json, os, subprocess, sys, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.github.com"
ENV_FILE = Path.home() / ".config" / "tt-github" / "env"
LIB_FILE = Path.home() / ".config" / "tt-github" / "repos.json"


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



def load_library():
    if not LIB_FILE.exists():
        return {"repos": []}
    try:
        data = json.loads(LIB_FILE.read_text())
        if isinstance(data, dict) and isinstance(data.get("repos"), list):
            return data
    except Exception:
        pass
    return {"repos": []}

def save_library(data):
    LIB_FILE.parent.mkdir(parents=True, exist_ok=True)
    LIB_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    try:
        os.chmod(LIB_FILE, 0o600)
    except Exception:
        pass

def remember_repo(full_name, url=None, desc=None, topics=None, private=None, note=None):
    if not full_name:
        return
    data = load_library()
    now = datetime.now(timezone.utc).isoformat()
    found = None
    for r in data["repos"]:
        if r.get("full_name") == full_name:
            found = r; break
    if not found:
        found = {"full_name": full_name, "created_at": now}
        data["repos"].append(found)
    found["updated_at"] = now
    if url is not None: found["url"] = url
    if desc is not None: found["description"] = desc
    if topics is not None: found["topics"] = topics
    if private is not None: found["private"] = bool(private)
    if note is not None: found["note"] = note
    save_library(data)

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


def cmd_library_list(a, t):
    data = load_library()
    repos = data.get("repos", [])
    if a.query:
        q = a.query.lower()
        repos = [r for r in repos if q in r.get("full_name", "").lower() or q in r.get("description", "").lower() or q in " ".join(r.get("topics", [])).lower()]
    out(repos[:a.limit])

def cmd_library_add(a, t):
    remember_repo(a.repo, url=a.url, desc=a.desc, topics=[x.strip() for x in (a.topics or "").split(",") if x.strip()], private=a.private, note=a.note)
    out({"ok": True, "repo": a.repo, "library": str(LIB_FILE)})

def cmd_library_remove(a, t):
    data = load_library()
    before = len(data.get("repos", []))
    data["repos"] = [r for r in data.get("repos", []) if r.get("full_name") != a.repo]
    save_library(data)
    out({"ok": True, "repo": a.repo, "removed": before - len(data["repos"])})

def cmd_update_repo(a, t):
    body = {}
    if a.desc is not None:
        body["description"] = a.desc
    if a.homepage is not None:
        body["homepage"] = a.homepage
    if a.private is not None:
        body["private"] = a.private == "true"
    if body:
        s, d = api("PATCH", f"/repos/{a.repo}", t, body)
        if s >= 400:
            out({"status": s, "error": d.get("message") if isinstance(d, dict) else d}); return
    topics = None
    if a.topics is not None:
        topics = [x.strip().lower() for x in a.topics.split(",") if x.strip()]
        s2, d2 = api("PUT", f"/repos/{a.repo}/topics", t, {"names": topics})
        if s2 >= 400:
            out({"status": s2, "error": d2.get("message") if isinstance(d2, dict) else d2}); return
    s3, d3 = api("GET", f"/repos/{a.repo}", t)
    remember_repo(a.repo, url=d3.get("html_url") if isinstance(d3, dict) else None, desc=d3.get("description") if isinstance(d3, dict) else a.desc, topics=topics, private=d3.get("private") if isinstance(d3, dict) else None, note=a.note)
    out({"status": s3, "repo": a.repo, "url": d3.get("html_url") if isinstance(d3, dict) else None, "description": d3.get("description") if isinstance(d3, dict) else a.desc, "topics": topics, "library_saved": True})

def cmd_list_repos(a, t):
    s, d = api("GET", f"/user/repos?per_page={a.limit}&sort=updated", t)
    if isinstance(d, list):
        out([{"full_name": r["full_name"], "private": r["private"], "url": r["html_url"]} for r in d])
    else:
        out({"status": s, "error": d})


def cmd_create_repo(a, t):
    s, d = api("POST", "/user/repos", t, {
        "name": a.name, "description": a.desc or "", "private": bool(a.private), "has_issues": True})
    remember_repo(d.get("full_name"), url=d.get("html_url"), desc=a.desc or "", private=bool(a.private))
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
    if ok:
        remember_repo(owner_repo, url=f"https://github.com/{owner_repo}", desc=a.desc or None, private=bool(a.private) if a.create else None, note="pushed")
    out({"pushed": ok, "repo": owner_repo, "branch": a.branch,
         "detail": (p.stderr or p.stdout).strip().splitlines()[-3:] if not ok else "ok", "library_saved": ok})


DEFAULT_TOPICS = ["openclaw", "ai-agent", "automation", "github", "developer-tools", "python"]


def cmd_set_topics(a, t):
    names = [x.strip().lower() for x in (a.topics.split(",") if a.topics else DEFAULT_TOPICS) if x.strip()]
    s, d = api("PUT", f"/repos/{a.repo}/topics", t, {"names": names})
    out({"status": s, "topics": d.get("names"), "error": d.get("message")})


def cmd_set_meta(a, t):
    body = {}
    if a.desc:
        body["description"] = a.desc
    if a.homepage:
        body["homepage"] = a.homepage
    s, d = api("PATCH", f"/repos/{a.repo}", t, body)
    out({"status": s, "description": d.get("description"), "homepage": d.get("homepage"), "error": d.get("message")})


def _push_via_api(a, t, repo):
    """Push every file in --path via the Contents API (robust vs. git-over-HTTPS auth)."""
    import base64
    root = a.path
    pushed, failed = [], []
    for dp, _dirs, fs in os.walk(root):
        if any(seg in dp for seg in (".git", "__pycache__", ".pytest_cache")):
            continue
        for f in fs:
            rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
            if rel.endswith(".pyc"):
                continue
            content = base64.b64encode(open(os.path.join(dp, f), "rb").read()).decode()
            sg, dg = api("GET", f"/repos/{repo}/contents/{rel}", t)
            body = {"message": a.message or f"publish {rel}", "content": content, "branch": a.branch}
            if sg == 200 and isinstance(dg, dict) and dg.get("sha"):
                body["sha"] = dg["sha"]
            sp, dp2 = api("PUT", f"/repos/{repo}/contents/{rel}", t, body)
            (pushed if sp < 400 else failed).append(rel)
    return pushed, failed


def cmd_publish(a, t):
    """One-shot: optimize + publish a repo (the auto polish step).

    Steps: ensure repo -> push files (Contents API) -> set description ->
    set topics -> optional release. Each step is idempotent and reported.
    """
    repo = a.repo
    steps = {}
    # 1) ensure repo exists
    s, d = api("GET", f"/repos/{repo}", t)
    if s == 404 and a.create:
        name = repo.split("/")[-1]
        cs, cd = api("POST", "/user/repos", t, {"name": name, "description": a.desc or "", "private": bool(a.private), "has_issues": True})
        steps["create"] = {"status": cs, "error": cd.get("message")}
    else:
        steps["create"] = {"status": s, "exists": s == 200}
    # 2) push files
    pushed, failed = _push_via_api(a, t, repo)
    steps["push"] = {"pushed": len(pushed), "failed": failed}
    # 3) description / homepage
    if a.desc or a.homepage:
        meta = {}
        if a.desc: meta["description"] = a.desc
        if a.homepage: meta["homepage"] = a.homepage
        ms, md = api("PATCH", f"/repos/{repo}", t, meta)
        steps["meta"] = {"status": ms, "description": md.get("description")}
    # 4) topics
    names = [x.strip().lower() for x in (a.topics.split(",") if a.topics else DEFAULT_TOPICS) if x.strip()]
    ts, td = api("PUT", f"/repos/{repo}/topics", t, {"names": names})
    steps["topics"] = {"status": ts, "topics": td.get("names")}
    # 5) optional release
    if a.tag:
        rs, rd = api("POST", f"/repos/{repo}/releases", t, {"tag_name": a.tag, "name": a.release_name or a.tag, "body": a.notes or ""})
        steps["release"] = {"status": rs, "url": rd.get("html_url"), "error": rd.get("message")}
    out({"repo": repo, "url": f"https://github.com/{repo}", "failed": failed, "steps": steps})

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
    ur = sub.add_parser("update-repo"); ur.add_argument("--repo", required=True); ur.add_argument("--desc", default=None); ur.add_argument("--topics", default=None, help="comma-separated topics"); ur.add_argument("--homepage", default=None); ur.add_argument("--private", choices=["true", "false"], default=None); ur.add_argument("--note", default=None); ur.set_defaults(fn=cmd_update_repo)
    ll = sub.add_parser("library-list"); ll.add_argument("--query", default=""); ll.add_argument("--limit", type=int, default=50); ll.set_defaults(fn=cmd_library_list)
    la = sub.add_parser("library-add"); la.add_argument("--repo", required=True); la.add_argument("--url", default=None); la.add_argument("--desc", default=None); la.add_argument("--topics", default=""); la.add_argument("--private", action="store_true"); la.add_argument("--note", default=None); la.set_defaults(fn=cmd_library_add)
    lrm = sub.add_parser("library-remove"); lrm.add_argument("--repo", required=True); lrm.set_defaults(fn=cmd_library_remove)
    dr = sub.add_parser("delete-repo"); dr.add_argument("--repo", required=True); dr.add_argument("--confirm", required=True); dr.set_defaults(fn=cmd_delete_repo)
    st = sub.add_parser("set-topics"); st.add_argument("--repo", required=True); st.add_argument("--topics", default=""); st.set_defaults(fn=cmd_set_topics)
    sm = sub.add_parser("set-meta"); sm.add_argument("--repo", required=True); sm.add_argument("--desc", default=""); sm.add_argument("--homepage", default=""); sm.set_defaults(fn=cmd_set_meta)
    pb = sub.add_parser("publish"); pb.add_argument("--path", required=True); pb.add_argument("--repo", required=True); pb.add_argument("--branch", default="main"); pb.add_argument("--message", default="publish"); pb.add_argument("--create", action="store_true"); pb.add_argument("--private", action="store_true"); pb.add_argument("--desc", default=""); pb.add_argument("--homepage", default=""); pb.add_argument("--topics", default=""); pb.add_argument("--tag", default=""); pb.add_argument("--release-name", default=""); pb.add_argument("--notes", default=""); pb.set_defaults(fn=cmd_publish)

    a = p.parse_args()
    t = get_token()
    if not t:
        out({"error": "no token. Set GH_TOKEN env or ~/.config/tt-github/env"}); sys.exit(1)
    a.fn(a, t)


if __name__ == "__main__":
    main()
