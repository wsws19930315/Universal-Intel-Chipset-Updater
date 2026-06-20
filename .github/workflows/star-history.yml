#!/usr/bin/env python3
import os
import sys
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path

REPO = os.environ["REPO"]
TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github.v3.star+json",
    "Authorization": f"Bearer {TOKEN}",
}

# ── fetch all stargazers with timestamps ──────────────────────────────────────
def fetch_stars(repo: str) -> list[datetime]:
    dates = []
    page = 1
    while True:
        r = requests.get(
            f"https://api.github.com/repos/{repo}/stargazers",
            headers=HEADERS,
            params={"per_page": 100, "page": page},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        for item in data:
            dates.append(datetime.fromisoformat(item["starred_at"].rstrip("Z")))
        page += 1
    return sorted(dates)


# ── build cumulative series ───────────────────────────────────────────────────
def cumulative(dates: list[datetime]) -> tuple[list, list]:
    return dates, list(range(1, len(dates) + 1))


# ── plot ──────────────────────────────────────────────────────────────────────
BG        = "#0d1117"
PLOT_BG   = "#161b22"
GRID      = "#21262d"
LINE      = "#1f6feb"
LINE_FILL = "#1f6feb"
TEXT      = "#c9d1d9"
TITLE     = "#c9d1d9"
POINT     = "#58a6ff"

def generate(dates, counts, repo: str, out: Path):
    repo_name = repo.split("/")[-1]
    owner     = repo.split("/")[0]

    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PLOT_BG)

    ax.plot(dates, counts,
            color=LINE, linewidth=1.8, zorder=3)
    ax.fill_between(dates, counts,
                    color=LINE_FILL, alpha=0.15, zorder=2)
    ax.scatter(dates, counts,
               color=POINT, s=12, zorder=4, linewidths=0)

    # grid
    ax.set_axisbelow(True)
    ax.grid(True, color=GRID, linewidth=0.6, linestyle="-")
    ax.tick_params(colors=TEXT, labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)

    # axes
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=12))
    fig.autofmt_xdate(rotation=0, ha="center")

    ax.yaxis.set_label_text("Stars", color=TEXT, fontsize=8)
    ax.xaxis.set_label_text("Date",  color=TEXT, fontsize=8)

    ax.set_title(
        f"{owner} aka {repo_name} · Star History",
        color=TITLE, fontsize=10, fontweight="bold", pad=10
    )

    plt.tight_layout(pad=0.8)

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight",
                facecolor=BG, transparent=False)
    plt.close(fig)
    print(f"Saved → {out}")


if __name__ == "__main__":
    print(f"Fetching stars for {REPO}...")
    star_dates = fetch_stars(REPO)
    if not star_dates:
        print("No stars yet, exiting.")
        sys.exit(0)
    dates, counts = cumulative(star_dates)
    out_path = Path("assets/star-history.svg")
    generate(dates, counts, REPO, out_path)
