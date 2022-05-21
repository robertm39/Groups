# -*- coding: utf-8 -*-
"""
Created on Sat May 21 09:04:21 2022

@author: rober
"""

import itertools

# Check that the given group is associative.
# Runs in cubic time relative to the order of the group.
def check_associative(group):
    with group.mul():
        for a, b, c in itertools.product(group.elements, repeat=3):
            p1 = (a*b)*c
            p2 = a*(b*c)
            if p1 != p2:
                raise ValueError('(a*b)*c: {}, a*(b*c): {}'.format(p1, p2))

def check_is_closed(group):
    with group.mul():
        for a, b in itertools.product(group.elements, repeat=2):
            if not a*b in group:
                raise ValueError('a*b not in group: {}*{}={}'.format(a, b, a*b))

def check_identity(group):
    with group.mul():
        for a in group:
            if a*group.identity != a:
                raise ValueError('a*e != a: {}'.format(a))
            if group.identity*a != a:
                raise ValueError('e*a != a: {}'.format(a))

def check_inverses(group):
    with group.mul():
        for a in group:
            has_inverse = False
            for b in group:
                if a*b == b*a == group.identity:
                    has_inverse = True
                    break
            if not has_inverse:
                print('{} has no inverse'.format(a))

# Check whether the given group satisfies the group axioms.
def check_valid(group):
    check_identity(group)
    check_inverses(group)
    check_is_closed(group)
    check_associative(group)
