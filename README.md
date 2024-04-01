# Labcraft
A Digital Physics Lab in a Blocky Voxel World

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

The purpose of this project is to develop a Virtual Environment (V.E) in which students can learn how to code through working on simulations, I have been working on this project with Dr. Trevor Tomesh, since February of 2023, and we plan on publishing a paper together by the end of this semester. My work this semester will be to establish an in game code editor that actually changes the code of the game file, as not to overwhelm new coders with the (as of 2/5/2024) 2000+ lines of code. Below you can see the features I've added since starting my work which I go into more detail in my walkthrough video. 
# Dependencies:
## On Linux: 
Labcraft uses python 3.6:
```bash
sudo apt-get install python3
```

## On Windows:
1. Check Your Python version from the Windows CMD or PowerShell:
``` 
python --version
```
If Python 3.6 or newer is already installed, you may skip to the [Ursina installation](https://github.com/quickMaffs44/labcraft/blob/main/README.md#ursina).

2. Download and run the installer from Python.org's [Downloads page for Windows](https://www.python.org/downloads/windows/)


## Ursina:
Labcraft is built on the Ursina engine (https://www.ursinaengine.org)
To install Ursina use pip:
``` bash
pip install ursina
```

Or on Windows CMD/PowerShell:
```CMD
python -m pip install ursina
```

#### Troubleshooting:
If you run into an error concerning a ".deleteme" file, just re-run the installation command.

# Running:
To run, simply:
```bash
python3 labcraft.py
```
Or:
```bash
python labcraft.py
```

# Manifest:
- README.md:
  The file you are currently reading.

- labcraft.py:
  The main labcraft code.

- assetTest.py:
  A little script to test new models and textures.

- sims.py:
  Methods that control the various simulations in the world. Might change
  this later as there becomes more simulations.

- assets:
  Folder that contains all of the models, textures and audio files.
<<<<<<< HEAD

 # NEW FEATURES:

 -WRITE VALUES TO A FILE ON YOUR COMPUTER WITH THE PLANET AND PENDULUM SIM,
    SO YOU CAN CHART AND GRAPH, OR GRAPH AND CHART IF YOU'RE CANADIAN
    
 -PENDULUM NOW BEHAVES LIKE AN ACTUAL PENDULUM (MINUS GRAVITY), AND YOU CAN
    CAN CHANGE THE FREQUENCY AND AMPLITUDE IN GAME.
    
 -THE SAVE SYSTEM HAS BEEN STARTED, CURRENTLY ALL PLACED BLOCKS WILL BE THERE
    NEXT GAME!!! (DELETED BLOCKS WILL NOT BE DELETED BUT THIS IS BEING WORKED ON)
    
 -THE EARTH ROTATES!!! LEON FOUCAULT EAT YOUR HEART OUT

 -New Sims! We've got a Cannon, We've got apples, We've even got visual representations of FOR LOOOOOOOPS 

 -Also other computer logic statements, but FOOOOOOOOOOOOOOOOR LOOOOOOOOOOPS is the most impressive

 -I have started work on an in game code editor that will actually change the code of the game itself. This will be the focus of my CapStone project.

 -Added a Ursina test program that lets you edit code and test it while the file is running

 -Started integrating this into LabCraft, this is barebones currently is terrible. But so is the rest of this projects.
