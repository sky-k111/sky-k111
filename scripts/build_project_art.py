"""Build original, self-contained SVG project vignettes for the profile.

These are conceptual animations, not product screenshots or live repository data.
Run with Python's standard library: python scripts/build_project_art.py
"""
from pathlib import Path
from html import escape
import random
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "atelier"
INK = "#dce3f1"
MUTED = "#8f9bb4"
GOLD = "#e8bd8a"
MINT = "#94d3be"
LILAC = "#b5a2e2"
BLUE = "#9abedb"


def rect(x, y, w, h, fill, radius=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" {extra}/>'


def text(x, y, value, size=14, color=INK, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'


def path(d, color=MUTED, width=1.5, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def dot(x, y, color, r=3, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'


def chip(x, y, label, color, width=None):
    width = width or len(label) * 7.2 + 18
    return rect(x, y, width, 21, color, 4, 'fill-opacity=".10"') + text(x + 9, y + 14.5, label, 11, color)


def lines(x, y, lengths, color=MUTED, gap=12):
    return "".join(rect(x, y + i * gap, length, 3, color, 1, 'opacity=".45"') for i, length in enumerate(lengths))


def typed(x, y, value, start, duration, color, prefix):
    result = f'<text x="{x}" y="{y}" font-size="13" xml:space="preserve" fill="{color}">'
    rules = []
    for i, c in enumerate(value):
        at = (start + duration * i / max(1, len(value) - 1)) / 10 * 100
        name = f'{prefix}-char-{i}'
        rules.append(f'@keyframes {name}{{0%,{at:.2f}%{{opacity:0}}{at+.1:.2f}%,94%{{opacity:1}}98%,100%{{opacity:0}}}}')
        result += f'<tspan style="animation:{name} 10s step-end infinite">{escape(c)}</tspan>'
    return result + '</text>', ''.join(rules)


def pixel_night(seed, accent):
    rng = random.Random(seed)
    out = rect(0, 0, 640, 480, '#141a30', 12)
    # Original vector skyline; no raster, remote dependency or reference asset.
    for i in range(20):
        x, y = rng.randrange(10, 630), rng.randrange(6, 460)
        out += rect(x, y, 2, 2, accent, extra=f'opacity=".3" class="star s{i%3}"')
    for side, start in enumerate((0, 606)):
        for i in range(3):
            x = start + i * 12
            y = 110 + rng.randrange(20, 190)
            out += rect(x, y, 12, 480-y, '#0b1020')
            for j in range(10):
                if rng.random() > .48:
                    out += rect(x+3, y+8+j*14, 2, 4, GOLD, extra='opacity=".42"')
    out += path('M 8 452 H 18 M 622 452 H 632 M 12 42 V 16 H 42 M 598 16 H 628 V 42', '#49536d', 1)
    out += dot(595, 15, GOLD, 4) + dot(597, 13, '#141a30', 4)
    return out


def preview_edu(accent):
    out = text(376, 132, 'Notebook', 14, accent)
    out += chip(376, 146, 'notes', BLUE, 60) + chip(442, 146, 'media', GOLD, 60)
    out += rect(376, 181, 192, 64, '#202b42', 5)
    out += text(388, 201, 'Ask. Create. Learn.', 13, INK)
    out += lines(388, 215, [115, 153], BLUE)
    out += '<g class="answer">' + lines(388, 237, [124], accent) + '</g>'
    out += path('M 405 262 H 536 M 470 262 V 286', '#526581', 1.4)
    out += dot(405, 262, accent, 4) + dot(536, 262, LILAC, 4)
    out += '<g class="signal">' + dot(470, 262, GOLD, 4) + '</g>'
    out += chip(377, 285, 'Voice', accent, 74) + chip(464, 285, 'Canvas', LILAC, 87)
    return out


def preview_forge(accent):
    out = text(376, 132, 'Business question', 13, accent)
    out += rect(376, 146, 192, 27, '#25304a', 4) + text(386, 164, '本月经营趋势？', 13, INK)
    for y in (196, 222, 248):
        out += path(f'M 383 {y} H 560', '#2c3850', 1)
    out += path('M 383 255 V 185 M 383 255 H 560', '#54607a', 1)
    out += path('M 387 242 L 410 233 L 436 240 L 461 214 L 485 220 L 510 191 L 533 203 L 557 186', accent, 2.5, 'class="chart"')
    out += dot(557, 186, GOLD, 3.5, 'class="answer"')
    out += chip(376, 282, 'Evidence', BLUE, 91) + chip(476, 282, 'Report', GOLD, 82)
    return out


def preview_name(accent):
    out = text(376, 132, 'A name, a meaning', 13, accent)
    out += rect(376, 146, 192, 145, '#24293c', 6, 'stroke="#465068"')
    out += path('M 390 159 V 151 H 399 M 553 275 V 284 H 544', accent, 1)
    out += '<g class="name-reveal">'
    out += text(412, 207, '清和', 39, '#f0dbc0', 'font-family="Noto Serif SC,SimSun,serif" letter-spacing="8"')
    out += text(405, 233, '清朗 · 平和', 13, MUTED)
    out += '</g>' + path('M 405 248 H 539', '#566078', 1)
    out += text(405, 270, '寓意  /  偏好  /  比较', 12, accent)
    out += rect(542, 161, 12, 12, '#a76a67', 2)
    out += text(544, 170, '笺', 8, '#f9dfc7')
    out += text(376, 310, 'Generate → Refine → Compare', 10.5, MUTED)
    return out


def preview_portfolio(accent):
    out = text(376, 132, 'Creative portfolio', 13, accent)
    out += rect(376, 146, 192, 145, '#141c30', 5, 'stroke="#35445c"')
    out += text(390, 169, 'Ethan Chen', 18, INK)
    out += text(390, 186, 'Design meets engineering.', 9.5, accent)
    out += '<g class="orbit">'
    out += path('M 455 199 L 493 213 L 518 246 L 483 277 L 444 256 Z M 455 199 L 483 277 M 493 213 L 444 256 M 518 246 L 455 199 M 444 256 L 518 246', accent, 1.3)
    out += path('M 433 240 Q 480 198 534 242 Q 485 281 433 240', LILAC, .9)
    out += dot(493, 213, GOLD, 3)
    out += '</g>'
    out += text(376, 310, 'Scene / Motion / Interaction', 10.5, MUTED)
    return out


def preview_home(accent):
    out = text(376, 132, 'Personal homepage', 13, accent)
    out += rect(376, 146, 192, 145, '#e4dccf', 5)
    out += rect(376, 146, 192, 20, '#c9c4bf', 4)
    out += dot(386, 156, '#998c82', 2) + text(406, 159, 'a place for ideas', 9, '#504e59')
    out += '<g clip-path="url(#page-content)"><g class="scroll-page">'
    out += text(389, 188, 'Hello, I’m Ethan.', 15, '#3c4052')
    out += lines(389, 201, [92, 143], '#595c6f')
    out += rect(389, 228, 78, 45, '#97a9a5', 3) + rect(475, 228, 80, 45, '#bda899', 3)
    out += path('M 400 260 L 414 241 L 428 250 L 453 237', '#3f6561', 1.5)
    out += text(486, 257, '{ ideas }', 10, '#664f47')
    out += text(389, 298, 'Notes & experiments', 14, '#3c4052')
    out += lines(389, 309, [143, 114, 137], '#595c6f') + '</g></g>'
    out += text(376, 310, 'Narrative / Scroll / Canvas', 10.5, MUTED)
    return out


def preview_translate(accent):
    out = text(376, 132, 'Read. Save. Remember.', 12.5, accent)
    out += rect(376, 146, 192, 145, '#202b42', 5)
    out += lines(388, 163, [151, 104, 155], BLUE)
    out += rect(388, 202, 126, 21, accent, 3, 'fill-opacity=".12" class="word-focus"')
    out += text(394, 217, 'serendipity', 15, accent)
    out += '<g class="answer">' + rect(392, 234, 162, 42, '#303852', 4)
    out += text(402, 253, '偶然的美好发现', 13, INK)
    out += text(402, 269, 'Save to vocabulary  +', 10, GOLD) + '</g>'
    out += text(376, 310, 'Vocabulary / Flashcards / Review', 10, MUTED)
    return out


def preview_digest(accent):
    out = text(376, 132, 'A quieter information flow', 11.5, accent)
    out += rect(390, 159, 164, 139, '#242b41', 5, 'transform="rotate(4 472 225)"')
    out += rect(376, 148, 178, 143, '#ded9d1', 4)
    out += text(389, 170, 'Trending Digest', 15, '#344257')
    out += path('M 389 179 H 540', '#a6aaa9', 1)
    for i, (label, size) in enumerate([('GitHub', 104), ('Official sources', 125), ('Document preview', 111)]):
        y = 193+i*30
        out += rect(389, y, 6, 6, '#617a76', 1, f'class="digest-item d{i}"')
        out += text(403, y+7, label, 10.5, '#4b5968')
        out += lines(403, y+13, [size], '#7a8490')
    out += text(376, 310, 'Sources / Dedup / PDF + Word', 10.5, MUTED)
    return out


def preview_adaptive(accent):
    out = text(376, 132, 'Choose with evidence', 13, accent)
    positions = [(411,171,'Evidence'),(513,214,'Method'),(411,261,'Verify')]
    out += path('M 436 171 H 513 V 196 M 513 232 V 261 H 438', '#546383', 1.5)
    out += path('M 410 243 V 189', '#546383', 1.5, 'stroke-dasharray="3 4"')
    for i, (x,y,label) in enumerate(positions):
        out += rect(x-35, y-16, 76, 32, '#27334d', 5, f'stroke="{accent}" stroke-opacity=".35"')
        out += rect(x-35,y-16,76,32,accent,5,f'fill-opacity=".15" class="route r{i}"')
        out += text(x-27,y+4,label,12,INK)
    out += text(376, 310, 'Preserve progress. Check outcomes.', 10, MUTED)
    return out


PROJECTS = [
    dict(slug='educanvas', title='EduCanvas', file='notebook.ts', accent=GOLD, language='TypeScript', category='Learning agent', tags=['Agent','Canvas','Voice'],
         command='make doctor', result='make all', startup='repo root / shell', preview=preview_edu),
    dict(slug='forgesight', title='ForgeSight', file='analysis.py', accent=MINT, language='Python', category='Data intelligence', tags=['Query','Evidence','Modeling'],
         command='cd forge-sight', result=r'.\fs.bat', startup='Windows / startup', preview=preview_forge),
    dict(slug='naming', title='名笺 / Mingjian', file='preferences.ts', accent=GOLD, language='TypeScript', category='Names with meaning', tags=['Generate','Refine','Compare'],
         command='cd frontend', result='npm run dev', startup='frontend / dev', preview=preview_name),
    dict(slug='portfolio', title='Portfolio V5', file='scene.ts', accent=LILAC, language='TypeScript', category='Creative interaction', tags=['Three.js','GSAP','React'],
         command='npm install', result='npm run dev', startup='repo root / dev', preview=preview_portfolio),
    dict(slug='homepage', title='Personal Homepage', file='page.js', accent=BLUE, language='JavaScript', category='Visual storytelling', tags=['Narrative','Scroll','Canvas'],
         command='page.compose(sections)', result='content → layout → experience', preview=preview_home),
    dict(slug='translation', title='Translation', file='reader.js', accent=MINT, language='JavaScript', category='Reading to learning', tags=['Translate','Save','Review'],
         command='reader.lookup(selection)', result='read → translate → remember', preview=preview_translate),
    dict(slug='digest', title='GitHub Trending Digest', file='briefing.py', accent=GOLD, language='Python', category='Project in progress', tags=['Sources','Dedup','Preview'],
         command='briefing.preview(sources)', result='sources → deduplication → preview', preview=preview_digest),
    dict(slug='adaptive', title='Adaptive Workflow', file='workflow.yaml', accent=LILAC, language='YAML', category='Evidence before method', tags=['Evidence','Method','Verify'],
         command='workflow.choose(evidence)', result='inspect → choose → verify', preview=preview_adaptive),
]

# Large README excerpts remain legible at GitHub's ~400px card width.
PROJECT_NOTES = {
    'educanvas': ('EduCanvas', 'Ask. Create. Learn.', ['多模态对话与学习画布', '文件预览与桌面助手']),
    'forgesight': ('ForgeSight', 'Questions into insight.', ['自然语言问析与证据追溯', '经营看板与智能建模']),
    'naming': ('名笺', 'A name with meaning.', ['偏好生成与多轮调整', '寓意分析与名字比较']),
    'portfolio': ('Portfolio V5', 'A space for my work.', ['个人品牌与创意视觉', '3D 场景与页面转场']),
    'homepage': ('Personal Homepage', 'Stories, in motion.', ['页面叙事与滚动动效', '内容编排与绘图空间']),
    'translation': ('Translation', 'Read. Save. Remember.', ['网页翻译与生词管理', '闪卡练习与间隔复习']),
    'digest': ('Trending Digest', 'Less noise. More context.', ['信息来源与事件去重', '摘要整理与文档预览']),
    'adaptive': ('Adaptive Workflow', 'Evidence before method.', ['依据证据与风险选方法', '保留成果并验证结果']),
}


def build(project, index):
    p = project
    slug, accent = p['slug'], p['accent']
    headline, strap, features = PROJECT_NOTES[slug]
    code = ''.join(text(51, 148+i*29, str(i+1), 11, '#55617b') for i in range(5))
    code += text(73, 149, '#', 24, '#677184') + text(97, 149, headline, 22 if len(headline)>16 else 25, accent, 'font-weight="600"')
    code += text(73, 179, '> '+strap, 15.5, INK, 'font-style="italic"')
    code += ''.join(text(73, 227+i*29, '- '+feature, 17, INK) for i,feature in enumerate(features))
    command, animation_rules = typed(83, 372, p['command'], .5, 1.6, INK, slug)
    result, more_rules = typed(63, 397, p['result'], 3.1, 1.4, accent, slug+'-result')
    css = '''
    @keyframes cursor {0%,48%{opacity:1}49%,100%{opacity:0}}
    @keyframes twinkle {0%,100%{opacity:.2}50%{opacity:.55}}
    @keyframes answer {0%,25%{opacity:.25}43%,91%{opacity:1}100%{opacity:.25}}
    @keyframes chart {0%,18%{stroke-dashoffset:260}48%,92%{stroke-dashoffset:0}100%{stroke-dashoffset:260}}
    @keyframes name {0%,15%{opacity:.45}40%,94%{opacity:1}100%{opacity:.45}}
    @keyframes orbit {0%,100%{transform:rotate(-7deg)}50%{transform:rotate(7deg)}}
    @keyframes scroll {0%,22%,100%{transform:translateY(0)}55%,82%{transform:translateY(-49px)}}
    @keyframes focus {0%,18%,100%{fill-opacity:.12}40%,85%{fill-opacity:.45}}
    @keyframes item {0%,24%{opacity:.35}50%,94%{opacity:1}100%{opacity:.35}}
    @keyframes route {0%,15%,100%{opacity:0}27%,40%{opacity:1}53%,95%{opacity:.15}}
    @keyframes signal {0%,100%{opacity:.2}50%{opacity:1}}
    .cursor{animation:cursor 1.25s step-end infinite}
    .star{animation:twinkle 6s ease-in-out infinite}.s1{animation-delay:-2s}.s2{animation-delay:-4s}
    .answer{animation:answer 10s ease-in-out infinite}
    .chart{stroke-dasharray:260;animation:chart 10s ease-in-out infinite}
    .name-reveal{animation:name 10s ease-in-out infinite}
    .orbit{transform-box:fill-box;transform-origin:center;animation:orbit 10s ease-in-out infinite}
    .scroll-page{animation:scroll 10s ease-in-out infinite}
    .word-focus{animation:focus 10s ease-in-out infinite}
    .digest-item{animation:item 10s ease-in-out infinite}.d1{animation-delay:.5s}.d2{animation-delay:1s}
    .route{animation:route 10s ease-in-out infinite}.r1{animation-delay:1.8s}.r2{animation-delay:3.6s}
    .signal{animation:signal 4s ease-in-out infinite}
    @media(prefers-reduced-motion:reduce){*{animation:none!important}.chart{stroke-dashoffset:0}}
    ''' + animation_rules + more_rules
    out = f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" viewBox="0 0 640 480" role="img" aria-labelledby="title desc"><title id="title">{escape(p["title"])} — 像素夜景编辑器</title><desc id="desc">项目概念动画，展示 {escape(p["category"])}。代码与终端内容为功能示意，不代表实际运行记录。</desc><style>{css}</style>'
    out += '<defs><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#080c19" flood-opacity=".5"/></filter><clipPath id="page-content"><rect x="382" y="169" width="180" height="115"/></clipPath></defs>'
    out += pixel_night(index+16, accent)
    out += '<g font-family="Cascadia Code,Consolas,Microsoft YaHei,monospace">'
    out += rect(24,30,592,423,'#101829',8,'stroke="#3b4661" filter="url(#shadow)"')
    out += rect(25,31,590,34,'#252d46',7) + rect(25,55,590,10,'#252d46')
    for x,c in zip((41,54,67),('#af8286','#c4a379','#7fada0')):
        out += dot(x,48,c,3.5)
    out += text(87,52,p['title'],14,INK)
    out += text(600,52,'Ethan’s atelier',10,MUTED,'text-anchor="end"')
    out += rect(25,65,590,28,'#192237')
    out += rect(39,65,170,28,'#101829') + rect(39,65,170,2,accent)
    out += text(52,84,'M↓  README.md',12,accent) + text(231,84,'□  Preview',11,MUTED)
    out += rect(42,106,304,210,'#101829',3)
    out += rect(359,106,225,216,'#182238',5,'stroke="#2e3b53"')
    out += code
    out += rect(75,270,2,17,accent,extra='class="cursor"')
    x = 73
    for tag in p['tags']:
        width = len(tag)*7.2+18
        out += chip(x,294,tag,accent,width)
        x += width+6
    out += p['preview'](accent)
    out += path('M 25 330 H 615','#344058',1)
    out += rect(25,331,590,97,'#0d1424')
    out += text(44,348,'TERMINAL',10,accent) + rect(44,352,59,1,accent)
    out += text(127,348,'OUTPUT',10,'#58677f') + text(594,348,p.get('startup','concept session'),10,'#64718a','text-anchor="end"')
    out += text(44,372,'❯',14,accent) + command + text(44,397,'❯' if p.get('startup') else '↳',14,accent if p.get('startup') else MUTED) + result
    out += rect(25,429,590,23,'#27334d',0) + text(39,445,'⎇ main',11,accent)
    out += dot(115,440,accent,2.5,'class="signal"') + text(126,445,'product sketch',10,MUTED)
    out += text(598,445,p['language']+'   UTF-8',10,MUTED,'text-anchor="end"')
    out += '</g></svg>'
    # Parse every artifact before it can be written.
    ET.fromstring(out)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for index,p in enumerate(PROJECTS):
        svg=build(p,index)
        (OUT/(p['slug']+'.svg')).write_text(svg,encoding='utf-8')
        print(f'{p["slug"]}: {len(svg.encode("utf-8")):,} bytes')


if __name__=='__main__':
    main()
