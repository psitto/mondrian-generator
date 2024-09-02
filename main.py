from pygame import *
from random import *
from sys import argv
from time import sleep, time
import os

SEED_CASE_SENSITIVE = False
LINE_WIDTH = 4 # for each rect (doubled in practice)
BLACK_COLOR = "gray7"
COLOR_WEIGHTS = {
    "red": 1,
    "blue": 1,
    "yellow": 1,
    "white": 5,
    BLACK_COLOR: 0.5,
    "gray": 1
}
DRAWING_FREQ = 60
DIV_DISTANCE_MIN = 96
DIV_MARGIN = 64
DIV_AMOUNT_RANGE = range(3, 5)
DIV_OPTIONS = [2/3, 1/2, 1/3, 1/4]
DIV_SIZE_MIN = 80
DIV_HORIZONTAL_CHANCE = 0.5
DIV_CHANCE = 0.7
DIV_FIRST_MAX = 0.5


if(len(argv) > 1):
    if SEED_CASE_SENSITIVE:
        seed(argv[1])
    else:
        seed(argv[1].lower())
else:
    seed(time())

def generate_main_rects() -> list:
    def generate_axis_divisions(extent: int): # includes 0 and extent
        divs = [ 0, randrange(DIV_MARGIN, int(extent*DIV_FIRST_MAX)) ]
        for __ in range(randrange(DIV_AMOUNT_RANGE.start, DIV_AMOUNT_RANGE.stop)):
            spaceleft = extent - divs[-1] - DIV_DISTANCE_MIN - DIV_MARGIN
            if spaceleft <= 0:
                break
            divs.append(divs[-1] + DIV_DISTANCE_MIN + int(spaceleft * random()))
        divs.append(extent)
        return divs
    
    xdivs = generate_axis_divisions(wwidth)
    ydivs = generate_axis_divisions(wheight)

    rects = []
    for i in range(len(xdivs)-1):
        x = xdivs[i]
        nextx = xdivs[i + 1]
        for j in range(len(ydivs)-1):
            y = ydivs[j]
            nexty = ydivs[j + 1]
            rects.append(Rect(x, y, nextx - x, nexty - y))
    return rects

def divide_rect(r: Rect):
    isvdiv = random() > DIV_HORIZONTAL_CHANCE
    if isvdiv: # if division is vertical
        dw = int(r.width * choice(DIV_OPTIONS))
        r1 = Rect(r.left, r.top, dw, r.height)
        r2 = Rect(r.left + dw, r.top, r.width - dw, r.height)
    else:
        dh = int(r.height * choice(DIV_OPTIONS))
        r1 = Rect(r.left, r.top, r.width, dh)
        r2 = Rect(r.left, r.top + dh, r.width, r.height - dh)
    return [r1, r2]

def make_divisions(rects: list): # recursive
    result = []
    for r in rects:
        if random() > DIV_CHANCE or r.width < DIV_SIZE_MIN or r.height < DIV_SIZE_MIN:
            result.append(r)
        else:
            result += make_divisions(divide_rect(r))
    return result

def adjust_size_for_drawing(r: Rect): # makes it so that rect can be drawn with LINE_WIDTH * 2, which looks better
    r.left -= LINE_WIDTH
    r.top -= LINE_WIDTH
    r.width += LINE_WIDTH*2
    r.height += LINE_WIDTH*2
    return r

if __name__ == "__main__":
    init()
    wsize = (768, 768)
    wwidth, wheight = wsize
    sfc = display.set_mode(wsize)
    display.set_caption("Mondrian Emulator")

    # https://ambientcg.com/view?id=Fabric036 adapted
    canvastex = image.load(os.path.join(os.path.dirname(__file__), "Fabric036_2K_Color.png"))

    mainrects = generate_main_rects()
    divs = make_divisions(mainrects)
    shuffle(divs)

    sfc.fill("white")
    for r in mainrects:
        draw.rect(sfc, BLACK_COLOR, r, LINE_WIDTH)
        display.flip()
        sleep(1/DRAWING_FREQ)
    for d in divs:
        dadj = adjust_size_for_drawing(d)
        clr = choices(population=list(COLOR_WEIGHTS.keys()), weights=list(COLOR_WEIGHTS.values()))[0]
        draw.rect(sfc, clr, d)
        draw.rect(sfc, BLACK_COLOR, dadj, LINE_WIDTH*2)
        display.flip()
        sleep(1/DRAWING_FREQ)
    sfc.blit(canvastex, (0, 0), special_flags=BLEND_MULT)
    display.flip()

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
    quit()