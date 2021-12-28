# Process node
export PROCESS = 130

# Rules for metal fill
export FILL_CONFIG = ../../../common/platforms/$(PLATFORM)/fill.json

# Set the TIEHI/TIELO cells
# These are used in yosys synthesis to avoid logical 1/0's in the netlist
export TIEHI_CELL_AND_PORT = sky130_fd_sc_hvl__conb_1 HI
export TIELO_CELL_AND_PORT = sky130_fd_sc_hvl__conb_1 LO

# Used in synthesis
export MIN_BUF_CELL_AND_PORTS = sky130_fd_sc_hvl__buf_4 A X

# Used in synthesis
export MAX_FANOUT = 5

# Blackbox verilog file
# List all standard cells and cells yosys should treat as blackboxes here
export BLACKBOX_V_FILE = ../../../common/platforms/$(PLATFORM)/sky130_fd_sc_hvl.blackbox.v

# Yosys mapping files
#export LATCH_MAP_FILE = ../../../common/platforms/$(PLATFORM)/cells_latch_hvl.v
#export CLKGATE_MAP_FILE = ../../../common/platforms/$(PLATFORM)/cells_clkgate_hvl.v
#export BLACKBOX_MAP_TCL = ../../../common/platforms/$(PLATFORM)/blackbox_map.tcl

# Placement site for core cells
# This can be found in the technology lef
export PLACE_SITE = unithv

export MACRO_PLACE_HALO ?= 1 1
export MACRO_PLACE_CHANNEL ?= 80 80

export TECH_LEF = ../../../common/platforms/$(PLATFORM)/lef/sky130_fd_sc_hvl.tlef
export SC_LEF = ../../../common/platforms/$(PLATFORM)/lef/sky130_fd_sc_hvl_merged.lef

export LIB_FILES = ../../../common/platforms/$(PLATFORM)/lib/sky130_fd_sc_hvl__tt_025C_3v30.lib \
                     $(ADDITIONAL_LIBS)
export GDS_FILES = $(wildcard ../../../common/platforms/$(PLATFORM)/gds/*.gds) \
                     $(ADDITIONAL_GDS_FILES)

# Cell padding in SITE widths to ease rout-ability
export CELL_PAD_IN_SITES = 4

# Endcap and Welltie cells
export TAPCELL_TCL = ../../../common/platforms/$(PLATFORM)/tapcell.tcl

# TritonCTS options
export CTS_BUF_CELL   = sky130_fd_sc_hvl__buf_1
export CTS_MAX_SLEW   = 1.5e-9
export CTS_MAX_CAP    = .1532e-12
export CTS_TECH_DIR   = ../../../common/platforms/$(PLATFORM)/tritonCTShd

# FastRoute options
export MIN_ROUTING_LAYER = met1
export MAX_ROUTING_LAYER = met5

# IO Pin fix margin
export IO_PIN_MARGIN = 70

# Layer to use for parasitics estimations
export WIRE_RC_LAYER = met3

# KLayout technology file
export KLAYOUT_TECH_FILE = ../../../common/platforms/$(PLATFORM)/$(PLATFORM).lyt

# Dont use cells to ease congestion
# Specify at least one filler cell if none

# The *probe* are for inserting probe points and have metal shapes
# on all layers.
# *lpflow* cells are for multi-power domains
export DONT_USE_CELLS += \
    sky130_fd_sc_hvl__probe_p_8 sky130_fd_sc_hvl__probec_p_8 \

# Define ABC driver and load
export ABC_DRIVER_CELL = sky130_fd_sc_hvl__buf_1
export ABC_LOAD_IN_FF = 5
#export ABC_CLOCK_PERIOD_IN_PS = 10

# Define default PDN config
export PDN_CFG ?= ../../../common/platforms/$(PLATFORM)/pdn.cfg

# Define fastRoute tcl
export FASTROUTE_TCL = ../../../common/platforms/$(PLATFORM)/fastroute.tcl

# Template definition for power grid analysis
export TEMPLATE_PGA_CFG ?= ../../../common/platforms/sky130/template_pga.cfg

export PLACE_DENSITY ?= 0.60

# Define Hold Buffer
export HOLD_BUF_CELL = sky130_fd_sc_hvl__buf_1

# IO Placer pin layers
export IO_PLACER_H = met3
export IO_PLACER_V = met2

# keep with gf
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT = 4
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT = 2

# Define fill cells
export FILL_CELLS = sky130_fd_sc_hvl__fill_1 sky130_fd_sc_hvl__fill_2 sky130_fd_sc_hvl__fill_4 sky130_fd_sc_hvl__fill_8

# resizer repair_long_wires -max_length
export MAX_WIRE_LENGTH = 21000

export CDL_FILE = ../../../common/platforms/sky130hvl/cdl/sky130_fd_sc_hvl.spice
