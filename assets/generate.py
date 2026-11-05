"""Rebuild pixel assets: python assets/generate.py (requires Pillow)."""
from pathlib import Path
from collections import deque
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
    snake = deque([(10-i,3) for i in range(9)])
    target, eaten, flash = (28,1), 0, 0
    history, frames = set(), []

    def path(goal):
        queue, seen = deque([(snake[0],[])]), {snake[0]}
        occupied = set(list(snake)[:-1])
        while queue:
            (x,y), route = queue.popleft()
            if (x,y) == goal:
                return route
            neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            rng.shuffle(neighbors)
            for p in neighbors:
                if 0 <= p[0] < 53 and 0 <= p[1] < 7 and p not in seen and p not in occupied:
                    seen.add(p)
                    queue.append((p,route+[p]))
        return []

    for tick in range(510):
        if tick:
            route = path(target)
            assert route, 'Target must remain reachable'
            snake.appendleft(route[0])
            snake.pop()
            assert len(set(snake)) == len(snake)
            if snake[0] == target:
                eaten += 1
                flash = 5
                history.add(target)
                options = [(x,y) for x in range(53) for y in range(7) if (x,y) not in snake and abs(x-snake[0][0])+abs(y-snake[0][1]) > 13]
                rng.shuffle(options)
                target = next(p for p in options if path(p))
        im = canvas(250)
        d = ImageDraw.Draw(im)
        d.text((36,21), 'SNAKE / DEPLOY FEED', font=FONT, fill=GREEN)
        d.text((727,21), f'DEPLOYS COLLECTED  {eaten:02d}', font=FONT, fill=LIGHT)
        for m,label in enumerate(['NOV','DEC','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT']):
            d.text((53+m*76,57), label, font=SMALL, fill=MUTED)
        for x in range(53):
            for y in range(7):
                px,py = 53+x*17,81+y*17
                d.rectangle((px,py,px+12,py+12), fill='#1b3c29' if (x,y) in history else '#14291e')
        tx,ty = 53+target[0]*17,81+target[1]*17
        d.rectangle((tx-2,ty-2,tx+14,ty+14), outline=GREEN if tick%8<4 else '#2b7145')
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
        status = f'DEPLOY {eaten:02d} ABSORBED +1' if flash else f'NEXT DEPLOY  [{target[0]:02d}:{target[1]:02d}]'
        d.text((36,218), status, font=SMALL, fill=GREEN)
        d.text((692,218), 'PIXEL SIMULATION / ALWAYS GROWING', font=SMALL, fill=MUTED)
        flash = max(0,flash-1)
        frames.append(im)
    last = frames[-1]
    for width in range(0,1001,100):
        im = last.copy()
        ImageDraw.Draw(im).rectangle((0,0,width,249), fill=BG)
        frames.append(im)
    for width in range(0,1001,100):
        im = frames[0].copy()
        ImageDraw.Draw(im).rectangle((width,0,1000,249), fill=BG)
        frames.append(im)
    frames[0].save(ROOT/'deploy-snake.gif', save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True, disposal=1)
    frames[150].save(ROOT/'deploy-snake-preview.png')
    assert eaten >= 10
    print(f'{len(frames)} frames; {eaten} deploys; {len(frames)*.09:.1f}s loop')


if __name__ == '__main__':
    header()
    animation()
