# Project 1 Solution

<div align='right'>3160103838 Li Jiachen</div>

---

## N-Puzzle Problem
### Prerequisite
* n_puzzle_state_main.py
* puzzle_state.py

The implementation of the game process is given. The main goal of the project is to determine several heuristic functions.

### Heuristics Design
To run the A* search algorithm, we need to define appropriate heuristics. Any possible heuristics should have following properties:

* Admissive (for tree search): $0 \le h(n) \le h^{*}(n)$
* Consistent (for graph search): $h(n) \le c(n, a, n') + h(n')$

where $h^{*}(n)$ is the true cost to a nearest goal and $c(n,a,n')$ is the cost of one transition from node $n$ to $n'$ via action $a$.

In the N-Puzzle problem, different states with particular position of each number can be considered as different nodes in a tree or a graph. We need to use some metrics to evaluate the "similarity" between the initial node and the goal node. All of the valid metrics can act as heuristics.

I developed 3 portential distance metrics as heuristics:
* Euclidean distance
* Position of the blank
* Chebyshev distance

I will interpret the insight that guides me to think so.

### Insight
#### 1. Euclidean distance
The Euclidean distance is the first metric I realized.

The permutation of numbers can be seen as a certain point in a high-dimensional Euclidean space so that we can use a vector to represent a state.

For example, vector $\bold{g}=\begin{bmatrix}1&2&3&\dots&8&-1\end{bmatrix}^T$ stands for the final state $\def\arraystretch{1.5}
   \begin{array}{c|c|c}
   1 & 2 & 3 \\
   \hline
   4 & 5 & 6 \\
   \hline
   7 & 8 & 
\end{array}$, where the numbers are extracted row-by-row into a column vector.

In this way, each state will refer to a point. Then we can calculate the Euclidean distance between two points like this:

For a certain state $\bold{s} = \begin{bmatrix}
s_1 & s_2 & \dots & s_N
\end{bmatrix}^T$ and final state $\bold{g}= \begin{bmatrix}
g_1 & g_2 & \dots & g_N
\end{bmatrix}^T$ of a playboard of size $n$,

$$
h(\bold{s}) = ||\bold{s} - \bold{g}||_2
$$

where $h(\bold{s})$ is the heuristic of state $\bold{s}$ and $N=n^2$.

This definition of $h$ implements such a mapping:

$$h:\mathbb{R}^{N\times1} \rightarrow \mathbb{R}$$

It conforms with the requirement of a heuristic function. Because the Euclidean distance is always non-negative and in the Euclidean space it is always the closest distance.

#### 2. Position of the blank box
The Euclidean distance is available, but it works in a high dimension of $n^2$, where $n$ is the size of the playboard. Can we reduce the dimension so that we can calculate the distance with less effort?

The position of the blank can be used as a metric to help cut down the complexity of calculation.

We assume the playboard as a coordinate system with its origin (0,0) at the left-top box of the playboard like this example:

$$\def\arraystretch{1.5}
   \begin{array}{c|c|c}
   (0,0) & (0,1) & (0,2) \\
   \hline
   (1,0) & (1,1) & (1,2) \\
   \hline
   (2,0) & (2,1) & (2,2) 
\end{array}
$$

In this way, we can describe the position of the blank box via the coordinate system.

Since the boxes can only move vertically or horizontally, we use the Manhattan distance as a heuristic function to evaluate the state.

At the goal state, the blank box should be at the right-bottom corner of the playboard, thus we can define the heuristic function like this:

$$
h(x,y) = |x-x_g| + |y-y_g|
$$

where $(x,y)$ is the position of the blank box, $x_g=n-1$, $y_g=n-1$ and $n$ is the size of the playboard.

This definition also conforms with the requirement of a heuristic function, because the absolute value is always non-negative and the Manhattan distance is the closest in a vertical-and-horizontal-only moving pattern.

Obviously, compared with calculating Euclidean distance, this method is much more efficient in calculation.

#### 3. Chebyshev distance
Based on the coordinate system mentioned in last section, we can apply a new metric, the Chebyshev distance, as the heuristic function.

We define the heuristic function like this:
$$
h(x,y) = \max(|x-x_g|,|y-y_g|)
$$

where $(x,y)$ is the position of the blank box, $x_g=n-1$, $y_g=n-1$ and $n$ is the size of the playboard. This is called the Chebyshev distance between $(x,y)$ and $(x_g,y_g)$.

To prove its correctness, we use the conclusion of the Manhattan distance:

$$
h(x,y) = \max(|x-x_g|,|y-y_g|) < |x-x_g| + |y-y_g| \le h^*(x,y)
$$

where $h^*(x,y)$ is the true cost in the game.

Therefore, $h(x,y)$ can be used as a heuristic function.

### Performance
To evaluate the performance of aforementioned 3 heuristic functions,


---



## Tic-Tac-Toe Problem




