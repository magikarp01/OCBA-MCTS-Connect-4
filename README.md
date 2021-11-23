# OCBA-MCTS-Connect-4
An implementation of "Monte Carlo tree search with optimal computing budget allocation" on Connect 4.

OCBA.py and UCT.py define states of a Connect 4 Markov Decision Process. The classes OCBAState and UCBState are used in Monte Carlo Tree Search for a Connect 4 AI, according to the OCBA and UCB search algorithms. 

comparison.py has methods for comparing the two search algorithms. 
From comparison.py, the OCBAGame() and UCBGame() methods allow the user to play full games against the AI, and playAgainst() method pits the two algorithms against each other in a full game. 
comparePlot() creates graphs for comparing the behavior of the two algorithms. 
compareDepth() compares which move the algorithms choose given instructions to go down a certain depth in MCTS.

To test out the program, main.py has several predefined game positions and commented out calls to comparePlot, compareDepth, playAgainst, OCBAGame, and UCBGame with appropriate parameters. The user can uncomment any of the method calls (I recommend comparePlot, then OCBAGame or UCBGame, then playAgainst) and run main.py.
The libraries matplotlib and tqdm must be installed. 

When playing OCBAGame or UCBGame, the program will choose a column to place their piece in, following standard connect 4 rules. Then, the user should choose a column to play their piece in, ranging from 1 to 7 (left to right). Once the user has played, the AI plays, and so on until the game has finished.
