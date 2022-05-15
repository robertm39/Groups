# -*- coding: utf-8 -*-
"""
Created on Sat May 14 19:40:57 2022

@author: rober
"""

import groups
from groups import GroupType, Group, Element

def test_1():
    elements = Element(0), Element(1)
    a0, a1 = elements
    
    op = lambda a, b: Element((a.val + b.val)%2)
    group = Group(elements, op, GroupType.ADDITIVE, a0)
    
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
    
    
def main():
    test_1()

if __name__ == '__main__':
    main()