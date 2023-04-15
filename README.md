# upper-envelope

Code for calculating the upper envelope of a set of linear approximation functions described by points.

My algorithm is implemented using, among other tricks, a lightweight interpolation with optimisations which improves the expected calculation time by ~30%. The time complexity is $O(n^2)$, and this is the fastest algorithm I know to solve this variant of the upper envelope problem.

![](problem.jpg)

The plot describes the problem nicely. The red line is the **upper envelope** of the set of three functions (blue, orange and green). It is guaranteed that all functions' domain is the same (the starting and ending points have the same X-coordinate).