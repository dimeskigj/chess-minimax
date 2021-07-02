<h2>Chess AI</h2>
A simple chess AI demonstrating the minimax algorithm. 
There's also a simpler tic-tac-toe implementation, the core of the algorithm is the same.

Minimax is essentially a brute-force algorithm so it's rather slow, not noticeable with tic tac toe,
but with chess (where the branching factor is ~35) it takes a lot of time to evaluate all the nodes, so the tree depth must be limited. 
A max tree depth of 4 is the best I could achieve - anything above would require too much time to evaluate.
Besides this, I've implemented alpha-beta pruning to make the algorithm somewhat faster.

I've tested this against a ~550 elo chess.com bot and it manages to win/lead. Haven't tested with better bots.

I am using the chess python library. You can use the standard move notation to play with the computer.

[sample game against a ~1000 elo lichess player](https://lichess.org/PDoaR6C5ztwF) (my friend), with the computer playing as white.
