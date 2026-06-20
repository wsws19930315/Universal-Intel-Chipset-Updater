#!/usr/bin/env python3
import os, sys, requests, numpy as np, matplotlib
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

LINK_BLUE = "#58a6ff"
LINE      = "#1f6feb"
GRID_MAJ  = "#444444"
GRID_MIN  = "#2a2a2a"

def generate(dates, repo, out):
    counts   = list(range(1, len(dates) + 1))
    owner, name = repo.split("/")

    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=150)
    fig.patch.set_facecolor("none")   # transparent
    ax.set_facecolor("none")           # transparent

    # ── line + fill ───────────────────────────────────────────────────────────
    date_nums = mdates.date2num(dates)
    ax.plot(dates, counts, color=LINE, linewidth=1.8, zorder=3)
    ax.fill_between(dates, counts, color=LINE, alpha=0.15, zorder=2)

    # ── dots at 31 evenly spaced vertical positions ───────────────────────────
    x31 = np.linspace(date_nums[0], date_nums[-1], 31)
    y31 = np.interp(x31, date_nums, counts)
    ax.scatter(mdates.num2date(x31), y31,
               color=LINK_BLUE, s=49, zorder=4, linewidths=0)

    # ── grid: major = monthly, minor = 5 per month (~6-day interval) ──────────
    ax.set_axisbelow(True)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=6))
    ax.grid(True, which="major", color=GRID_MAJ, linewidth=0.7)
    ax.grid(True, which="minor", color=GRID_MIN, linewidth=0.4)

    # 10 horizontal lines
    ax.yaxis.set_major_locator(plt.MaxNLocator(10, integer=True))
    ax.yaxis.grid(True, which="major", color=GRID_MAJ, linewidth=0.7)

    # ── axes styling ──────────────────────────────────────────────────────────
    ax.tick_params(colors=LINK_BLUE, labelsize=7, which="both")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    fig.autofmt_xdate(rotation=0, ha="center")

    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_MAJ)

    ax.set_ylabel("Stars", color=LINK_BLUE, fontsize=8,
                  fontfamily="DejaVu Sans")
    ax.set_xlabel("Date",  color=LINK_BLUE, fontsize=8,
                  fontfamily="DejaVu Sans")

    # ── title — not bold, link blue, normal weight ────────────────────────────
    ax.set_title(
        f"{owner} / {name} · Star History",
        color=LINK_BLUE, fontsize=10, fontweight="normal",
        fontfamily="DejaVu Sans", pad=10
    )

    plt.tight_layout(pad=0.8)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight",
                transparent=True)
    plt.close(fig)

if __name__ == "__main__":
    stars = fetch_stars(REPO)
    if not stars:
        sys.exit(0)
    generate(stars, REPO, Path("assets/star-history.svg"))
