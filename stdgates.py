#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 09:40:46 2022

@author: adrianschneider
"""

import logicsim as ls

class Source(ls.Gate):
    def __init__(self, circuit, name, bits=1, divider=0, start=0 \
                 , const=0xFFFFFFFF):
        super().__init__(circuit, name)
        self._divider = divider
        self._counter = start
        self._const = const
        self.pout = ls.Port(self, "pout", bits, False)
        self.pinv = ls.Port(self, "pinv", bits, False)
        
    def response_function(self, divider, counter):
        if divider:
            return counter // divider
        else:
            return self._const
    
    def setup(self):
        value = self.response_function(self._divider, self._counter)
        self.pout.assign(value)
        self.pinv.assign(~value)
        self._counter += 1
        

class Inv(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin = ls.Port(self, "pin", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        
    def setup(self):
        self.pout.assign(not self.pin.value())
        
        
class Drv(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin = ls.Port(self, "pin", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        self.pinv = ls.Port(self, "pinv", 1, False)
        
    def setup(self):
        value = self.pin.value()
        self.pout.assign(value)
        self.pinv.assign(not value)
        

class Delay(ls.Gate):
    def __init__(self, circuit, name, depth):
        super().__init__(circuit, name)
        self._buffer = [0] * depth
        self.pin = ls.Port(self, "pin", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        self.pinv = ls.Port(self, "pinv", 1, False)

    def setup(self):
        self._buffer[0] = self.pin.value()
        self._buffer = [self._buffer[(i>0)*(i-1)] for i in range(len(self._buffer))]
        print(self._buffer)
        value = self._buffer[-1]
        self.pout.assign(value)
        self.pinv.assign(not value)
        
        
class And(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin1 = ls.Port(self, "pin1", 1)
        self.pin2 = ls.Port(self, "pin2", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        
    def setup(self):
        self.pout.assign((self.pin1.value() and self.pin2.value()))
            
        
class Or(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin1 = ls.Port(self, "pin1", 1)
        self.pin2 = ls.Port(self, "pin2", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        
    def setup(self):
        self.pout.assign((self.pin1.value() or self.pin2.value()))
            
        
class Xor(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin1 = ls.Port(self, "pin1", 1)
        self.pin2 = ls.Port(self, "pin2", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        
    def setup(self):
        self.pout.assign((self.pin1.value() != self.pin2.value()))
            
        
class Nand(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin1 = ls.Port(self, "pin1", 1)
        self.pin2 = ls.Port(self, "pin2", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        
    def setup(self):
        self.pout.assign(not (self.pin1.value() and self.pin2.value()))
            
        
class Nand3(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pin1 = ls.Port(self, "pin1", 1)
        self.pin2 = ls.Port(self, "pin2", 1)
        self.pin3 = ls.Port(self, "pin3", 1)
        self.pout = ls.Port(self, "pout", 1, False)
        
    def setup(self):
        self.pout.assign(
            not (self.pin1.value() 
                 and self.pin2.value() 
                 and self.pin3.value()))
