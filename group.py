# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:52:11 2022

@author: rober
"""

from enum import Enum
import itertools

class OpType(Enum):
    ADDITIVE='+'
    MULTIPLICATIVE='*'

#_current_add_groups = list()
#_current_mul_groups = list()

_add_group = None
_mul_group = None
_current_groups = list()

class Element:
    def __init__(self, val):
        self.val = val
    
    def __add__(self, o):
        add = _add_group.op
        return add(self, o)
    
    def __rmul__(self, o):
        if isinstance(o, Element):
            return o.__mul__(self)
        
        # If we are in an additive group,
        # and the multiplicand is an integer,
        # multiply like in an additive group
        if o != int(o):
            raise ValueError('Left multiplicand: {}'.format(o))
        
        #group = _current_add_groups[-1]
        if not self in _add_group:
            raise ValueError('Right multiplicand: {}'.format(self))
        
        result = _add_group.identity
        
        for _ in range(o):
            result = result + self
        
        return result
    
    def __mul__(self, o):
        mul = _mul_group.op
        return mul(self, o)
    
    def __pow__(self, o):
        result = _mul_group.identity
        
        if o != int(o):#not isinstance(o, int):
            raise ValueError('Exponent: {}'.format(o))
        
        for _ in range(o):
            result = result * self
        
        return result
    
    def __eq__(self, o):
        return self.val == o.val
    
    def __neq__(self, o):
        return self.val != o.val
    
    def __hash__(self):
        return hash(self.val) * 31
    
    def __str__(self):
        return str(self.val)
    
    def __repr__(self):
        return 'Element({})'.format(repr(self.val))

class BoundGroup:
    def __init__(self, group, op_type):
        self.group = group
        self.op_type = op_type
    
    def __enter__(self):
        global _add_group
        global _mul_group
        
        if self.op_type == OpType.ADDITIVE:
            _add_group = self.group
        elif self.op_type == OpType.MULTIPLICATIVE:
            _mul_group = self.group
        else:
            raise ValueError('Op type: {}'.format(self.op_type))
            
        _current_groups.append(self)
    
    def __exit__(self, *vals):
        global _add_group
        global _mul_group
        
        _current_groups.pop()
        
        if _current_groups:
            new_top = _current_groups[-1]
            if new_top.op_type == OpType.ADDITIVE:
                _add_group = new_top.group
            elif new_top.op_type == OpType.MULTIPLICATIVE:
                _mul_group = new_top.group
            else:
                raise ValueError('Op type: {}'.format(new_top.op_type))

class Group:
    def __init__(self, elements, op, default_type, identity=None):
        self.elements = list(elements)
        self.op = op
        self.default_type = default_type
        
        # Determine the identity element if not specified
        if identity is None:
            for e in elements:
                if op(e, e) == e:
                    self.identity = e
                    break
            # We couldn't fine one
            if identity is None:
                raise ValueError('No identity element')
        else:
            self.identity = identity
    
    def add(self):
        return BoundGroup(self, OpType.ADDITIVE)
    
    def mul(self):
        return BoundGroup(self, OpType.MULTIPLICATIVE)
    
    def __contains__(self, e):
        return e in self.elements
    
    def __iter__(self):
        return iter(self.elements)
    
    def __enter__(self):
        BoundGroup(self, self.default_type).__enter__()
    
    def __exit__(self, *vals):
        BoundGroup(self, self.default_type).__exit__()

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
                print('{} has no iverse'.format(a))

# Check whether the given group satisfies the group axioms.
def check_valid(group):
    check_identity(group)
    check_inverses(group)
    check_is_closed(group)
    check_associative(group)