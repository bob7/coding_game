# coding_game

A coding game co-written with Chen Shichao in javascript, for understanding redundancy in coding methods.

![alt text](https://github.com/bob7/coding_game/blob/master/screenshots/static_screenshot.png)

I had written it before in python, so I include those versions too.

![alt text](https://github.com/bob7/coding_game/blob/master/screenshots/staticp_screeen1.png)

# Brief overview for the js version:

This is a coding game. In the full binary tree, one player (red) chooses to destroy a fixed proportion of leafs (viewed as codes), and the second player (blue) has to re-code the missing information to other available leafs, which will now contain two tracks of information (the one they originally had, plus the additional they accepted). The difficulty is that the coding needs to be prefix-faithful, in the sense that if string B is asked to describe string A (apart from itself) then for each n<|B|, the first n bit segment of B needs to describe the first n bit segment of A (with respect to its second track).

Board: the nested circles can be seen as levels of a binary tree, so the outer cells are the leafs of the tree. Nodes (which are binary strings) are labelled by the integer corresponding canonically to the binary string (this saves space).

Objective: the red player choses a fixed proportion of leafs, usually between 1/4 and 1/3, and the blue player tries to move these to "legitimate positions" (see below). If the blue manages to move all chosen red leafs to legitimate positions, he wins; otherwise he loses.

Legal moves (shown in green): if node A is moved to node B, the latter becomes double-labelled, with label B/A. Moreover the same happens to the predecessors of B, down to the last node before the longest common initial segment between A,B. A move is legal if it does not force a third label on any node, under the above mechanism.
