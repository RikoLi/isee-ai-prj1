# N-Puzzle Problem Solution

<div align='right'>3160103838 Li Jiachen</div>

---

## Prerequisite
* n_puzzle_state_main.py
* puzzle_state.py
* Anaconda 4.4.10
    * Numpy 1.15.4
    * Python 3.6.4

The implementation of the game process is given. The main goal of the project is to determine several heuristic functions.

## Usage
Enter the directory of `n_puzzle_state_main.py`, start your command line and input this command:

```bash
python n_puzzle_state_main.py
```

## Heuristics Design
To run the A* search algorithm, we need to define appropriate heuristics. Any possible heuristics should have following properties:

* Admissive (for tree search): $0 \le h(n) \le h^{*}(n)$
* Consistent (for graph search): $h(n) \le c(n, a, n') + h(n')$

where $h^{*}(n)$ is the true cost to a nearest goal and $c(n,a,n')$ is the cost of one transition from node $n$ to $n'$ via action $a$.

In the N-Puzzle problem, different states with particular position of each number can be considered as different nodes in a tree or a graph. We need to use some metrics to evaluate the "similarity" between the initial node and the goal node. All of the valid metrics can act as heuristics.

I developed 6 portential distance metrics as heuristics:
1. Euclidean distance
1. Position of the blank
1. Chebyshev distance
1. Hamming distance
1. Manhattan distance
1. Mixed method

## Insight
### 1. Euclidean distance
The Euclidean distance is the first metric I realized.

The permutation of numbers can be seen as a certain point in a high-dimensional Euclidean space so that we can use a vector to represent a state.

For example, vector $\bold{g}=\begin{bmatrix}1&2&3&\dots&8&-1\end{bmatrix}^T$ stands for the state $\def\arraystretch{1.5}
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
\end{bmatrix}^T$ and a final state $\bold{g}= \begin{bmatrix}
g_1 & g_2 & \dots & g_N
\end{bmatrix}^T$ of a playboard of size $n$,

$$
h(\bold{s}) = ||\bold{s} - \bold{g}||_2
$$

where $h(\bold{s})$ is the heuristic function of state $\bold{s}$ and $N=n^2$.

This metric conforms with the requirement of a heuristic function. Because the Euclidean distance is always non-negative and in the Euclidean space it is always the closest distance.

### 2. Position of the blank box
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

### 3. Chebyshev distance
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

### 4. Hamming distance
This metric consider the playboard as a binary array. For each element in current state, except the blank box, this metric will check whether the element is at the same place with that in goal state. If they are at the same place, we get a 0, otherwise we get a 1. In this way, we finally convert the playboard into a binary array with 0 and 1 only. Sum up all the 1 in the array, then we get a number showing the total amount of misplaced boxes, except the blank box.

This metric must be heuristic because the amount of misplaced boxes must be non-negative and in a determined state, it must be a fixed value.

### 5. Manhattan distance
This metric works in this way:

$$
h(n) = \sum_{i=0}^{K-1}||\bold{x}_i - \bold{x}_{ig}||_1,\space Value(\bold{x}_i)\neq-1
$$

where $\bold{x}_i$ is a two-dimension vector that illustrates the $i$th box's position, $\bold{x}_g$ is a two-dimension vector that illustrates the $i$th box's goal position, $K$ is the total amount of the boxes, and $Value(\bold{x}_i)$ means that the box value corresponds to vector $\bold{x}_i$.

The equation calculates the sum of Manhattan distance of all misplaced boxes on the playboard, except the blank box, acting as a heuristic function of state $n$. Since the Manhattan distance is a heuristic function in a vertically-and-horizontally-move-only environment, the sum of the Manhattan, thus, should be a available heuristic function as well.

### 6. Mixed method
Just like what the title says, "mixed method" uses a bundle of methods together. It can contain any possible terms, combining in this way:

$$
h(n) = \sum_i^M \alpha_i h_i(n)
$$

where $M$ is the total amount of sub-heuristics, $\alpha_i$ is a weight coefficient, and $h_i(n)$ is the $i$th sub-heuristics.

The insight to sum them up stems from a thought that if one metric works, together work better.

In this project, we only use Metric 4 and 5 together as a mixed method. The implementation is very easy, since they performs pretty well in following performance tests. Parameters are setted like this:

$$
h(n) = 0.5h_{hamming}(n) + 0.5h_{manhattan}(n)
$$

This metric should be available, since the sum and multiplication operation are linear so that the linear combination of sub-heuristics will still be heuristic.



## Performance
In this section, let us evaluate the performance of aforementioned 6 heuristic functions.

When the initial state is fixed, Metric 2~6 usually work better than Metric 1, finding the shortest way to the goal state. Metric 1 can also find a way out but takes more steps.

For both testing samples of size of 3 and 4, if we set the initial move steps lower than 60, in most cases, all of the designs, evaluated by Metric 2&3 can find a solution in a reasonable time. If we set move steps much higher, however, such as 90 or 100, they work terriblely, meaning that they can hardly find a solution. In most cases, Metric 4~6 find a way out after a higher-than-90-step initial movement, which supports that these heuristic functions do work in solving the problem in complexer environments.

**Test sample 1:**
* size: 3
* step: 100

![sample1](n_puzzle/sample1.png)![sample1_res](n_puzzle/test5.png)

**Test sample 2:**
* size: 4
* step: 100

![sample2](n_puzzle/sample2.png)

### Which one to choose?
I did lots of experiments, testing the performance of those functions. However, it is quite hard for me to make a dicision, because the performance varies from time to time, possibly resulting from undetermined complexity of state space trees that are randomly generated in each test. But in general, some functions are better than others, such as Metric 4~6.

To choose a suitable function, I assume some naive premise. The Euclidean distance is calculated in a high dimensional space, which actually wastes lots of resources on float arithmetic operations. Comparing Metric 2&3, I believe that these two metrics are not convincing enough due to the exploitation of only one box on the playboard, though these two functions are less time-consuming than the Euclidean. Metric 4, which I consider as the best metric in this project, combines the less calculation with the use of information from all boxes. So, I prefer **Metric 4: Hamming distance** to be the final heuristic function.

At first, I predict that Metric 6, the mixed method, will perform much better. However, in experiments, it did not show any advancements than its components: Metric 4&5. That's why I give up choosing it to be the final function.

**Attention:** The code file contains all of the functions I designed. You can choose whichever you like to solve the problem. Just change the parameter `heuristics`. Here is a list of functions:

Name | Metric
---|---
'euclidean' | Euclidean distance
'blank_pos' | Position of the blank box
'chebyshev' | Chebyshev distance
'hamming' (default) | Hamming distance
'manhattan' | Manhattan distance
'mix' | Mixed method


