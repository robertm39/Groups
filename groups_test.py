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

def isos_same(isos_1, isos_2):
    for iso_1 in isos_1:
        has_same = False
        for iso_2 in isos_2:
            is_same = True
            for x, y in iso_1.f.items():
                if iso_2(x) != y:
                    is_same = False
                    break
            if is_same:
                has_same = True
        
        if not has_same:
            return False
    
    return True

def test_5():
    # Get Z_2 x Z_2 x Z_2
    g = group.product_group(group.add_cyclic(8))
    
    # isos_1 = group.all_isomorphisms(g, g)
    # print('{} automorphisms'.format(len(isos_1)))
    # isoclasses = group.get_isoclasses(g, autos=isos_1)
    # for isoclass in isoclasses:
    #     print(('{}, '*len(isoclass)).format(*[a.val for a in isoclass]))
    
    # print('')
    
    isos_2 = group.get_isomorphisms(g, g)
    print('{} automorphisms'.format(len(isos_2)))
    
    # for iso in isos:
    #     if not group.is_isomorphism(iso, g, g):
    #         print('Not an isomorphism!')
    #     for a in g:
    #         print('{} -> {}'.format(a, iso(a)))
    #     print('')
    # print('')
    
    isoclasses = group.get_isoclasses(g, autos=isos_2)
    for isoclass in isoclasses:
        print(('{}, '*len(isoclass)).format(*[a.val for a in isoclass]))
        
    print('')
    print('Isos the same? {}'.format(isos_same(isos_1, isos_2)))

def main():
    test_5()

if __name__ == '__main__':
    main()