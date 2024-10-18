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
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("C:\Windows\Fonts\ARLRDBD.TTF", 30)

# array/dict of all peggle maps (constant)
# 2d array of chapters-levels?

# array of levels to choose from
levels = []
for chapter in range(5):
    for level in range(5):
        levels.append(str(chapter+1) + '-' + str(level+1))

# array/list of all heroes (constant)
heroes = ["Bjorn", "Jimmy", "Kat", "Splork", "Claude", "Renfield", "Tula", "Warren", "Cinderbottom", "Hu"]


# array/list of main map (21 spots)
main_map = []


# add chapter-level and hero to map slot
def add_level():
    stage = levels.pop(random.randint(0, len(levels)-1))
    # roll rng, pull a hero from array, put in main map/dict
    hero = random.choice(heroes)

    option = stage + " " + hero
    main_map.append(option)


# roll rng, pull 3 heroes from array, put in starting inventory (unique ideally)
inventory = [random.choice(heroes), random.choice(heroes), random.choice(heroes)]

# generate main_map slots
while len(main_map) < 25:
    add_level()

print("map ")
print(main_map)
print("inventory ")
print(inventory)


# draw board
board = Image.open('images/board.png').convert("RGBA")

# board coords list
# 515/185                                   x=185
# 260/380 515/380 750/380                   x=380
# 125/560 320/560 485/560 670/560 870/560   x=560
# 200/730 430/730 650/730 820/730           x=730
# 80/910 270/910 460/910 720/910 900/910    x=910
# 260/1080 520/1080 840/1080                x=1080
row1 = [515]
row2 = [260, 515, 750]
row3 = [125, 320, 485, 670, 870]
row4 = [200, 430, 650, 820]
row5 = [80, 270, 460, 720, 900]
row6 = [260, 520, 840]
row_height = [185, 380, 560, 730, 910, 1080]

# 2d array of the above
rows, cols = (6, 5)
coords = [row1, row2, row3, row4, row5, row6]

# add heroes to board
# bjorn = Image.open('images/Bjornn.webp')

# add levels to board
# temp txt for level pic
# ImageDraw.Draw(board).text((450, 140), main_map[0], font=font, fill="white", stroke_fill="black",
# stroke_width=2, anchor="mm")

slot = 0  # main_map[] iterator

# cycle through main_map to add images to board
for i in range(rows):
    x = row_height[i]

    for j in range(len(coords[i])):

        stage = Image.open("images/stages/" + main_map[slot][:3] + ".webp").convert("RGBA")
        stage = stage.resize((100, 100))

        # crop stage image into a circle diameter of 130
        mask = Image.new('L', stage.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, stage.size), fill=255)
        board.paste(stage, (coords[i][j]-50, x-50), mask=mask)

        # stage text
        ImageDraw.Draw(board).text((coords[i][j], x), main_map[slot][:3], font=font, fill="white",
                                   stroke_fill="black", stroke_width=2, anchor="mm")

        # hero at slot
        hero = Image.open("images/heroes/" + main_map[slot][4:] + ".webp")
        hero = hero.resize((50, 50))

        # crop stage image into a circle diameter of 130
        mask = Image.new('L', hero.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, hero.size), fill=255)

        board.paste(hero, (coords[i][j]+20, x+20), mask=mask)

        slot += 1

for inv in range(len(inventory)):
    hero = Image.open("images/heroes/" + inventory[inv] + ".webp")
    hero = hero.resize((70, 70))

    board.paste(hero, (650+(80*inv), 1280))

board.show()
