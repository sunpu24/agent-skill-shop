# -*- coding: utf-8 -*-
"""
GitHub 仓库指标增强脚本

读取 data/skills.json 中的 skill 链接，提取 GitHub 仓库 owner/repo，
通过 GitHub REST API 获取仓库指标，并写入 data/github_repo_metrics.json。

建议在 .env 文件或环境变量中配置：
    GITHUB_TOKEN=你的 GitHub Token

使用示例：
    python github_metrics_enricher.py
    python github_metrics_enricher.py --limit 20
    python github_metrics_enricher.py --force
"""

import argparse
import base64
import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse

import requests


SKILLS_PATH = "data/skills.json"
OUTPUT_PATH = "data/github_repo_metrics.json"
GITHUB_API_BASE = "https://api.github.com"


def load_env_file(path: str = ".env") -> None:
    """读取 .env 文件并写入环境变量。

    为了避免额外安装 python-dotenv，这里实现一个轻量版本：
    - 支持 KEY=VALUE
    - 忽略空行和 # 注释
    - 不覆盖系统里已经存在的环境变量
    """
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


def load_json(path: str, default):
    """读取 JSON 文件，不存在则返回默认值。"""
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: str, data) -> None:
    """保存 JSON 文件。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def parse_github_repo(link: str) -> Optional[str]:
    """从 GitHub 链接中提取 owner/repo。

    支持：
    - https://github.com/owner/repo
    - https://github.com/owner/repo/tree/main/xxx
    - https://github.com/owner/repo/blob/main/xxx
    """
    if not link:
        return None

    parsed = urlparse(link.strip())
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None

    owner, repo = parts[0], parts[1]
    if owner.lower() in {"features", "topics", "marketplace", "explore"}:
        return None
    if repo.lower() in {"issues", "pulls", "discussions", "actions", "projects", "wiki"}:
        return None

    return f"{owner}/{repo}"


def extract_repos(skills: Iterable[Dict]) -> Dict[str, List[Dict]]:
    """提取唯一 GitHub 仓库，并记录每个仓库对应的 skills。"""
    repos: Dict[str, List[Dict]] = {}
    for skill in skills:
        repo_id = parse_github_repo(skill.get("link", ""))
        if repo_id:
            repos.setdefault(repo_id, []).append(skill)
    return repos


def build_headers(token: Optional[str]) -> Dict[str, str]:
    """构造 GitHub API 请求头。"""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "skill-visualization-enricher",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_get(session: requests.Session, url: str, headers: Dict[str, str], timeout: int = 30) -> Optional[requests.Response]:
    """执行 GitHub GET 请求，遇到限流给出提示。"""
    response = session.get(url, headers=headers, timeout=timeout)

    remaining = response.headers.get("X-RateLimit-Remaining")
    reset = response.headers.get("X-RateLimit-Reset")
    if response.status_code == 403 and remaining == "0":
        reset_time = datetime.fromtimestamp(int(reset), tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S") if reset else "unknown"
        print(f"GitHub API 限流，剩余额度为 0，重置时间：{reset_time}")
        return None

    if response.status_code == 404:
        return response

    response.raise_for_status()
    return response


def fetch_repo_info(session: requests.Session, headers: Dict[str, str], repo_id: str) -> Dict:
    """获取单个仓库的基础信息。"""
    url = f"{GITHUB_API_BASE}/repos/{repo_id}"
    response = github_get(session, url, headers)
    if response is None:
        return {"repo": repo_id, "fetch_status": "rate_limited"}
    if response.status_code == 404:
        return {"repo": repo_id, "fetch_status": "not_found"}

    data = response.json()
    license_info = data.get("license") or {}

    return {
        "repo": repo_id,
        "fetch_status": "ok",
        "html_url": data.get("html_url"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "watchers": data.get("watchers_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "language": data.get("language"),
        "license": license_info.get("spdx_id") or license_info.get("name"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "pushed_at": data.get("pushed_at"),
        "archived": data.get("archived", False),
        "disabled": data.get("disabled", False),
        "is_fork": data.get("fork", False),
        "default_branch": data.get("default_branch"),
        "topics": data.get("topics", []),
    }


def fetch_readme_info(session: requests.Session, headers: Dict[str, str], repo_id: str) -> Dict:
    """获取仓库 README 信息。"""
    url = f"{GITHUB_API_BASE}/repos/{repo_id}/readme"
    response = github_get(session, url, headers)
    if response is None:
        return {"has_readme": None, "readme_length": None, "readme_status": "rate_limited"}
    if response.status_code == 404:
        return {"has_readme": False, "readme_length": 0, "readme_status": "not_found"}

    data = response.json()
    encoded_content = data.get("content", "")
    readme_length = data.get("size") or 0

    # size 是 GitHub 返回的字节大小；如果没有 size，就尝试解码后计算。
    if not readme_length and encoded_content:
        try:
            decoded = base64.b64decode(encoded_content).decode("utf-8", errors="ignore")
            readme_length = len(decoded)
        except Exception:
            readme_length = 0

    return {
        "has_readme": True,
        "readme_length": readme_length,
        "readme_status": "ok",
        "readme_url": data.get("html_url"),
    }


def enrich_repositories(limit: Optional[int] = None, force: bool = False, sleep_seconds: float = 0.1) -> Dict:
    """增强 GitHub 仓库指标。"""
    load_env_file()

    skills_data = load_json(SKILLS_PATH, {})
    skills = skills_data.get("skills", [])
    repo_to_skills = extract_repos(skills)
    repo_ids = sorted(repo_to_skills.keys())

    if limit:
        repo_ids = repo_ids[:limit]

    token = os.getenv("GITHUB_TOKEN")
    headers = build_headers(token)

    existing_output = load_json(OUTPUT_PATH, {"repositories": {}})
    existing_repos = existing_output.get("repositories", {})
    output_repos = dict(existing_repos)

    session = requests.Session()
    fetched_count = 0
    skipped_count = 0

    print(f"skills 总数：{len(skills)}")
    print(f"GitHub 去重仓库数：{len(repo_to_skills)}")
    print(f"本次计划处理仓库数：{len(repo_ids)}")
    print(f"GitHub Token：{'已配置' if token else '未配置，可能遇到 60次/小时 限流'}")

    for index, repo_id in enumerate(repo_ids, start=1):
        if not force and repo_id in output_repos and output_repos[repo_id].get("fetch_status") == "ok":
            skipped_count += 1
            continue

        print(f"[{index}/{len(repo_ids)}] 获取 {repo_id}")
        repo_info = fetch_repo_info(session, headers, repo_id)
        if repo_info.get("fetch_status") == "rate_limited":
            break

        readme_info = {}
        if repo_info.get("fetch_status") == "ok":
            readme_info = fetch_readme_info(session, headers, repo_id)

        related_skills = repo_to_skills.get(repo_id, [])
        output_repos[repo_id] = {
            **repo_info,
            **readme_info,
            "related_skill_count": len(related_skills),
            "related_skill_examples": [
                {
                    "name": skill.get("name"),
                    "description": skill.get("description"),
                    "category": skill.get("category"),
                    "link": skill.get("link"),
                }
                for skill in related_skills[:5]
            ],
            "metrics_fetched_at": datetime.now().isoformat(),
        }
        fetched_count += 1

        if sleep_seconds:
            time.sleep(sleep_seconds)

    result = {
        "generated_at": datetime.now().isoformat(),
        "source_skills_file": SKILLS_PATH,
        "total_skills": len(skills),
        "unique_github_repositories": len(repo_to_skills),
        "repositories_in_file": len(output_repos),
        "fetched_this_run": fetched_count,
        "skipped_cached_this_run": skipped_count,
        "used_github_token": bool(token),
        "repositories": output_repos,
    }
    save_json(OUTPUT_PATH, result)
    print(f"完成：本次新增/更新 {fetched_count} 个仓库，跳过缓存 {skipped_count} 个仓库")
    print(f"输出文件：{OUTPUT_PATH}")
    return result


def main():
    parser = argparse.ArgumentParser(description="GitHub API 仓库指标增强脚本")
    parser.add_argument("--limit", type=int, default=None, help="只处理前 N 个仓库，便于测试")
    parser.add_argument("--force", action="store_true", help="忽略缓存，强制重新请求")
    parser.add_argument("--sleep", type=float, default=0.1, help="每个仓库请求后的暂停秒数，默认 0.1")
    args = parser.parse_args()

    enrich_repositories(limit=args.limit, force=args.force, sleep_seconds=args.sleep)


if __name__ == "__main__":
    main()