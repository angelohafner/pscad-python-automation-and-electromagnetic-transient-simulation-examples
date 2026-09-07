"""Reusable visual components for the PSCAD automation Manim presentation."""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C,
    GRAY_B,
    GRAY_C,
    GREEN_C,
    ORANGE,
    PURPLE_C,
    RED_C,
    WHITE,
    YELLOW_C,
    Arrow,
    Circle,
    Code,
    Dot,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
)


BG = "#101318"
PYTHON_COLOR = BLUE_C
PSCAD_COLOR = ORANGE
ELECTRIC_COLOR = YELLOW_C
SIGNAL_COLOR = GREEN_C
FFT_COLOR = PURPLE_C
DATA_COLOR = GRAY_B
ALERT_COLOR = RED_C


def fit_to_box(mobject, max_width: float, max_height: float):
    """Scale a mobject down so that it fits inside a target box."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def scene_title(title: str, subtitle: str | None = None) -> VGroup:
    """Create a reusable top-left scene heading."""
    title_obj = Text(title, font_size=38, weight="BOLD")
    fit_to_box(title_obj, 12.9, 1.0)
    group = VGroup(title_obj)
    if subtitle:
        subtitle_obj = Text(subtitle, font_size=20, color=GRAY_B)
        fit_to_box(subtitle_obj, 12.9, 0.55)
        subtitle_obj.next_to(title_obj, direction=np.array([0, -1, 0]), aligned_edge=np.array([-1, 0, 0]), buff=0.12)
        group.add(subtitle_obj)
    return group


def workflow_icon(kind: str, color=WHITE) -> VGroup:
    """Draw compact, offline pictograms without miniature schematic labels."""
    if kind == "code":
        icon = VGroup(
            Line([-0.15, 0.3, 0], [-0.45, 0, 0]),
            Line([-0.45, 0, 0], [-0.15, -0.3, 0]),
            Line([0.15, 0.3, 0], [0.45, 0, 0]),
            Line([0.45, 0, 0], [0.15, -0.3, 0]),
            Line([0.08, 0.35, 0], [-0.08, -0.35, 0]),
        )
    elif kind in ("source", "simulation"):
        wave = VGroup(*[
            Line([x, 0.17 * np.sin(2 * np.pi * x), 0],
                 [x + 0.025, 0.17 * np.sin(2 * np.pi * (x + 0.025)), 0])
            for x in np.arange(-0.35, 0.35, 0.025)
        ])
        icon = VGroup(Circle(radius=0.43), wave)
    elif kind == "spectrum":
        icon = VGroup(Line([-0.4, -0.32, 0], [0.45, -0.32, 0]), *[
            Line([x, -0.32, 0], [x, h, 0])
            for x, h in [(-0.3, 0.38), (-0.05, 0.05), (0.2, -0.08), (0.4, -0.2)]
        ])
    elif kind == "meter":
        icon = VGroup(Circle(radius=0.4), Line([0, 0, 0], [0.22, 0.22, 0]), Dot(radius=0.045))
    elif kind == "rectifier":
        icon = VGroup(Polygon([-0.3, -0.3, 0], [-0.3, 0.3, 0], [0.2, 0, 0]),
                      Line([0.23, -0.32, 0], [0.23, 0.32, 0]),
                      Line([-0.5, 0, 0], [-0.3, 0, 0]), Line([0.23, 0, 0], [0.5, 0, 0]))
    elif kind == "load":
        icon = VGroup(Rectangle(width=0.3, height=0.55).shift([0.25, 0, 0]),
                      Line([-0.4, 0.12, 0], [-0.1, 0.12, 0]),
                      Line([-0.4, -0.12, 0], [-0.1, -0.12, 0]),
                      Line([-0.25, 0.4, 0], [-0.25, 0.12, 0]),
                      Line([-0.25, -0.12, 0], [-0.25, -0.4, 0]))
    elif kind == "file":
        icon = VGroup(Rectangle(width=0.6, height=0.8), *[
            Line([-0.18, y, 0], [0.18, y, 0]) for y in (0.2, 0, -0.2)
        ])
    else:
        screen = Rectangle(width=0.9, height=0.6)
        icon = VGroup(screen, Line([0, -0.3, 0], [0, -0.45, 0]),
                      Line([-0.25, -0.45, 0], [0.25, -0.45, 0]))
    icon.set_color(color).set_stroke(width=2.5)
    return icon


def boundary_arrow(source, target, color=GRAY_C) -> Arrow:
    """Connect rectangular boundaries along the center-to-center direction."""
    direction = target.get_center() - source.get_center()
    def boundary(obj, vector):
        factors = [extent / (2 * abs(value)) for extent, value in
                   zip((obj.width, obj.height), vector[:2]) if abs(value) > 1e-9]
        return obj.get_center() + vector * min(factors)
    return Arrow(boundary(source, direction), boundary(target, -direction),
                 buff=0.06, color=color, stroke_width=3,
                 tip_length=0.18, max_tip_length_to_length_ratio=0.24)


def flow_block(text: str, color=WHITE, width: float = 2.7, height: float = 0.78, font_size: int = 24, show_icon: bool = True) -> VGroup:
    """Create a rounded block used in architecture and workflow diagrams."""
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height, stroke_color=color, stroke_width=2)
    box.set_fill(color, opacity=0.08)
    label = Text(text, font_size=font_size, color=color)
    fit_to_box(label, width - 0.28, height - 0.18)
    label.move_to(box)
    kinds = {"Python": "code", "Python script": "code", "Python Code": "code",
             "mhi.pscad": "code", "NumPy": "code", "PSCAD": "screen",
             "PSCAD 5.1": "screen", "Automatic PSCAD Model": "screen",
             "Automation Library": "screen", "EMT": "simulation", "EMTDC": "simulation",
             "EMTDC simulation": "simulation", "EMT Simulation": "simulation",
             "Data": "file", "OUT / INF": "file", "OutFile → CSV": "file",
             "FFT": "spectrum", "FFT + Harmonics": "spectrum",
             "Harmonics + THD": "spectrum", "THD + Figures": "spectrum",
             "Engineering Results": "spectrum"}
    if show_icon and text in kinds:
        icon = workflow_icon(kinds[text], color).scale_to_fit_height(height * 0.55)
        icon.move_to(box.get_left() + np.array([0.17 + icon.width / 2, 0, 0]))
        available = width - icon.width - 0.48
        fit_to_box(label, available, height - 0.2)
        label.move_to(box.get_right() - np.array([0.14 + available / 2, 0, 0]))
        return VGroup(box, label, icon)
    return VGroup(box, label)


def vertical_flow(blocks: list[VGroup], buff: float = 0.32, arrow_color=GRAY_C) -> VGroup:
    """Stack workflow blocks vertically and connect them with arrows."""
    group = VGroup()
    for idx, block in enumerate(blocks):
        if idx:
            block.next_to(blocks[idx - 1], direction=np.array([0, -1, 0]), buff=buff)
            arrow = Arrow(
                blocks[idx - 1].get_bottom(),
                block.get_top(),
                buff=0.03,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.35,
                color=arrow_color,
            )
            group.add(arrow)
        group.add(block)
    return group


def horizontal_flow(blocks: list[VGroup], buff: float = 0.45, arrow_color=GRAY_C) -> VGroup:
    """Arrange workflow blocks horizontally and connect them with arrows."""
    group = VGroup()
    for idx, block in enumerate(blocks):
        if idx:
            block.next_to(blocks[idx - 1], direction=np.array([1, 0, 0]), buff=buff)
            arrow = Arrow(
                blocks[idx - 1].get_right(),
                block.get_left(),
                buff=0.03,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.35,
                color=arrow_color,
            )
            group.add(arrow)
        group.add(block)
    return group


def code_panel(code: str, width: float = 6.0, height: float = 3.1, line_numbers: bool = False) -> Code:
    """Create a compact syntax-highlighted Python code panel."""
    panel = Code(
        code_string=code.strip("\n"),
        language="python",
        formatter_style="monokai",
        add_line_numbers=line_numbers,
        background="rectangle",
        background_config={"stroke_color": GRAY_C, "stroke_width": 1.5},
        paragraph_config={"font_size": 26, "font": "Consolas"},
    )
    return fit_to_box(panel, width, height)


def library_card(scoped_name: str, description: str, group: str, width: float = 4.2) -> VGroup:
    """Create a PSCAD master-library definition card."""
    box = RoundedRectangle(corner_radius=0.12, width=width, height=1.2, stroke_color=PSCAD_COLOR, stroke_width=2)
    box.set_fill(PSCAD_COLOR, opacity=0.06)
    name = Text(scoped_name, font_size=23, color=PSCAD_COLOR, weight="BOLD")
    desc = Text(description, font_size=17, color=WHITE)
    grp = Text(group, font_size=14, color=GRAY_B)
    content = VGroup(name, desc, grp).arrange(np.array([0, -1, 0]), buff=0.08, aligned_edge=np.array([-1, 0, 0]))
    fit_to_box(content, width - 0.3, 0.95)
    content.move_to(box)
    return VGroup(box, content)


def source_symbol(scale: float = 1.0, label: str = "3φ") -> VGroup:
    """Create a compact three-phase AC source symbol."""
    circle = Circle(radius=0.48 * scale, stroke_color=ELECTRIC_COLOR, stroke_width=3)
    sine = MathTex(r"\sim", color=ELECTRIC_COLOR, font_size=int(40 * scale)).move_to(circle)
    tag = Text(label, font_size=int(18 * scale), color=WHITE).next_to(circle, np.array([0, -1, 0]), buff=0.08)
    left = Line(circle.get_left() + np.array([-0.42 * scale, 0, 0]), circle.get_left(), color=ELECTRIC_COLOR)
    right = Line(circle.get_right(), circle.get_right() + np.array([0.42 * scale, 0, 0]), color=ELECTRIC_COLOR)
    return VGroup(left, circle, sine, right, tag)


def diode_symbol(scale: float = 1.0, label: str | None = None, vertical: bool = False) -> VGroup:
    """Create a simple diode symbol suitable for schematic animation."""
    tri = Polygon(
        np.array([-0.25, -0.25, 0]),
        np.array([-0.25, 0.25, 0]),
        np.array([0.20, 0.00, 0]),
        stroke_color=ELECTRIC_COLOR,
        fill_color=ELECTRIC_COLOR,
        fill_opacity=0.15,
        stroke_width=2.4,
    )
    bar = Line(np.array([0.24, -0.3, 0]), np.array([0.24, 0.3, 0]), color=ELECTRIC_COLOR, stroke_width=2.4)
    lead_l = Line(np.array([-0.55, 0, 0]), np.array([-0.25, 0, 0]), color=ELECTRIC_COLOR)
    lead_r = Line(np.array([0.24, 0, 0]), np.array([0.55, 0, 0]), color=ELECTRIC_COLOR)
    group = VGroup(lead_l, tri, bar, lead_r).scale(scale)
    if vertical:
        group.rotate(np.pi / 2)
    if label:
        tag = Text(label, font_size=int(17 * scale), color=WHITE)
        tag.next_to(group, np.array([0, 1, 0]), buff=0.06)
        group.add(tag)
    return group


def resistor_symbol(scale: float = 1.0, label: str | None = None, vertical: bool = True) -> VGroup:
    """Create a resistor symbol."""
    pts = [
        np.array([-0.55, 0.0, 0]),
        np.array([-0.40, 0.0, 0]),
        np.array([-0.30, 0.18, 0]),
        np.array([-0.15, -0.18, 0]),
        np.array([0.0, 0.18, 0]),
        np.array([0.15, -0.18, 0]),
        np.array([0.30, 0.18, 0]),
        np.array([0.40, 0.0, 0]),
        np.array([0.55, 0.0, 0]),
    ]
    segments = VGroup(*[Line(a, b, color=ELECTRIC_COLOR, stroke_width=2.4) for a, b in zip(pts[:-1], pts[1:])])
    segments.scale(scale)
    if vertical:
        segments.rotate(np.pi / 2)
    if label:
        tag = Text(label, font_size=int(17 * scale), color=WHITE).next_to(segments, np.array([1, 0, 0]), buff=0.1)
        segments.add(tag)
    return segments


def capacitor_symbol(scale: float = 1.0, label: str | None = None, vertical: bool = True) -> VGroup:
    """Create a capacitor symbol."""
    plate1 = Line(np.array([-0.28, -0.28, 0]), np.array([-0.28, 0.28, 0]), color=ELECTRIC_COLOR, stroke_width=3)
    plate2 = Line(np.array([0.28, -0.28, 0]), np.array([0.28, 0.28, 0]), color=ELECTRIC_COLOR, stroke_width=3)
    lead1 = Line(np.array([-0.6, 0, 0]), np.array([-0.28, 0, 0]), color=ELECTRIC_COLOR)
    lead2 = Line(np.array([0.28, 0, 0]), np.array([0.6, 0, 0]), color=ELECTRIC_COLOR)
    group = VGroup(lead1, plate1, plate2, lead2).scale(scale)
    if vertical:
        group.rotate(np.pi / 2)
    if label:
        tag = Text(label, font_size=int(17 * scale), color=WHITE).next_to(group, np.array([1, 0, 0]), buff=0.1)
        group.add(tag)
    return group


def meter_symbol(label: str = "I", scale: float = 1.0) -> VGroup:
    """Create a circular current-meter symbol."""
    circle = Circle(radius=0.30 * scale, stroke_color=SIGNAL_COLOR, stroke_width=2.4)
    text = Text(label, font_size=int(20 * scale), color=SIGNAL_COLOR, weight="BOLD").move_to(circle)
    left = Line(circle.get_left() + np.array([-0.28 * scale, 0, 0]), circle.get_left(), color=ELECTRIC_COLOR)
    right = Line(circle.get_right(), circle.get_right() + np.array([0.28 * scale, 0, 0]), color=ELECTRIC_COLOR)
    return VGroup(left, circle, text, right)


def ground_symbol(scale: float = 1.0) -> VGroup:
    """Create a ground symbol."""
    stem = Line(np.array([0, 0.35, 0]), np.array([0, 0, 0]), color=ELECTRIC_COLOR)
    l1 = Line(np.array([-0.28, 0, 0]), np.array([0.28, 0, 0]), color=ELECTRIC_COLOR)
    l2 = Line(np.array([-0.18, -0.12, 0]), np.array([0.18, -0.12, 0]), color=ELECTRIC_COLOR)
    l3 = Line(np.array([-0.08, -0.24, 0]), np.array([0.08, -0.24, 0]), color=ELECTRIC_COLOR)
    return VGroup(stem, l1, l2, l3).scale(scale)


def make_rectifier_bridge(scale: float = 1.0, include_labels: bool = True) -> VGroup:
    """Build a six-diode conceptual bridge layout."""
    xs = [-1.1, 0.0, 1.1]
    upper = []
    lower = []
    names_u = ["D1", "D3", "D5"]
    names_l = ["D2", "D4", "D6"]
    for x, name in zip(xs, names_u):
        d = diode_symbol(0.65, name if include_labels else None, vertical=True).move_to(np.array([x, 0.9, 0]))
        upper.append(d)
    for x, name in zip(xs, names_l):
        d = diode_symbol(0.65, name if include_labels else None, vertical=True).move_to(np.array([x, -0.9, 0]))
        lower.append(d)

    top_bus = Line(np.array([-1.7, 1.45, 0]), np.array([1.7, 1.45, 0]), color=ELECTRIC_COLOR, stroke_width=2.4)
    bottom_bus = Line(np.array([-1.7, -1.45, 0]), np.array([1.7, -1.45, 0]), color=ELECTRIC_COLOR, stroke_width=2.4)
    ac_lines = VGroup()
    phase_y = [0.28, 0.0, -0.28]
    for x, y in zip(xs, phase_y):
        ac_lines.add(Line(np.array([-2.1, y, 0]), np.array([x, y, 0]), color=ELECTRIC_COLOR, stroke_width=2))
        ac_lines.add(Line(np.array([x, y, 0]), np.array([x, 0.4, 0]), color=ELECTRIC_COLOR, stroke_width=2))
        ac_lines.add(Line(np.array([x, y, 0]), np.array([x, -0.4, 0]), color=ELECTRIC_COLOR, stroke_width=2))
        ac_lines.add(Line(np.array([x, 1.2, 0]), np.array([x, 1.45, 0]), color=ELECTRIC_COLOR, stroke_width=2))
        ac_lines.add(Line(np.array([x, -1.2, 0]), np.array([x, -1.45, 0]), color=ELECTRIC_COLOR, stroke_width=2))

    phases = VGroup(
        Text("A", font_size=18, color=WHITE).move_to(np.array([-2.28, 0.28, 0])),
        Text("B", font_size=18, color=WHITE).move_to(np.array([-2.28, 0.0, 0])),
        Text("C", font_size=18, color=WHITE).move_to(np.array([-2.28, -0.28, 0])),
    )
    plus = Text("+Vdc", font_size=18, color=WHITE).next_to(top_bus, np.array([1, 0, 0]), buff=0.08)
    minus = Text("-Vdc", font_size=18, color=WHITE).next_to(bottom_bus, np.array([1, 0, 0]), buff=0.08)
    group = VGroup(*upper, *lower, top_bus, bottom_bus, ac_lines, phases, plus, minus)
    return group.scale(scale)


def dc_parallel_load(scale: float = 1.0) -> VGroup:
    """Position electrical geometry before adding labels; wire exact terminals."""
    top = Line([-1.15, 1.1, 0], [1.15, 1.1, 0], color=ELECTRIC_COLOR, stroke_width=2.4)
    bottom = Line([-1.15, -1.1, 0], [1.15, -1.1, 0], color=ELECTRIC_COLOR, stroke_width=2.4)
    cap = capacitor_symbol(0.9, vertical=True).move_to([-0.65, 0, 0])
    meter = meter_symbol("Idc", 0.60).rotate(np.pi / 2).move_to([0.65, 0.65, 0])
    meter[2].rotate(-np.pi / 2)
    resistor = resistor_symbol(0.75, vertical=True).move_to([0.65, -0.35, 0])
    wires = VGroup(
        Line([-0.65, 1.1, 0], cap.get_top(), color=ELECTRIC_COLOR),
        Line(cap.get_bottom(), [-0.65, -1.1, 0], color=ELECTRIC_COLOR),
        Line([0.65, 1.1, 0], meter.get_top(), color=ELECTRIC_COLOR),
        Line(meter.get_bottom(), resistor.get_top(), color=ELECTRIC_COLOR),
        Line(resistor.get_bottom(), [0.65, -1.1, 0], color=ELECTRIC_COLOR),
    )
    cap_label = Text("C_FILTER", font_size=16, color=WHITE).next_to(cap, [-1, 0, 0], buff=0.16)
    resistor_label = Text("R_LOAD", font_size=16, color=WHITE).next_to(resistor, [1, 0, 0], buff=0.16)
    return VGroup(top, bottom, cap, meter, resistor, wires, cap_label, resistor_label).scale(scale)


def mini_file(name: str, color=DATA_COLOR, width: float = 2.7) -> VGroup:
    """Create a small file card."""
    box = Rectangle(width=width, height=0.62, stroke_color=color, stroke_width=1.7)
    box.set_fill(color, opacity=0.06)
    label = Text(name, font_size=17, color=color)
    fit_to_box(label, width - 0.2, 0.45)
    label.move_to(box)
    return VGroup(box, label)


def terminal_pair(horizontal: bool = True) -> VGroup:
    """Create a two-terminal component abstraction with visible port dots."""
    body = RoundedRectangle(corner_radius=0.08, width=1.6, height=0.7, stroke_color=PSCAD_COLOR, stroke_width=2)
    body.set_fill(PSCAD_COLOR, opacity=0.08)
    left = Dot(body.get_left(), radius=0.06, color=SIGNAL_COLOR)
    right = Dot(body.get_right(), radius=0.06, color=SIGNAL_COLOR)
    group = VGroup(body, left, right)
    if not horizontal:
        group.rotate(np.pi / 2)
    return group


def waveform_points(x_min: float, x_max: float, samples: int = 700, kind: str = "phase_current") -> np.ndarray:
    """Generate deterministic conceptual waveform samples for educational plots."""
    x = np.linspace(x_min, x_max, samples)
    if kind == "phase_current":
        y = np.sin(x) + 0.20 * np.sin(5 * x) - 0.13 * np.sin(7 * x) + 0.07 * np.sin(11 * x)
    elif kind == "rectified":
        y = np.abs(np.sin(3 * x))
    elif kind == "filtered_dc":
        raw = np.abs(np.sin(3 * x))
        y = 0.82 + 0.16 * raw
    else:
        y = np.sin(x)
    return np.column_stack([x, y])
