"""Build self-contained profile header animations and a branded technology panel.

Run: python scripts/build_profile_identity.py
Brand paths are vendored from Simple Icons 16.35.0 (CC0-1.0).
"""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'workbench'
FONT = 'Cascadia Code, Consolas, Microsoft YaHei, monospace'


def header(dark=False):
    ink, muted, line = ('#E4ECF7', '#8FA3BC', '#34445E') if dark else ('#1A263C', '#586A83', '#D9E4EB')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="170" viewBox="0 0 1000 170" role="img" aria-labelledby="title desc">
<title id="title">Ethan Chen / 陈奕恺 — AI applications and full-stack products</title>
<desc id="desc">A name reveal, a terminal cursor and a mint signal moving along a fine line. / 姓名渐次显现、终端光标与流动细线。</desc>
<defs><linearGradient id="signal"><stop stop-color="#94D3BE" stop-opacity="0"/><stop offset=".5" stop-color="#94D3BE"/><stop offset="1" stop-color="#B5A2E2" stop-opacity="0"/></linearGradient><clipPath id="track"><rect x="220" y="140" width="560" height="12"/></clipPath></defs>
<style>
.name{{animation:reveal 1.8s cubic-bezier(.2,.7,.2,1) both}}
.subtitle{{animation:subtitle .8s .75s both}}
.cursor{{animation:blink 1.2s 1.6s step-end infinite}}
.signal{{animation:travel 7s 1.4s ease-in-out infinite}}
@keyframes reveal{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes subtitle{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes blink{{0%,50%{{opacity:1}}51%,100%{{opacity:0}}}}
@keyframes travel{{0%{{transform:translateX(0);opacity:0}}12%{{opacity:1}}88%{{opacity:1}}100%{{transform:translateX(700px);opacity:0}}}}
@media(prefers-reduced-motion:reduce){{.name,.subtitle,.cursor,.signal{{animation:none}}.cursor,.signal{{opacity:0}}}}
</style>
<g font-family="{FONT}" text-anchor="middle">
<text class="name" x="500" y="68" font-size="51" fill="{ink}" font-weight="700">Ethan Chen / 陈奕恺</text>
<text class="subtitle" x="500" y="113" font-size="20" fill="{muted}">AI applications / Full-stack products / Creative coding</text>
</g>
<rect class="cursor" x="834" y="96" width="3" height="21" rx="1" fill="#94D3BE"/>
<path d="M220 146H780" stroke="{line}"/>
<g clip-path="url(#track)"><g class="signal"><path d="M80 146H220" stroke="url(#signal)" stroke-width="2"/><circle cx="220" cy="146" r="2.5" fill="#94D3BE"/></g></g>
</svg>'''


GROUPS = [
    ('Frontend & interaction', '前端与交互', [
        ('typescript','TypeScript','#3178C6'), ('javascript','JavaScript','#F7DF1E'),
        ('react','React','#61DAFB'), ('vuedotjs','Vue','#4FC08D'),
        ('tailwindcss','Tailwind CSS','#06B6D4'), ('threedotjs','Three.js','#000000'),
        ('gsap','GSAP','#0AE448'), ('electron','Electron','#47848F')]),
    ('Backend & data', '后端与数据', [
        ('python','Python','#3776AB'), ('fastapi','FastAPI','#009688'),
        ('nodedotjs','Node.js','#5FA04E'), ('postgresql','PostgreSQL','#4169E1'),
        ('mysql','MySQL','#4479A1'), ('sqlite','SQLite','#003B57')]),
    ('AI & delivery', 'AI 与工程交付', [
        ('langgraph','LangGraph','#1C3C3C'), ('docker','Docker','#2496ED'),
        ('git','Git','#F05032'), ('githubactions','GitHub Actions','#2088FF'),
        ('pytest','pytest','#0A9EDC'), ('vitest','Vitest','#6E9F18')]),
]


def tech_stack():
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="536" viewBox="0 0 1000 536" role="img" aria-labelledby="title desc">
<title id="title">Ethan's tech stack / 常用技术栈</title>
<desc id="desc">Frontend: TypeScript, JavaScript, React, Vue, Tailwind CSS, Three.js, GSAP, Electron. Backend: Python, FastAPI, Node.js, PostgreSQL, MySQL, SQLite. AI and delivery: LangGraph, Docker, Git, GitHub Actions, pytest, Vitest. Also LLM APIs, Agent, RAG, Skills, MCP and Playwright.</desc>
<rect x="1" y="1" width="998" height="534" rx="18" fill="#1C2639" stroke="#36445C"/>
''']
    for index, (english, chinese, icons) in enumerate(GROUPS):
        top = 26 + index * 162
        parts.append(f'<text x="30" y="{top+13}" fill="#E4ECF7" font-family="{FONT}" font-weight="700" font-size="19">{escape(english)}</text>')
        parts.append(f'<text x="970" y="{top+13}" fill="#94D3BE" font-family="{FONT}" text-anchor="end" font-size="15">{chinese}</text>')
        if index:
            parts.append(f'<path d="M30 {top-17}H970" stroke="#36445C"/>')
        for i, (slug, label, color) in enumerate(icons):
            x = 76 + i * 120
            source = ET.parse(ROOT / 'assets' / 'tech-icons' / (slug+'.svg')).getroot()
            paths = ''.join(f'<path d="{node.attrib["d"]}"/>' for node in source if node.tag.endswith('path'))
            parts.append(f'<rect x="{x-26}" y="{top+29}" width="52" height="52" rx="12" fill="#F4F7FA"/>')
            # Yellow and cyan logos need a darker tile for sufficient contrast.
            if slug in ('javascript', 'react', 'gsap'):
                parts[-1] = f'<rect x="{x-26}" y="{top+29}" width="52" height="52" rx="12" fill="#101827"/>'
            parts.append(f'<g transform="translate({x-17} {top+38}) scale(1.4166667)" fill="{color}">{paths}</g>')
            parts.append(f'<text x="{x}" y="{top+105}" text-anchor="middle" fill="#DCE3F1" font-family="{FONT}" font-size="13">{escape(label)}</text>')
    parts.append(f'<text x="30" y="514" fill="#9BAEC6" font-family="{FONT}" font-size="14">LLM APIs / Agent / RAG / Skills / MCP / Playwright</text></svg>')
    return ''.join(parts)


for name, content in [('title-animated-light.svg',header()), ('title-animated-dark.svg',header(True)), ('tech-stack.svg',tech_stack())]:
    ET.fromstring(content)
    (OUT / name).write_text(content+'\n', encoding='utf-8')
    print('Built', name)
