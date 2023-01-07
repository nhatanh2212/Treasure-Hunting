# Treasure Island

## 1. The boardgame
“Long John Silver's crew has committed mutiny and has him cornered and tied up!
Round after round, they question him about the location of his treasure and explore the island following his directions — or perhaps his misdirections? Who knows... The old sea dog is surely planning an escape, after all, after which he will definitely try to get his treasure back. Treasure Island is a game of bluffing and adventure in which one player embodies Long John, trying to mislead the others in their search for his treasure. The hunt reaches its climax with Long John's escape, when he will make a final run to get the booty for himself!!” (boardgamegeek.com)


## 2. Installing
   
### a. venv for Visual studio
   - macOS/Linux: 
      - $ sudo apt-get install python3-venv
      - $ python3 -m venv .venv
   - Windown: 
      - $py -3 -m venv .venv OR $python -m venv .venv
   - The tutor for setting up venv can be found here: https://code.visualstudio.com/docs/python/environments 
    
### b. pypgame
   - $pip install pygame
   - The tutor for setting up pygame can be found here: https://github.com/pygame/pygame
   
## 3. Running
   User can specify the block size when running the game. Press Enter to see next turn in the game.
   - Main function:
      - python main.py <input_file> <output_file> <block_size>
      - Example: python main.py "MAP_1.txt" "OUTPUT_1.txt" 50
   - Visualization:
      - python visualization.py <input_file> <output_file> <block_size>
      - Example: python visualization.py "MAP_1.txt" "OUTPUT_1.txt" 50





