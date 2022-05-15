# -*- coding: utf-8 -*-
"""
Created on Sat May 14 19:40:57 2022

@author: rober
"""

import group
from group import OpType, Group, Element
import cyclic

def test_1():
    elements = Element(0), Element(1)
    a0, a1 = elements
    
    op = lambda a, b: Element((a.val + b.val)%2)
    group = Group(elements, op, OpType.ADDITIVE, a0)
    
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
    # Try the field of integers, module 5
    add_group = cyclic.add_cyclic(5)
    mul_group = cyclic.mul_cyclic(5)
    
    group.check_valid(add_group)
    group.check_valid(mul_group)
    
    a0, a1, a2, a3, a4 = add_group.elements
    
    with add_group:
        with mul_group:
            print('3 + 4: {}'.format(a3 + a4))
            print('2 * 3: {}'.format(a2 * a3))
            print('4 * 3: {}'.format(a4 * a3))
            print('2 ** 3: {}'.format(a2 ** 3))
            print('2 ** 4: {}'.format(a2 ** 4))
        print('1 + 4: {}'.format(a1 + a4))
    
def main():
    test_2()

if __name__ == '__main__':
    main()