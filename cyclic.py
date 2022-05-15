# -*- coding: utf-8 -*-
"""
Created on Sat May 14 20:05:08 2022

@author: rober
"""

from group import Element, Group, OpType

# Return an additive cyclic group of the given order.
def add_cyclic(modulo):
    if modulo == 0:
        raise ValueError('modulo: {}'.format(modulo))
    
    op = lambda a, b: Element((a.val + b.val) % modulo)
    elements = [Element(i) for i in range(modulo)]
    
    return Group(elements, op, OpType.ADDITIVE, Element(0))

# Return a multiplicative cyclic group of the given order.
# If the order isn't one less than a prime, it doesn't work.
def mul_cyclic(modulo):
    if modulo in (0, 1):
        raise ValueError('modulo: {}'.format(modulo))
    
    op = lambda a, b: Element((a.val * b.val) % (modulo))
    elements = [Element(i) for i in range(1, modulo)]
    
    return Group(elements, op, OpType.MULTIPLICATIVE, Element(1))