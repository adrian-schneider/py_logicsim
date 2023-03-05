#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 09:40:46 2022

@author: adrianschneider
"""

class Utility:
    F_COLOR = 7
    F_8BIT = 16
    F_SUBTITLE = 32
    F_INFILL = 64
    F_TIME_MARKS = 128
    
    # https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit
    # https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    
    CLOW = ""
    CHIGH = ""
    CEND = ""
       
    color = None
        
    @classmethod
    def no_color(cls):
        cls.color = [
            ("", "", "")
            , ("", "", "")
            , ("", "", "")
            , ("", "", "")
            , ("", "", "")
            , ("", "", "")
            , ("", "", "")
            , ("", "", "")
        ]

    @classmethod
    def default_color(cls):
        cls.color = [
            ("", "", "")
            , (cls.LIGHT_RED, cls.LIGHT_RED, cls.END)
            , (cls.YELLOW, cls.YELLOW, cls.END)
            , (cls.LIGHT_GREEN, cls.LIGHT_GREEN, cls.END)
            , (cls.LIGHT_BLUE, cls.LIGHT_BLUE, cls.END)
            , (cls.LIGHT_PURPLE, cls.LIGHT_PURPLE, cls.END)
            , (cls.LIGHT_WHITE, cls.LIGHT_WHITE, cls.END)
            , (cls.LIGHT_GREEN, cls.LIGHT_RED, cls.END)
        ]

    @classmethod
    def format_str(cls, fstr):
        fmt = cls.F_8BIT*('x' in fstr) \
            | cls.F_SUBTITLE*('s' in fstr) \
            | cls.F_INFILL*('i' in fstr) \
            | cls.F_TIME_MARKS*('t' in fstr)
            
        ci = fstr.find("c") + 1
        if ci:
            fmt = fmt + (int(fstr[ci]) & cls.F_COLOR)
        return fmt
    
    @classmethod
    def ascii_trace(cls, trace_list, fmt_list, maxwidth, trigger_mark):
        def tickmark(tick):
            return (":  ", "{:<3}".format(tick%100))[0==tick%5]
        
        def value_text(value, value_prev):
            vt = "  "
            if gformat&cls.F_INFILL and (value != value_prev):
                if gformat&cls.F_8BIT:
                    vt = "{:02X}".format(value&0xff)
                else:
                    vt = " {:1X}".format(value&0xf)
            return vt
        
        def subtitle(value, value_prev):
            st = "   "
            if value != value_prev:
                if gformat&cls.F_8BIT:
                    st = " {:02X}".format(value&0xff)
                else:
                    st = "  {:1X}".format(value&0xf)
            return st
        
        def trace_upper(value, value_prev):
            return ("", cls.CHIGH)[(value!=value_prev) and (value>0)] \
                + ("", cls.CLOW)[(value!=value_prev) and not value] \
                + ("", " ")[value!=value_prev] \
                + ("", " ", "_")[((value>0)+1)*(value==value_prev)] \
                + ("  ", "__")[value>0]
            
        def trace_lower(value, value_prev, slope_rise, slope_fall, value_text):
            return ("", cls.CHIGH)[(value!=value_prev) and (value>0)] \
                + ("", cls.CLOW)[(value!=value_prev) and not value] \
                + ("", slope_rise)[value>value_prev] \
                + ("", slope_fall)[value<value_prev] \
                + ("", "_", " ")[((value>0)+1)*(value==value_prev)] \
                + ("__", value_text)[value>0]
                
        def set_color(color_index):
            if cls.color is None:
                cls.default_color()
            cls.CLOW, cls.CHIGH, cls.CEND = cls.color[color_index]

        maxkeylen = 0
        datalen = 0
        for key, values in trace_list.items():
            if (values is not None) and (len(key) > maxkeylen):
                datalen = len(values.data())
                maxkeylen = len(key)
        assert datalen > 0
        assert maxkeylen > 0
        for ii in range(0, datalen, maxwidth):
            for key, values in trace_list.items():
                if values is None:
                    print(fmt_list[key])
                else:
                    data = values.data()
                    if key in fmt_list:
                        gformat = fmt_list[key]
                    else:
                        gformat = cls.F_8BIT | cls.F_INFILL
                    set_color(gformat & cls.F_COLOR)
                    str1 = " " * maxkeylen
                    str2 = "{:{}}".format(key, maxkeylen)
                    str3 = " " * maxkeylen
                    vvp = data[ii]
                    vvpt = -1
                    vv0 = vvp > 0
                    str1 += (cls.CLOW, cls.CHIGH)[vv0]
                    str2 += (cls.CLOW, cls.CHIGH)[vv0]
                    vs1, vs2 = "/", "\\"
                    for vv, kk in zip(data[ii:ii+maxwidth], range(len(data))):
                        vt = value_text(vv, vvpt)
                        str1 += trace_upper(vv, vvp)
                        str2 += trace_lower(vv, vvp, vs1, vs2, vt)
                        if gformat&cls.F_TIME_MARKS:
                            if kk == trigger_mark:
                                str3 += "T  "
                            else:
                                str3 += tickmark(ii+kk)
                        elif gformat&cls.F_SUBTITLE:
                            str3 += subtitle(vv,vvp)
                        vvp = vv
                        vvpt = vv
                    print(str1 + cls.CEND)
                    print(str2 + cls.CEND)
                    if gformat&(cls.F_SUBTITLE|cls.F_TIME_MARKS):
                        print(str3)
            print()
    

class Port:
    def __init__(self, gate, name, bits=0xff, is_input=True, hi_z=False):
        self._name = name
        self._parent = gate
        self._is_input = is_input
        self._value = 0
        self._previous_value = self._value
        self._next_value = self._value
        self._is_defined = False
        self._use_next = False
        self._bits = bits
        self._hi_z = hi_z
        self._parent.append_port(self)
        
    def name(self):
        return self._name
    
    def full_name(self):
        return "{}.{}".format(self._parent.name(), self.name())
    
    def is_defined(self):
        return self._is_defined
    
    def is_defined_next(self):
        return not self._is_defined and self._use_next
    
    def is_input(self):
        return self._is_input
    
    def is_output(self):
        return not self._is_input
    
    def _assert_is_defined(self):
        assert self.is_defined(), "Port {} is undefined.".format(
            self.full_name())
            
    def value(self, bits=None):
        self._assert_is_defined()
        vv = (not self._hi_z) * self._value
        if bits is not None:
            bit_nr, bit_pat = bits
            return (vv & (bit_pat<<bit_nr))>>bit_nr
        else:
            return vv
    
    def has_changed(self):
        self._assert_is_defined()
        return self._value != self._previous_value
    
    def has_changed_lo(self):
        self._assert_is_defined()
        return self._value < self._previous_value
    
    def has_changed_hi(self):
        self._assert_is_defined()
        return self._value > self._previous_value
    
    def hi_z(self, value):
        self._hi_z = value
    
    def is_hi_z(self):
        return self._hi_z
    
    def _assign(self, value):
        self._value = value & self._bits
        self._is_defined = True
        
    def assign(self, value, bits=None):
        if bits is not None:
            bit_nr, bit_pat = bits
            self._assign((self._value & ~(bit_pat<<bit_nr)) | ((value & bit_pat)<<bit_nr))
        else:
            self._assign(value)
        
    def _assign_next(self, value):
        self._next_value = value & self._bits
        self._use_next = True
        
    def assign_next(self, value, bits=None):
        assert self._is_input, f"Cannot assign-next to an output like {self.full_name()}."
        if bits is not None:
            bit_nr, bit_pat = bits
            self._assign_next((self._value & ~(bit_pat<<bit_nr)) | ((value & bit_pat)<<bit_nr))
        else:
            self._assign_next(value)
            
    def on_same_gate_as(self, port):
        return self._parent is port._parent

    def proceed(self):
        self._assert_is_defined()
        self._previous_value = self._value
        self._is_defined = False
        if (self._use_next):
            self._value = self._next_value
            self._use_next = False
            self._is_defined = True
        
    def state_str(self):
        if self.is_defined():
            sep = ('==', '=\\')[self.has_changed_lo()]
            sep = (sep, '=/')[self.has_changed_hi()]
            sep = (sep, '=Z')[self.is_hi_z()]
            nxt = ("", f"(next={self._next_value:x})")[self._use_next]
            return "{}{}{:x}{}".format(self.name(), sep, self.value(), nxt)
        else:
            return f"{self.name()} is undefined"
        
            
class Gate:
    debug = False
    
    def __init__(self, circuit, name):
        self._parent = circuit
        self._name = name
        self._is_defined = False
        self._all_ports = []
        self._parent.append_gate(self)
        
    def name(self):
        return self._name
    
    def append_port(self, port):
        self._all_ports.append(port)
        
    def is_defined(self):
        return self._is_defined
        
    def _assert_is_defined(self):
        assert self.is_defined(), "Gate {} is undefined.".format(self.name())
        
    def state_str(self):
        str = "{}:".format(self._name)
        first = True
        for port in self._all_ports:
            str += (",", "")[first] + " " + port.state_str()
            first = False
        return str
    
    def setup(self):
        assert False, "Method must be implemented in subclass."
        
    def _can_setup(self):
        res = True
        for port in self._all_ports:
            if port.is_input():
                res = res and port.is_defined()
        return res
    
    def _debug_undefined_ports(self):
        msg = ""
        if self.debug:
            first = True
            for port in self._all_ports:
                if port.is_input() and not port.is_defined():
                    if not msg:
                        msg = "   Undefined input(s) on {}:".format(self.name())
                    msg += (",", "")[first] + " {}".format(port.name())
                    first = False
            if msg:
                print(msg)
        
    def _debug_evaluate(self):
        if self.debug:
            ev = ("", "skip")[self._is_defined]
            if not self._is_defined:
                ev = ("fail", "success")[self._can_setup()]
            print("-- Gate {} {}.".format(self._name, ev))

    def evaluate(self):
        self._debug_evaluate()
        self._debug_undefined_ports()
        if not self._is_defined:
            if self._can_setup():
                self.setup()
                self._is_defined = True
    
    def proceed(self):
        self._assert_is_defined()
        self._is_defined = False;
        for port in self._all_ports:
            port.proceed()
            

class Circuit:
    def __init__(self, name):
        self._name = name
        self._all_gates = []
        self._all_wires = []
        self._trace_format = {}
        self._trace_source = {}
        self._bus = {}
        
    def name(self):
        return self._name
    
    def append_gate(self, gate):
        self._all_gates.append(gate)
        
    def _count_gates(self):
        return len(self._all_gates)
    
    def _count_gates_evaluated(self):
        count = 0
        for gate in self._all_gates:
            count += gate.is_defined()
        return count
    
    def state_str(self):
        str = "'{}'\n".format(self._name)
        for gate in self._all_gates:
            str += gate.state_str() + "\n"
        return str
    
    def _wire(self, p_out, p_in, is_back, bits_out, bits_in):
        self._all_wires.append((p_out, p_in, is_back, bits_out, bits_in))
        
    def wire(self, p_out, p_in, bits_out=None, bits_in=None):
        self._wire(p_out, p_in, False, bits_out, bits_in)
    
    def wire_back(self, p_out, p_in, bits_out=None, bits_in=None):
        self._wire(p_out, p_in, True, bits_out, bits_in)
        p_in.assign(0)
    
    def _wire_bus(self, all_bus_items):
        """
        Wire a bus by placing a wire from every output to every input of the
        bus.

        Parameters
        ----------
        all_bus_items : ((port, (bit_no, bit_shift)), ...)
            List of touples of a port and a bit selector.
            The bit selector can be None.

        Returns
        -------
        None.

        """
        for bus_item in all_bus_items:
            pout, pout_bits = bus_item
            for bus_item_2 in all_bus_items:
                pin, pin_bits = bus_item_2
                if pin.is_input():
                    if pin.on_same_gate_as(pout):
                        self.wire_back(pout, pin, pout_bits, pin_bits)
                    else:
                        self.wire(pout, pin, pout_bits, pin_bits)
    
    def define_bus(self, name, all_bus_items):
        """
        Define a bus with a list of all input and output ports with bit 
        selectors.

        Parameters
        ----------
        name : string
            Name of this bus.
        all_bus_items : ((port, (bit_no, bit_shift)), ...)
            List of touples of a port and a bit selector.
            The bit selector can be None.

        Returns
        -------
        None.

        """
        self._bus[name] = all_bus_items
        self._wire_bus(all_bus_items)
        
    def assert_no_bus_contention(self):
        for bus_name in self._bus:
            lo_z_count = 0
            msgstr = ""
            for bus_item in self._bus[bus_name]:
                pout, pout_bits = bus_item
                if not pout.is_input():
                    if not pout.is_hi_z():
                        lo_z_count += 1
                        msgstr += ("", ", ")[msgstr != ""] + f"{pout.full_name()}"
            assert lo_z_count <= 1, f"Bus contention on {bus_name}: {msgstr} are lo-z."
        
    def _evaluate_wire(self, wire):
        p_out, p_in, is_wire_back, bits_out, bits_in = wire
        if p_out.is_defined() and not p_out.is_hi_z():
            if is_wire_back:
                p_in.assign_next(p_out.value(bits_out), bits_in)
            else:
                p_in.assign(p_out.value(bits_out), bits_in)
                
    def _evaluate_wire_loom(self):
        for wire in self._all_wires:
            self._evaluate_wire(wire)
    
    def _evaluate_gates(self):
        for gate in self._all_gates:
            gate.evaluate()
            
    def evaluate(self):
        cycle = 0
        gtotal = self._count_gates()
        geval = self._count_gates_evaluated()
        while gtotal > geval:
            if Gate.debug:
                print("Circuit eval attempt {}".format(cycle))
            cycle += 1
            self._evaluate_gates()
            self._evaluate_wire_loom()
            geval2 = self._count_gates_evaluated()
            if geval2 > geval:
                geval = geval2
            elif geval2 < gtotal:
                assert False, "Circuit {} evaluation could not complete." \
                    .format(self._name)
                    
    def setup_trace(self, key, fmtstr, source):
        if source is None:
            self._trace_format[key] = fmtstr
        else:
            self._trace_format[key] = Utility.format_str(fmtstr)
        self._trace_source[key] = source
        
    def trace_format(self):
        return self._trace_format
        
    def trace_source(self):
        return self._trace_source
        
    def proceed(self):
        for gate in self._all_gates:
            gate.proceed()
            
    def setup(self):
        assert False, "Method must be implemented in subclass."
     
        
class Module:
    """
    """
    
    def __init__(self, circuit, name):
        """
        Initialize a module object.
        
        Parameters
        ----------
        circuit : Circuit
            The parent circuit which owns the module.
        name : a string
            A name for this module.

        Returns
        -------
        None.

        """
        self._parent = circuit
        self._name = name
        
    def wire(self, p_out, p_in, bits_out=None, bits_in=None):
        """
        Delegate creation of a wire from an output port to an input port to
        the parent circuit.

        Parameters
        ----------
        p_out : Port
            The output port to wire from.
        p_in : Port
            The input port to wire to.
        bits_out : TYPE, optional
            Bits selector tuple. The default is None.
        bits_in : TYPE, optional
            Bits selector tuple. The default is None.

        Returns
        -------
        None.

        """
        self._parent.wire(p_out, p_in, bits_out, bits_in)

    def wire_back(self, p_out, p_in, bits_out=None, bits_in=None):
        """
        Delegate creation of a back wire from an output port to an input port
        to the parent circuit.

        Parameters
        ----------
        p_out : Port
            The output port to back-wire from.
        p_in : Port
            The input port to wire to.
        bits_out : TYPE, optional
            Bits selector tuple. The default is None.
        bits_in : TYPE, optional
            Bits selector tuple. The default is None.

        Returns
        -------
        None.

        """
        self._parent.wire_back(p_out, p_in, bits_out, bits_in)
        
    def qualified(self, name):
        """
        Qualify a name with the name of this module to make it unique.

        Parameters
        ----------
        name : a string
            A name to be used for a gate which belongs to this module.

        Returns
        -------
        str
            The name prefixed with the name of this module.

        """
        return f"{self._name}-{name}"
        

class Trigger:
    def __init__(self, post_trigger=1):
        self._triggered = False
        self._armed = True
        self._stopped = False
        self._post_trigger_cnt = post_trigger
        self.post_trigger = post_trigger
        self.circuit = None
        self.cycle = -1
        self.cycle_started = -1
        self.cycle_stopped = -1
        
    def is_start(self):
        """
        TBD

        Returns
        -------
        bool
            DESCRIPTION.

        """
        return True
    
    def is_stop(self):
        """
        TBD

        Returns
        -------
        bool
            DESCRIPTION.

        """
        return False
    
    def is_triggered(self):
        """
        TBD

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if self._armed:
            if self._triggered:
                if self._stopped:
                    self._post_trigger_cnt -= 1
                else:
                    self._stopped = self.is_stop()
                    if self._stopped:
                        self.cycle_stopped = self.cycle
                self._triggered = not self._stopped or self._post_trigger_cnt
                self._armed = self._triggered
            else:
                self._triggered = self.is_start()
                self.cycle_started = self.cycle
        return self._triggered
    
    def trigger_mark_position(self):
        """
        TBD

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if self.cycle_started < 0 or self.cycle_stopped < 0:
            return -1
        else:
            return self.cycle_stopped - self.cycle_started
    
    def print_status(self):
        """
        TBD

        Returns
        -------
        None.

        """
        if self.cycle_started >= 0:
            print(f"Trigger started at {self.cycle_started}.")
        else:
            print("Trigger never started.")
        if self.cycle_stopped >= 0:
            print(f"Trigger stopped before {self.cycle_stopped}, post-Trigger {self.post_trigger}.")
        else:
            print("Trigger never stopped.")
        #print(f"Trigger mark position: {self.trigger_mark_position()}")


class RingBuffer:
    def __init__(self, size):
        """
        TBD

        Parameters
        ----------
        size : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self._data = []
        self._ring_size = size
        self._current = -1
        
    def append(self, item):
        if len(self._data) < self._ring_size:
            self._data.append(item)
        else:
            self._current = (self._current+1) % self._ring_size
            self._data[self._current] = item
            
    def data(self):
        #return self._data
        return self._data[self._current+1:] + self._data[:self._current+1]
            
    
class Simulation:
    def __init__(self, circuit, trigger=Trigger()):
        self._circuit = circuit
        self._circuit_trace_source = circuit.trace_source()
        self._trace = {}
        self._trigger = trigger
        self.debug = False
        self.cycles = 40
        self.show_state = False
        self.show_trace = True
        self.trace_start_stop = None
        self.trace_maxwidth = 40

    def _append_trace(self, key, value):
        self._trace[key].append(value)
 
    def _setup_trace(self):
        for key in self._circuit_trace_source:
            if self._circuit_trace_source[key] is None:
                self._trace[key] = None  # Used as trace title. No data.
            else:
                #self._trace[key] = []  # Used for trace data.
                self._trace[key] = RingBuffer(100)  # Used for trace data.

    def _update_trace(self):
        for key in self._circuit_trace_source:
            if self._circuit_trace_source[key] is not None:
                self._append_trace(key, self._circuit_trace_source[key].value())
                
    def _update_trace_triggered(self):
        if self._trigger.is_triggered():
            self._update_trace()
            
    def run(self):
        Gate.debug = self.debug
        self._circuit.setup()
        self._setup_trace()
        self._trigger.circuit = self._circuit
        for cycle in range(self.cycles):
            if Gate.debug:
                print("Circuit '{}' enter cycle {}".format(self._circuit.name(), cycle))
            self._trigger.cycle = cycle
            self._circuit.evaluate()
            self._update_trace_triggered()
            if self.show_state:
                print(f"State after cycle {cycle} of " + self._circuit.state_str())
            self._circuit.assert_no_bus_contention()
            self._circuit.proceed()
        print("{} Cycles done.".format(self.cycles))
        if self.show_trace:
            Utility.ascii_trace(
                self._trace
                , self._circuit.trace_format()
                , self.trace_maxwidth
                , self._trigger.trigger_mark_position())
            self._trigger.print_status()
        print()

        
