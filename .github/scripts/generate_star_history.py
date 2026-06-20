#!/usr/bin/env python3
import os, sys, requests, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path

REPO    = os.environ["REPO"]
TOKEN   = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3.star+json",
    "Authorization": f"Bearer {TOKEN}",
}

def fetch_stars(repo):
    dates, page = [], 1
    while True:
        r = requests.get(
            f"https://api.github.com/repos/{repo}/stargazers",
            headers=HEADERS, params={"per_page": 100, "page": page}, timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        dates += [datetime.fromisoformat(i["starred_at"].rstrip("Z")) for i in data]
        page += 1
    return sorted(dates)

BG, PLOT_BG = "#0d1117", "#161b22"
GRID, LINE, POINT, TEXT = "#21262d", "#1f6feb", "#58a6ff", "#c9d1d9"

def generate(dates, repo, out):
    counts = list(range(1, len(dates) + 1))
    owner, name = repo.split("/")

    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PLOT_BG)

    ax.plot(dates, counts, color=LINE, linewidth=1.8, zorder=3)
    ax.fill_between(dates, counts, color=LINE, alpha=0.15, zorder=2)
    ax.scatter(dates, counts, color=POINT, s=12, zorder=4, linewidths=0)

    ax.set_axisbelow(True)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.tick_params(colors=TEXT, labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    fig.autofmt_xdate(rotation=0, ha="center")

    ax.set_ylabel("Stars", color=TEXT, fontsize=8)
    ax.set_xlabel("Date",  color=TEXT, fontsize=8)
    ax.set_title(f"{owner} / {name} · Star History", color=TEXT, fontsize=10, fontweight="bold", pad=10)

    plt.tight_layout(pad=0.8)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight", facecolor=BG)
    plt.close(fig)

if __name__ == "__main__":
    stars = fetch_stars(REPO)
    if not stars:
        sys.exit(0)
    generate(stars, REPO, Path("assets/star-history.svg"))
