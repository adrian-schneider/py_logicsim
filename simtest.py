#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 09:40:46 2022

@author: adrianschneider
"""

import logicsim as ls
import stdgates as sg
import gates as gt

class InvTest(ls.Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.inv1 = sg.Inv(self, "INV1")
        self.inv2 = sg.Inv(self, "INV2")
        self.inv3 = sg.Inv(self, "INV3")
        
    def setup(self):
        self.wire(self.inv1.pout, self.inv2.pin)
        self.wire(self.inv2.pout, self.inv3.pin)
        self.wire_back(self.inv3.pout, self.inv1.pin)

        self.setup_trace("inv1", "v", self.inv1.pout)
        self.setup_trace("inv2", "v", self.inv2.pout)
        self.setup_trace("inv3", "tv", self.inv3.pout)
        
        
class FlipFlop(ls.Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.src = sg.Source(self, "SRC", 1, 4)
        self.nand1 = sg.Nand(self, "NAND1")
        self.nand2 = sg.Nand(self, "NAND2")
        
    def setup(self):
        self.wire(self.src.pout, self.nand1.pin1)
        self.wire(self.src.pinv, self.nand2.pin2)
        self.wire_back(self.nand1.pout, self.nand2.pin1)
        self.wire_back(self.nand2.pout, self.nand1.pin2)
        
        self.setup_trace("title1", "** Nand FlipFlop **", None)
        self.setup_trace("in1", "v", self.nand1.pin1)
        self.setup_trace("in2", "v", self.nand2.pin2)
        self.setup_trace("Q", "v", self.nand1.pout)
        self.setup_trace("Q_", "tv", self.nand2.pout)
        
        
class JKFlipFlop(ls.Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.src = sg.Source(self, "SRC", 1, 8)
        self.clk = sg.Source(self, "CLK", 1, 2)
        self.nand1 = sg.Nand(self, "NAND1")
        self.nand2 = sg.Nand(self, "NAND2")
        self.nandj = sg.Nand3(self, "NANDJ")
        self.nandk = sg.Nand3(self, "NANDK")
        
    def setup(self):
        # J K
        self.wire(self.src.pout, self.nandj.pin2)
        self.wire(self.src.pinv, self.nandk.pin2)
        
        # C
        self.wire(self.clk.pout, self.nandj.pin3)
        self.wire(self.clk.pout, self.nandk.pin1)
        
        # FlipFlop
        self.wire(self.nandj.pout, self.nand1.pin1)
        self.wire(self.nandk.pout, self.nand2.pin2)
        
        self.wire_back(self.nand1.pout, self.nandk.pin3)
        self.wire_back(self.nand2.pout, self.nandj.pin1)
        
        self.wire_back(self.nand1.pout, self.nand2.pin1)
        self.wire_back(self.nand2.pout, self.nand1.pin2)
        
        self.setup_trace("title1", "** Nand JK-FlipFlop **", None)
        self.setup_trace("CLK ", "", self.clk.pout)
        self.setup_trace("J", "", self.nandj.pin2)
        self.setup_trace("K", "", self.nandk.pin2)
        self.setup_trace("Q", "", self.nand1.pout)
        self.setup_trace("Q_", "t", self.nand2.pout)
        
        
class NandTest(ls.Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.src1 = sg.Source(self, "SRC", 1, 4)
        self.src2 = sg.Source(self, "SRC", 1, 4, 2)
        self.nand1 = sg.Nand(self, "NAND1")

    def setup(self):
        self.wire(self.src1.pout, self.nand1.pin1)
        self.wire(self.src2.pinv, self.nand1.pin2)
        
        self.setup_trace("title1", "** Nand **", None)
        self.setup_trace("in1", "", self.nand1.pin1)
        self.setup_trace("in2", "", self.nand1.pin2)
        self.setup_trace("NAND", "t", self.nand1.pout)
        
        
class DecoderTest(ls.Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.src1 = sg.Source(self, "SRC", 1)
        self.clk1 = sg.Source(self, "CLK", 1, 2)
        self.cnt1 = sg.Source(self, "CNT", 7, 4)
        self.dec1 = gt.Decoder_3to8_74138(self, "DEC1")
        
    def setup(self):
        self.wire(self.cnt1.pout, self.dec1.pinA, (0, 1))
        self.wire(self.cnt1.pout, self.dec1.pinB, (1, 1))
        self.wire(self.cnt1.pout, self.dec1.pinC, (2, 1))
        
        self.wire(self.clk1.pout, self.dec1.pinG1)
        self.wire(self.src1.pinv, self.dec1.pinG2A_)
        self.wire(self.src1.pinv, self.dec1.pinG2B_)

        self.setup_trace("title1", "** 74138 Decoder 3 to 8 **", None)
        self.setup_trace("A", "", self.dec1.pinA)
        self.setup_trace("B", "", self.dec1.pinB)
        self.setup_trace("C", "", self.dec1.pinC)
        self.setup_trace("G1", "", self.dec1.pinG1)
        self.setup_trace("G2A_ ", "", self.dec1.pinG2A_)
        self.setup_trace("G2B_ ", "", self.dec1.pinG2B_)
        self.setup_trace("Y", "txi", self.dec1.poutY)

class SourceTest(ls.Circuit):
    def __init__(self, name):
        super().__init__(name)
        self.src1 = sg.Source(self, "SRC", 1, 0)        # constabnt
        self.clk1 = sg.Source(self, "CLK1", 1, 4)       # div 4
        self.clk2 = sg.Source(self, "CLK2", 1, 4, 2)    # div 4, start 2
        self.cnt1 = sg.Source(self, "CNT1", 255, 4, 2)  # div 4, start 2
        
    def setup(self):
        self.setup_trace("title1", "** Source Test **", None)
        self.setup_trace("SRC", "c1", self.src1.pout)
        self.setup_trace("SRC_ ", "c2", self.src1.pinv)
        self.setup_trace("CLK1", "c3", self.clk1.pout)
        self.setup_trace("CLK2", "sc4", self.clk2.pout)
        self.setup_trace("CNT1", "txic5", self.cnt1.pout)
        
        
class SourceTestTrigger(ls.Trigger):
    def is_start(self):
        return self.circuit.clk1.pout.value() and self.circuit.clk2.pout.value()
    
    def is_stop(self):
        return not self.circuit.clk1.pout.value() and self.circuit.clk2.pout.has_changed_hi()
               

#print("\f")
            
# circuit = InvTest("invTest1")
# circuit = NandTest("NandTest")
# circuit = FlipFlop("flipFlop1")
circuit = JKFlipFlop("JKFlipFlop")
# circuit = DecoderTest("3 to 8 Decoder")
# circuit = SourceTest("Source")

ls.Utility.no_color()
ls.Utility.default_color()

sim = ls.Simulation(circuit)
sim.debug = False
sim.show_state = True
sim.show_trace = True
sim.cycles = 30
sim.trace_maxwidth = 30
sim.run()

# circuit = SourceTest("Source")
# trigger = SourceTestTrigger(5)

# sim = ls.Simulation(circuit, trigger)
# sim.debug = False
# sim.show_state = False
# sim.show_trace = True
# sim.cycles = 30
# sim.trace_maxwidth = 30
# sim.run()
