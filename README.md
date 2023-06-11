# README

# Introduction

This repository contains all the files from our Artificial Intelligence final project, where two multiple-player groups challenge each other with their agent.

The project is named after the homonymous [Codingame challenge](https://www.notion.so/Readme-48f58f9165464fe8b9a83cf53fb059a1), which is directly inspired by the board game “*[**Quoridor**](https://it.wikipedia.org/wiki/Quoridor)*”. 

The project’s main goal is to develop a bot (mainly implemented via Answer Set Programming) that plays the game autonomously.

To make the bot play the game, you also need the game itself: that’s why we also had to develop it.

# Technical info

The game is written in **Python** and uses the [**Pygame**](https://www.pygame.org/) library.

Since the project is evaluated solely on how smart the AI is, don’t expect the rest of the code to be well-designed. 

In the case of Team 1, the AI is implemented through some functions in Python, and the rest of the task is given to a single ASP program, which then runs on [**Clingo**](https://potassco.org/clingo/) and the resulting optimal Answer Set is the effective players’ move.

…info on Team 2 to be written soon…

# Game rules

The game rules are practically identical to the [Codingame challenge](https://www.notion.so/Readme-48f58f9165464fe8b9a83cf53fb059a1)’s, except for the time constraint, which is a little bit more relaxed. You can check them out there.

# How can I write my personal AI?

If you want to write your bot, you have to follow some steps:

1. Install pygame;
    
    ```bash
    pip install pygame
    ```
    
2. Install [EmbASP](https://github.com/DeMaCS-UNICAL/EmbASP/releases/download/7.4.0/EmbASP-7.4.0-py2.py3-none-any.whl) for python;
    
    ```bash
    pip install EmbASP-7.4.0-py2.py3-none-any.whl
    ```
    
3. Create your AIManager child class and let it handle your moves. Please bear in mind that you have **limited time to do it (*you can check the correct amount in the “Timekeeper” class*);
4. Override the *ask_for_a_move* method inside the AIManager;
5. If you are going to use an ASP program, override also the *prepare_programs_for_handler* method;
6. Pass your freshly created AIManager and your name to a new AIPlayer instance, which then you need to append to the *ai_manager_pool* list, inside the Game class (***Note**: the ai_manager_pool is shuffled in the create_players method, so if you want to make sure that one of the players is gonna be yours, comment the shuffle instruction and let your manager be in position 0 or 1 of the list*);
7. Run main.py as you wish (***Note**: If you are a Linux user and you want to run it as an executable, you should probably run a **chmod u+x** on it);*

# The Team(s)

Each “*sub*” team is composed of two members.

## Team 1

- [Alessandro **Monetti**](https://github.com/ilveron)
- [Andrea **Tocci**](https://github.com/AndreaYpmY)

## Team 2

- [Gianmarco **Raso**](https://github.com/Giarco)
- [Luigi **Villella**](https://github.com/GiVill)

# Credits

The ASP solvers [DLV2](https://dlv.demacs.unical.it/home) and [Clingo](https://potassco.org/clingo/)

Many thanks to Angelo Fittipaldi ([@imbngy](https://github.com/imbngy)), who made the HUD layout and the players’ pawns assets for us.

All credits for the music must go to:

- **skuter** for [.giana sisters.](https://modarchive.org/index.php?request=view_by_moduleid&query=57367)
- **laxity** for [laxity again](https://modarchive.org/index.php?request=view_by_moduleid&query=85532) and [checknobankh](https://demozoo.org/music/67817/) (*[desert dream demo](https://youtu.be/jziQBWQxvok?t=274)*)
- **Johannes Bjerregaard** and **Thomas Mogensen** for [Tiger Mission Hi-score](https://modarchive.org/index.php?request=view_by_moduleid&query=141569) (*fairstars*)
- **Renard** for [untitled](https://modarchive.org/index.php?request=view_by_moduleid&query=179148) (*zerd_01*)

# In-game Screenshots

Here are some in-game screenshots for you to see:
![python_KWaGIgQiBk](https://github.com/AndreaYpmY/GreatEscape/assets/85177113/55d4e26f-b5ea-4ee2-bd54-d2a76cb23812)
![python_zV6BIHmFW0](https://github.com/AndreaYpmY/GreatEscape/assets/85177113/dd96c759-60df-4790-b75e-d326077852f0)

