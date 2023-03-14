# LazyQuantile

## Problem Description

Given an unordered collection of customer payment records :

    vs : [pay_time_0, pay_time_1, ...]
    ws : [pay_amount_0, pay_amount_1, ...]

For a query with a number `x`, we want to find the record after which our total received amount surpasses x.

## Assumption

To simplify, all pay times are supposed to be distinct, i.e., `assert len(set(vs)) == len(vs)` 

## Example
Suppose we have payment records :

    vs = [2, 1, 3]
    ws = [5, 7, 6]
    x = 13

If we sort the payment record according to the pay_time `vs`, we obtain a sorted collection of payment records:
    
    vs' = [1, 2, 3]
    ws' = [7, 5, 6]

Then, we compute a total received amount after each payment :

    total = [7, (7+5), (7+5+6)] = [7, 12, 18]
         
The first total amount that is greater than `x=13` is `18`, which corresponds to pay time `3`. Thus, the answer is `3` for `x = 13`.

## Performance
Given `k` queries, answer them within `O(n(ln(k)))` time complexity
