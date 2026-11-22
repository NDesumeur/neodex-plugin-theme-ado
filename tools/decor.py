# Le décor du thème Ado, rangé dans ado.css (entre /*decor*/ et /*/decor*/) ; les images (dossier img, préparées par tools/images.py) sont
# mises dans le fichier, rien ne vient d'Internet.
#  - le fond : l'illustration, assombrie sur les bords pour que les cadres restent lisibles ;
#  - les roses bleues dans les coins, tournées vers le milieu, avec des autocollants gyaru qui scintillent (cœurs, strass, « GYARU » en rouge, « Ado♡ ») ;
#  - Abo (la peluche du mème « I am Ado ») assis en bas à droite de chaque cadre ; il se promène dans la barre des tâches (ado-barre.css, entre /*abo*/ et /*/abo*/) ;
#  - en bas, la liste de ses chansons qui défile comme l'écran d'une scène (les titres seulement).
# La police : Rampart One (fonts/RampartOne.woff2, licence SIL OFL 1.1), elle aussi rangée dans ado.css (entre /*font*/ et /*/font*/).
# python tools/decor.py   (depuis le dossier du plugin)
import base64, re, urllib.parse

def b64(f, mime):
    return 'url("data:' + mime + ';base64,' + base64.b64encode(open('img/' + f, 'rb').read()).decode() + '")'

def uri(s):  # une image SVG dans le CSS ; les parenthèses sont codées pour que NeoDex ne les prenne pas pour un lien
    return 'url("data:image/svg+xml,' + urllib.parse.quote(s, safe=" =:/;,'-.") + '")'

JP = "font-family='Segoe UI Black,Arial Black,Arial,sans-serif' font-weight='900'"
TW = "<animate attributeName='opacity' values='{a};1;{a}' dur='{d}s' begin='{b}s' repeatCount='indefinite'/>"

def spark(x, y, s, d=1.6, b=0):  # une étincelle qui scintille
    return (f"<path d='M{x} {y-s} L{x+s*.22:.1f} {y-s*.22:.1f} L{x+s} {y} L{x+s*.22:.1f} {y+s*.22:.1f} L{x} {y+s} L{x-s*.22:.1f} {y+s*.22:.1f} L{x-s} {y} L{x-s*.22:.1f} {y-s*.22:.1f}Z' fill='#fff'>"
            + TW.format(a=.15, d=d, b=b) + "</path>")

def heart(x, y, s, c, rot=0, stroke='#fff'):
    return (f"<path transform='translate({x} {y}) rotate({rot}) scale({s})' d='M0 8 C-14 -2 -12 -14 -4 -14 C-1 -14 0 -11 0 -9 C0 -11 1 -14 4 -14 C12 -14 14 -2 0 8Z' "
            f"fill='{c}' stroke='{stroke}' stroke-width='{2.4/s:.2f}' stroke-linejoin='round'/>")

def gem(x, y, r, b=0):  # un strass : un rond brillant avec son reflet
    return (f"<circle cx='{x}' cy='{y}' r='{r}' fill='#cfe6ff' stroke='#2f6bff' stroke-width='1'/><circle cx='{x-r*.3:.1f}' cy='{y-r*.3:.1f}' r='{r*.35:.1f}' fill='#fff'>"
            + TW.format(a=.3, d=1.3, b=b) + "</circle>")

def sticker(x, y, rot, text, size, fg, bg):  # un autocollant façon purikura : texte épais, contour blanc, ombre
    return (f"<g transform='translate({x} {y}) rotate({rot})'><text {JP} font-size='{size}' text-anchor='middle' fill='none' stroke='#02061a' stroke-width='{size*.42:.1f}' stroke-linejoin='round' transform='translate(3 3)'>{text}</text>"
            f"<text {JP} font-size='{size}' text-anchor='middle' fill='none' stroke='{bg}' stroke-width='{size*.34:.1f}' stroke-linejoin='round'>{text}</text>"
            f"<text {JP} font-size='{size}' text-anchor='middle' fill='{fg}'>{text}</text></g>")

def svg(w, h, body):
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{body}</svg>"

# les autocollants gyaru autour de chaque rose (un jeu par coin)
DECO_TL = svg(300, 260, sticker(180, 64, -12, 'GYARU', 40, '#ff2d55', '#fff') + heart(250, 120, 1.4, '#ff6fb5', 15) + heart(70, 210, 1, '#2f6bff', -20)
              + gem(120, 30, 6) + gem(140, 22, 4, .4) + gem(156, 30, 3, .8) + spark(270, 30, 12) + spark(40, 150, 9, 2.1, .6) + spark(230, 200, 7, 1.8, 1))
DECO_TR = svg(300, 260, heart(50, 150, 1.2, '#2f6bff', -15) + heart(240, 220, .9, '#ff6fb5', 20)
              + gem(200, 120, 6, .2) + gem(214, 132, 4, .7) + spark(30, 40, 11, 1.7, .3) + spark(260, 170, 8, 2, .9))
DECO_BL = svg(300, 260, heart(260, 140, 1.3, '#ff6fb5', 12) + gem(240, 90, 6, .5) + gem(256, 80, 4)
              + spark(40, 40, 10, 1.9, .2) + spark(280, 40, 8, 1.5, .8))
DECO_BR = svg(300, 260, sticker(130, 220, -8, 'Ado♡', 32, '#fff', '#2f6bff') + heart(40, 120, 1.3, '#2f6bff', -12) + heart(70, 60, .8, '#ff6fb5', 18)
              + gem(30, 190, 6, .3) + gem(46, 200, 4, .9) + spark(260, 50, 11, 1.6, .5) + spark(20, 30, 7, 2.2))

# la bulle « I am Abo » au-dessus d'Abo quand il se promène
BUBBLE = svg(150, 70, "<path d='M10 6 H140 Q146 6 146 12 V44 Q146 50 140 50 H62 L44 66 L48 50 H10 Q4 50 4 44 V12 Q4 6 10 6Z' fill='#fff' stroke='#02061a' stroke-width='3'/>"
                      "<text x='75' y='37' font-family='Segoe UI,Arial,sans-serif' font-size='22' text-anchor='middle' fill='#02061a'>I am Abo</text>")

# la liste des titres qui défile en bas (les titres seulement), séparés par des cœurs
SONGS = ['Usseewa', 'Shinjidai', 'Show', 'Odo', 'Watashi wa Saikyou', 'Gyakkou', 'Gira Gira', 'Ashura-chan', 'Readymade', 'Yoru no Pierrot', 'Kura Kura', 'Tot Musica', 'Aishite Aishite Aishite', 'Value', 'Zanmu']
x, parts = 20, []
for s in SONGS:
    parts.append(f"<text x='{x}' y='24' {JP} font-size='20' fill='#cfe2ff'>{s}</text>")
    x += round(len(s) * 12.5) + 18
    parts.append(heart(x, 18, .8, '#2f6bff', 0, '#cfe2ff')); x += 30
TICK_W = x
TICK = svg(TICK_W, 34, ''.join(parts))

def css():
    hg, hd, bg, bd, abo = (b64(f, 'image/png') for f in ('rose-hg.png', 'rose-hd.png', 'rose-bg.png', 'rose-bd.png', 'abo.png'))
    R = 'clamp(150px,14vw,260px)'   # la taille des roses
    D = 'clamp(170px,16vw,300px)'   # celle de leurs autocollants
    return (
        # Abo une seule fois dans le fichier : les deux endroits qui le montrent passent par --abo
        f'html[data-style]{{--abo:{abo};--rose:{bg}}}'  # la rose du coin en bas à gauche sert aussi devant le titre
        # le fond : l'illustration, sombre sur les bords et en bas
        'html[data-style]{background:radial-gradient(ellipse 75% 80% at 55% 40%,rgba(3,5,11,.12),rgba(3,5,11,.72) 100%),'
        'linear-gradient(to bottom,rgba(3,5,11,.3),rgba(3,5,11,.05) 40%,rgba(3,5,11,.7)),'
        f'{b64("fond.jpg", "image/jpeg")} 50% 30%/cover no-repeat fixed,#03050b}}'
        'html[data-style] body{background:transparent}'
        # les roses dans les coins, leurs autocollants, la liste des chansons
        'html[data-style] body::before{content:"";position:fixed;left:56px;right:0;top:44px;bottom:0;z-index:1;pointer-events:none;background:'
        f'{uri(DECO_TL)} 0 0/{D} auto no-repeat,{uri(DECO_TR)} 100% 0/{D} auto no-repeat,'
        f'{uri(DECO_BL)} 0 calc(100% - 34px)/{D} auto no-repeat,{uri(DECO_BR)} 100% calc(100% - 34px)/{D} auto no-repeat,'
        f'{hg} -46px -46px/{R} auto no-repeat,{hd} calc(100% + 46px) -46px/{R} auto no-repeat,'
        f'var(--rose) -46px calc(100% + 12px)/{R} auto no-repeat,{bd} calc(100% + 46px) calc(100% + 12px)/{R} auto no-repeat,'
        f'linear-gradient(90deg,transparent,#2f6bff 20%,#ff2d55 50%,#2f6bff 80%,transparent) 0 calc(100% - 33px)/100% 2px no-repeat,'
        f'linear-gradient(180deg,rgba(23,57,184,.55),rgba(3,5,11,.95)) 0 100%/100% 34px no-repeat,{uri(TICK)} 0 calc(100% - 1px)/{TICK_W}px 34px repeat-x;'
        'filter:drop-shadow(0 0 10px rgba(47,107,255,.45));animation:adoTicker 70s linear infinite}'
        '@keyframes adoTicker{from{background-position:0 0,100% 0,0 calc(100% - 34px),100% calc(100% - 34px),-46px -46px,calc(100% + 46px) -46px,-46px calc(100% + 12px),calc(100% + 46px) calc(100% + 12px),0 calc(100% - 33px),0 100%,0 calc(100% - 1px)}'
        f'to{{background-position:0 0,100% 0,0 calc(100% - 34px),100% calc(100% - 34px),-46px -46px,calc(100% + 46px) -46px,-46px calc(100% + 12px),calc(100% + 46px) calc(100% + 12px),0 calc(100% - 33px),0 100%,-{TICK_W}px calc(100% - 1px)}}}}'
        # Abo assis en bas à droite de chaque cadre
        'html[data-style] .panel{position:relative}'
        'html[data-style] .panel::after{content:"";position:absolute;right:10px;bottom:-14px;width:46px;height:56px;background:var(--abo) 50% 100%/contain no-repeat;'
        'pointer-events:none;filter:drop-shadow(0 3px 4px rgba(0,0,0,.6));transform-origin:50% 100%;transition:transform .25s}'
        'html[data-style] .panel:hover::after{transform:rotate(-8deg) scale(1.12)}'
    )

# Abo qui se promène dans la barre des tâches, en se dandinant : il va jusqu'au bout, se retourne et revient ; les clics passent à travers lui
def bar_css():
    abo = b64('abo.png', 'image/png')
    return ('html[data-style]::after{content:"";position:fixed;left:0;bottom:1px;width:28px;height:34px;z-index:5;pointer-events:none;'
            f'background:{abo} 50% 100%/contain no-repeat;filter:drop-shadow(0 2px 3px rgba(0,0,0,.7));transform-origin:50% 100%;'
            'animation:adoBarWalk 70s linear infinite,adoBarWaddle .7s ease-in-out infinite alternate}'
            '@keyframes adoBarWalk{0%{translate:-30px 0;scale:1 1}49.9%{translate:calc(100vw + 2px) 0;scale:1 1}50%{translate:calc(100vw + 2px) 0;scale:-1 1}99.9%{translate:-30px 0;scale:-1 1}100%{translate:-30px 0;scale:1 1}}'
            '@keyframes adoBarWaddle{from{rotate:-7deg}to{rotate:7deg}}')

if __name__ == '__main__':
    b = open('ado-barre.css', encoding='utf-8').read()
    b = re.sub(r'\n?/\*abo\*/.*?/\*/abo\*/', '', b, flags=re.S).rstrip('\n') + '\n/*abo*/' + bar_css() + '/*/abo*/\n'
    open('ado-barre.css', 'w', encoding='utf-8', newline='\n').write(b)
    c = open('ado.css', encoding='utf-8').read()
    c = re.sub(r'/\*decor\*/.*?/\*/decor\*/', lambda m: '/*decor*/' + css() + '/*/decor*/', c, flags=re.S)
    # la police Rampart One (Fontworks, licence SIL OFL 1.1), réduite aux lettres latines, accents, chiffres et cœurs
    font = 'url("data:font/woff2;base64,' + base64.b64encode(open('fonts/RampartOne.woff2', 'rb').read()).decode() + '")'
    c = re.sub(r'/\*font\*/.*?/\*/font\*/', lambda m: "/*font*/@font-face{font-family:'Rampart One';src:" + font + " format('woff2')}/*/font*/", c, flags=re.S)
    open('ado.css', 'w', encoding='utf-8', newline='\n').write(c)
    print('décor :', len(css()), 'caractères · ado.css :', len(c))
