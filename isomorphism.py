# -*- coding: utf-8 -*-
"""
Created on Sat May 14 21:13:47 2022

@author: rober
"""

import itertools

import group

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

class Function:
    def __init__(self, f, domain, codomain):
        self.f = dict()
        
        for x in domain:
            y = f[x] if isinstance(f, dict) else f(x)
            if not y in codomain:
                raise ValueError('f({}) = {} not in codomain'.format(x, y))
            self.f[x] = y
    
    def __call__(self, x):
        return self.f[x]

# # Return a list of all isomorphisms from g1 to g2.
# def all_isomorphisms(g1, g2):
#     f = {g1.identity: g2.identity}
    
#     # For now, do it the dumb way
#     g1_rest = list(g1)
#     g1_rest.remove(g1.identity)
#     g2_rest = list(g2)
#     g2_rest.remove(g2.identity)
    
#     # Go through all bijections from g1 to g2 that map identity to identity
#     # and keep only the isomorphisms
#     isos = list()
#     for perm in itertools.permutations(g2_rest):
#         iso = dict(f)
#         for x, y in zip(g1_rest, perm):
#             iso[x] = y
        
#         iso = Function(iso, g1.elements, g2.elements)
#         if is_isomorphism(iso, g1, g2):
#             isos.append(iso)
    
#     return isos

def get_isomorphisms_helper(g1, g2, g1_o, g2_o, f, reached):
    # Are we already done?
    if len(f) == g1.order():
        return [f]
    
    # Get an element to add to the isomorphism
    # we'll get more extra information out of high-order elements
    # I could optimize this by sorting the elements by order at the start
    # and just taking from the top
    g1_h = max([a for a in g1 if not a in f],
                key = lambda a: g1_o[a])
    
    # Try out different elements to map g1_h to
    g2_hs = [a for a in g2 if g2_o[a] == g1_o[g1_h] and not a in reached]
    results = list()
    for g2_h in g2_hs:
        new_f = dict(f)
        new_reached = set(reached)
        new_vals = {g1_h}
        new_f[g1_h] = g2_h
        new_reached.add(g2_h)
        
        # Combine the newly calculated mappings with old mappings
        # to infer more mappings
        # Also, check that this still could be an isomorphism
        works = True
        while works and new_vals:
            # val = new_vals.pop()
            val = next(iter(new_vals))
            new_vals.remove(val)
            all_maps = list()
            for a in new_f:
                pairs = ((val, a), (a, val))
                maps = list()
                for a, b in pairs:
                    with g1:
                        left = a @ b
                    with g2:
                        right = new_f[a] @ new_f[b]
                    
                    maps.append((left, right))
                all_maps.extend(maps)
                
                for left, right in maps:
                    if left in new_f:
                        if new_f[left] != right:
                            # We've found an inconsistency
                            # This cannot be an isomorphism
                            works = False
                            break
                    else:
                        if right in new_reached:
                            # This mapping violates injectivity
                            works = False
                        else:
                            # We added a new mapping to the isomorphism
                            # new_f[left] = right
                            new_vals.add(left)
                            #new_reached.add(right)
                
                if not works:
                    break
            
            if not works:
                break
            
            for left, right in all_maps:
                new_f[left] = right
                new_reached.add(right)
    
        if works:
            # We've added all that we can and verified that the mapping
            # still could be an isomorphism
            
            # # Are we done?
            # if len(new_f) == g1.order():
            #     # We've figure out an entire isomorphism
            #     results.append(new_f)
            # else:
                
            # Time to recurse
            results.extend(get_isomorphisms_helper(g1,
                                                   g2,
                                                   g1_o,
                                                   g2_o,
                                                   new_f,
                                                   new_reached))
    
    return results    

def get_order_counts(orders):
    order_counts = dict()
    for _, order in orders.items():
        if not order in order_counts:
            order_counts[order] = 1
        else:
            order_counts[order] += 1

# Get all isomorphisms from g1 to g2.
# I'm pretty sure that this works correctly.
def get_isomorphisms(g1, g2):
    if g1.order() != g2.order():
        return list()
        # raise ValueError('g1.order(): {}, g2.order(): {}'
        #                  .format(g1.order(), g2.order()))
    
    f = {g1.identity: g2.identity}
    
    with g1:
        g1_o = {a: group.order(a) for a in g1}
    with g2:
        g2_o = {a: group.order(a) for a in g2}
    
    if get_order_counts(g1_o) != get_order_counts(g2_o):
        return list()
        # raise ValueError('Groups not isomorphic')
    
    reached = {g2.identity}
    
    isos = get_isomorphisms_helper(g1, g2, g1_o, g2_o, f, reached)
    return [Function(iso, g1.elements, g2.elements) for iso in isos]

# Return a list containing the isoclasses of g.
def get_isoclasses(g, autos=None):
    is_equiv = {(a, b): False for a in g for b in g}
    
    if autos is None:
        autos = all_isomorphisms(g, g)
    
    # Record which elements are equivalent
    for auto in autos:
        for a in g:
            # No need to do the other way around
            # because the inverse is also an automorphism
            is_equiv[a, auto(a)] = True
    
    elements = set(g.elements)
    isoclasses = list()
    
    while elements:
        a = next(iter(elements))
        isoclass = list()
        for b in elements:
            if is_equiv[a, b]:
                isoclass.append(b)
        for b in isoclass:
            elements.remove(b)
        isoclasses.append(isoclass)
    
    return isoclasses