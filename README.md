# Readme

# Introduction

This repository contains all the files from our Artificial Intelligence final project, where two multiple-player groups challenge each other with their agent.

The project is named after the homonymous [Codingame challenge](https://www.notion.so/Readme-48f58f9165464fe8b9a83cf53fb059a1), which is directly inspired by the board game “*[**Quoridor**](https://it.wikipedia.org/wiki/Quoridor)*”. 

The project’s main goal is to develop a bot (mainly implemented via Answer Set Programming) that plays the game autonomously.

To make the bot play the game, you also need the game itself: that’s why we also had to develop it.

# Technical info

The game is written in **Python** and uses the [**Pygame](https://www.pygame.org/)** library.

Since the project is evaluated solely on how smart the AI is, don’t expect the rest of the code to be well-designed. 

In the case of Team 1, the AI is implemented through some functions in Python, and the rest of the task is given to a single ASP program, which then runs on [**Clingo**](https://potassco.org/clingo/) and the resulting optimal Answer Set is the effective players’ move.

…info on Team 2 to be written soon…

# What do you need

If you want to write your own bot, you have to follow some steps:

1. Install pygame
    
    ```bash
    pip install pygame
    ```
    
2. Install [EmbASP](https://github.com/DeMaCS-UNICAL/EmbASP/releases/download/7.4.0/EmbASP-7.4.0-py2.py3-none-any.whl) for python
    
    ```bash
    pip install EmbASP-7.4.0-py2.py3-none-any.whl
    ```
    
3. Create your ai_manager and let it handle your moves

# The Team(s)

Each “*sub*” team is composed of two members.

## Team 1

- [Alessandro **Monetti**](https://github.com/ilveron)
- [Andrea **Tocci**](https://github.com/AndreaYpmY)

## Team 2

- [Gianmarco **Raso**](https://github.com/Giarco)
- [Luigi **Villella**](https://github.com/GiVill)

# Credits

Many thanks to Angelo Fittipaldi ([@imbngy](https://github.com/imbngy)), who made the HUD layout and the players’ pawns for us.

All credits for the music must go to:

- **skuter** for [.giana sisters.](https://modarchive.org/index.php?request=view_by_moduleid&query=57367)
- **laxity** for [laxity again](https://modarchive.org/index.php?request=view_by_moduleid&query=85532)
- **Johannes Bjerregaard** and **Thomas Mogensen** for [Tiger Mission Hi-score](https://modarchive.org/index.php?request=view_by_moduleid&query=141569) (*fairstars*)
- **Renard** for [untitled](https://modarchive.org/index.php?request=view_by_moduleid&query=179148) (*zerd_01*)