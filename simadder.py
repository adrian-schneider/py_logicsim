#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 18:28:35 2022

@author: adrianschneider
"""

import logicsim as ls
import stdgates as sg


class HalfAdder(ls.Module):
    #         _____
    # pinx>--|HA   |-->poutc
    #        |     |
    # piny>--|_____|-->pouts
    #
    #                   _____
    # pinx>-[DRVX]---+-|AND1 |
    #                | | &   |-->poutc
    # piny>-[DRVY]-+-|-|_____|
    #              | |
    #              | |  _____
    #              | +-|XOR1 |
    #              |   | =1  |-->pouts
    #              +---|_____|
    
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        # Internal gates.
        self.drvx = sg.Drv(circuit, self.qualified("DRVX"))
        self.drvy = sg.Drv(circuit, self.qualified("DRVY"))
        self.and1 = sg.And(circuit, self.qualified("AND"))
        self.xor1 = sg.Xor(circuit, self.qualified("XOR"))
        # Interface ports.
        self.pinx = self.drvx.pin
        self.piny = self.drvy.pin
        self.poutc = self.and1.pout
        self.pouts = self.xor1.pout
        # Internal wiring.
        self.wire(self.drvx.pout, self.and1.pin1)
        self.wire(self.drvy.pout, self.and1.pin2)
        self.wire(self.drvx.pout, self.xor1.pin1)
        self.wire(self.drvy.pout, self.xor1.pin2)
        
        
        
class FullAdder(ls.Module):
    #         _____                              _____
    # pinx>--|HA1  |-poutc----------------------|OR1  |
    #        |     |             _____          |>=1  |-->poutc
    # piny>--|_____|-pouts-pinx-|HA2  |--poutc--|_____|
    #                           |     |
    # pinc>----------------piny-|_____|------------------>pouts

    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        # Internal gates and modules.
        self.or1 = sg.Or(circuit, self.qualified("OR1"))
        self.ha1 = HalfAdder(circuit, self.qualified("HA1"))
        self.ha2 = HalfAdder(circuit, self.qualified("HA2"))
        # Interface ports.
        self.pinx = self.ha1.pinx
        self.piny = self.ha1.piny
        self.pinc = self.ha2.piny
        self.pouts = self.ha2.pouts
        self.poutc = self.or1.pout
        # Internal wiring.
        self.wire(self.ha1.poutc, self.or1.pin1)
        self.wire(self.ha2.poutc, self.or1.pin2)
        self.wire(self.ha1.pouts, self.ha2.pinx)
        
  
class QuickTestHA(ls.Circuit):
    """
    Perform a quick test of the half adder.
    This is done without using the simulator.
    Assign test values to the inputs directly and then call the evaluate and
    proceed methods on the circuit.
    Between evaluate and proceed, the ciruit's state is printed.
    """
    
    def __init__(self, name):
        super().__init__(name)
        self.ha1 = HalfAdder(self, "HA1")
        
        #ls.Gate.debug = True
        
        print(name)
        
        for xx in range(2):
            for yy in range(2):
                self.ha1.pinx.assign(xx)
                self.ha1.piny.assign(yy)
                
                self.evaluate()
                
                #print(self.state_str())
                
                print(f"x: {xx}, pouts: {self.ha1.pouts.value()}")
                print(f"y: {yy}, poutc: {self.ha1.poutc.value()}")
                
                self.proceed()
                
                print("-"*20)
                
                
class QuickTestFA(ls.Circuit):
    """
    Perform a quick test of the full adder.
    This is done without using the simulator.
    Assign test values to the inputs directly and then call the evaluate and
    proceed methods on the circuit.
    Between evaluate and proceed, the ciruit's state is printed.
    """
    
    def __init__(self, name):
        super().__init__(name)
        self.fa1 = FullAdder(self, "FA1")
        
        #ls.Gate.debug = True
        
        print(name)
        
        for xx in range(2):
            for yy in range(2):
                for inc in range(2):
                    self.fa1.pinx.assign(xx)
                    self.fa1.piny.assign(yy)
                    self.fa1.pinc.assign(inc)
                    
                    self.evaluate()
                    
                    #print(self.state_str())
                    
                    print(f"inc: {inc}")
                    print(f"x: {xx}, pouts: {self.fa1.pouts.value()}")
                    print(f"y: {yy}, poutc: {self.fa1.poutc.value()}")
                    
                    self.proceed()
                    
                    print("-"*20)

    
class Adder8Bit(ls.Circuit):
    
    def __init__(self, name):
        super().__init__(name)
        self.srcvv = sg.Source(self, "SRCVV")
        logic_0 = self.srcvv.pinv
        logic_1 = self.srcvv.pout

        #ls.Gate.debug = True

        self.fa0 = FullAdder(self, "FA0")
        self.fa1 = FullAdder(self, "FA1")
        self.fa2 = FullAdder(self, "FA2")
        self.fa3 = FullAdder(self, "FA3")
        self.fa4 = FullAdder(self, "FA4")
        self.fa5 = FullAdder(self, "FA5")
        self.fa6 = FullAdder(self, "FA6")
        self.fa7 = FullAdder(self, "FA7")
        
        self.srcx = sg.Source(self, "SRCX", 255, 0, 0, 9)
        self.srcy = sg.Source(self, "SRCY", 255, 0, 0, 11)
        
        self.wire(logic_0, self.fa0.pinc)
        self.wire(self.fa0.poutc, self.fa1.pinc)
        self.wire(self.fa1.poutc, self.fa2.pinc)
        self.wire(self.fa2.poutc, self.fa3.pinc)
        self.wire(self.fa3.poutc, self.fa4.pinc)
        self.wire(self.fa4.poutc, self.fa5.pinc)
        self.wire(self.fa5.poutc, self.fa6.pinc)
        self.wire(self.fa6.poutc, self.fa7.pinc)
        
        self.wire(self.srcx.pout, self.fa0.pinx, (0, 1))
        self.wire(self.srcx.pout, self.fa1.pinx, (1, 1))
        self.wire(self.srcx.pout, self.fa2.pinx, (2, 1))
        self.wire(self.srcx.pout, self.fa3.pinx, (3, 1))
        self.wire(self.srcx.pout, self.fa4.pinx, (4, 1))
        self.wire(self.srcx.pout, self.fa5.pinx, (5, 1))
        self.wire(self.srcx.pout, self.fa6.pinx, (6, 1))
        self.wire(self.srcx.pout, self.fa7.pinx, (7, 1))
        
        self.wire(self.srcy.pout, self.fa0.piny, (0, 1))
        self.wire(self.srcy.pout, self.fa1.piny, (1, 1))
        self.wire(self.srcy.pout, self.fa2.piny, (2, 1))
        self.wire(self.srcy.pout, self.fa3.piny, (3, 1))
        self.wire(self.srcy.pout, self.fa4.piny, (4, 1))
        self.wire(self.srcy.pout, self.fa5.piny, (5, 1))
        self.wire(self.srcy.pout, self.fa6.piny, (6, 1))
        self.wire(self.srcy.pout, self.fa7.piny, (7, 1))
        
        self.evaluate()
        
        print(self.state_str())
        
        xx = self.srcx.pout.value()
        yy = self.srcy.pout.value()
        
        outsum = (
            self.fa0.pouts.value()
            + (self.fa1.pouts.value() << 1)
            + (self.fa2.pouts.value() << 2)
            + (self.fa3.pouts.value() << 3)
            + (self.fa4.pouts.value() << 4)
            + (self.fa5.pouts.value() << 5)
            + (self.fa6.pouts.value() << 6)
            + (self.fa7.pouts.value() << 7)
        )
        print(f"sum of {xx} and {yy} is {outsum}.")
        
        self.proceed()
        
        print("-"*20)
        
        
# circuit = QuickTestHA("QuickTestHA")
# circuit = QuickTestFA("QuickTestFA")


circuit = Adder8Bit("8bit Adder")

# ls.Utility.no_color()
# # ls.Utility.default_color()

# sim = ls.Simulation(circuit)
# sim.debug = False
# sim.show_state = False
# sim.show_trace = True
# sim.cycles = 30
# sim.trace_maxwidth = 30
# sim.run()
