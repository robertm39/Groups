# -*- coding: utf-8 -*-
"""
Created on Sat May 14 21:13:47 2022

@author: rober
"""

import itertools

# Returns whether f is an isomorphism from g1 to g2.
def is_isomorphism(f, g1, g2):
    # Check that g1 and g2 are of the same order
    if g1.order() != g2.order():
        return False
    
    # Check that f is surjective
    image = [f(a) for a in g1]
    for a in g2:
        if not a in image:
            return False
    
    # Check that f respects the group operation
    for a, b in itertools.product(g1.elements, repeat=2):
        with g1.mul():
            p1 = f(a*b)
        with g2.mul():
            p2 = f(a)*f(b)
        if p1 != p2:
            return False
    
    return True