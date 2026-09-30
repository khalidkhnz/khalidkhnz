import base64
import os
import textwrap
from xml.sax.saxutils import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")

SANS = "'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,Inter,Ubuntu,Cantarell,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'Cascadia Code','SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

BG = "#0a0c11"
WIN = "#12151c"
BAR = "#171b24"
LINE = "#262c38"
TXT = "#e8ebf1"
MUTED = "#8a93a6"
DIM = "#5c6476"
ACCENT = "#60cdff"
VIOLET = "#a78bfa"
GREEN = "#6ee7a8"
AMBER = "#fbbf6a"
PINK = "#f472b6"

BASE_CSS = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO};white-space:pre}}
.fade{{opacity:0;animation:fade .6s ease-out forwards}}
@keyframes fade{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important}}}}
"""


def svg(w, h, body, css="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f"<style>{BASE_CSS}{css}</style>{body}</svg>\n"
    )


def defs_common(uid):
    return f"""
<defs>
  <linearGradient id="{uid}-win" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#151923"/><stop offset="1" stop-color="#0f1218"/>
  </linearGradient>
  <linearGradient id="{uid}-edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#3a4254"/><stop offset=".5" stop-color="#232834"/><stop offset="1" stop-color="#2c3342"/>
  </linearGradient>
  <filter id="{uid}-shadow" x="-20%" y="-20%" width="140%" height="160%">
    <feGaussianBlur stdDeviation="14"/>
  </filter>
</defs>"""


def window(uid, x, y, w, h, title, icon_color=ACCENT, glyph=">_", shadow=True):
    """Win11-style window: rounded, title bar with app glyph + caption controls."""
    sh = f'<rect x="{x+8}" y="{y+18}" width="{w-16}" height="{h-8}" rx="14" fill="#000" fill-opacity=".55" filter="url(#{uid}-shadow)"/>' if shadow else ""
    cx = x + w
    return f"""
{sh}
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#{uid}-win)"/>
<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="11.5" fill="none" stroke="url(#{uid}-edge)"/>
<path d="M{x} {y+40}h{w}" stroke="{LINE}"/>
<rect x="{x+14}" y="{y+11}" width="18" height="18" rx="5" fill="{icon_color}" fill-opacity=".16" stroke="{icon_color}" stroke-opacity=".5"/>
<text x="{x+23}" y="{y+24}" text-anchor="middle" class="mono" font-size="9" font-weight="700" fill="{icon_color}">{esc(glyph)}</text>
<text x="{x+42}" y="{y+25}" class="sans" font-size="12.5" fill="{MUTED}">{esc(title)}</text>
<g stroke="{MUTED}" stroke-width="1.1" fill="none">
  <path d="M{cx-118} {y+20.5}h10"/>
  <rect x="{cx-76}" y="{y+15.5}" width="10" height="10" rx="2"/>
  <path d="M{cx-34} {y+15.5}l10 10M{cx-24} {y+15.5}l-10 10"/>
</g>"""


def chip(x, y, label, color, size=12.5, pad=10, h=26):
    cw = size * 0.61
    w = round(len(label) * cw + pad * 2)
    s = f"""<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".35"/>
<text x="{x + w/2}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" class="mono" font-size="{size}" fill="{color}">{esc(label)}</text>"""
    return s, w


def write(name, content):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content)
    print(name, len(content))


# ---------------------------------------------------------------- hero
def hero():
    W, H = 900, 380
    uid = "h"
    CW = 9.05  # mono advance at 15px
    lines = [
        ("cmd", "whoami"),
        ("out", [("Mohd Khalid Khan", TXT, True)]),
        ("cmd", "cat role.txt"),
        ("out", [("Frontend focused Full Stack Developer", ACCENT, False), ("  ·  5+ yrs  ·  India", MUTED, False)]),
        ("cmd", "ls ~/stack"),
        ("out", [("react", "#7dd3fc", False), ("  typescript", "#93c5fd", False), ("  next.js", TXT, False),
                 ("  java", AMBER, False), ("  spring-boot", GREEN, False), ("  kafka", MUTED, False),
                 ("  k8s", "#818cf8", False), ("  solidity", VIOLET, False)]),
        ("cmd", "open https://khalidkhnz.in"),
    ]
    x0, y0, lh = 92, 142, 30
    t = 0.5
    parts = []
    clips = []
    for i, (kind, val) in enumerate(lines):
        y = y0 + i * lh
        if kind == "cmd":
            parts.append(
                f'<text x="{x0}" y="{y}" class="mono fade" font-size="15" style="animation-delay:{t:.2f}s">'
                f'<tspan fill="{GREEN}">khalid</tspan><tspan fill="{DIM}">@</tspan><tspan fill="{ACCENT}">desktop</tspan>'
                f'<tspan fill="{DIM}"> ~ </tspan><tspan fill="{VIOLET}">❯</tspan></text>'
            )
            px = x0 + 20 * CW
            n = len(val)
            dur = max(0.35, n * 0.055)
            vals = ";".join(str(round(k * CW, 1)) for k in range(n + 1))
            kt = ";".join(f"{k/n:.3f}" for k in range(n + 1))
            clips.append(
                f'<clipPath id="c{i}"><rect x="{px}" y="{y-16}" height="22" width="0">'
                f'<animate attributeName="width" begin="{t+0.25:.2f}s" dur="{dur:.2f}s" values="{vals}" keyTimes="{kt}" '
                f'calcMode="discrete" fill="freeze"/></rect></clipPath>'
            )
            parts.append(f'<text x="{px}" y="{y}" class="mono" font-size="15" fill="{TXT}" clip-path="url(#c{i})">{esc(val)}</text>')
            t += 0.25 + dur + 0.2
            last_cmd = (px + n * CW, y, t)
        else:
            spans = "".join(
                f'<tspan fill="{c}"{" font-weight=\"700\"" if b else ""}>{esc(s)}</tspan>' for s, c, b in val
            )
            size = 17 if val[0][2] else 15
            parts.append(f'<text x="{x0}" y="{y}" class="mono fade" font-size="{size}" style="animation-delay:{t:.2f}s">{spans}</text>')
            t += 0.35
    cx, cy, ct = last_cmd
    cursor = (
        f'<rect x="{cx+4}" y="{cy-14}" width="9" height="18" fill="{ACCENT}" opacity="0">'
        f'<animate attributeName="opacity" begin="{ct:.2f}s" dur="1.05s" values="1;1;0;0" keyTimes="0;.5;.5;1" repeatCount="indefinite"/></rect>'
    )
    wall = f"""
<defs>
  <radialGradient id="b1" cx="22%" cy="30%" r="55%"><stop offset="0" stop-color="#1d6fa3" stop-opacity=".55"/><stop offset="1" stop-color="#1d6fa3" stop-opacity="0"/></radialGradient>
  <radialGradient id="b2" cx="82%" cy="78%" r="55%"><stop offset="0" stop-color="#6d3fd6" stop-opacity=".45"/><stop offset="1" stop-color="#6d3fd6" stop-opacity="0"/></radialGradient>
  <radialGradient id="b3" cx="60%" cy="0%" r="40%"><stop offset="0" stop-color="#60cdff" stop-opacity=".22"/><stop offset="1" stop-color="#60cdff" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".05"/></pattern>
  {''.join(clips)}
</defs>
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#b1)"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#b2)"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#b3)"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#grid)"/>
<g class="bloom"><path d="M650 380c40-120 150-190 250-200v200z" fill="#60cdff" fill-opacity=".05"/><path d="M700 380c30-80 110-130 200-140v140z" fill="#a78bfa" fill-opacity=".06"/></g>
"""
    body = wall + defs_common(uid) + window(uid, 60, 58, 780, 294, "Terminal — khalid@khalidkhnz.in") + "".join(parts) + cursor
    css = ""
    return svg(W, H, body, css, "Mohd Khalid Khan — Frontend focused Full Stack Developer")


# ---------------------------------------------------------------- about
def about():
    W, H = 900, 330
    uid = "a"
    with open(os.path.join(HERE, "avatar.jpeg"), "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    bio = ("Frontend focused Full Stack Developer with 5+ years of hands-on experience building "
           "high-performance UIs and scalable backends. React and TypeScript on the front, Java and "
           "Spring Boot on the back, plus distributed ledger tech, event-driven microservices on Kafka, "
           "and cloud-native deployments on AWS and Azure with Docker and Kubernetes.")
    wrapped = textwrap.wrap(bio, 74)
    lines = "".join(
        f'<text x="236" y="{150 + i*22}" class="sans fade" font-size="14.5" fill="{MUTED}" style="animation-delay:{.15+i*.06:.2f}s">{esc(l)}</text>'
        for i, l in enumerate(wrapped)
    )
    chips_y = 150 + len(wrapped) * 22 + 12
    x = 236
    cs = []
    for label, col in [("fintech", GREEN), ("ai", ACCENT), ("blockchain", VIOLET), ("dlt", PINK), ("iot", AMBER), ("saas", "#93c5fd"), ("enterprise", MUTED)]:
        s, w = chip(x, chips_y, label, col, size=12, h=24)
        cs.append(s)
        x += w + 8
    body = defs_common(uid) + window(uid, 10, 10, 880, 310, "About Me — C:\\Users\\khalid", VIOLET, "i", shadow=False) + f"""
<defs><clipPath id="av"><rect x="44" y="76" width="160" height="160" rx="24"/></clipPath>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>
<rect x="40" y="72" width="168" height="168" rx="27" fill="none" stroke="url(#ring)" stroke-width="2"/>
<image href="data:image/jpeg;base64,{b64}" x="44" y="76" width="160" height="160" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>
<g class="fade"><circle cx="196" cy="228" r="9" fill="{WIN}"/><circle cx="196" cy="228" r="5.5" fill="{GREEN}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle></g>
<text x="124" y="270" text-anchor="middle" class="mono" font-size="12" fill="{MUTED}">📍 India · UTC+5:30</text>
<text x="124" y="292" text-anchor="middle" class="mono" font-size="12" fill="{GREEN}">● usually shipping</text>
<text x="236" y="98" class="sans fade" font-size="26" font-weight="700" fill="{TXT}">Hey, I'm Khalid <tspan font-weight="400">👋</tspan></text>
<text x="236" y="122" class="mono fade" font-size="13" fill="{ACCENT}" style="animation-delay:.08s">frontend-focused · full stack · web3 · ai tooling</text>
{lines}
{''.join(cs)}
"""
    return svg(W, H, body, "", "About Mohd Khalid Khan")


# ---------------------------------------------------------------- stack
def stack():
    groups = [
        ("frontend", ACCENT, ["React 18/19", "Next.js", "TypeScript", "Tailwind", "MUI", "Zustand", "GSAP · Framer"]),
        ("backend", GREEN, ["Java 21", "Spring Boot 3", "Spring Security", "JPA · jOOQ", "Node · NestJS", "Go"]),
        ("data", AMBER, ["PostgreSQL", "MongoDB", "Redis", "Drizzle", "Prisma", "Kafka"]),
        ("cloud", "#818cf8", ["AWS", "Azure", "GCP", "Docker", "Kubernetes (EKS/GKE)", "CI/CD"]),
        ("web3", VIOLET, ["Solidity", "Ethereum", "Hyperledger Fabric", "Ethers.js", "Web3.js"]),
        ("ai", PINK, ["MCP servers", "LiteLLM", "Vercel AI SDK", "Multi-agent"]),
        ("testing", MUTED, ["Jest", "Vitest", "Playwright", "Testing Library", "JUnit"]),
    ]
    W = 900
    uid = "s"
    top = 68
    rh = 40
    H = top + len(groups) * rh + 24
    rows = []
    for i, (name, col, items) in enumerate(groups):
        y = top + i * rh
        rows.append(f'<g class="fade" style="animation-delay:{i*.08:.2f}s">')
        rows.append(f'<text x="40" y="{y+18}" class="mono" font-size="13" fill="{DIM}">~/</text>')
        rows.append(f'<text x="60" y="{y+18}" class="mono" font-size="13" font-weight="700" fill="{col}">{name}</text>')
        x = 150
        for it in items:
            s, w = chip(x, y, it, col, size=12.5, h=26)
            rows.append(s)
            x += w + 8
        rows.append("</g>")
    body = defs_common(uid) + window(uid, 10, 10, W - 20, H - 20, "Skills — tree ~/stack", GREEN, "{}", shadow=False) + "".join(rows)
    return svg(W, H, body, "", "Tech stack: React, Next.js, TypeScript, Java, Spring Boot, Kafka, Kubernetes, Solidity and more")


# ---------------------------------------------------------------- project cards
CARDS = [
    ("buildify", "Buildify", "AI app builder", ACCENT, "✦",
     "Chat-to-full-app generator on the T3 stack via the v0 SDK. AI chat, LaTeX resume builder, dual credit system and Razorpay subscriptions.",
     ["Next.js", "v0 SDK", "Drizzle", "Razorpay"]),
    ("context-manager", "Context Manager MCP", "MCP server", GREEN, "⌘",
     "Gives AI assistants structured access to plans, guidelines, skills and prompt templates. 40+ techstacks, 29 patterns. CLI, REST and MCP.",
     ["MCP", "TypeScript", "REST", "Docker"]),
    ("prism", "Prism", "Multi-agent social SaaS", PINK, "◆",
     "A team of specialist agents (topic, hook, writer, editor, scheduler) that drafts and schedules posts across LinkedIn, X, IG, FB and Threads.",
     ["T3 Stack", "AI Agents", "5 platforms"]),
    ("transport", "Transportation Platform", "Enterprise · live routing", AMBER, "⇄",
     "Next.js 16 + React 19 front end with live Mapbox / Google Maps tracking on a Java 21, Spring Boot 3, PostgreSQL back end on AWS EKS.",
     ["Java 21", "Spring Boot", "EKS", "AG Grid"]),
    ("dlt", "DLT Supply Chain", "Hyperledger traceability", VIOLET, "⛓",
     "Immutable product-lifecycle records on Hyperledger Fabric with a Spring Boot gateway, Kafka analytics and QR verification dashboard.",
     ["Fabric", "Spring Boot", "Kafka", "K8s"]),
    ("defi", "DeFi Trading Platform", "On-chain + off-chain", "#818cf8", "Ξ",
     "ERC-20 swap and liquidity-staking contracts on Ethereum, with Spring Boot middleware for off-chain order matching and indexing.",
     ["Solidity", "Ethers.js", "Spring", "Postgres"]),
    ("win11", "Windows 11 Portfolio", "The OS you can visit", ACCENT, "⊞",
     "Faux operating system portfolio with real window management, a start menu and themable Windows, macOS and Linux variants.",
     ["Next.js", "Tailwind", "Framer Motion"]),
    ("hyper", "Custom Hyper", "Terminal, my way", GREEN, ">_",
     "Personalised build of the Vercel Hyper terminal (Electron) with my plugin set, keymaps and theme. Daily driver on macOS, Linux and Windows.",
     ["Electron", "TypeScript", "Plugins"]),
]


def card(slug, name, sub, col, glyph, desc, tags):
    W, H = 440, 232
    uid = "k"
    lines = textwrap.wrap(desc, 52)[:3]
    dl = "".join(f'<text x="30" y="{128 + i*20}" class="sans" font-size="13.5" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(lines))
    x = 30
    cs = []
    for t in tags:
        s, w = chip(x, 186, t, col, size=11.5, pad=9, h=23)
        cs.append(s)
        x += w + 7
    body = defs_common(uid) + window(uid, 6, 6, W - 12, H - 12, f"{slug}.app", col, glyph, shadow=False) + f"""
<text x="30" y="84" class="sans" font-size="21" font-weight="700" fill="{TXT}">{esc(name)}</text>
<text x="30" y="104" class="mono" font-size="12" fill="{col}">{esc(sub)}</text>
<g transform="translate(398 70)" stroke="{DIM}" stroke-width="1.6" fill="none" stroke-linecap="round"><path d="M0 10L10 0M3 0h7v7"/></g>
{dl}
{''.join(cs)}
"""
    return svg(W, H, body, "", f"{name} — {sub}")


# ---------------------------------------------------------------- contact + buttons + taskbar
def contact():
    W, H = 900, 170
    uid = "c"
    body = defs_common(uid) + window(uid, 10, 10, 880, 150, "Contact — new message", ACCENT, "@", shadow=False) + f"""
<text x="40" y="96" class="sans fade" font-size="24" font-weight="700" fill="{TXT}">Got a project, a role, or just want to say hi?</text>
<text x="40" y="126" class="sans fade" font-size="15" fill="{MUTED}" style="animation-delay:.1s">Drop me a line. I reply within a day or two.</text>
<g transform="translate(760 78)"><g class="fade" style="animation-delay:.2s">
  <rect width="96" height="40" rx="8" fill="{ACCENT}"/>
  <text x="48" y="25" text-anchor="middle" class="sans" font-size="14" font-weight="600" fill="#06121a">Send  ➤</text>
</g></g>
"""
    return svg(W, H, body, "", "Contact Khalid")


ICONS = {
    "portfolio": ('<rect x="1.5" y="3" width="17" height="13" rx="2"/><path d="M1.5 7h17M5 5h.01M7.5 5h.01"/>', ACCENT),
    "linkedin": ('<rect x="2" y="2" width="16" height="16" rx="3"/><path d="M6 8.5v5.5M6 5.8v.01M9.5 14v-3.2a2 2 0 0 1 4 0V14M9.5 8.5V14"/>', "#7aa7ff"),
    "x": ('<path d="M3 3l14 14M17 3L3 17"/>', TXT),
    "email": ('<rect x="2" y="4" width="16" height="12" rx="2"/><path d="M2.5 5l7.5 6 7.5-6"/>', GREEN),
    "resume": ('<path d="M5 2h7l4 4v12H5z"/><path d="M12 2v4h4M8 10h5M8 13h5"/>', AMBER),
}


def button(key, label):
    path, col = ICONS[key]
    W, H = 210, 52
    return svg(W, H, f"""
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{WIN}" stroke="#2a303d"/>
<rect x="12" y="11" width="30" height="30" rx="8" fill="{col}" fill-opacity=".12"/>
<g transform="translate(17 16)" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{path}</g>
<text x="54" y="31.5" class="sans" font-size="14.5" font-weight="600" fill="{TXT}">{esc(label)}</text>
<path d="M{W-24} 22l5 4-5 4" fill="none" stroke="{DIM}" stroke-width="1.6" stroke-linecap="round"/>
""", "", label)


def taskbar():
    W, H = 900, 56
    icons = [(ACCENT, "⊞"), (GREEN, ">_"), (AMBER, "▤"), (VIOLET, "{}"), (PINK, "◆"), ("#7aa7ff", "in")]
    n = len(icons)
    start = W / 2 - (n * 44) / 2
    g = []
    for i, (c, gl) in enumerate(icons):
        x = start + i * 44
        g.append(f'<rect x="{x+4}" y="10" width="36" height="36" rx="8" fill="#fff" fill-opacity="{.07 if i==1 else 0}"/>'
                 f'<text x="{x+22}" y="33" text-anchor="middle" class="mono" font-size="14" font-weight="700" fill="{c}">{esc(gl)}</text>')
        if i in (0, 1):
            g.append(f'<rect x="{x+{0:17,1:14}[i]}" y="47" width="{ {0:10,1:16}[i] }" height="3" rx="1.5" fill="{ACCENT if i==1 else DIM}"/>')
    body = f"""
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="#10131a" fill-opacity=".92" stroke="#262c38"/>
<text x="22" y="33" class="mono" font-size="12" fill="{MUTED}">Mohd Khalid Khan</text>
{''.join(g)}
<text x="{W-22}" y="25" text-anchor="end" class="sans" font-size="12" fill="{TXT}">khalidkhnz.in</text>
<text x="{W-22}" y="42" text-anchor="end" class="mono" font-size="11" fill="{MUTED}">thanks for visiting ✦</text>
"""
    return svg(W, H, body, "", "Taskbar")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("hero.svg", hero())
    write("about.svg", about())
    write("stack.svg", stack())
    for c in CARDS:
        write(f"card-{c[0]}.svg", card(*c))
    write("contact.svg", contact())
    for k, lbl in [("portfolio", "khalidkhnz.in"), ("linkedin", "LinkedIn"), ("x", "@khalidkhnz"), ("email", "Email me")]:
        write(f"btn-{k}.svg", button(k, lbl))
    write("taskbar.svg", taskbar())
