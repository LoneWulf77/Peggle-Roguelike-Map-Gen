"""
    DougDoug's twitch chat Peggle roguelike stream
    -build a map/hero generator
    -idea to show the chapter number on all hidden slots, only show the levels of the next row
    -future qol plan, have integration with Peggle to auto open/select hero


    currently want to auto-populate default map first (done)
    second is add ui/click events
    third is to generate custom map based on customization variables (WIP)

    image filenames for levels should be named in the style "1-1.png"
    image for heroes should be named matching the heroes list "Bjorn.png"
"""


import random
import math
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype("C:\Windows\Fonts\ARLRDBD.TTF", 30)

#chapters in game
chap = 11           # EDIT THIS FOR NUMBER OF CHAPTERS
#levels per chapter
lvls = 5           # EDIT THIS FOR NUMBER OF LEVELS IN EACH CHAPTER


# draw board
board = Image.open('images/board.png').convert("RGBA")

# board coords list             WILL BE DEPRECIATED ONCE AUTOMATIC GENERATION IS COMPLETE
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


# rolls a unique stage   NEED TO MODIFY THE RANDOMS TO BE BASED ON CHAPTERS, WHILE ALLOWING POP() TO KEEP LEVELS UNIQUE
def stage_roll(difficulty):
    global stage
    global LEVELS
    if len(unique_stages) <= 0:
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

# rolls hero semi-unique value
def hero_roll():
    # roll rng, pull a hero from array, put in main map/dict
    global unique_heroes
    global hero
    if len(unique_heroes) <= math.ceil(total_heroes/3):
        unique_heroes = HEROES.copy()
    hero = unique_heroes.pop(random.randint(0, len(unique_heroes)-1))
    return hero

# add chapter-level and hero to map slot
def add_slot(diff):
    # add slot to main_map
    slot = stage_roll(diff) + " " + hero_roll()
    main_map.append(slot)

# circle crop for stages/heroes
def circle_crop(img):
    m = Image.new('L', img.size, 0)
    md = ImageDraw.Draw(m)
    md.ellipse((0, 0, img.size), fill=255)
    return m

#string input (lowercase and leading/trailing spaces removed)
def str_response(question):
    answer = ''
    while True:
        try:
            answer = input(question)
            answer.lower().strip()
            if answer == "cancel":
                break
        except ValueError:
            print("ValueError. Please input a proper answer or \"cancel\"")
        else:
            break
    return answer

# int input (absolute value)
def int_response(question):
    answer = ''
    while True:
        try:
            answer = input(question)
            if answer.lower() == "cancel":
                break
            abs(int(answer))
        except ValueError:
            print("ValueError. Please input a proper whole number or \"cancel\"")
            continue
        else:
            break
    return answer

#reset custom variables to default
def default_custom():
    global custom_vars
    custom_vars.clear()
    custom_vars = {"levels": 6, "min_options": 3, "max_options": 5, "response": '', "customizing": False}

# how many rows in map? how many slots per row (range 3-5?)   FUTURE CREATING CUSTOM MAP
# initializing custom variables default
levels, min_options, max_options, inv_size, response, customizing = 6, 3, 5, 3, '', False
custom_vars = {"levels": levels, "minimum options": min_options, "maximum options": max_options, "inventory size": inv_size, "response": response, "customizing": customizing}

# ask if custom map
while True:
    response = str_response("Do you want to create a fully customized map? (yes/no)\n")
    if response == "yes":
        customizing = True
        break
    elif response == "no" or response == "cancel":
        default_custom()
        break
    else:
        print("Invalid response. Please input yes, no, or cancel.")

# custom build map (can have choices such as: specify how many options, level by level, and what difficulty the level is designed to be)
# customizing can probably be moved to its own file
while customizing:
    # display current variable values
    print(custom_vars)
    response = str_response("Please enter which variable you would like to change, \"reset\" to reset to default values, or \"done\" if finished:\n")

    match response:
        case "cancel":
            # confirm?
            response = str_response("Are you sure you want to cancel customization and use default values? (yes/no)\n")
            if response == "yes":
                default_custom()
                break
            elif response == "no":
                pass
            else:
                print("Invalid response. Please input yes or no.\n")
        case "levels":
            # how many levels?
            levels = int_response("How many levels in map?\n")
        case "minimum options":
            # minimum options per level?
            min_options = int_response("Minimum options per level:\n")
        case "maximum options":
            # maximum options per level?
            max_options = int_response("Maximum options per level:\n")
        case "inventory size":
            #inventory size?
            inv_size = int_response("How many inventory slots?\n")
        case "done":
            print(custom_vars)
            response = str_response("Are you done customizing your map with the above values? (yes/no)\n")
            if response == "yes":
                break
        case "reset":
            default_custom()
            customizing = True
        case _:
            print("Please enter a valid option.")


# hard coding number of slots for each difficulty based on board map
boss = 1
hard = 3
medium = 9
easy = 8
inv_size = 3

# add boss stages
add_slot("boss")
# add hard stages
for i in range(hard):
    add_slot("hard")
# add medium stages
for i in range(medium):
    add_slot("medium")
# add easy stages
for i in range(easy):
    add_slot("easy")


main_map_i = 0  # main_map[] iterator
inventory = random.sample(HEROES, inv_size) # fill inventory slots with 3 random unique heroes


# cycle through coords on board for each slot   PROBABLY CAN BE WRITTEN BETTER
for i in range(rows):
    x = row_height[i]

    for j in range(len(coords[i])) :

        #break if main_map[x] out of range
        if main_map_i >= len(main_map):
            break

        #pull and draw cropped stage image
        stage = Image.open("images/stages/" + main_map[main_map_i].split()[0] + ".webp").convert("RGBA")
        stage = stage.resize((100, 100))
        board.paste(stage, (coords[i][j]-50, x-50), mask=circle_crop(stage))

        # stage text displayed
        ImageDraw.Draw(board).text((coords[i][j], x), main_map[main_map_i].split()[0], font=font, fill="white",
                                   stroke_fill="black", stroke_width=2, anchor="mm")

        #pull and draw cropped hero image
        hero = Image.open("images/heroes/" + main_map[main_map_i].split()[1] + ".webp")
        hero = hero.resize((50, 50))
        board.paste(hero, (coords[i][j]+20, x+20), mask=circle_crop(hero))

        main_map_i += 1   # increment to next slot

    #break if main_map[x] out of range
    if main_map_i >= len(main_map):
        break


# inventory display             BETTER USE AND FUNCTIONALITY WIP
for inv in range(len(inventory)):
    hero = Image.open("images/heroes/" + inventory[inv] + ".webp")
    hero = hero.resize((70, 70))
    board.paste(hero, (650+(80*inv), 1250))

board.show()
