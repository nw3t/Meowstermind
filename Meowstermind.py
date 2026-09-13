#!/usr/bin/env python3

import subprocess
import random
import readchar #nonstandard, gotta learn how to package this one


################
# Sigils
################
miss   = "\033[37m\u25cf\033[0m "
hit    = "\033[31m\u25cf\033[0m "
red    = "\033[31m\u29bf\033[0m "
blue   = "\033[34m\u2609\033[0m "
green  = "\033[32m\u25c8\033[0m "
yellow = "\033[33m\u2742\033[0m "
black  = "\033[90m\u25cb\033[0m "
white  = "\033[37m\u25ce\033[0m "
blank  = "\033[30m\u25cc\033[0m "
neutral_cat = "\033[35m=^-ω-^=\033[0m"
shocked_cat = "\033[35m=^ㅇㅅㅇ^=\033[0m"
smug_cat = "\033[35m=^-u-^=\033[0m"
worried_cat = "\033[35m=^⊏.⊏^=\033[0m"


################
# Loop order
################
colour_cycle = [red, yellow, green, blue, white, black]


################
# Screen drawing
################
def clear_screen():
    subprocess.run('clear')

def newline():
    print("")

def printf(chars):
    print(chars, end="")

def print_welcome():
    print("      ---~~***===MEOWSTERMIND===***~~---")
    print("       =automatic mastermind by Woland=")


################
# Init game state
################
player_guess = [blank, blank, blank, blank]
hint = []
secret = [blank, blank, blank, blank]
player_selection = 1
feedback = [blank, blank, blank, blank]
history = []
hint_history = []
current_cat = neutral_cat


################
# Gameplay
################
def set_secret():
    secret[:] = [random.choice(colour_cycle) for _ in range(4)]


def debug_secret():
    for each in secret:
        printf(each)
    newline()

def update_game(key):
    global player_selection

    index = player_selection -1
    selected = player_guess[index]

    colours = len(colour_cycle)
    colour_blank = colours+1 #loop through the colour cycle, blank is unselectable and between black and red
    colour_index = colour_cycle.index(selected) if selected in colour_cycle else colour_blank
    next_colour = colour_cycle[(colour_index + 1) % colours]
    prev_colour = colour_cycle[(colour_index - 1) % colours]

    match key:
        case 'h':
            if player_selection > 1:
                player_selection -= 1
        case 'j':
            player_guess[index] = prev_colour if colour_index != colour_blank else black
        case 'k':
            player_guess[index] = next_colour if colour_index != colour_blank else red
        case 'l':
            if player_selection < 4:
                player_selection += 1
        case readchar.key.ENTER:
            guess()
        case 'win':
            draw_ui()
            win()

def draw_ui():
    clear_screen()
    print_welcome()
    #debug_secret()
    for i, each in enumerate(history):
        for historic in each:
            printf(historic)
        printf(31 * " ")
        for meow_hint in hint_history[i]:
            printf(meow_hint)
        newline()
    newline()
    print("  " * (player_selection-1) + "⤓")
    for each in player_guess:
        printf(each)
    printf(" <- Player " + current_cat + " Meowster->  ")
    for each in feedback:
        printf(each)
    newline()

def guess():
    global current_cat, player_selection
    secret_copy = secret.copy()
    hint[:] = [None]*4
    if blank not in player_guess:
        for i, each in enumerate(player_guess):
            if each == secret_copy[i]:
                secret_copy[i] = blank
                hint[i]=hit
        for i, each in enumerate(player_guess):
            if hint[i] is None:
                if each in secret_copy:
                    secret_copy[secret_copy.index(each)] = blank
                    hint[i]=miss
                else:
                    hint[i]=blank

        priority = {hit: 0, miss: 1, blank: 2}
        hint.sort(key=lambda h: priority[h])

        current_cat = neutral_cat
        if hint.count(blank) > hint.count(hit)+hint.count(miss):
            current_cat = smug_cat
        if hint.count(blank) == 0:
            current_cat = worried_cat
        if hint.count(hit) > hint.count(miss)+hint.count(blank):
            current_cat = shocked_cat
        hint_history.append(hint[:])
        history.append(player_guess[:])
        if hint.count(hit) == 4:
            update_game('win')
        player_guess[:] = [blank, blank, blank, blank]
        player_selection = 1
        hint.clear()

def win():
    print("Won in",len(history),"guesses!")
    print("Try again?")
    if readchar.readkey() == 'q':
        exit()
    else:
        restart_game()

def restart_game():
    global current_cat, player_selection
    player_guess[:] = [blank, blank, blank, blank]
    feedback[:] = [blank, blank, blank, blank]
    current_cat = neutral_cat
    player_selection = 1
    set_secret()
    history.clear()
    hint.clear()
    hint_history.clear()

if __name__ == '__main__':
    print("        hjkl to select, enter to guess, q to quit")
    print("               =Press Any key to start=")
    set_secret()
    while (keypress := readchar.readkey()) != 'q':
        update_game(keypress)
        draw_ui()