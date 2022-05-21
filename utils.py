# -*- coding: utf-8 -*-
"""
Created on Sat May 21 09:05:31 2022

@author: rober
"""

import itertools
from group import *

# Return the order of the given element.
def order(a, op_type=OpType.DEFAULT):
    
    with op_type:
        # Get the identity
        e = ~a
        val = a
        i = 1
        while True:
            if val == e:
                return i
            val = val @ a
            i += 1

# def product_mul(a, b, op1, op2):
#     a0 = Element(a.val[0])
#     a1 = Element(a.val[1])
#     b0 = Element(b.val[0])
#     b1 = Element(b.val[1])
    
#     return Element((op1(a0, b0).val, op2(a1, b1).val))

# def product_group(g1, g2):
#     elements = list()
#     for a, b in itertools.product(g1, g2):
        
#         elements.append(Element((a.val, b.val)))
    
#     #op = lambda a, b: g1.op(a.val[0], b.val[0]), g2.op(a.val[1], b.val[1])
#     op = lambda a, b: product_mul(a, b, g1.op, g2.op)
    
#     identity = Element((g1.identity.val, g2.identity.val))
    
#     def_type = g1.default_type if g1.default_type == g2.default_type else OpType.MUL
    
#     return Group(elements, op, def_type, identity)

def product_mul(a, b, ops):
    result = list()
    
    for i, op in enumerate(ops):
        prod = op(Element(a.val[i]), Element(b.val[i])) 
        result.append(prod.val)
    
    return Element(tuple(result))

# Return a group that is the product of all the given groups
def product_group(*gs):
    # The product of no groups is isomorphic to the identity group
    if not gs:
        return group.add_cyclic(1)
    
    elements = list()
    for xs in itertools.product(*gs):
        elements.append(Element(tuple([x.val for x in xs])))
    
    #op = lambda a, b: g1.op(a.val[0], b.val[0]), g2.op(a.val[1], b.val[1])
    g_ops = [g.op for g in gs]
    # op = lambda a, b: product_mul(a, b, g1.op, g2.op)
    op = lambda a, b: product_mul(a, b, g_ops)
    
    # identity = Element((g1.identity.val, g2.identity.val))
    identity = Element(tuple([g.identity.val for g in gs]))
    
    # def_type = g1.default_type if g1.default_type == g2.default_type else OpType.MUL
    def_type = gs[0].default_type
    for g in gs[1:]:
        if g.default_type != def_type:
            def_type = OpType.MUL
            break
    
    return Group(elements, op, def_type, identity)