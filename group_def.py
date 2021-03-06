# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:52:11 2022

@author: rober
"""

from enum import Enum

#_current_add_groups = list()
#_current_mul_groups = list()

_ops = list()

class OpType(Enum):
    ADD='+'
    MUL='*'
    DEFAULT='?'
    
    def __enter__(self):
        global _ops
        _ops.append(self)
    
    def __exit__(self, *vals):
        global _ops
        _ops.pop()

#_add_group = None
#_mul_group = None
#_current_groups = list()

_group_context = list()

class Element:
    def __init__(self, val):
        self.val = val
    
    def check_in_group(self):
        # if _add_group and self in _add_group:
        #     return
        
        # if _mul_group and self in _mul_group:
        #     return
        if not _group_context:
            raise ValueError('Not in any active groups')
        
        context = _group_context[-1]
        if context.add and self in context.add:
            return
        if context.mul and self in context.mul:
            return
        
        raise ValueError('Not in any active groups')
    
    def __add__(self, o):
        self.check_in_group()
        
        # add = _add_group.op
        add = _group_context[-1].add.op
        return add(self, o)
    
    def __rmul__(self, o):
        self.check_in_group()
        
        if isinstance(o, Element):
            return o.__mul__(self)
        
        # If we are in an additive group,
        # and the multiplicand is an integer,
        # multiply like in an additive group
        if o != int(o):
            raise ValueError('Left multiplicand: {}'.format(o))
        
        #group = _current_add_groups[-1]
        # if not self in _add_group:
        if not self in _group_context[-1].add:
            raise ValueError('Right multiplicand: {}'.format(self))
        
        # result = _add_group.identity
        result = _group_context[-1].add.identity
        
        for _ in range(o):
            result = result + self
        
        return result
    
    def __mul__(self, o):
        self.check_in_group()
        
        # Accept integer multiplication, even on the right
        if type(o) in (int, float) and o == int(o):
            return o * self
        
        # mul = _mul_group.op
        mul = _group_context[-1].mul.op
        return mul(self, o)
    
    # Do whatever operation is the current operation
    # If none is specified, do the only one possible
    # If both are possible, fail
    def __matmul__(self, o):
        self.check_in_group()
        
        global _ops
        if _ops:
            op = _ops[-1]
            if op == OpType.ADD:
                return self + o
            elif op == OpType.MUL:
                return self * o
            elif op != OpType.DEFAULT:
                raise ValueError('Op type: {}'.format(op))
        
        # if _add_group and self in _add_group:
        #     if _mul_group and self in _mul_group:
        context = _group_context[-1]
        if context.add and self in context.add:
            if context.mul and self in context.mul:
                raise ValueError('Operation ambiguous')
            return self + o
        elif self in context.mul:
            return self * o
    
    # Return the element either times zero or the the zeroth power
    def __invert__(self):
        self.check_in_group()
        
        global _ops
        if _ops:
            op = _ops[-1]
            if op == OpType.ADD:
                return 0 * self
            elif op == OpType.MUL:
                return self ** 0
            elif op != OpType.DEFAULT:
                raise ValueError('Op type: {}'.format(op))
        
        # if _add_group and self in _add_group:
        #     if _mul_group and self in _mul_group:
        context = _group_context[-1]
        if context.add and self in context.add:
            if context.mul and self in context.mul:
                raise ValueError('Operation ambiguous')
            return 0 * self
        # elif self in _mul_group:
        elif self in context.mul:
            return self ** 0
    
    def __pow__(self, o):
        self.check_in_group()
        
        # result = _mul_group.identity
        result = _group_context[-1].mul.identity
        
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

class GroupContext:
    def __init__(self, add, mul):
        self.add = add
        self.mul = mul
    
    def __enter__(self):
        global _group_context
        _group_context.append(self)
    
    def __exit__(self, *vars):
        global _group_context
        _group_context.pop()

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
        # return BoundGroup(self, OpType.ADD)
        return GroupContext(self, None)
    
    def mul(self):
        # return BoundGroup(self, OpType.MUL)
        return GroupContext(None, self)
    
    def order(self):
        return len(self)
    
    def __contains__(self, e):
        return e in self.elements
    
    def __iter__(self):
        return iter(self.elements)
    
    def __len__(self):
        return len(self.elements)
    
    def __enter__(self):
        # BoundGroup(self, self.default_type).__enter__()
        context = self.add() if self.default_type == OpType.ADD else self.mul()
        context.__enter__()
    
    def __exit__(self, *vals):
        context = self.add() if self.default_type == OpType.ADD else self.mul()
        context.__exit__()
        # BoundGroup(self, self.default_type).__exit__()