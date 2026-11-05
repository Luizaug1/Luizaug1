"""Rebuild pixel assets: python assets/generate.py (requires Pillow)."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BG, GREEN, LIGHT, MUTED = '#07110d', '#59f58a', '#d6ffe3', '#7ea68c'
FONT = ImageFont.load_default(size=14)
SMALL = ImageFont.load_default(size=11)


def canvas(h):
    im = Image.new('RGB', (1000, h), BG)
    ImageDraw.Draw(im).rounded_rectangle((1, 1, 998, h-2), radius=14, outline='#254b35', width=2)
    return im


def header():
    im = canvas(260)
    d = ImageDraw.Draw(im)
    d.text((36,28), 'LUIZ AUGUSTO  /  SOFTWARE DEVELOPER', font=FONT, fill=GREEN)
    d.text((33,69), 'DEPLOY GARDEN', font=ImageFont.load_default(size=49), fill=LIGHT)
    d.text((36,143), 'Ideias criam raizes. Sistemas ganham vida.', font=ImageFont.load_default(size=20), fill=MUTED)
    d.line((36,192,964,192), fill='#254b35')
    d.text((36,215), 'IA & AUTOMACOES     /     SAAS & APIS     /     BUILD. SHIP. GROW.', font=FONT, fill=GREEN)
    im.save(ROOT/'deploy-garden-header.png')


def animation():
    rng = random.Random(20261105)
    # A closed, self-avoiding route makes the last -> first frame a normal step.
    route = ([(x,1) for x in range(2,51)] + [(50,y) for y in range(2,6)]
             + [(x,5) for x in range(49,1,-1)] + [(2,y) for y in range(4,1,-1)])
    for _ in range(2400):
        j = rng.randrange(len(route))
        a, b = route[j], route[(j+1)%len(route)]
        dx, dy = b[0]-a[0], b[1]-a[1]
        side = rng.choice([-1,1])
        c = (a[0]-dy*side, a[1]+dx*side)
        e = (b[0]-dy*side, b[1]+dx*side)
        if all(0<=v[0]<53 and 0<=v[1]<7 and v not in route for v in (c,e)):
            route[j+1:j+1] = [c,e]
    n = len(route)
    assert len(set(route)) == n
    assert all(abs(route[i][0]-route[(i+1)%n][0])+abs(route[i][1]-route[(i+1)%n][1]) == 1 for i in range(n))
    # Irregular intervals; targets, flashes and snake state are all periodic.
    targets, cursor = [], 8
    while cursor < n-12:
        targets.append(cursor)
        cursor += rng.randint(13,25)
    frames = []
    for tick in range(n):
        snake = [route[(tick-i)%n] for i in range(9)]
        target_index = next((v for v in targets if v>tick), targets[0])
        target = route[target_index]
        last_collect = min((tick-v)%n for v in targets)
        flash = last_collect < 4
        im = canvas(250)
        d = ImageDraw.Draw(im)
        d.text((36,21), 'SNAKE / DEPLOY FEED', font=FONT, fill=GREEN)
        d.text((727,21), 'DEPLOY FEED / ACTIVE', font=FONT, fill=LIGHT)
        for m,label in enumerate(['NOV','DEC','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT']):
            d.text((53+m*76,57), label, font=SMALL, fill=MUTED)
        for x in range(53):
            for y in range(7):
                px,py = 53+x*17,81+y*17
                d.rectangle((px,py,px+12,py+12), fill='#14291e')
        tx,ty = 53+target[0]*17,81+target[1]*17
        d.rectangle((tx-2,ty-2,tx+14,ty+14), outline=GREEN if (target_index-tick)%8<4 else '#2b7145')
        d.rectangle((tx+3,ty+3,tx+9,ty+9), fill=LIGHT)
        for i,(x,y) in reversed(list(enumerate(snake))):
            px,py = 53+x*17,81+y*17
            color = GREEN if i<4 else '#2eaa5d'
            if i:
                nx,ny = snake[i-1]
                d.rectangle((min(px,53+nx*17)+3,min(py,81+ny*17)+3,max(px,53+nx*17)+10,max(py,81+ny*17)+10), fill=color)
            d.rectangle((px,py,px+13,py+13), fill=LIGHT if i==0 else color)
        hx,hy = snake[0]
        dx,dy = hx-snake[1][0],hy-snake[1][1]
        px,py = 53+hx*17,81+hy*17
        eyes = [(10 if dx>0 else 2,3),(10 if dx>0 else 2,9)] if dx else [(3,10 if dy>0 else 2),(9,10 if dy>0 else 2)]
        for ex,ey in eyes:
            d.rectangle((px+ex,py+ey,px+ex+2,py+ey+2), fill=BG)
        status = 'DEPLOY ABSORBED +1' if flash else f'NEXT DEPLOY  [{target[0]:02d}:{target[1]:02d}]'
        d.text((36,218), status, font=SMALL, fill=GREEN)
        d.text((692,218), 'PIXEL SIMULATION / ALWAYS GROWING', font=SMALL, fill=MUTED)
        frames.append(im)
    frames[0].save(ROOT/'deploy-snake.gif', save_all=True, append_images=frames[1:], duration=160, loop=0, optimize=True, disposal=1)
    frames[150].save(ROOT/'deploy-snake-preview.png')
    assert snake[0] == route[-1]
    assert [route[(0-i)%n] for i in range(1,9)] == snake[:8]
    print(f'{n} frames; {len(targets)} targets; {n*.16:.1f}s seamless loop')


if __name__ == '__main__':
    header()
    animation()
