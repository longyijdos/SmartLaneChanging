# SmartLaneChanging
This repository contains the Python implementation for our game theory group project on lane-changing in autonomous vehicles.

  
![Lane Changing](image/lane_change.png)

## Description

This script implements a game theory approach to the lane-changing problem for autonomous vehicles. The main goal is to optimize lane-changing decisions based on game theory strategies.

## How to Run the Script

### Prerequisites

- Ensure you have installed the necessary Python libraries (e.g., `argparse`, `json`) and the `players` module which defines the `Player1` and `Player2` classes.
- Make sure you have the parameters file (e.g., `setting舒适_效率.json`) ready, containing the required configuration data. The file should have a structure similar to:

  ```json
  {
      "player1": { /* parameters for player1 */ },
      "player2": { /* parameters for player2 */ }
  }
