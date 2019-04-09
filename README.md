# HSLU RobLab Projekt "DeskCleaner"

## Team

- Barmettler Reto
- Gröger Fabian
- Hurschler André

## Project

"Grabbing a box", sounds easy right? Well it isn't with the NaoQi Framework.

How it works:

1. Pepper looks for an object to grab
2. Pepper moves to it
3. Pepper grabs it
4. Pepper looks for drop area
5. Pepper drops object in drop area

This project contains workarounds for:

- "grabbing bug", pepper can't leave his hands closed
- "move arms while driving", pepper always puts his arms down when driving

### pynaoqi_mate

The code is based on pynaoqi_mate
https://github.com/uts-magic-lab/pynaoqi_mate
and was adapted to work with pynaoqi 2.5 and our two pepper robots "amber" and "porter".