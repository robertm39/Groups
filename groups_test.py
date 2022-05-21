# -*- coding: utf-8 -*-
"""
Created on Sat May 14 19:40:57 2022

@author: rober
"""

import group
from group import OpType, Group, Element, GroupContext
import cyclic
import isomorphism

def test_1():
    elements = Element(0), Element(1)
    a0, a1 = elements
    
    op = lambda a, b: Element((a.val + b.val)%2)
    group = Group(elements, op, OpType.ADD, a0)
    
    with group:
        print(a0 + a0)
        print(a1 + a0)
        print(a0 + a1)
        print(a1 + a1)
        print('')
        print(0*a1)
        print(1*a1)
        print(2*a1)
        print(3*a1)

def test_2():
    # Try the field of integers, modulo 5
    add_group = group.add_cyclic(5)
    mul_group = group.mul_cyclic(5)
    
    group.check_valid(add_group)
    group.check_valid(mul_group)
    
    a0, a1, a2, a3, a4 = add_group.elements
    
    # with add_group:
    #     with mul_group:
    with add_group:
        print('order(1): {}'.format(group.order(a1)))
    
    with GroupContext(add_group, mul_group):
        print('3 + 4: {}'.format(a3 + a4))
        print('2 * 3: {}'.format(a2 * a3))
        print('4 * 3: {}'.format(a4 * a3))
        print('2 ** 3: {}'.format(a2 ** 3))
        print('2 ** 4: {}'.format(a2 ** 4))
        print('1 + 4: {}'.format(a1 + a4))

def iso(base, a, group):
    with group.mul():
        return base ** a.val

def test_3():
    g = group.add_cyclic(9)
    a2 = Element(2)
    func = lambda a: iso(a2, a, g)
    
    print('Is isomorphism? {}'.format(isomorphism.is_isomorphism(func, g, g)))

def test_4():
    g1 = group.add_cyclic(2)
    g2 = group.add_cyclic(2)
    
    g = group.product_group(g1, g2)
    for a in g:
        print(a)
    
    print('')
    
    with g:
        a = Element((0, 1))
        b = Element((1, 0))
        c = a+b
        print(a+b)
        print(a+c)
        print(b+c)
        print(c+c)
        print(a+a)
        print(b+b)

def main():
    test_4()

if __name__ == '__main__':
    main()