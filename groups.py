# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:52:11 2022

@author: rober
"""

from enum import Enum

class GroupType(Enum):
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
        
        result = _add_group.id
        
        for _ in range(o):
            result = result + self
        
        return result
    
    def __mul__(self, o):
        mul = _mul_group.op
        return mul(self, o)
    
    def __exp__(self, o):
        result = _mul_group.id
        
        if o != int(o):#not isinstance(o, int):
            raise ValueError('Exponent: {}'.format(o))
        
        for _ in range(o):
            result = result * self
        
        return result

class BoundGroup:
    def __init__(self, group, op_type):
        self.group = group
        self.op_type = op_type

class Group:
    def __init__(self, elements, op, default_type):
        self.elements = list(elements)
        self.op = op
        self.default_type = default_type
    
    def __enter__(self):
        global _add_group
        global _mul_group
        
        if self.default_type == GroupType.ADDITIVE:
            _add_group = self
        elif self.default_type == GroupType.MULTIPLICATIVE:
            _mul_group = self
        else:
            raise ValueError('Op type: {}'.format(self.default_type))
            
        _current_groups.append(BoundGroup(self, self.default_type))
    
    def __exit__(self):
        popped = _current_groups.pop()
        if not popped is self:
            raise ValueError('Stack error: {} != {}'.format(self, popped))
        
        if _current_groups:
            new_top = _current_groups[-1]
            if new_top.op_type == GroupType.ADDITIVE:
                _add_group = new_top
            elif new_top.op_type == GroupType.MULTIPLICATIVE:
                _mul_group = new_top
            else:
                raise ValueError('Op type: {}'.format(new_top.op_type))