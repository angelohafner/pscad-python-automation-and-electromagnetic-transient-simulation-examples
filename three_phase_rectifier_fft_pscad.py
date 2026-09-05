"""
PSCAD 5.1.0 Automation
Three-Phase Six-Pulse Diode Rectifier with Capacitor Filter,
Current Measurements and Phase-A FFT Analysis.

Main features
-------------
1. Launch PSCAD 5.1.0 x64.
2. Load or create the PSCAD workspace and case.
3. Rebuild the complete rectifier schematic.
4. Create a 480 V line-to-line RMS, 60 Hz three-phase source.
5. Create a six-pulse diode bridge.
6. Measure Ia, Ib, Ic and Idc.
7. Create a parallel DC R-C load.
8. Place C_FILTER to the left of R_LOAD.
9. Place the source ground horizontally aligned with the source neutral.
10. Configure Output Channels with "Use Signal Name as Title? = YES".
11. Create PSCAD time-domain graphs.
12. Run the PSCAD simulation.
13. Read PSCAD output data.
14. Calculate the Phase-A FFT.
15. Calculate harmonic RMS magnitudes up to the 25th harmonic.
16. Calculate Phase-A current THD.
17. Save FFT plots, harmonic table and summary.

Python code, comments, and docstrings are intentionally written in English.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path
from typing import Any

import numpy as np
import matplotlib.pyplot as plt

import mhi.pscad
from mhi.pscad.utilities.file import OutFile


# =============================================================================
# PSCAD CONFIGURATION
# =============================================================================

PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True


# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path(
    r"C:\Users\z005b93y\PycharmProjects\pscad-test-1\PSCAD_Project"
)

WORKSPACE_NAME = "ThreePhaseRectifier.pswx"
CASE_NAME = "ThreePhaseRectifier"

WORKSPACE_PATH = OUTPUT_DIR / WORKSPACE_NAME
CASE_PATH = OUTPUT_DIR / f"{CASE_NAME}.pscx"


# =============================================================================
# ELECTRICAL PARAMETERS
# =============================================================================

SOURCE_VLL_KV = 0.480
SOURCE_FREQUENCY_HZ = 60.0
SOURCE_BASE_MVA = 1.0

LOAD_RESISTANCE_OHM = 10.0

# PSCAD basic capacitor value in microfarads
FILTER_CAPACITANCE_UF = 2200.0


# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

SIMULATION_DURATION_S = 0.60

# PSCAD uses microseconds for these runtime parameters
SOLUTION_TIME_STEP_US = 50.0
CHANNEL_PLOT_STEP_US = 50.0

RUN_SIMULATION = True


# =============================================================================
# FFT CONFIGURATION
# =============================================================================

FUNDAMENTAL_FREQUENCY_HZ = 60.0

MAX_HARMONIC_ORDER = 25

# Use the last 12 fundamental cycles.
#
# 12 / 60 = 0.2 s
FFT_ANALYSIS_CYCLES = 12

USE_HANN_WINDOW = True

FFT_MAX_FREQUENCY_HZ = (
    MAX_HARMONIC_ORDER
    * FUNDAMENTAL_FREQUENCY_HZ
)


# =============================================================================
# OUTPUT FILES
# =============================================================================

PSCAD_OUTPUT_NAME = "rectifier_currents.out"

PSCAD_CSV_FILE = (
    OUTPUT_DIR
    / "rectifier_currents.csv"
)

FFT_SPECTRUM_FILE = (
    OUTPUT_DIR
    / "phase_a_fft_spectrum.png"
)

HARMONIC_BAR_FILE = (
    OUTPUT_DIR
    / "phase_a_harmonics.png"
)

HARMONIC_CSV_FILE = (
    OUTPUT_DIR
    / "phase_a_harmonics.csv"
)

HARMONIC_SUMMARY_FILE = (
    OUTPUT_DIR
    / "phase_a_harmonic_summary.txt"
)


# =============================================================================
# MASTER LIBRARY DEFINITIONS
# =============================================================================

SOURCE_DEFINITION = "master:source3"
BREAKOUT_DEFINITION = "master:breakout"

DIODE_DEFINITION = "master:peswitch"

RESISTOR_DEFINITION = "master:resistor"
CAPACITOR_DEFINITION = "master:capacitor"

GROUND_DEFINITION = "master:ground"

AMMETER_DEFINITION = "master:ammeter"

OUTPUT_CHANNEL_DEFINITION = "master:pgb"
DATA_LABEL_DEFINITION = "master:datalabel"


# =============================================================================
# SCHEMATIC LAYOUT
# =============================================================================

SOURCE_POSITION = (16, 34)

BREAKOUT_POSITION = (28, 34)


# -----------------------------------------------------------------------------
# Diode bridge
# -----------------------------------------------------------------------------

D1_POSITION = (52, 20)
D3_POSITION = (62, 20)
D5_POSITION = (72, 20)

D2_POSITION = (52, 48)
D4_POSITION = (62, 48)
D6_POSITION = (72, 48)


# -----------------------------------------------------------------------------
# Phase levels
# -----------------------------------------------------------------------------

PHASE_A_Y = 32
PHASE_B_Y = 34
PHASE_C_Y = 36


# -----------------------------------------------------------------------------
# Phase ammeters
# -----------------------------------------------------------------------------

IA_METER_POSITION = (
    38,
    PHASE_A_Y,
)

IB_METER_POSITION = (
    38,
    PHASE_B_Y,
)

IC_METER_POSITION = (
    38,
    PHASE_C_Y,
)


# -----------------------------------------------------------------------------
# DC side
#
# Requested arrangement:
#
#     C_FILTER      R_LOAD
#       left         right
# -----------------------------------------------------------------------------

CAPACITOR_BRANCH_X = 86
RESISTOR_BRANCH_X = 96

CAPACITOR_POSITION = (
    CAPACITOR_BRANCH_X,
    36,
)

IDC_METER_POSITION = (
    RESISTOR_BRANCH_X,
    27,
)

RESISTOR_POSITION = (
    RESISTOR_BRANCH_X,
    38,
)


# -----------------------------------------------------------------------------
# Output Channels
# -----------------------------------------------------------------------------

OUTPUT_CHANNEL_Y = 60

IA_LABEL_POSITION = (
    14,
    OUTPUT_CHANNEL_Y,
)

IA_OUTPUT_POSITION = (
    19,
    OUTPUT_CHANNEL_Y,
)

IB_LABEL_POSITION = (
    30,
    OUTPUT_CHANNEL_Y,
)

IB_OUTPUT_POSITION = (
    35,
    OUTPUT_CHANNEL_Y,
)

IC_LABEL_POSITION = (
    46,
    OUTPUT_CHANNEL_Y,
)

IC_OUTPUT_POSITION = (
    51,
    OUTPUT_CHANNEL_Y,
)

IDC_LABEL_POSITION = (
    62,
    OUTPUT_CHANNEL_Y,
)

IDC_OUTPUT_POSITION = (
    67,
    OUTPUT_CHANNEL_Y,
)


# -----------------------------------------------------------------------------
# PSCAD graphs
# -----------------------------------------------------------------------------

PHASE_GRAPH_POSITION = (
    15,
    70,
)

DC_GRAPH_POSITION = (
    60,
    70,
)


# =============================================================================
# GENERAL HELPERS
# =============================================================================

def print_header(
    title: str,
) -> None:
    """Print a formatted console section."""

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def safe_string(
    value: Any,
) -> str:
    """Convert any value safely to text."""

    if value is None:
        return ""

    try:
        return str(value)

    except Exception:
        return "<unavailable>"


def normalize_name(
    value: str,
) -> str:
    """Normalize a name for robust comparisons."""

    return "".join(
        character.lower()
        for character in str(value)
        if character.isalnum()
    )


# =============================================================================
# PSCAD LAUNCH
# =============================================================================

def launch_pscad():
    """Launch PSCAD 5.1.0 x64."""

    print_header(
        "Launching PSCAD"
    )

    print(
        f"Launching PSCAD "
        f"{PSCAD_VERSION} x64..."
    )

    pscad = mhi.pscad.launch(
        version=PSCAD_VERSION,
        x64=PSCAD_X64,
        minimize=False,
    )

    if pscad is None:

        raise RuntimeError(
            "PSCAD could not be launched."
        )

    print(
        f"Connected to PSCAD "
        f"{pscad.version}"
    )

    return pscad


# =============================================================================
# WORKSPACE
# =============================================================================

def create_or_load_project(
    pscad,
):
    """Load or create the PSCAD workspace and case."""

    print_header(
        "Workspace and Case"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------------------
    # Existing workspace
    # -------------------------------------------------------------------------

    if WORKSPACE_PATH.is_file():

        print(
            "Existing workspace found:"
        )

        print(
            WORKSPACE_PATH
        )

        pscad.load(
            str(WORKSPACE_PATH)
        )

        project = pscad.project(
            CASE_NAME
        )

        if project is None:

            raise RuntimeError(
                f"Project '{CASE_NAME}' "
                f"was not found."
            )

        print(
            "Existing project "
            "loaded successfully."
        )

        return project

    # -------------------------------------------------------------------------
    # Create workspace
    # -------------------------------------------------------------------------

    print(
        "Creating new workspace..."
    )

    pscad.new_workspace(
        filename=WORKSPACE_NAME,
        folder=str(OUTPUT_DIR),
    )

    print(
        "Creating new PSCAD case..."
    )

    project = pscad.create_case(
        filename=CASE_NAME,
        folder=str(OUTPUT_DIR),
    )

    if project is None:

        raise RuntimeError(
            "PSCAD case could not be created."
        )

    project.save()

    pscad.save_workspace(
        save_projects=True
    )

    print(
        "Workspace and case "
        "created successfully."
    )

    return project


# =============================================================================
# PROJECT SETTINGS
# =============================================================================

def configure_project(
    project,
) -> None:
    """Configure simulation and PSCAD output settings."""

    print_header(
        "Configuring Simulation"
    )

    project.parameters(
        time_duration=SIMULATION_DURATION_S,
        time_step=SOLUTION_TIME_STEP_US,
        sample_step=CHANNEL_PLOT_STEP_US,
        PlotType="OUT",
        output_filename=PSCAD_OUTPUT_NAME,
    )

    parameters = project.parameters()

    print(
        f"Duration          = "
        f"{parameters.get('time_duration')} s"
    )

    print(
        f"Solution step     = "
        f"{parameters.get('time_step')} us"
    )

    print(
        f"Plot step         = "
        f"{parameters.get('sample_step')} us"
    )

    print(
        f"Output type       = "
        f"{parameters.get('PlotType')}"
    )

    print(
        f"Output filename   = "
        f"{parameters.get('output_filename')}"
    )


# =============================================================================
# CANVAS
# =============================================================================

def get_main_canvas(
    project,
):
    """Access the Main schematic canvas."""

    print_header(
        "Main Canvas"
    )

    canvas = project.canvas(
        "Main"
    )

    if canvas is None:

        raise RuntimeError(
            "Main canvas could not be accessed."
        )

    try:

        canvas.parameters(
            show_grid=True,
            show_terminals=False,
            show_virtual=False,
            size="100X100",
        )

    except Exception:
        pass

    print(
        "Main canvas accessed successfully."
    )

    return canvas


# =============================================================================
# CLEAR CANVAS
# =============================================================================

def clear_canvas(
    canvas,
) -> None:
    """Remove the previously generated schematic."""

    print_header(
        "Clearing Previous Schematic"
    )

    # Delete graphs first
    try:

        graph_frames = canvas.find_all(
            "GraphFrame"
        )

        if graph_frames:

            canvas.delete(
                *graph_frames
            )

    except Exception:
        pass

    # Delete components
    components = canvas.components()

    if components:

        canvas.delete(
            *components
        )

    print(
        "Previous schematic removed."
    )


# =============================================================================
# COMPONENT CREATION
# =============================================================================

def create_component(
    canvas,
    definition,
    position,
    **parameters,
):
    """Create one PSCAD component."""

    x, y = position

    component = canvas.create_component(
        definition,
        x=x,
        y=y,
        **parameters,
    )

    print(
        f"Created "
        f"{component.defn_name} "
        f"at ({x}, {y})"
    )

    return component


# =============================================================================
# PORT HELPERS
# =============================================================================

def get_ports(
    component,
) -> dict:
    """Return all active component ports."""

    ports = component.ports()

    if ports is None:

        return {}

    if isinstance(
        ports,
        dict,
    ):

        return ports

    result = {}

    for port in ports:

        result[
            safe_string(
                port.name
            )
        ] = port

    return result


def resolved_port(
    component,
    port_name,
):
    """Return a port considering rotation and mirror state."""

    try:

        port = component.port(
            port_name
        )

        if port is not None:

            return port

    except Exception:
        pass

    return get_ports(
        component
    )[port_name]


def port_xy(
    component,
    port_name,
):
    """Return grid coordinates of one named port."""

    port = resolved_port(
        component,
        port_name,
    )

    return (
        int(port.x),
        int(port.y),
    )


def port_type_number(
    port,
):
    """Return PSCAD node type as an integer when possible."""

    try:

        return int(
            port.type
        )

    except Exception:

        text = safe_string(
            getattr(
                port,
                "type",
                "",
            )
        ).upper()

        if "ELECTRICAL" in text:

            return 3

        return None


def electrical_ports(
    component,
):
    """Return electrical component ports."""

    result = []

    for name in get_ports(
        component
    ):

        port = resolved_port(
            component,
            name,
        )

        if port_type_number(
            port
        ) == 3:

            result.append(
                (
                    name,
                    port,
                )
            )

    return result


def signal_ports(
    component,
):
    """Return signal/control component ports."""

    result = []

    for name in get_ports(
        component
    ):

        port = resolved_port(
            component,
            name,
        )

        if port_type_number(
            port
        ) != 3:

            result.append(
                (
                    name,
                    port,
                )
            )

    return result


def two_terminal_coordinates(
    component,
):
    """Return electrical coordinates of a two-terminal device."""

    ports = electrical_ports(
        component
    )

    if len(ports) != 2:

        raise RuntimeError(
            f"{component.defn_name} should have "
            f"exactly two electrical terminals, "
            f"but {len(ports)} were found."
        )

    return [
        (
            int(port.x),
            int(port.y),
        )
        for _, port in ports
    ]


# =============================================================================
# COMPONENT ORIENTATION
# =============================================================================

def ensure_horizontal(
    canvas,
    component,
    position,
):
    """Ensure a two-terminal device is horizontal."""

    component.location = position

    terminals = two_terminal_coordinates(
        component
    )

    if (
        terminals[0][1]
        != terminals[1][1]
    ):

        canvas.rotate_right(
            component
        )

        component.location = position

        terminals = two_terminal_coordinates(
            component
        )

    terminals.sort(
        key=lambda point:
            point[0]
    )

    return (
        terminals[0],
        terminals[1],
    )


def ensure_vertical(
    canvas,
    component,
    position,
):
    """Ensure a two-terminal device is vertical."""

    component.location = position

    terminals = two_terminal_coordinates(
        component
    )

    if (
        terminals[0][0]
        != terminals[1][0]
    ):

        canvas.rotate_right(
            component
        )

        component.location = position

        terminals = two_terminal_coordinates(
            component
        )

    terminals.sort(
        key=lambda point:
            point[1]
    )

    return (
        terminals[0],
        terminals[1],
    )


# =============================================================================
# WIRE
# =============================================================================

def create_wire(
    canvas,
    *points,
):
    """Create one PSCAD wire."""

    if len(points) < 2:

        raise ValueError(
            "At least two points are required."
        )

    return canvas.create_wire(
        *points
    )


# =============================================================================
# SOURCE
# =============================================================================

def create_source(
    canvas,
):
    """Create and configure the three-phase source."""

    source = create_component(
        canvas,
        SOURCE_DEFINITION,
        SOURCE_POSITION,
    )

    source.parameters(
        Name="SOURCE",
        Ctrl="FIXED",
        MVA=SOURCE_BASE_MVA,
        Vbase=SOURCE_VLL_KV,
        Vm=SOURCE_VLL_KV,
        Es=SOURCE_VLL_KV,
        F=SOURCE_FREQUENCY_HZ,
        F0=SOURCE_FREQUENCY_HZ,
        Ph=0.0,
    )

    print(
        f"Source = "
        f"{SOURCE_VLL_KV * 1000:.0f} V L-L RMS, "
        f"{SOURCE_FREQUENCY_HZ:.1f} Hz"
    )

    return source


# =============================================================================
# GROUND
# =============================================================================

def create_and_connect_ground(
    canvas,
    source,
):
    """
    Create a mirrored ground horizontally aligned
    with the source neutral.
    """

    print_header(
        "Connecting Source Ground"
    )

    neutral = port_xy(
        source,
        "N",
    )

    # Create the symbol to the left of the source
    ground = create_component(
        canvas,
        GROUND_DEFINITION,
        (
            neutral[0] - 6,
            neutral[1],
        ),
    )

    # Mirror the ground so its connection points toward the source
    canvas.mirror(
        ground
    )

    ground.location = (
        neutral[0] - 6,
        neutral[1],
    )

    ground_port = port_xy(
        ground,
        "A",
    )

    # Desired ground terminal position
    desired_ground_port = (
        neutral[0] - 4,
        neutral[1],
    )

    dx = (
        desired_ground_port[0]
        - ground_port[0]
    )

    dy = (
        desired_ground_port[1]
        - ground_port[1]
    )

    gx, gy = ground.location

    ground.location = (
        gx + dx,
        gy + dy,
    )

    ground_port = port_xy(
        ground,
        "A",
    )

    create_wire(
        canvas,
        ground_port,
        neutral,
    )

    print(
        f"Ground terminal = "
        f"{ground_port}"
    )

    print(
        f"Source neutral  = "
        f"{neutral}"
    )

    return ground


# =============================================================================
# DIODE
# =============================================================================

def create_diode(
    canvas,
    name,
    position,
):
    """Create one diode."""

    diode = create_component(
        canvas,
        DIODE_DEFINITION,
        position,
        Type="DIODE",
    )

    diode.parameters(
        Name=name
    )

    return diode


# =============================================================================
# DIODE BRIDGE
# =============================================================================

def create_bridge(
    canvas,
):
    """Create and connect the classical six-pulse bridge."""

    print_header(
        "Creating Diode Bridge"
    )

    d1 = create_diode(
        canvas,
        "D1",
        D1_POSITION,
    )

    d3 = create_diode(
        canvas,
        "D3",
        D3_POSITION,
    )

    d5 = create_diode(
        canvas,
        "D5",
        D5_POSITION,
    )

    d2 = create_diode(
        canvas,
        "D2",
        D2_POSITION,
    )

    d4 = create_diode(
        canvas,
        "D4",
        D4_POSITION,
    )

    d6 = create_diode(
        canvas,
        "D6",
        D6_POSITION,
    )

    # -------------------------------------------------------------------------
    # Read diode ports
    # -------------------------------------------------------------------------

    d1_dn = port_xy(
        d1,
        "DN",
    )

    d1_dp = port_xy(
        d1,
        "DP",
    )

    d3_dn = port_xy(
        d3,
        "DN",
    )

    d3_dp = port_xy(
        d3,
        "DP",
    )

    d5_dn = port_xy(
        d5,
        "DN",
    )

    d5_dp = port_xy(
        d5,
        "DP",
    )

    d2_dn = port_xy(
        d2,
        "DN",
    )

    d2_dp = port_xy(
        d2,
        "DP",
    )

    d4_dn = port_xy(
        d4,
        "DN",
    )

    d4_dp = port_xy(
        d4,
        "DP",
    )

    d6_dn = port_xy(
        d6,
        "DN",
    )

    d6_dp = port_xy(
        d6,
        "DP",
    )

    # -------------------------------------------------------------------------
    # Positive DC bus
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        d1_dn,
        d3_dn,
        d5_dn,
    )

    # -------------------------------------------------------------------------
    # Negative DC bus
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        d2_dp,
        d4_dp,
        d6_dp,
    )

    # -------------------------------------------------------------------------
    # AC phase nodes
    # -------------------------------------------------------------------------

    phase_a = (
        d1_dp[0],
        PHASE_A_Y,
    )

    phase_b = (
        d3_dp[0],
        PHASE_B_Y,
    )

    phase_c = (
        d5_dp[0],
        PHASE_C_Y,
    )

    create_wire(
        canvas,
        d1_dp,
        phase_a,
        d2_dn,
    )

    create_wire(
        canvas,
        d3_dp,
        phase_b,
        d4_dn,
    )

    create_wire(
        canvas,
        d5_dp,
        phase_c,
        d6_dn,
    )

    return {
        "phase_a": phase_a,
        "phase_b": phase_b,
        "phase_c": phase_c,

        "positive_dc": d5_dn,
        "negative_dc": d6_dp,
    }


# =============================================================================
# AMMETER
# =============================================================================

def create_ammeter(
    canvas,
    signal_name,
    position,
    orientation,
):
    """Create one series current meter."""

    ammeter = create_component(
        canvas,
        AMMETER_DEFINITION,
        position,
    )

    ammeter.parameters(
        Name=signal_name
    )

    if orientation == "horizontal":

        terminals = ensure_horizontal(
            canvas,
            ammeter,
            position,
        )

    elif orientation == "vertical":

        terminals = ensure_vertical(
            canvas,
            ammeter,
            position,
        )

    else:

        raise ValueError(
            "Invalid ammeter orientation."
        )

    return (
        ammeter,
        terminals,
    )


# =============================================================================
# AC SIDE
# =============================================================================

def connect_ac_side(
    canvas,
    source,
    breakout,
    bridge,
):
    """Connect source, breakout and phase-current meters."""

    print_header(
        "Connecting AC Side"
    )

    # Source -> breakout
    create_wire(
        canvas,
        port_xy(
            source,
            "N3",
        ),
        port_xy(
            breakout,
            "N",
        ),
    )

    phase_data = (
        (
            "Ia",
            IA_METER_POSITION,
            port_xy(
                breakout,
                "N1",
            ),
            bridge[
                "phase_a"
            ],
        ),

        (
            "Ib",
            IB_METER_POSITION,
            port_xy(
                breakout,
                "N2",
            ),
            bridge[
                "phase_b"
            ],
        ),

        (
            "Ic",
            IC_METER_POSITION,
            port_xy(
                breakout,
                "N3",
            ),
            bridge[
                "phase_c"
            ],
        ),
    )

    meters = {}

    for (
        signal_name,
        position,
        breakout_port,
        bridge_node,
    ) in phase_data:

        meter, (
            terminal_1,
            terminal_2,
        ) = create_ammeter(
            canvas,
            signal_name,
            position,
            "horizontal",
        )

        create_wire(
            canvas,
            breakout_port,
            terminal_1,
        )

        create_wire(
            canvas,
            terminal_2,
            bridge_node,
        )

        meters[
            signal_name
        ] = meter

    return meters


# =============================================================================
# DC LOAD
# =============================================================================

def create_dc_load(
    canvas,
    bridge,
):
    """
    Create the DC load.

    Requested visual arrangement:

        C_FILTER      R_LOAD
          left         right

    Both branches are connected in parallel.
    """

    print_header(
        "Creating DC Load"
    )

    positive_dc = bridge[
        "positive_dc"
    ]

    negative_dc = bridge[
        "negative_dc"
    ]

    # -------------------------------------------------------------------------
    # Capacitor - LEFT branch
    # -------------------------------------------------------------------------

    capacitor = create_component(
        canvas,
        CAPACITOR_DEFINITION,
        CAPACITOR_POSITION,
    )

    capacitor.parameters(
        C=FILTER_CAPACITANCE_UF
    )

    try:

        capacitor.parameters(
            Name="C_FILTER"
        )

    except Exception:
        pass

    (
        capacitor_top,
        capacitor_bottom,
    ) = ensure_vertical(
        canvas,
        capacitor,
        CAPACITOR_POSITION,
    )

    # -------------------------------------------------------------------------
    # Resistor current meter - RIGHT branch
    # -------------------------------------------------------------------------

    idc_meter, (
        idc_top,
        idc_bottom,
    ) = create_ammeter(
        canvas,
        "Idc",
        IDC_METER_POSITION,
        "vertical",
    )

    # -------------------------------------------------------------------------
    # Resistor - RIGHT branch
    # -------------------------------------------------------------------------

    resistor = create_component(
        canvas,
        RESISTOR_DEFINITION,
        RESISTOR_POSITION,
    )

    resistor.parameters(
        Name="R_LOAD",
        R=LOAD_RESISTANCE_OHM,
    )

    (
        resistor_top,
        resistor_bottom,
    ) = ensure_vertical(
        canvas,
        resistor,
        RESISTOR_POSITION,
    )

    capacitor_x = (
        capacitor_top[0]
    )

    resistor_x = (
        resistor_top[0]
    )

    # -------------------------------------------------------------------------
    # Positive bus -> capacitor
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        positive_dc,
        (
            capacitor_x,
            positive_dc[1],
        ),
        capacitor_top,
    )

    # -------------------------------------------------------------------------
    # Capacitor -> negative bus
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        capacitor_bottom,
        (
            capacitor_x,
            negative_dc[1],
        ),
        negative_dc,
    )

    # -------------------------------------------------------------------------
    # Positive bus -> Idc meter
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        (
            capacitor_x,
            positive_dc[1],
        ),
        (
            resistor_x,
            positive_dc[1],
        ),
        idc_top,
    )

    # -------------------------------------------------------------------------
    # Idc meter -> resistor
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        idc_bottom,
        resistor_top,
    )

    # -------------------------------------------------------------------------
    # Resistor -> negative bus
    # -------------------------------------------------------------------------

    create_wire(
        canvas,
        resistor_bottom,
        (
            resistor_x,
            negative_dc[1],
        ),
        (
            capacitor_x,
            negative_dc[1],
        ),
    )

    print(
        "DC layout:"
    )

    print(
        "    LEFT  -> C_FILTER"
    )

    print(
        "    RIGHT -> R_LOAD"
    )

    print(
        f"    C = "
        f"{FILTER_CAPACITANCE_UF:.1f} uF"
    )

    print(
        f"    R = "
        f"{LOAD_RESISTANCE_OHM:.3f} ohm"
    )

    return {
        "capacitor": capacitor,
        "resistor": resistor,
        "Idc": idc_meter,
    }


# =============================================================================
# SIGNAL PORT
# =============================================================================

def first_signal_port(
    component,
):
    """Return the first signal/control port coordinate."""

    ports = signal_ports(
        component
    )

    if ports:

        _, port = ports[0]

        return (
            int(port.x),
            int(port.y),
        )

    all_ports = get_ports(
        component
    )

    if len(all_ports) == 1:

        name = next(
            iter(all_ports)
        )

        port = resolved_port(
            component,
            name,
        )

        return (
            int(port.x),
            int(port.y),
        )

    raise RuntimeError(
        f"No unique signal port detected on "
        f"{component.defn_name}."
    )


# =============================================================================
# DATA LABEL
# =============================================================================

def create_data_label(
    canvas,
    signal_name,
    position,
):
    """Create one Data Label."""

    label = create_component(
        canvas,
        DATA_LABEL_DEFINITION,
        position,
    )

    label.parameters(
        Name=signal_name
    )

    return label


# =============================================================================
# OUTPUT CHANNEL
# =============================================================================

def configure_output_channel(
    pgb,
    signal_name,
):
    """
    Configure one PSCAD Output Channel.

    Important:
        "Use Signal Name as Title?" is explicitly set to YES.
    """

    parameters = pgb.parameters()

    # -------------------------------------------------------------------------
    # Use Signal Name as Title? = YES
    # -------------------------------------------------------------------------

    if "UseSignalName" in parameters:

        pgb.parameters(
            UseSignalName="YES"
        )

    else:

        # Fallback search
        for parameter_name in parameters:

            normalized = normalize_name(
                parameter_name
            )

            if normalized in {
                "usesignalname",
                "usesignalnameastitle",
            }:

                pgb.parameters(
                    **{
                        parameter_name:
                            "YES"
                    }
                )

                break

    # -------------------------------------------------------------------------
    # Scale current from kA to A
    # -------------------------------------------------------------------------

    if "Scale" in parameters:

        pgb.parameters(
            Scale=1000.0
        )

    # -------------------------------------------------------------------------
    # Engineering units
    # -------------------------------------------------------------------------

    if "Units" in parameters:

        pgb.parameters(
            Units="A"
        )

    # -------------------------------------------------------------------------
    # Optional fallback title
    # -------------------------------------------------------------------------

    if "Name" in parameters:

        pgb.parameters(
            Name=signal_name
        )

    # -------------------------------------------------------------------------
    # Verify
    # -------------------------------------------------------------------------

    verification = pgb.parameters()

    print(
        f"Output Channel {signal_name}:"
    )

    print(
        f"    UseSignalName = "
        f"{verification.get('UseSignalName', '<unknown>')}"
    )

    print(
        f"    Scale         = "
        f"{verification.get('Scale', '<unknown>')}"
    )

    print(
        f"    Units         = "
        f"{verification.get('Units', '<unknown>')}"
    )


def create_output_channel(
    canvas,
    signal_name,
    label_position,
    output_position,
):
    """Create Data Label and Output Channel for one signal."""

    label = create_data_label(
        canvas,
        signal_name,
        label_position,
    )

    output = create_component(
        canvas,
        OUTPUT_CHANNEL_DEFINITION,
        output_position,
    )

    configure_output_channel(
        output,
        signal_name,
    )

    create_wire(
        canvas,
        first_signal_port(
            label
        ),
        first_signal_port(
            output
        ),
    )

    return output


def create_output_channels(
    canvas,
):
    """Create Ia, Ib, Ic and Idc Output Channels."""

    print_header(
        "Creating Output Channels"
    )

    ia = create_output_channel(
        canvas,
        "Ia",
        IA_LABEL_POSITION,
        IA_OUTPUT_POSITION,
    )

    ib = create_output_channel(
        canvas,
        "Ib",
        IB_LABEL_POSITION,
        IB_OUTPUT_POSITION,
    )

    ic = create_output_channel(
        canvas,
        "Ic",
        IC_LABEL_POSITION,
        IC_OUTPUT_POSITION,
    )

    idc = create_output_channel(
        canvas,
        "Idc",
        IDC_LABEL_POSITION,
        IDC_OUTPUT_POSITION,
    )

    return {
        "Ia": ia,
        "Ib": ib,
        "Ic": ic,
        "Idc": idc,
    }


# =============================================================================
# PSCAD GRAPHS
# =============================================================================

def create_pscad_graphs(
    canvas,
    channels,
):
    """Create PSCAD time-domain current graphs."""

    print_header(
        "Creating PSCAD Graphs"
    )

    # -------------------------------------------------------------------------
    # Three-phase current graph
    # -------------------------------------------------------------------------

    (
        phase_frame,
        phase_overlay,
        _,
    ) = canvas.create_graph(
        channels["Ia"],
        x=PHASE_GRAPH_POSITION[0],
        y=PHASE_GRAPH_POSITION[1],
    )

    phase_overlay.create_curve(
        channels["Ib"]
    )

    phase_overlay.create_curve(
        channels["Ic"]
    )

    try:

        phase_frame.parameters(
            title="Instantaneous Phase Currents",
            xtitle="Time [s]",
        )

    except Exception:
        pass

    # -------------------------------------------------------------------------
    # DC current graph
    # -------------------------------------------------------------------------

    (
        dc_frame,
        dc_overlay,
        _,
    ) = canvas.create_graph(
        channels["Idc"],
        x=DC_GRAPH_POSITION[0],
        y=DC_GRAPH_POSITION[1],
    )

    try:

        dc_frame.parameters(
            title="DC Load Current",
            xtitle="Time [s]",
        )

    except Exception:
        pass

    print(
        "Graph 1: Ia, Ib, Ic"
    )

    print(
        "Graph 2: Idc"
    )

    return {
        "phase_frame": phase_frame,
        "phase_overlay": phase_overlay,

        "dc_frame": dc_frame,
        "dc_overlay": dc_overlay,
    }


# =============================================================================
# ANNOTATIONS
# =============================================================================

def create_annotations(
    canvas,
):
    """Create schematic annotations."""

    try:

        canvas.create_annotation(
            x=50,
            y=9,
            line1=(
                "Three-Phase Six-Pulse "
                "Diode Rectifier"
            ),
            line2=(
                "480 V L-L RMS | "
                "60 Hz | Capacitor Filter"
            ),
        )

        canvas.create_annotation(
            x=76,
            y=16,
            line1="+Vdc",
        )

        canvas.create_annotation(
            x=76,
            y=51,
            line1="-Vdc",
        )

        canvas.create_annotation(
            x=83,
            y=44,
            line1="C_FILTER",
        )

        canvas.create_annotation(
            x=93,
            y=44,
            line1="R_LOAD",
        )

    except Exception:
        pass


# =============================================================================
# SAVE
# =============================================================================

def save_project(
    pscad,
    project,
):
    """Save PSCAD project and workspace."""

    print_header(
        "Saving PSCAD Files"
    )

    project.save()

    pscad.save_workspace(
        save_projects=True
    )

    print(
        "PSCAD files saved successfully."
    )


# =============================================================================
# PSCAD MESSAGES
# =============================================================================

def print_project_messages(
    project,
):
    """Print PSCAD project messages."""

    has_errors = False

    for message in project.messages():

        status = safe_string(
            getattr(
                message,
                "status",
                "",
            )
        )

        text = safe_string(
            getattr(
                message,
                "text",
                message,
            )
        )

        print(
            f"{status:<10} | {text}"
        )

        if "error" in status.lower():

            has_errors = True

    return has_errors


# =============================================================================
# SIMULATION
# =============================================================================

def run_simulation(
    project,
    graphs,
):
    """Run the PSCAD simulation."""

    print_header(
        "Running PSCAD Simulation"
    )

    if not RUN_SIMULATION:

        print(
            "Simulation disabled."
        )

        return

    try:

        project.run()

    except Exception as exc:

        print_project_messages(
            project
        )

        raise RuntimeError(
            "PSCAD simulation failed."
        ) from exc

    if print_project_messages(
        project
    ):

        raise RuntimeError(
            "PSCAD reported build errors."
        )

    try:

        graphs[
            "phase_overlay"
        ].zoom_extents()

    except Exception:
        pass

    try:

        graphs[
            "dc_overlay"
        ].zoom_extents()

    except Exception:
        pass

    print(
        "Simulation completed."
    )


# =============================================================================
# FIND PSCAD OUTPUT
# =============================================================================

def find_pscad_output_basename(
    project,
):
    """Locate the generated PSCAD INF/OUT data files."""

    temp_folder = Path(
        project.temp_folder
    )

    print_header(
        "Locating PSCAD Output"
    )

    print(
        temp_folder
    )

    inf_files = list(
        temp_folder.glob(
            "*.inf"
        )
    )

    if not inf_files:

        raise FileNotFoundError(
            f"No .inf output file was found in:\n"
            f"{temp_folder}"
        )

    requested_stem = Path(
        PSCAD_OUTPUT_NAME
    ).stem.lower()

    matching = [
        path
        for path in inf_files
        if requested_stem
        in path.stem.lower()
    ]

    candidates = (
        matching
        if matching
        else inf_files
    )

    candidates.sort(
        key=lambda path:
            path.stat().st_mtime,
        reverse=True,
    )

    selected = candidates[0]

    print(
        "Selected:"
    )

    print(
        selected
    )

    return selected.with_suffix(
        ""
    )


# =============================================================================
# PSCAD OUTPUT -> CSV
# =============================================================================

def convert_output_to_csv(
    project,
):
    """
    Convert PSCAD OUT data to CSV.

    Important
    ---------
    OutFile.toCSV() internally opens the OutFile.

    Therefore:
        1. Open manually only to inspect columns.
        2. Close the OutFile.
        3. Call toCSV() while the file is closed.

    This avoids:
        OSError: Already open
    """

    print_header(
        "Converting PSCAD Output"
    )

    basename = (
        find_pscad_output_basename(
            project
        )
    )

    output = OutFile(
        str(basename)
    )

    # -------------------------------------------------------------------------
    # Inspect available columns
    # -------------------------------------------------------------------------

    output.open()

    try:

        columns = output.columns()

        print(
            "Available columns:"
        )

        for column in columns:

            print(
                f"    {column}"
            )

    finally:

        output.close()

    # -------------------------------------------------------------------------
    # Remove previous CSV if it exists
    # -------------------------------------------------------------------------

    if PSCAD_CSV_FILE.is_file():

        PSCAD_CSV_FILE.unlink()

    # -------------------------------------------------------------------------
    # IMPORTANT:
    #
    # Do NOT call output.open() here.
    #
    # toCSV() opens the file internally.
    # -------------------------------------------------------------------------

    output.toCSV(
        str(PSCAD_CSV_FILE)
    )

    print()

    print(
        "CSV created successfully:"
    )

    print(
        PSCAD_CSV_FILE
    )

    return columns


# =============================================================================
# CSV COLUMN SEARCH
# =============================================================================

def find_csv_column(
    fieldnames,
    candidates,
):
    """Find one CSV field using normalized matching."""

    # Exact normalized match
    for candidate in candidates:

        target = normalize_name(
            candidate
        )

        for field in fieldnames:

            if (
                normalize_name(field)
                == target
            ):

                return field

    # Partial match
    for candidate in candidates:

        target = normalize_name(
            candidate
        )

        for field in fieldnames:

            if (
                target
                in normalize_name(field)
            ):

                return field

    return None


# =============================================================================
# READ IA
# =============================================================================

def read_phase_a_current():
    """Read time and Phase-A current from the PSCAD CSV."""

    print_header(
        "Reading Phase-A Current"
    )

    with PSCAD_CSV_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(
            file
        )

        fields = reader.fieldnames

        if not fields:

            raise RuntimeError(
                "CSV header could not be read."
            )

        print(
            f"CSV fields:"
        )

        print(
            fields
        )

        time_column = find_csv_column(
            fields,
            (
                "TIME",
                "time",
            ),
        )

        ia_column = find_csv_column(
            fields,
            (
                "Ia",
                "Phase A Current",
            ),
        )

        if time_column is None:

            raise RuntimeError(
                "Time column could not be identified."
            )

        if ia_column is None:

            raise RuntimeError(
                "Ia column could not be identified."
            )

        time_values = []
        current_values = []

        for row in reader:

            try:

                time_value = float(
                    row[
                        time_column
                    ]
                )

                current_value = float(
                    row[
                        ia_column
                    ]
                )

            except (
                ValueError,
                TypeError,
                KeyError,
            ):

                continue

            time_values.append(
                time_value
            )

            current_values.append(
                current_value
            )

    time_array = np.asarray(
        time_values,
        dtype=float,
    )

    current_array = np.asarray(
        current_values,
        dtype=float,
    )

    if len(time_array) < 100:

        raise RuntimeError(
            "Too few samples were read "
            "from the PSCAD output."
        )

    print(
        f"Samples = "
        f"{len(time_array)}"
    )

    print(
        f"Initial time = "
        f"{time_array[0]:.6f} s"
    )

    print(
        f"Final time   = "
        f"{time_array[-1]:.6f} s"
    )

    return (
        time_array,
        current_array,
    )


# =============================================================================
# FFT
# =============================================================================

def calculate_fft(
    time_array,
    current_array,
):
    """
    Calculate the one-sided RMS FFT spectrum.

    The final steady-state cycles are selected automatically.
    """

    print_header(
        "Phase-A FFT"
    )

    dt = float(
        np.median(
            np.diff(
                time_array
            )
        )
    )

    if dt <= 0.0:

        raise RuntimeError(
            "Invalid sampling interval."
        )

    sampling_frequency = (
        1.0
        / dt
    )

    requested_duration = (
        FFT_ANALYSIS_CYCLES
        / FUNDAMENTAL_FREQUENCY_HZ
    )

    sample_count = int(
        round(
            requested_duration
            / dt
        )
    )

    sample_count = min(
        sample_count,
        len(
            current_array
        ),
    )

    if sample_count < 100:

        raise RuntimeError(
            "FFT window contains "
            "too few samples."
        )

    time_segment = (
        time_array[
            -sample_count:
        ]
    )

    current_segment = (
        current_array[
            -sample_count:
        ].copy()
    )

    # -------------------------------------------------------------------------
    # Remove DC component
    # -------------------------------------------------------------------------

    current_segment -= np.mean(
        current_segment
    )

    # -------------------------------------------------------------------------
    # Window
    # -------------------------------------------------------------------------

    if USE_HANN_WINDOW:

        window = np.hanning(
            sample_count
        )

        window_name = "Hann"

    else:

        window = np.ones(
            sample_count
        )

        window_name = "Rectangular"

    windowed_current = (
        current_segment
        * window
    )

    # -------------------------------------------------------------------------
    # FFT
    # -------------------------------------------------------------------------

    spectrum = np.fft.rfft(
        windowed_current
    )

    frequencies = np.fft.rfftfreq(
        sample_count,
        d=dt,
    )

    # -------------------------------------------------------------------------
    # Coherent gain correction
    #
    # Peak amplitude:
    #
    #     A_peak = 2 |FFT| / sum(window)
    #
    # RMS:
    #
    #     A_rms = A_peak / sqrt(2)
    # -------------------------------------------------------------------------

    scale = (
        2.0
        / np.sum(
            window
        )
        / math.sqrt(
            2.0
        )
    )

    rms_spectrum = (
        np.abs(
            spectrum
        )
        * scale
    )

    if len(
        rms_spectrum
    ):

        rms_spectrum[0] = 0.0

    frequency_resolution = (
        sampling_frequency
        / sample_count
    )

    print(
        f"Sampling frequency = "
        f"{sampling_frequency:.2f} Hz"
    )

    print(
        f"Samples used       = "
        f"{sample_count}"
    )

    print(
        f"Window             = "
        f"{window_name}"
    )

    print(
        f"FFT duration       = "
        f"{sample_count * dt:.6f} s"
    )

    print(
        f"Frequency spacing  = "
        f"{frequency_resolution:.4f} Hz"
    )

    return (
        frequencies,
        rms_spectrum,
        time_segment,
        current_segment,
    )


# =============================================================================
# HARMONICS
# =============================================================================

def extract_harmonics(
    frequencies,
    rms_spectrum,
):
    """Extract harmonic magnitudes from 1st through 25th order."""

    harmonic_results = []

    for order in range(
        1,
        MAX_HARMONIC_ORDER + 1,
    ):

        target_frequency = (
            order
            * FUNDAMENTAL_FREQUENCY_HZ
        )

        index = int(
            np.argmin(
                np.abs(
                    frequencies
                    - target_frequency
                )
            )
        )

        measured_frequency = float(
            frequencies[
                index
            ]
        )

        current_rms = float(
            rms_spectrum[
                index
            ]
        )

        harmonic_results.append(
            {
                "order":
                    order,

                "frequency_hz":
                    measured_frequency,

                "current_rms_a":
                    current_rms,
            }
        )

    fundamental = (
        harmonic_results[
            0
        ]["current_rms_a"]
    )

    if fundamental <= 0.0:

        raise RuntimeError(
            "Fundamental current is zero."
        )

    for result in harmonic_results:

        result[
            "percent_fundamental"
        ] = (
            100.0
            * result[
                "current_rms_a"
            ]
            / fundamental
        )

    # -------------------------------------------------------------------------
    # THD
    #
    # Includes harmonics from 2nd through 25th.
    # -------------------------------------------------------------------------

    thd_squared = sum(
        (
            result[
                "current_rms_a"
            ]
            / fundamental
        ) ** 2
        for result in harmonic_results[
            1:
        ]
    )

    thd_percent = (
        100.0
        * math.sqrt(
            thd_squared
        )
    )

    return (
        harmonic_results,
        fundamental,
        thd_percent,
    )


# =============================================================================
# PRINT HARMONIC TABLE
# =============================================================================

def print_harmonic_table(
    results,
    thd_percent,
):
    """Print the Phase-A harmonic table."""

    print_header(
        "Phase-A Harmonics"
    )

    print(
        f"{'h':>4} "
        f"{'Frequency [Hz]':>16} "
        f"{'I RMS [A]':>14} "
        f"{'% I1':>12}"
    )

    print(
        "-" * 52
    )

    for result in results:

        print(
            f"{result['order']:>4d} "
            f"{result['frequency_hz']:>16.1f} "
            f"{result['current_rms_a']:>14.5f} "
            f"{result['percent_fundamental']:>11.3f}%"
        )

    print(
        "-" * 52
    )

    print(
        f"THD "
        f"(2nd to {MAX_HARMONIC_ORDER}th) "
        f"= {thd_percent:.3f}%"
    )


# =============================================================================
# SAVE HARMONIC RESULTS
# =============================================================================

def save_harmonic_results(
    results,
    fundamental,
    thd_percent,
):
    """Save harmonic table and summary files."""

    # -------------------------------------------------------------------------
    # CSV
    # -------------------------------------------------------------------------

    with HARMONIC_CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "Harmonic Order",
                "Frequency [Hz]",
                "Current RMS [A]",
                "Percent of Fundamental [%]",
            ]
        )

        for result in results:

            writer.writerow(
                [
                    result[
                        "order"
                    ],

                    result[
                        "frequency_hz"
                    ],

                    result[
                        "current_rms_a"
                    ],

                    result[
                        "percent_fundamental"
                    ],
                ]
            )

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    with HARMONIC_SUMMARY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "Phase-A Current Harmonic Analysis\n"
        )

        file.write(
            "=" * 60
        )

        file.write(
            "\n\n"
        )

        file.write(
            f"Fundamental frequency: "
            f"{FUNDAMENTAL_FREQUENCY_HZ:.3f} Hz\n"
        )

        file.write(
            f"Fundamental current: "
            f"{fundamental:.6f} A RMS\n"
        )

        file.write(
            f"Maximum harmonic order: "
            f"{MAX_HARMONIC_ORDER}\n"
        )

        file.write(
            f"THD: "
            f"{thd_percent:.6f} %\n"
        )

    print(
        "Harmonic CSV:"
    )

    print(
        HARMONIC_CSV_FILE
    )

    print()

    print(
        "Harmonic summary:"
    )

    print(
        HARMONIC_SUMMARY_FILE
    )


# =============================================================================
# FFT SPECTRUM PLOT
# =============================================================================

def create_fft_spectrum_plot(
    frequencies,
    rms_spectrum,
):
    """Create the Phase-A frequency-domain spectrum."""

    mask = (
        frequencies
        <= FFT_MAX_FREQUENCY_HZ
    )

    fig, ax = plt.subplots(
        figsize=(
            12,
            6,
        )
    )

    ax.plot(
        frequencies[
            mask
        ],
        rms_spectrum[
            mask
        ],
    )

    ax.set_xlabel(
        "Frequency [Hz]"
    )

    ax.set_ylabel(
        "Phase-A current [A RMS]"
    )

    ax.set_title(
        "Phase-A Current FFT Spectrum"
    )

    ax.set_xlim(
        0.0,
        FFT_MAX_FREQUENCY_HZ,
    )

    ax.grid(
        True
    )

    # Mark fundamental frequency
    ax.axvline(
        FUNDAMENTAL_FREQUENCY_HZ,
        linestyle="--",
    )

    fig.tight_layout()

    fig.savefig(
        FFT_SPECTRUM_FILE,
        dpi=180,
    )

    plt.close(
        fig
    )

    print(
        "FFT spectrum:"
    )

    print(
        FFT_SPECTRUM_FILE
    )


# =============================================================================
# HARMONIC BAR CHART
# =============================================================================

def create_harmonic_bar_plot(
    results,
    thd_percent,
):
    """Create the harmonic-order spectrum."""

    orders = [
        result[
            "order"
        ]
        for result in results
    ]

    percentages = [
        result[
            "percent_fundamental"
        ]
        for result in results
    ]

    fig, ax = plt.subplots(
        figsize=(
            12,
            6,
        )
    )

    bars = ax.bar(
        orders,
        percentages,
    )

    ax.set_xlabel(
        "Harmonic order"
    )

    ax.set_ylabel(
        "Current [% of fundamental]"
    )

    ax.set_title(
        "Phase-A Current Harmonics "
        f"- THD = {thd_percent:.2f}%"
    )

    ax.set_xticks(
        orders
    )

    ax.grid(
        True,
        axis="y",
    )

    # Label significant harmonics
    for (
        bar,
        percentage,
    ) in zip(
        bars,
        percentages,
    ):

        if percentage >= 1.0:

            ax.text(
                bar.get_x()
                + bar.get_width()
                / 2.0,

                bar.get_height(),

                f"{percentage:.1f}%",

                ha="center",
                va="bottom",
                rotation=90,
                fontsize=8,
            )

    fig.tight_layout()

    fig.savefig(
        HARMONIC_BAR_FILE,
        dpi=180,
    )

    plt.close(
        fig
    )

    print(
        "Harmonic spectrum:"
    )

    print(
        HARMONIC_BAR_FILE
    )


# =============================================================================
# OPEN GENERATED PLOTS
# =============================================================================

def open_fft_results():
    """Open generated FFT images in Windows."""

    if os.name != "nt":

        return

    for path in (
        FFT_SPECTRUM_FILE,
        HARMONIC_BAR_FILE,
    ):

        if not path.is_file():

            continue

        try:

            os.startfile(
                str(path)
            )

        except Exception:
            pass


# =============================================================================
# FINAL SUMMARY
# =============================================================================

def print_final_summary(
    fundamental,
    thd_percent,
):
    """Print the final automation summary."""

    print_header(
        "AUTOMATION COMPLETED"
    )

    print(
        "Electrical system:"
    )

    print(
        f"    Source voltage = "
        f"{SOURCE_VLL_KV * 1000:.0f} V L-L RMS"
    )

    print(
        f"    Frequency      = "
        f"{SOURCE_FREQUENCY_HZ:.1f} Hz"
    )

    print(
        f"    Load resistor  = "
        f"{LOAD_RESISTANCE_OHM:.3f} ohm"
    )

    print(
        f"    Filter capacitor = "
        f"{FILTER_CAPACITANCE_UF:.1f} uF"
    )

    print()

    print(
        "DC layout:"
    )

    print(
        "    LEFT  -> C_FILTER"
    )

    print(
        "    RIGHT -> R_LOAD"
    )

    print()

    print(
        "Output Channels:"
    )

    print(
        "    Ia"
    )

    print(
        "    Ib"
    )

    print(
        "    Ic"
    )

    print(
        "    Idc"
    )

    print(
        "    Use Signal Name as Title? = YES"
    )

    print()

    print(
        "Phase-A FFT:"
    )

    print(
        f"    Fundamental = "
        f"{fundamental:.5f} A RMS"
    )

    print(
        f"    THD         = "
        f"{thd_percent:.3f}%"
    )

    print()

    print(
        "Generated files:"
    )

    print(
        f"    {PSCAD_CSV_FILE}"
    )

    print(
        f"    {FFT_SPECTRUM_FILE}"
    )

    print(
        f"    {HARMONIC_BAR_FILE}"
    )

    print(
        f"    {HARMONIC_CSV_FILE}"
    )

    print(
        f"    {HARMONIC_SUMMARY_FILE}"
    )

    print()

    print(
        "PSCAD will remain open."
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    """Run the complete PSCAD rectifier automation."""

    try:

        # ---------------------------------------------------------------------
        # Launch PSCAD
        # ---------------------------------------------------------------------

        pscad = launch_pscad()

        # ---------------------------------------------------------------------
        # Workspace / case
        # ---------------------------------------------------------------------

        project = create_or_load_project(
            pscad
        )

        # ---------------------------------------------------------------------
        # Runtime configuration
        # ---------------------------------------------------------------------

        configure_project(
            project
        )

        # ---------------------------------------------------------------------
        # Main canvas
        # ---------------------------------------------------------------------

        canvas = get_main_canvas(
            project
        )

        # ---------------------------------------------------------------------
        # Remove previous schematic
        # ---------------------------------------------------------------------

        clear_canvas(
            canvas
        )

        # ---------------------------------------------------------------------
        # Three-phase source
        # ---------------------------------------------------------------------

        source = create_source(
            canvas
        )

        # ---------------------------------------------------------------------
        # Breakout
        # ---------------------------------------------------------------------

        breakout = create_component(
            canvas,
            BREAKOUT_DEFINITION,
            BREAKOUT_POSITION,
        )

        # ---------------------------------------------------------------------
        # Diode bridge
        # ---------------------------------------------------------------------

        bridge = create_bridge(
            canvas
        )

        # ---------------------------------------------------------------------
        # AC phase currents
        # ---------------------------------------------------------------------

        connect_ac_side(
            canvas,
            source,
            breakout,
            bridge,
        )

        # ---------------------------------------------------------------------
        # Source ground
        # ---------------------------------------------------------------------

        create_and_connect_ground(
            canvas,
            source,
        )

        # ---------------------------------------------------------------------
        # Parallel C-R DC load
        # ---------------------------------------------------------------------

        create_dc_load(
            canvas,
            bridge,
        )

        # ---------------------------------------------------------------------
        # Output Channels
        # ---------------------------------------------------------------------

        channels = create_output_channels(
            canvas
        )

        # ---------------------------------------------------------------------
        # PSCAD time-domain graphs
        # ---------------------------------------------------------------------

        graphs = create_pscad_graphs(
            canvas,
            channels,
        )

        # ---------------------------------------------------------------------
        # Labels
        # ---------------------------------------------------------------------

        create_annotations(
            canvas
        )

        # ---------------------------------------------------------------------
        # Save before simulation
        # ---------------------------------------------------------------------

        save_project(
            pscad,
            project,
        )

        # ---------------------------------------------------------------------
        # Run PSCAD
        # ---------------------------------------------------------------------

        run_simulation(
            project,
            graphs,
        )

        # ---------------------------------------------------------------------
        # Save simulation state
        # ---------------------------------------------------------------------

        save_project(
            pscad,
            project,
        )

        # ---------------------------------------------------------------------
        # PSCAD output -> CSV
        #
        # The previous "Already open" problem is fixed here.
        # ---------------------------------------------------------------------

        convert_output_to_csv(
            project
        )

        # ---------------------------------------------------------------------
        # Read Phase-A current
        # ---------------------------------------------------------------------

        (
            time_array,
            current_array,
        ) = read_phase_a_current()

        # ---------------------------------------------------------------------
        # FFT
        # ---------------------------------------------------------------------

        (
            frequencies,
            rms_spectrum,
            _,
            _,
        ) = calculate_fft(
            time_array,
            current_array,
        )

        # ---------------------------------------------------------------------
        # Harmonic extraction
        # ---------------------------------------------------------------------

        (
            harmonics,
            fundamental,
            thd_percent,
        ) = extract_harmonics(
            frequencies,
            rms_spectrum,
        )

        # ---------------------------------------------------------------------
        # Console table
        # ---------------------------------------------------------------------

        print_harmonic_table(
            harmonics,
            thd_percent,
        )

        # ---------------------------------------------------------------------
        # Save harmonic data
        # ---------------------------------------------------------------------

        save_harmonic_results(
            harmonics,
            fundamental,
            thd_percent,
        )

        # ---------------------------------------------------------------------
        # Full FFT plot
        # ---------------------------------------------------------------------

        create_fft_spectrum_plot(
            frequencies,
            rms_spectrum,
        )

        # ---------------------------------------------------------------------
        # Harmonic-order plot
        # ---------------------------------------------------------------------

        create_harmonic_bar_plot(
            harmonics,
            thd_percent,
        )

        # ---------------------------------------------------------------------
        # Open plots
        # ---------------------------------------------------------------------

        open_fft_results()

        # ---------------------------------------------------------------------
        # Final report
        # ---------------------------------------------------------------------

        print_final_summary(
            fundamental,
            thd_percent,
        )

    except Exception as exc:

        print_header(
            "ERROR"
        )

        print(
            f"{type(exc).__name__}: "
            f"{exc}"
        )

        raise


# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()