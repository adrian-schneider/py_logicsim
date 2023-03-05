#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 18:28:35 2022

@author: adrianschneider
"""

import logicsim as ls
import stdgates as sg


class RAM(ls.Gate):
    """
    One byte RAM.
    
    Outputs
    -------
        pdout : 
            8bit data out.
    Inputs
    ------
        pdin :
            8bit data in.
        pcs :
            Chip select. Data output is hi-z on low.
        prw_ :
            Read write select. Write on low.
    """

    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self._mem = 0
        self.pdout = ls.Port(self, "pdout", 255, False)
        self.pdin = ls.Port(self, "pdin", 255, True)
        self.pcs = ls.Port(self, "pcs", 1, True)
        self.prw_ = ls.Port(self,"prw_", 1, True)

    def setup(self):
        cs = self.pcs.value()
        rw_ = self.prw_.value()
        self.pdout.assign(0)
        self.pdout.hi_z(not cs or (cs and not rw_))
        if cs:
            if rw_:
                print(f"*** RAM {self.name()} read {self._mem}")
                self.pdout.assign(self._mem)
            else:
                self._mem = self.pdin.value()
                print(f"*** RAM {self.name()} write {self._mem}")
            
            
class DRV(ls.Gate):
    """
    One byte output buffer.
    
    Outputs
    -------
        pdout :
            8bit data out.
    Inputs
    ------
        pdin :
            8bit data in.
    """
    
    def __init__(self, circuit, name):
        super().__init__(circuit, name)
        self.pdout = ls.Port(self, "pdout", 255, False)
        self.pdin = ls.Port(self, "pdin", 255, True)
        self.pcs = ls.Port(self, "pcs", 1, True)
        
    def setup(self):
        self.pdout.assign(self.pdin.value())
        self.pdout.hi_z(not self.pcs.value())

  
class BusTest(ls.Circuit):
    """
    SRC     SDRV   RAM1       RAM2       DRVO
            cs     cs   rw_   cs   rw_   cs
    00      1      1    0     0    0     0
    01      1      0    0     1    0     0
    10      0      1    1     0    1     1
    11      0      0    1     1    1     1
    
    SDRV.cs := ~SRC(1, 1)
    RAM1.rw_ := RAM2.rw_ := DRVO.cs := SRC(1, 1)
    RAM1.cs := ~SRC(1, 0)
    RAM2.cs := SRC(1, 0)
    """
    
    def __init__(self, name):
        super().__init__(name)
        # self.vpp =sg.Source(self, "VPP")
        # self.logic_0 = self.vpp.pinv
        # self.logic_1 = self.vpp.pout
        self.src = sg.Source(self, "SRC", 255, 4)
        self.ram1 = RAM(self, "RAM1")
        self.ram2 = RAM(self, "RAM2")
        self.drvo = DRV(self, "DRVO")
        self.drvs = DRV(self, "DRVS")
        self.inv1 = sg.Inv(self, "INV1")
        self.inv2 = sg.Inv(self, "INV2")

    def setup(self):
        self.wire(self.src.pout, self.drvs.pdin)
        self.wire(self.src.pout, self.inv2.pin, (1,1))
        self.wire(self.inv2.pout, self.drvs.pcs)
        
        self.define_bus("DATABUS", (
            (self.drvs.pdout, None)
            , (self.ram1.pdin, None), (self.ram1.pdout, None)
            , (self.ram2.pdin, None), (self.ram2.pdout, None)
            , (self.drvo.pdin, None)
        ))
        
        self.wire(self.src.pout, self.ram1.prw_, (1,1))
        self.wire(self.src.pout, self.ram2.prw_, (1,1))
        self.wire(self.src.pout, self.inv1.pin, (0,1))
        self.wire(self.inv1.pout, self.ram1.pcs)
        self.wire(self.src.pout, self.ram2.pcs, (0,1))
        self.wire(self.src.pout, self.drvo.pcs, (1,1))
        
        self.setup_trace("title1", "** 8bit Bus Test **", None)
        self.setup_trace("SRC.out", "ic1x", self.src.pout)
        self.setup_trace("DRVS.dout", "ic1x", self.drvs.pdout)
        self.setup_trace("rw_", "c1", self.ram1.prw_)
        self.setup_trace("RAM1.cs", "c1", self.ram1.pcs)
        self.setup_trace("RAM2.cs", "c1", self.ram2.pcs)
        self.setup_trace("DRVO.dout", "ic1xt", self.drvo.pdout)
        

circuit = BusTest("8bit Bus Test")

ls.Utility.no_color()
# ls.Utility.default_color()

sim = ls.Simulation(circuit)
sim.debug = True
sim.show_state = True
sim.show_trace = True
sim.cycles = 60
sim.trace_maxwidth = 30
sim.run()
