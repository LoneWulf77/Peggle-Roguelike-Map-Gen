# doug doug's twitch chat peggle roguelike stream
# -build a map/hero generator
# -idea to show the chapter number on all hidden slots, only show the levels of the next row
# -future qol plan, have integration with peggle to auto open/select hero


# currently want to auto populate map first
# second is add ui to handle inventory

#  will need to remove the option on each choice, or minimize duplicates

# image filenames for levels should be named in the style "1-1.png"
# image for heroes should be named matching the heroes list "Bjorn.png"


import random
import math
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("C:\Windows\Fonts\ARLRDBD.TTF", 30)

# draw board
board = Image.open('images/board.png').convert("RGBA")

# board coords list
# canvas 950 x 1350
# 490/180                                   x=185
# 235/380 515/380 750/380                   x=380
# 125/560 320/560 485/560 670/560 870/560   x=560
# 200/730 430/730 650/730 820/730           x=730
# 80/910 270/910 460/910 720/910 900/910    x=910
# 260/1080 520/1080 840/1080                x=1080
row1 = [493]
row2 = [235, 493, 727]
row3 = [100, 298, 468, 643, 853]
row4 = [180, 412, 630, 800]
row5 = [60, 250, 438, 695, 875]
row6 = [235, 500, 815]
row_height = [180, 375, 555, 730, 910, 1085]

# 2d array of the above
rows, cols = (6, 5)
coords = [row1, row2, row3, row4, row5, row6]

#chapters in game
chap = 11
#levels per chapter
lvls = 5

# array of all peggle maps (constant)
LEVELS = []
for chapter in range(chap):
    for level in range(lvls):
        LEVELS.append(str(chapter + 1) + '-' + str(level + 1))

unique_stages = LEVELS.copy()
total_stages = len(LEVELS)
stage = ""

# array/list of all heroes (constant)
HEROES = ["Bjorn", "Jimmy", "Kat", "Splork", "Claude", "Renfield", "Tula", "Warren", "Cinderbottom", "Hu"]
unique_heroes = HEROES.copy()
total_heroes = len(HEROES)
hero = ""


# array/list of main map
main_map = []

print("unique_heroes[] ", unique_heroes)

# add chapter-level and hero to map slot
def stage_roll(difficulty):
    global stage
    global LEVELS
    if len(unique_stages) <= len(LEVELS)/3:
        print("not enough levels")
        quit()
    match difficulty:
        case "easy":
            stage = unique_stages.pop(random.randint(0, math.ceil(total_stages * .33)))
        case "medium":
            stage = unique_stages.pop(random.randint(math.floor(total_stages * .33), math.ceil(total_stages * .66)))
        case "hard":
            stage = unique_stages.pop(random.randint(math.floor(total_stages * .66), math.ceil(total_stages - 6)))
        case "boss":
            stage = unique_stages.pop(random.randint(total_stages - 6, total_stages - 1))

    return stage

def hero_roll():
    # roll rng, pull a hero from array, put in main map/dict
    global unique_heroes
    global hero
    if len(unique_heroes) <= math.ceil(total_heroes/3):
        unique_heroes = HEROES.copy()
    hero = unique_heroes.pop(random.randint(0, len(unique_heroes)-1))
    return hero

def add_slot(diff):
    # add slot to main_map
    slot = stage_roll(diff) + " " + hero_roll()
    main_map.append(slot)


# roll rng, pull 3 heroes from array, put in starting inventory (unique ideally)
inventory = random.sample(HEROES, 3)

# generate main_map slots
# how many rows in map? how many slots per row (range 3-5?)

# hard coding number of slots for each difficulty based on board map
boss = 1
hard = 3
medium = 9
easy = 8

# add boss
add_slot("boss")
# add hard
for i in range(hard):
    add_slot("hard")
# add medium
for i in range(medium):
    add_slot("medium")
# add easy
for i in range(easy):
    add_slot("easy")

print("main_map[] = ", main_map)
print("inventory ", inventory)


main_map_i = 0  # main_map[] iterator

# cycle through main_map to add images to board
for i in range(rows):
    x = row_height[i]

    for j in range(len(coords[i])) :

        #break if main_map[x] out of range
        if main_map_i >= len(main_map):
            break

        stage = Image.open("images/stages/" + main_map[main_map_i].split()[0] + ".webp").convert("RGBA")
        stage = stage.resize((100, 100))

        # crop stage image into a circle diameter of 130
        mask = Image.new('L', stage.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, stage.size), fill=255)
        board.paste(stage, (coords[i][j]-50, x-50), mask=mask)

        # stage text
        ImageDraw.Draw(board).text((coords[i][j], x), main_map[main_map_i].split()[0], font=font, fill="white",
                                   stroke_fill="black", stroke_width=2, anchor="mm")

        # hero at slot
        hero = Image.open("images/heroes/" + main_map[main_map_i].split()[1] + ".webp")
        hero = hero.resize((50, 50))

        # crop stage image into a circle diameter of 130
        mask = Image.new('L', hero.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, hero.size), fill=255)

        board.paste(hero, (coords[i][j]+20, x+20), mask=mask)

        main_map_i += 1

    #break if main_map[x] out of range
    if main_map_i >= len(main_map):
        break

for inv in range(len(inventory)):
    hero = Image.open("images/heroes/" + inventory[inv] + ".webp")
    hero = hero.resize((70, 70))

    board.paste(hero, (650+(80*inv), 1250))

board.show()
