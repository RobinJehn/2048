# 2048
Tensorflow only works with Python 3.5-3.8. Use pip3 install -r requirements.txt to install the required packages.
Start without render will freeze the screen and output to the console. After that the option Train Model will be visible, which again freezes the screen but outputs to the console. Lastly Play Model will be visible which shows how the AI performs.

# AI
The generated data only contains moves that resulted in the highest value being in the bottom right corner. Since this happens relatively infrequent just by chance and usually only in the early game, the AI will not perform well after the value is higher than 32.

# Outlook
I will implement the NEAT algorithm soon and update the reward function so that the AI will learn how to play in the late game.
