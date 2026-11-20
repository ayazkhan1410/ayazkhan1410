"""Build assets/card.svg: a neofetch-style profile card with live public GitHub stats."""
import json
import os
import urllib.request
from collections import Counter
from xml.sax.saxutils import escape

USER = "ayazkhan1410"
QUERY = """query($u:String!){user(login:$u){
contributionsCollection{totalCommitContributions}
repositories(isFork:false,privacy:PUBLIC,first:100){totalCount nodes{primaryLanguage{name}}}}}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        json.dumps({"query": QUERY, "variables": {"u": USER}}).encode(),
        {"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]["user"]


BANNER = [
    r"    _ __   __    _    _____",
    r"   / \\ \ / /   / \  |__  /",
    r"  / _ \\ V /   / _ \   / / ",
    r" / ___ \| |   / ___ \ / /_ ",
    r"/_/   \_\_|  /_/   \_\/____|",
]
CODE = [
    ("class", " Ayaz:"),
    ("", '    role  = "Backend Developer"'),
    ("", '    stack = ["Django", "Kafka",'),
    ("", '             "Celery", "Postgres"]'),
    ("", '    loves = "simple, fast code"'),
]
W = 52  # width of the right-hand column in characters


def row(key, val):
    dots = "." * max(2, W - len(key) - len(val) - 4)
    return (
        f'<tspan class="d">. </tspan><tspan class="k">{escape(key)}</tspan>'
        f'<tspan class="d">: {dots} </tspan><tspan class="v">{escape(val)}</tspan>'
    )


def head(title):
    return f'<tspan class="d">- {escape(title)} {"-" * (W - len(title) - 2)}</tspan>'


def main():
    u = fetch()
    repos = u["repositories"]["nodes"]
    langs = Counter(r["primaryLanguage"]["name"] for r in repos if r["primaryLanguage"])
    top = ", ".join(n for n, _ in langs.most_common(4))
    right = [
        f'<tspan class="t">ayaz@khan</tspan> <tspan class="d">{"-" * (W - 10)}</tspan>',
        row("Role", "Backend Developer @ BetaCodes"),
        row("Location", "Bahawalpur, Pakistan"),
        row("Experience", "2+ years"),
        "",
        row("Languages", "Python, SQL, Java"),
        row("Frameworks", "Django, DRF, Celery, Flask"),
        row("Data", "PostgreSQL, MySQL, Redis"),
        row("Infra", "Kafka, AWS, Docker, GitHub Actions"),
        row("Focus", "APIs, jobs, pipelines, AI integrations"),
        "",
        head("Contact"),
        row("LinkedIn", "studywithayaz"),
        row("YouTube", "Study with Ayaz"),
        "",
        head("GitHub Stats"),
        row("Public repos", str(u["repositories"]["totalCount"])),
        row("Commits (last year)", str(u["contributionsCollection"]["totalCommitContributions"])),
        row("Top languages", top),
    ]
    lh, top_y, left_x, right_x = 20, 44, 28, 380
    height = top_y + lh * len(right) + 10
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
        f'viewBox="0 0 900 {height}" role="img" aria-label="Ayaz Khan profile card">',
        "<style>text{font:14px 'DejaVu Sans Mono',Consolas,Menlo,monospace;white-space:pre}"
        ".k{fill:#ffa657}.v{fill:#79c0ff}.d{fill:#8b949e}.t{fill:#7ee787;font-weight:bold}"
        ".b{fill:#2f81f7}.kw{fill:#ff7b72}.c{fill:#c9d1d9}</style>",
        '<rect width="900" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>',
    ]
    for i, line in enumerate(BANNER):
        out.append(f'<text x="{left_x}" y="{top_y + lh * i}" class="b">{escape(line)}</text>')
    for i, (kw, rest) in enumerate(CODE):
        y = top_y + lh * (len(BANNER) + 2 + i)
        kws = f'<tspan class="kw">{kw}</tspan>' if kw else ""
        out.append(f'<text x="{left_x}" y="{y}" class="c">{kws}{escape(rest)}</text>')
    for i, line in enumerate(right):
        out.append(f'<text x="{right_x}" y="{top_y + lh * i}">{line}</text>')
    out.append("</svg>")
    with open("assets/card.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
