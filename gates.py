#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:11:54 2022

@author: adrianschneider
"""

import logicsim as ls

class Decoder_3to8_74138(ls.Gate):
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pinA = ls.Port(self, "pinA", 1)
        self.pinB = ls.Port(self, "pinB", 1)
        self.pinC = ls.Port(self, "pinC", 1)
        self.pinG1 = ls.Port(self, "pinG1", 1)
        self.pinG2A_ = ls.Port(self, "pinG2A_", 1)
        self.pinG2B_ = ls.Port(self, "pinG2B_", 1)
        self.poutY = ls.Port(self, "poutY", 255, False)
        
    def setup(self):
        if self.pinG1.value() and not self.pinG2A_.value() and not self.pinG2B_.value():
            self.poutY.assign(1<<(self.pinA.value() + (self.pinB.value()<<1) + (self.pinC.value()<<2)))
        else:
            self.poutY.assign(0)
