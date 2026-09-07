"""Animated technical presentation of the PSCAD rectifier automation example.

This presentation is intentionally independent from PSCAD.  It reproduces the
logic of the public automation script using vector graphics and synthetic
educational waveforms, so it can be rendered on a computer that does not have
PSCAD or the mhi.pscad package installed.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C,
    GRAY_A,
    GRAY_B,
    GRAY_C,
    GREEN_C,
    ORANGE,
    PURPLE_C,
    RED_C,
    WHITE,
    YELLOW_C,
    AnimationGroup,
    Arrow,
    Axes,
    Brace,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    TransformMatchingTex,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    config,
)

from pscad_visuals import (
    ALERT_COLOR,
    BG,
    DATA_COLOR,
    ELECTRIC_COLOR,
    FFT_COLOR,
    PSCAD_COLOR,
    PYTHON_COLOR,
    SIGNAL_COLOR,
    capacitor_symbol,
    code_panel,
    dc_parallel_load,
    diode_symbol,
    fit_to_box,
    flow_block,
    ground_symbol,
    horizontal_flow,
    library_card,
    make_rectifier_bridge,
    meter_symbol,
    mini_file,
    resistor_symbol,
    scene_title,
    source_symbol,
    terminal_pair,
    vertical_flow,
    workflow_icon,
    boundary_arrow,
)


config.background_color = BG


class TechnicalScene(Scene):
    """Base scene with consistent heading placement and transition helpers."""

    def add_heading(self, title: str, subtitle: str | None = None) -> VGroup:
        heading = scene_title(title, subtitle)
        heading.to_corner(np.array([-1, 1, 0]), buff=0.35)
        self.play(FadeIn(heading, shift=np.array([0, 0.18, 0])), run_time=0.6)
        return heading

    def fade_all_except(self, *keep):
        """Fade every displayed object except explicitly retained objects."""
        keep_ids = {id(obj) for obj in keep}
        targets = [obj for obj in self.mobjects if id(obj) not in keep_ids]
        if targets:
            self.play(*[FadeOut(obj) for obj in targets], run_time=0.5)


class IntroScene(TechnicalScene):
    """Introduce the complete Python-to-engineering-results pipeline."""

    def construct(self):
        title = Text("PSCAD Automation with Python", font_size=54, weight="BOLD")
        subtitle = Text(
            "Three-Phase Six-Pulse Diode Rectifier and Harmonic Analysis",
            font_size=25,
            color=GRAY_A,
        )
        title_group = VGroup(title, subtitle).arrange(np.array([0, -1, 0]), buff=0.20)
        title_group.to_edge(np.array([0, 1, 0]), buff=0.65)

        blocks = []
        for label, kind, color, width in [
            ("Python", "code", PYTHON_COLOR, 1.6),
            ("PSCAD", "screen", PSCAD_COLOR, 1.7),
            ("EMT", "simulation", ELECTRIC_COLOR, 1.5),
            ("Data", "file", DATA_COLOR, 1.5),
            ("FFT", "spectrum", FFT_COLOR, 1.4),
            ("Harmonics + THD", "spectrum", SIGNAL_COLOR, 2.8),
        ]:
            box = flow_block(label, color, width, show_icon=False)
            icon = workflow_icon(kind, color).scale_to_fit_height(0.75)
            icon.next_to(box, np.array([0, 1, 0]), buff=0.3)
            blocks.append(VGroup(box, icon))
        pipeline = horizontal_flow(blocks, buff=0.28)
        fit_to_box(pipeline, 12.8, 2.1)
        pipeline.move_to(np.array([0, -0.4, 0]))


        self.play(Write(title), FadeIn(subtitle, shift=np.array([0, -0.2, 0])))
        self.play(LaggedStart(*[FadeIn(block, scale=0.95) for block in blocks], lag_ratio=0.12))
        arrows = [m for m in pipeline if isinstance(m, Arrow)]
        if arrows:
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.10))
        self.wait(1.4)


class ManualVsAutomationScene(TechnicalScene):
    """Contrast manual schematic construction with Python automation."""

    def construct(self):
        self.add_heading("From manual work to automation", "Python controls PSCAD; PSCAD solves the EMT equations")

        manual_box = Rectangle(width=5.4, height=4.7, stroke_color=GRAY_C)
        manual_box.move_to(np.array([-3.3, -0.55, 0]))
        automated_box = Rectangle(width=5.4, height=4.7, stroke_color=PYTHON_COLOR)
        automated_box.move_to(np.array([3.3, -0.55, 0]))

        manual_title = Text("Manual workflow", font_size=28, color=GRAY_A).next_to(manual_box, np.array([0, 1, 0]), buff=-0.48)
        auto_title = Text("Automated workflow", font_size=28, color=PYTHON_COLOR).next_to(automated_box, np.array([0, 1, 0]), buff=-0.48)

        manual_steps = VGroup(*[
            Text(step, font_size=20, color=GRAY_A)
            for step in [
                "Open PSCAD",
                "Create a case",
                "Find components",
                "Place and connect",
                "Add measurements",
                "Run and export",
            ]
        ]).arrange(np.array([0, -1, 0]), buff=0.18, aligned_edge=np.array([-1, 0, 0]))
        manual_steps.move_to(manual_box)

        python = flow_block("Python script", PYTHON_COLOR, 2.8, 0.9, 26)
        pscad = flow_block("PSCAD 5.1", PSCAD_COLOR, 2.8, 0.9, 26)
        solver = flow_block("EMTDC simulation", ELECTRIC_COLOR, 2.8, 0.9, 24)
        auto_flow = vertical_flow([python, pscad, solver], buff=0.35)
        auto_flow.move_to(automated_box)

        caption = Text(
            "Python is controlling PSCAD — PSCAD still solves the electromagnetic transient.",
            font_size=22,
            color=WHITE,
        ).to_edge(np.array([0, -1, 0]), buff=0.35)

        self.play(Create(manual_box), Create(automated_box), FadeIn(manual_title), FadeIn(auto_title))
        self.play(LaggedStart(*[FadeIn(step, shift=np.array([0.2, 0, 0])) for step in manual_steps], lag_ratio=0.12))
        self.play(LaggedStart(*[FadeIn(m) for m in auto_flow], lag_ratio=0.10))
        self.play(FadeIn(caption))
        self.wait(1.2)


class ArchitectureScene(TechnicalScene):
    """Explain automation, numerical simulation, and post-processing responsibilities."""

    def construct(self):
        self.add_heading("Example architecture", "Automation, EMT simulation and post-processing")

        left = vertical_flow([
            flow_block("Python script", PYTHON_COLOR, 3.2),
            flow_block("mhi.pscad", PYTHON_COLOR, 3.2),
            flow_block("Automation Library", PSCAD_COLOR, 3.2),
            flow_block("PSCAD 5.1", PSCAD_COLOR, 3.2),
            flow_block("EMTDC", ELECTRIC_COLOR, 3.2),
        ], buff=0.24)
        left.move_to(np.array([-3.7, -0.5, 0]))

        right = vertical_flow([
            flow_block("OUT / INF", DATA_COLOR, 3.1),
            flow_block("OutFile → CSV", DATA_COLOR, 3.1),
            flow_block("NumPy", PYTHON_COLOR, 3.1),
            flow_block("FFT + Harmonics", FFT_COLOR, 3.1),
            flow_block("THD + Figures", SIGNAL_COLOR, 3.1),
        ], buff=0.24)
        right.move_to(np.array([3.7, -0.5, 0]))

        bridge = Arrow(left.get_right(), right.get_left(), buff=0.25, color=GRAY_A, stroke_width=3)
        bridge_label = Text("results", font_size=19, color=GRAY_B).next_to(bridge, np.array([0, 1, 0]), buff=0.08)

        self.play(LaggedStart(*[FadeIn(obj) for obj in left], lag_ratio=0.08))
        self.play(GrowArrow(bridge), FadeIn(bridge_label))
        self.play(LaggedStart(*[FadeIn(obj) for obj in right], lag_ratio=0.08))
        self.wait(1.1)


class ScriptOverviewScene(TechnicalScene):
    """Map the real main() sequence into a compact execution storyboard."""

    def construct(self):
        self.add_heading("Overview of main()", "Follow the execution order of the source script")

        stages = [
            ("launch_pscad", PYTHON_COLOR),
            ("workspace / case", PSCAD_COLOR),
            ("canvas", PSCAD_COLOR),
            ("source + bridge", ELECTRIC_COLOR),
            ("meters + load", SIGNAL_COLOR),
            ("channels + graphs", SIGNAL_COLOR),
            ("project.run()", PSCAD_COLOR),
            ("OUT → CSV", DATA_COLOR),
            ("FFT", FFT_COLOR),
            ("harmonics + THD", FFT_COLOR),
            ("plots + summary", DATA_COLOR),
        ]
        boxes = [flow_block(text, color, 2.2, 0.62, 19) for text, color in stages]
        rows = VGroup()
        for row_idx in range(3):
            subset = boxes[row_idx * 4 : (row_idx + 1) * 4]
            if not subset:
                continue
            row = horizontal_flow(subset, buff=0.25)
            rows.add(row)
        rows.arrange(np.array([0, -1, 0]), buff=0.45)
        fit_to_box(rows, 12.2, 4.8)
        rows.move_to(np.array([0, -0.55, 0]))

        self.play(LaggedStart(*[FadeIn(b, scale=0.96) for b in boxes], lag_ratio=0.07), run_time=2.1)
        for b in boxes:
            self.play(Indicate(b, color=WHITE, scale_factor=1.04), run_time=0.16)
        self.wait(0.6)


class WorkspaceScene(TechnicalScene):
    """Explain how the script loads an existing workspace or creates a new one."""

    def construct(self):
        self.add_heading("Workspace and case", "create_or_load_project(pscad)")

        code = code_panel(
            '''if WORKSPACE_PATH.is_file():
    pscad.load(str(WORKSPACE_PATH))
    project = pscad.project(CASE_NAME)
else:
    pscad.new_workspace(...)
    project = pscad.create_case(...)''',
            width=5.5,
            height=3.2,
        ).move_to(np.array([-3.5, -0.45, 0]))

        decision = flow_block("Workspace exists?", WHITE, 3.0, 0.78, 23).move_to(np.array([2.8, 1.35, 0]))
        yes = flow_block("YES: load()", SIGNAL_COLOR, 2.25, 0.7, 22).move_to(np.array([1.6, 0.05, 0]))
        no = flow_block("NO: new_workspace()", PSCAD_COLOR, 3.5, 0.7, 22).move_to(np.array([4.8, 0.05, 0]))
        case = flow_block("Project / Case", PSCAD_COLOR, 3.0, 0.78, 22).move_to(np.array([3.0, -1.35, 0]))
        canvas = flow_block("Main Canvas", ELECTRIC_COLOR, 3.0, 0.78, 22).move_to(np.array([3.0, -2.45, 0]))

        arrows = VGroup(
            Arrow(decision.get_bottom(), yes.get_top(), buff=0.08, color=SIGNAL_COLOR),
            Arrow(decision.get_bottom(), no.get_top(), buff=0.08, color=PSCAD_COLOR),
            Arrow(yes.get_bottom(), case.get_top() + np.array([-0.55, 0, 0]), buff=0.08),
            Arrow(no.get_bottom(), case.get_top() + np.array([0.55, 0, 0]), buff=0.08),
            Arrow(case.get_bottom(), canvas.get_top(), buff=0.08),
        )

        self.play(FadeIn(code))
        self.play(FadeIn(decision), LaggedStart(*[GrowArrow(a) for a in arrows[:2]], lag_ratio=0.15), FadeIn(yes), FadeIn(no))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows[2:]], lag_ratio=0.12), FadeIn(case), FadeIn(canvas))
        self.wait(1.0)


class ComponentLibraryScene(TechnicalScene):
    """Show the difference between library definitions and component instances."""

    def construct(self):
        self.add_heading("Component library", "A library definition becomes an instance when placed on the canvas")

        cards = VGroup(
            library_card("master:source3", "Three Phase Voltage Source Model 1", "Sources", 4.1),
            library_card("master:breakout", "3 Phase to SLD Electrical Wire Converter", "Passive", 4.1),
            library_card("master:peswitch", "Power electronic switch", "HVDC FACTS PE", 4.1),
            library_card("master:capacitor", "Capacitor", "Passive", 4.1),
            library_card("master:pgb", "Output Channel", "I/O Devices", 4.1),
            library_card("master:datalabel", "Data signal label", "Meters / Misc.", 4.1),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3))
        fit_to_box(cards, 12.6, 3.0)
        cards.move_to(np.array([0, 0.55, 0]))

        definition = Text("definition", font_size=22, color=PSCAD_COLOR)
        create = code_panel('canvas.create_component(\n    definition, x=x, y=y\n)', width=5.0, height=1.3)
        instance = flow_block("component instance", ELECTRIC_COLOR, 3.1, 0.8, 22)
        chain = VGroup(definition, create, instance).arrange(np.array([1, 0, 0]), buff=0.65)
        chain.move_to(np.array([0, -2.15, 0]))
        arrows = VGroup(
            boundary_arrow(definition, create),
            boundary_arrow(create, instance),
        )

        self.play(LaggedStart(*[FadeIn(card, shift=np.array([0.1, 0, 0])) for card in cards], lag_ratio=0.08))
        self.play(FadeIn(definition), FadeIn(create), FadeIn(instance), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
        self.play(Circumscribe(cards[3], color=ELECTRIC_COLOR))
        self.wait(0.9)


class CreateComponentScene(TechnicalScene):
    """Animate the helper that turns a definition and position into a PSCAD instance."""

    def construct(self):
        self.add_heading("create_component()", "Code → meaning → visual action")

        code = code_panel(
            '''def create_component(
    canvas, definition, position,
    **parameters,
):
    x, y = position
    component = canvas.create_component(
        definition, x=x, y=y, **parameters
    )
    return component''',
            width=6.6,
            height=4.3,
        ).move_to(np.array([-3.25, -0.35, 0]))

        definition = flow_block("master:capacitor", PSCAD_COLOR, 3.0, 0.78, 21).move_to(np.array([3.4, 1.25, 0]))
        position = flow_block("position = (86, 36)", PYTHON_COLOR, 3.0, 0.78, 20).move_to(np.array([3.4, 0.2, 0]))
        arrow = Arrow(np.array([3.4, -0.25, 0]), np.array([3.4, -1.05, 0]), buff=0.08, color=GRAY_A)
        cap = capacitor_symbol(1.1, "C_FILTER", vertical=True).move_to(np.array([3.4, -1.75, 0]))
        instance = Text("PSCAD component instance", font_size=19, color=ELECTRIC_COLOR).next_to(cap, np.array([0, -1, 0]), buff=0.25)

        self.play(FadeIn(code))
        self.play(FadeIn(definition), FadeIn(position))
        self.play(GrowArrow(arrow))
        self.play(FadeIn(cap, scale=0.65), FadeIn(instance))
        self.play(Circumscribe(cap, color=ELECTRIC_COLOR))
        self.wait(0.9)


class CoordinateAndPortsScene(TechnicalScene):
    """Explain component placement, ports, orientation checks, and wire geometry."""

    def construct(self):
        self.add_heading("Coordinates, ports and orientation", "Automation must account for the actual component geometry")

        grid = VGroup()
        for x in range(-5, 6):
            grid.add(Line(np.array([x * 0.48 - 2.7, -2.4, 0]), np.array([x * 0.48 - 2.7, 2.0, 0]), color="#28303A", stroke_width=1))
        for y in range(-4, 5):
            grid.add(Line(np.array([-5.1, y * 0.48 - 0.2, 0]), np.array([-0.3, y * 0.48 - 0.2, 0]), color="#28303A", stroke_width=1))

        component = terminal_pair(horizontal=False).move_to(np.array([-2.7, -0.2, 0]))
        target = terminal_pair(horizontal=True).move_to(np.array([-2.7, -0.2, 0]))
        label = Text("two-terminal device", font_size=20, color=PSCAD_COLOR).next_to(component, np.array([0, -1, 0]), buff=0.25)

        code = code_panel(
            '''ports = component.ports()
if terminals[0][1] != terminals[1][1]:
    canvas.rotate_right(component)

canvas.create_wire(*points)''',
            width=5.7,
            height=2.6,
        ).move_to(np.array([3.6, 0.6, 0]))

        p1 = Dot(np.array([1.3, -1.6, 0]), color=SIGNAL_COLOR)
        p2 = Dot(np.array([5.3, -1.6, 0]), color=SIGNAL_COLOR)
        p1_label = MathTex(r"(x_1,y_1)", font_size=27).next_to(p1, np.array([0, -1, 0]), buff=0.12)
        p2_label = MathTex(r"(x_2,y_2)", font_size=27).next_to(p2, np.array([0, -1, 0]), buff=0.12)
        wire = Line(p1.get_center(), p2.get_center(), color=ELECTRIC_COLOR, stroke_width=3)

        self.play(Create(grid), FadeIn(component), FadeIn(label))
        self.play(FadeIn(code))
        self.play(Transform(component, target), Transform(label, label.copy().next_to(target, np.array([0, -1, 0]), buff=0.25)))
        self.play(FadeIn(p1), FadeIn(p2), Write(p1_label), Write(p2_label))
        self.play(Create(wire))
        self.wait(1.0)


class SourceCreationScene(TechnicalScene):
    """Show creation and parameterization of the three-phase source."""

    def construct(self):
        self.add_heading("Three-phase source", "master:source3 and the example parameters")

        code = code_panel(
            '''source = create_component(
    canvas, "master:source3",
    SOURCE_POSITION,
)
source.parameters(
    MVA=1.0,
    Vbase=0.480,
    Vm=0.480,
    F=60.0,
    Ph=0.0,
)''',
            width=5.7,
            height=4.0,
        ).move_to(np.array([-3.5, -0.45, 0]))

        source = source_symbol(1.0, "3-phase source").move_to(np.array([1.6, 1.0, 0]))
        specs = VGroup(
            Text("480 V L-L RMS", font_size=25, color=ELECTRIC_COLOR),
            Text("60 Hz", font_size=25, color=SIGNAL_COLOR),
            Text("1.0 MVA base", font_size=25, color=GRAY_A),
        ).arrange(np.array([0, -1, 0]), buff=0.22).move_to(np.array([4.65, 1.0, 0]))

        axes = Axes(x_range=[0, 2 * np.pi, np.pi / 2], y_range=[-1.3, 1.3, 1], x_length=4.3, y_length=1.9, tips=False)
        axes.move_to(np.array([3.2, -1.6, 0]))
        waves = VGroup(
            axes.plot(lambda x: np.sin(x), x_range=[0, 2 * np.pi], color=BLUE_C),
            axes.plot(lambda x: np.sin(x - 2 * np.pi / 3), x_range=[0, 2 * np.pi], color=GREEN_C),
            axes.plot(lambda x: np.sin(x + 2 * np.pi / 3), x_range=[0, 2 * np.pi], color=YELLOW_C),
        )

        self.play(FadeIn(code))
        self.play(FadeIn(source, scale=0.7), LaggedStart(*[FadeIn(s) for s in specs], lag_ratio=0.12))
        self.play(Create(axes), LaggedStart(*[Create(w) for w in waves], lag_ratio=0.10))
        self.wait(1.0)


class RectifierConstructionScene(TechnicalScene):
    """Build the six-diode bridge in the same D1-D6 grouping used by the script."""

    def construct(self):
        self.add_heading("Building the six-pulse bridge", "create_bridge(canvas)")

        bridge = make_rectifier_bridge(1.35, include_labels=True).move_to(np.array([1.8, -0.45, 0]))
        code = code_panel(
            '''d1 = create_diode(canvas, "D1", D1_POSITION)
d3 = create_diode(canvas, "D3", D3_POSITION)
d5 = create_diode(canvas, "D5", D5_POSITION)
d2 = create_diode(canvas, "D2", D2_POSITION)
d4 = create_diode(canvas, "D4", D4_POSITION)
d6 = create_diode(canvas, "D6", D6_POSITION)''',
            width=4.9,
            height=3.0,
        ).move_to(np.array([-4.2, -0.4, 0]))

        pieces = list(bridge[:6])
        rest = VGroup(*bridge[6:])
        self.play(FadeIn(code))
        self.play(LaggedStart(*[FadeIn(piece, scale=0.6) for piece in pieces], lag_ratio=0.18), run_time=2.0)
        self.play(Create(rest), run_time=1.2)
        self.play(Circumscribe(bridge, color=ELECTRIC_COLOR))
        self.wait(1.0)


class RectifierOperationScene(TechnicalScene):
    """Explain conduction paths and the origin of six-pulse behavior."""

    def construct(self):
        self.add_heading("Rectifier conduction", "Ideal conduction: one diode pair per 60 electrical degrees")

        bridge = make_rectifier_bridge(1.35, include_labels=True).move_to(np.array([-2.7, -0.3, 0]))
        self.play(FadeIn(bridge))

        path = VGroup(
            Line(np.array([-5.3, 0.1, 0]), np.array([-3.8, 0.1, 0]), color=SIGNAL_COLOR, stroke_width=5),
            Line(np.array([-3.8, 0.1, 0]), np.array([-3.8, 1.65, 0]), color=SIGNAL_COLOR, stroke_width=5),
            Line(np.array([-3.8, 1.65, 0]), np.array([-1.0, 1.65, 0]), color=SIGNAL_COLOR, stroke_width=5),
        )
        current_label = Text("current path", font_size=20, color=SIGNAL_COLOR).next_to(path, np.array([0, 1, 0]), buff=0.1)

        axes = Axes(x_range=[0, 2 * np.pi, np.pi / 3], y_range=[0, 1.25, 0.5], x_length=5.3, y_length=2.3, tips=False)
        axes.move_to(np.array([3.4, -0.2, 0]))
        rectified = axes.plot(lambda x: 0.45 + 0.55 * abs(np.sin(3 * x)), x_range=[0, 2 * np.pi], color=ELECTRIC_COLOR)
        pulses = Text("6 pulses / electrical cycle", font_size=24, color=ELECTRIC_COLOR).next_to(axes, np.array([0, -1, 0]), buff=0.28)

        self.play(Create(path), FadeIn(current_label))
        self.play(Create(axes), Create(rectified), FadeIn(pulses))
        self.wait(1.2)


class DCFilterScene(TechnicalScene):
    """Explain the exact capacitor-left/resistor-right DC arrangement."""

    def construct(self):
        self.add_heading("DC load and capacitor filter", "C_FILTER on the left; Idc and R_LOAD on the right")

        load = dc_parallel_load(1.65).move_to(np.array([-3.2, -0.3, 0]))
        specs = VGroup(
            Text("C = 2200 µF", font_size=25, color=ELECTRIC_COLOR),
            Text("R = 10 Ω", font_size=25, color=ELECTRIC_COLOR),
        ).arrange(np.array([0, -1, 0]), buff=0.22).next_to(load, np.array([0, -1, 0]), buff=0.32)

        axes = Axes(x_range=[0, 4 * np.pi, 2 * np.pi], y_range=[0, 1.2, 0.5], x_length=5.7, y_length=2.6, tips=False)
        axes.move_to(np.array([3.5, -0.1, 0]))
        raw = axes.plot(lambda x: abs(np.sin(3 * x)), x_range=[0, 4 * np.pi], color=GRAY_B)
        filtered = axes.plot(lambda x: 0.82 + 0.16 * abs(np.sin(3 * x)), x_range=[0, 4 * np.pi], color=SIGNAL_COLOR)
        legend = VGroup(
            Text("unfiltered", font_size=19, color=GRAY_B),
            Text("with capacitor", font_size=19, color=SIGNAL_COLOR),
        ).arrange(np.array([0, -1, 0]), aligned_edge=np.array([-1, 0, 0]), buff=0.12).next_to(axes, np.array([0, -1, 0]), buff=0.18)

        note = Text("Smoother DC voltage, but more distorted AC current.", font_size=21, color=WHITE).to_edge(np.array([0, -1, 0]), buff=0.22)

        self.play(FadeIn(load), FadeIn(specs))
        self.play(Create(axes), Create(raw))
        self.play(Transform(raw, filtered), FadeIn(legend))
        self.play(FadeIn(note))
        self.wait(1.0)


class MeasurementsAndChannelsScene(TechnicalScene):
    """Explain phase/DC current meters, Data Labels, and Output Channels."""

    def construct(self):
        self.add_heading("Measurements and output channels", "Export Ia, Ib, Ic and Idc from the schematic to data files")

        meters = VGroup(*[
            VGroup(meter_symbol(name, 1.0), Text(name, font_size=20, color=SIGNAL_COLOR)).arrange(np.array([0, -1, 0]), buff=0.08)
            for name in ["Ia", "Ib", "Ic", "Idc"]
        ]).arrange(np.array([1, 0, 0]), buff=0.65)
        meters.move_to(np.array([-2.7, 1.0, 0]))

        chain = horizontal_flow([
            flow_block("Meter", SIGNAL_COLOR, 1.55, 0.7, 20),
            flow_block("Data Label", SIGNAL_COLOR, 1.8, 0.7, 19),
            flow_block("Output Channel", PSCAD_COLOR, 2.2, 0.7, 18),
            flow_block("OUT / INF", DATA_COLOR, 1.8, 0.7, 19),
            flow_block("CSV", DATA_COLOR, 1.4, 0.7, 20),
        ], buff=0.22)
        fit_to_box(chain, 11.5, 1.4)
        chain.move_to(np.array([0, -0.55, 0]))

        code = code_panel(
            '''pgb.parameters(UseSignalName="YES")
pgb.parameters(Scale=1000.0)
pgb.parameters(Units="A")''',
            width=4.7,
            height=1.65,
        ).move_to(np.array([3.6, 1.55, 0]))

        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in meters], lag_ratio=0.12), FadeIn(code))
        self.play(LaggedStart(*[FadeIn(obj) if not isinstance(obj, Arrow) else GrowArrow(obj) for obj in chain], lag_ratio=0.08))
        self.wait(1.0)


class SimulationSettingsScene(TechnicalScene):
    """Explain duration, solution time step, and output sample step."""

    def construct(self):
        self.add_heading("Simulation settings", "configure_project(project)")

        code = code_panel(
            '''SIMULATION_DURATION_S = 0.60
SOLUTION_TIME_STEP_US = 50.0
CHANNEL_PLOT_STEP_US = 50.0

project.parameters(
    time_duration=SIMULATION_DURATION_S,
    time_step=SOLUTION_TIME_STEP_US,
    sample_step=CHANNEL_PLOT_STEP_US,
)''',
            width=5.4,
            height=3.3,
        ).move_to(np.array([-3.6, -0.4, 0]))

        timeline = Line(np.array([0.4, -0.2, 0]), np.array([6.0, -0.2, 0]), color=WHITE, stroke_width=3)
        start = Dot(timeline.get_start(), color=SIGNAL_COLOR)
        end = Dot(timeline.get_end(), color=SIGNAL_COLOR)
        t0 = MathTex(r"t=0", font_size=27).next_to(start, np.array([0, -1, 0]), buff=0.15)
        tf = MathTex(r"t=0.60\,\mathrm{s}", font_size=27).next_to(end, np.array([0, -1, 0]), buff=0.15)
        ticks = VGroup(*[
            Line(np.array([0.4 + i * 0.56, -0.35, 0]), np.array([0.4 + i * 0.56, -0.05, 0]), color=GRAY_C)
            for i in range(11)
        ])
        labels = VGroup(
            Text("solution step: 50 µs", font_size=22, color=ELECTRIC_COLOR),
            Text("channel plot step: 50 µs", font_size=22, color=DATA_COLOR),
        ).arrange(np.array([0, -1, 0]), buff=0.20).move_to(np.array([3.2, -1.4, 0]))

        self.play(FadeIn(code))
        self.play(Create(timeline), FadeIn(start), FadeIn(end), Create(ticks), Write(t0), Write(tf))
        self.play(LaggedStart(*[FadeIn(x) for x in labels], lag_ratio=0.18))
        self.wait(1.0)


class ExecutionScene(TechnicalScene):
    """Emphasize that PSCAD performs the EMT numerical solution."""

    def construct(self):
        self.add_heading("Execution", "project.run() starts the numerical solution in PSCAD")

        python = flow_block("Python", PYTHON_COLOR, 2.7, 0.9, 28).move_to(np.array([-4.0, 0.6, 0]))
        pscad = flow_block("PSCAD", PSCAD_COLOR, 2.7, 0.9, 28).move_to(np.array([0, 0.6, 0]))
        solver = flow_block("EMTDC solver", ELECTRIC_COLOR, 2.7, 0.9, 25).move_to(np.array([4.0, 0.6, 0]))
        a1 = Arrow(python.get_right(), pscad.get_left(), buff=0.15, color=GRAY_A)
        a2 = Arrow(pscad.get_right(), solver.get_left(), buff=0.15, color=GRAY_A)

        command = code_panel("project.run()", width=3.2, height=0.8).move_to(np.array([-2.0, -0.6, 0]))
        progress_bg = Rectangle(width=7.2, height=0.42, stroke_color=GRAY_C).move_to(np.array([1.0, -1.45, 0]))
        tracker = ValueTracker(0.0)
        progress = always_redraw(
            lambda: Rectangle(
                width=max(0.05, 7.2 * tracker.get_value()),
                height=0.42,
                stroke_width=0,
                fill_color=SIGNAL_COLOR,
                fill_opacity=0.85,
            ).align_to(progress_bg, np.array([-1, 0, 0])).move_to(
                progress_bg.get_left() + np.array([3.6 * tracker.get_value(), 0, 0])
            )
        )
        label = Text("EMT simulation", font_size=20, color=GRAY_A).next_to(progress_bg, np.array([0, -1, 0]), buff=0.16)

        self.play(FadeIn(python), GrowArrow(a1), FadeIn(pscad), GrowArrow(a2), FadeIn(solver))
        self.play(FadeIn(command), Create(progress_bg), FadeIn(progress), FadeIn(label))
        self.play(tracker.animate.set_value(1.0), run_time=2.0)
        emphasis = Text("PSCAD solves the EMT equations; Python orchestrates the workflow.", font_size=26, color=WHITE).to_edge(np.array([0, -1, 0]), buff=0.3)
        self.play(FadeIn(emphasis))
        self.wait(0.9)


class WaveformsScene(TechnicalScene):
    """Show conceptual three-phase distorted currents and focus on Phase A."""

    def construct(self):
        self.add_heading("Current waveforms", "The capacitor load produces non-sinusoidal line current")

        axes = Axes(x_range=[0, 4 * np.pi, np.pi], y_range=[-1.6, 1.6, 1], x_length=10.5, y_length=4.2, tips=False)
        axes.move_to(np.array([0, -0.55, 0]))
        ia = axes.plot(lambda x: np.sin(x) + 0.20 * np.sin(5 * x) - 0.13 * np.sin(7 * x), x_range=[0, 4 * np.pi], color=BLUE_C)
        ib = axes.plot(lambda x: np.sin(x - 2 * np.pi / 3) + 0.20 * np.sin(5 * (x - 2 * np.pi / 3)) - 0.13 * np.sin(7 * (x - 2 * np.pi / 3)), x_range=[0, 4 * np.pi], color=GREEN_C)
        ic = axes.plot(lambda x: np.sin(x + 2 * np.pi / 3) + 0.20 * np.sin(5 * (x + 2 * np.pi / 3)) - 0.13 * np.sin(7 * (x + 2 * np.pi / 3)), x_range=[0, 4 * np.pi], color=YELLOW_C)
        legend = VGroup(
            Text("Ia", font_size=20, color=BLUE_C),
            Text("Ib", font_size=20, color=GREEN_C),
            Text("Ic", font_size=20, color=YELLOW_C),
        ).arrange(np.array([1, 0, 0]), buff=0.4).next_to(axes, np.array([0, 1, 0]), buff=0.15)

        self.play(Create(axes), LaggedStart(Create(ia), Create(ib), Create(ic), lag_ratio=0.12), FadeIn(legend))
        self.play(FadeOut(ib), FadeOut(ic), Indicate(legend[0], color=BLUE_C))
        note = Text("The FFT analysis uses Phase A only.", font_size=24, color=FFT_COLOR).to_edge(np.array([0, -1, 0]), buff=0.28)
        self.play(FadeIn(note))
        self.wait(1.0)


class OutputReadingScene(TechnicalScene):
    """Explain output-file discovery, OutFile handling, CSV conversion, and Ia reading."""

    def construct(self):
        self.add_heading("From PSCAD to NumPy", "INF/OUT → OutFile → CSV → arrays")

        chain = horizontal_flow([
            mini_file("rectifier_currents.inf", DATA_COLOR, 2.4),
            mini_file("rectifier_currents.out", DATA_COLOR, 2.4),
            flow_block("OutFile", PYTHON_COLOR, 1.8, 0.7, 21),
            mini_file("rectifier_currents.csv", DATA_COLOR, 2.4),
            flow_block("time_array", PYTHON_COLOR, 1.8, 0.7, 19),
            flow_block("current_array", PYTHON_COLOR, 2.0, 0.7, 18),
        ], buff=0.15)
        fit_to_box(chain, 12.2, 1.35)
        chain.move_to(np.array([0, 0.55, 0]))

        code = code_panel(
            '''output = OutFile(str(basename))
output.open()
columns = output.columns()
output.close()
output.toCSV(str(PSCAD_CSV_FILE))

time_array, current_array = read_phase_a_current()''',
            width=6.1,
            height=3.0,
        ).move_to(np.array([0, -1.55, 0]))

        warning = Text("Close OutFile before toCSV() to avoid the 'Already open' error.", font_size=19, color=ALERT_COLOR).to_edge(np.array([0, -1, 0]), buff=0.18)

        self.play(LaggedStart(*[FadeIn(obj) if not isinstance(obj, Arrow) else GrowArrow(obj) for obj in chain], lag_ratio=0.07))
        self.play(FadeIn(code))
        self.play(FadeIn(warning))
        self.wait(1.0)


class FFTWindowScene(TechnicalScene):
    """Show selection of the final 12 cycles, corresponding to 0.2 seconds at 60 Hz."""

    def construct(self):
        self.add_heading("FFT analysis interval", "Use the final 12 cycles to exclude the initial capacitor charging transient")

        axes = Axes(x_range=[0, 0.60, 0.10], y_range=[-1.5, 1.5, 1], x_length=10.6, y_length=3.4, tips=False)
        axes.move_to(np.array([0, -0.6, 0]))
        wave = axes.plot(
            lambda t: (1 - np.exp(-10 * t)) * (np.sin(2 * np.pi * 60 * t) + 0.18 * np.sin(2 * np.pi * 300 * t)),
            x_range=[0, 0.60, 0.0005],
            color=BLUE_C,
        )
        window = Rectangle(width=10.6 * (0.2 / 0.6), height=3.4, stroke_color=FFT_COLOR, stroke_width=3, fill_color=FFT_COLOR, fill_opacity=0.10)
        window.align_to(axes, np.array([1, 0, 0]))
        window.move_to(np.array([axes.get_right()[0] - window.width / 2, axes.get_center()[1], 0]))

        eq1 = MathTex(r"T_1=\frac{1}{60}=16.67\,\mathrm{ms}", font_size=30)
        eq2 = MathTex(r"T_{\mathrm{FFT}}=12T_1=0.20\,\mathrm{s}", font_size=30, color=FFT_COLOR)
        equations = VGroup(eq1, eq2).arrange(np.array([1, 0, 0]), buff=0.65).to_edge(np.array([0, -1, 0]), buff=0.28)

        self.play(Create(axes), Create(wave))
        self.play(FadeIn(window))
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.wait(1.0)


class FFTScene(TechnicalScene):
    """Transform a conceptual time waveform into a one-sided RMS spectrum."""

    def construct(self):
        self.add_heading("FFT: time to frequency", "DFT is the mathematical transform; FFT is the efficient algorithm")

        time_axes = Axes(x_range=[0, 0.1, 0.02], y_range=[-1.5, 1.5, 1], x_length=5.1, y_length=3.0, tips=False).move_to(np.array([-3.4, -0.3, 0]))
        time_wave = time_axes.plot(
            lambda t: np.sin(2 * np.pi * 60 * t) + 0.23 * np.sin(2 * np.pi * 300 * t) + 0.16 * np.sin(2 * np.pi * 420 * t),
            x_range=[0, 0.1, 0.0003],
            color=BLUE_C,
        )
        time_label = Text("Ia(t)", font_size=24, color=BLUE_C).next_to(time_axes, np.array([0, 1, 0]), buff=0.15)

        arrow = Arrow(np.array([-0.45, -0.3, 0]), np.array([0.65, -0.3, 0]), color=FFT_COLOR, stroke_width=4)
        fft_label = Text("rFFT", font_size=26, color=FFT_COLOR).next_to(arrow, np.array([0, 1, 0]), buff=0.08)

        freq_axes = Axes(x_range=[0, 900, 180], y_range=[0, 1.2, 0.4], x_length=5.1, y_length=3.0, tips=False).move_to(np.array([3.4, -0.3, 0]))
        bars = VGroup(
            Line(freq_axes.c2p(60, 0), freq_axes.c2p(60, 1.0), color=FFT_COLOR, stroke_width=7),
            Line(freq_axes.c2p(300, 0), freq_axes.c2p(300, 0.23), color=FFT_COLOR, stroke_width=7),
            Line(freq_axes.c2p(420, 0), freq_axes.c2p(420, 0.16), color=FFT_COLOR, stroke_width=7),
        )
        freq_label = Text("Ia(f) RMS", font_size=24, color=FFT_COLOR).next_to(freq_axes, np.array([0, 1, 0]), buff=0.15)

        self.play(Create(time_axes), Create(time_wave), FadeIn(time_label))
        self.play(GrowArrow(arrow), FadeIn(fft_label))
        self.play(Create(freq_axes), LaggedStart(*[Create(bar) for bar in bars], lag_ratio=0.18), FadeIn(freq_label))
        self.wait(1.0)


class HarmonicsScene(TechnicalScene):
    """Explain integer harmonic extraction and characteristic six-pulse orders."""

    def construct(self):
        self.add_heading("Harmonics", "Select the nearest bin to h x 60 Hz, for orders 1 through 25")

        formula = MathTex(r"f_h=h f_1", r"\qquad f_1=60\,\mathrm{Hz}", font_size=38).move_to(np.array([0, 1.5, 0]))
        characteristic = MathTex(r"h=6k\pm1", font_size=46, color=ELECTRIC_COLOR).move_to(np.array([0, 0.45, 0]))

        sets = VGroup(
            Text("k = 1: 5th, 7th", font_size=27, color=WHITE),
            Text("k = 2: 11th, 13th", font_size=27, color=WHITE),
            Text("k = 3: 17th, 19th", font_size=27, color=WHITE),
            Text("k = 4: 23rd, 25th", font_size=27, color=WHITE),
        ).arrange(np.array([0, -1, 0]), buff=0.22).move_to(np.array([0, -1.05, 0]))

        caveat = Text(
            "Ideal characteristic orders; the actual spectrum depends on the circuit and operating point.",
            font_size=20,
            color=GRAY_B,
        ).to_edge(np.array([0, -1, 0]), buff=0.30)

        self.play(Write(formula))
        self.play(Write(characteristic))
        self.play(LaggedStart(*[FadeIn(s, shift=np.array([0.15, 0, 0])) for s in sets], lag_ratio=0.18))
        self.play(FadeIn(caveat))
        self.wait(1.0)


class THDScene(TechnicalScene):
    """Build the exact 2nd-through-25th THD expression used by the script."""

    def construct(self):
        self.add_heading("Phase-A current THD", "The calculation includes harmonic orders 2 through 25")

        harmonics = VGroup(*[
            flow_block(f"I{h}", FFT_COLOR if h != 1 else SIGNAL_COLOR, 1.05, 0.60, 20)
            for h in [1, 2, 3, 5, 7, 11, 13, 25]
        ]).arrange(np.array([1, 0, 0]), buff=0.22).move_to(np.array([0, 1.2, 0]))

        eq_a = MathTex(r"\mathrm{THD}_I", font_size=48, color=FFT_COLOR).move_to(np.array([-4.4, -1.25, 0]))
        eq_b = MathTex(r"=\sqrt{\sum_{h=2}^{25}\left(\frac{I_h}{I_1}\right)^2}", font_size=46, color=WHITE).next_to(eq_a, np.array([1, 0, 0]), buff=0.20)
        eq_c = MathTex(r"\times100\%", font_size=46, color=SIGNAL_COLOR).next_to(eq_b, np.array([1, 0, 0]), buff=0.20)
        brace = Brace(harmonics[1:], direction=np.array([0, -1, 0]), color=FFT_COLOR)
        brace_label = Text("included harmonic orders", font_size=20, color=FFT_COLOR).next_to(brace, np.array([0, -1, 0]), buff=0.10)

        self.play(LaggedStart(*[FadeIn(h) for h in harmonics], lag_ratio=0.10))
        self.play(Create(brace), FadeIn(brace_label))
        self.play(Write(eq_a), Write(eq_b), Write(eq_c))
        self.wait(1.1)


class ResultsScene(TechnicalScene):
    """Show the files produced by the actual automation example."""

    def construct(self):
        self.add_heading("Generated files", "PSCAD outputs and Python post-processing results")

        folder = flow_block("PSCAD_Project/", DATA_COLOR, 4.8, 0.65, 26).move_to(np.array([-3.5, 2.05, 0]))
        files = VGroup(
            mini_file("ThreePhaseRectifier.pswx", PSCAD_COLOR, 5.2),
            mini_file("ThreePhaseRectifier.pscx", PSCAD_COLOR, 5.2),
            mini_file("rectifier_currents.csv", DATA_COLOR, 5.2),
            mini_file("phase_a_fft_spectrum.png", FFT_COLOR, 5.2),
            mini_file("phase_a_harmonics.png", FFT_COLOR, 5.2),
            mini_file("phase_a_harmonics.csv", DATA_COLOR, 5.2),
            mini_file("phase_a_harmonic_summary.txt", DATA_COLOR, 5.2),
        ).arrange(np.array([0, -1, 0]), buff=0.08, aligned_edge=np.array([-1, 0, 0]))
        files.next_to(folder, np.array([0, -1, 0]), buff=0.18, aligned_edge=np.array([-1, 0, 0]))

        summary = VGroup(
            flow_block("Fundamental RMS", SIGNAL_COLOR, 3.1, 0.75, 21),
            flow_block("Harmonic table", FFT_COLOR, 3.1, 0.75, 21),
            flow_block("THD", FFT_COLOR, 3.1, 0.75, 22),
            flow_block("Plots", DATA_COLOR, 3.1, 0.75, 22),
        ).arrange(np.array([0, -1, 0]), buff=0.28).move_to(np.array([3.2, -0.3, 0]))

        self.play(FadeIn(folder))
        self.play(LaggedStart(*[FadeIn(f, shift=np.array([0.15, 0, 0])) for f in files], lag_ratio=0.10))
        self.play(LaggedStart(*[FadeIn(s, scale=0.95) for s in summary], lag_ratio=0.14))
        self.wait(1.0)


class FullWorkflowScene(TechnicalScene):
    """Summarize the complete real sequence with three synchronized columns."""

    def construct(self):
        self.add_heading("The complete workflow at a glance", "Python code, PSCAD actions and execution progress")

        left_box = Rectangle(width=4.2, height=5.2, stroke_color=PYTHON_COLOR).move_to(np.array([-4.3, -0.45, 0]))
        center_box = Rectangle(width=4.2, height=5.2, stroke_color=ELECTRIC_COLOR).move_to(np.array([0, -0.45, 0]))
        right_box = Rectangle(width=4.2, height=5.2, stroke_color=SIGNAL_COLOR).move_to(np.array([4.3, -0.45, 0]))
        headings = VGroup(
            Text("Python", font_size=24, color=PYTHON_COLOR).next_to(left_box, np.array([0, 1, 0]), buff=-0.4),
            Text("PSCAD", font_size=24, color=PSCAD_COLOR).next_to(center_box, np.array([0, 1, 0]), buff=-0.4),
            Text("Progress", font_size=24, color=SIGNAL_COLOR).next_to(right_box, np.array([0, 1, 0]), buff=-0.4),
        )
        self.play(Create(left_box), Create(center_box), Create(right_box), FadeIn(headings))

        steps = [
            ("create_source()", workflow_icon("source", ELECTRIC_COLOR), "Create Source ✓"),
            ("create_bridge()", workflow_icon("rectifier", ELECTRIC_COLOR), "Create Rectifier ✓"),
            ("create_dc_load()", workflow_icon("load", ELECTRIC_COLOR), "Create DC Load ✓"),
            ("create_output_channels()", workflow_icon("meter", SIGNAL_COLOR), "Measurements ✓"),
            ("project.run()", workflow_icon("simulation", ELECTRIC_COLOR), "Simulation ✓"),
            ("calculate_fft()", workflow_icon("spectrum", FFT_COLOR), "FFT ✓"),
        ]

        y_positions = [1.25, 0.49, -0.27, -1.03, -1.79, -2.55]
        for (code_text, visual, progress_text), y in zip(steps, y_positions):
            code_obj = Text(code_text, font_size=19, color=PYTHON_COLOR).move_to(np.array([-4.3, y, 0]))
            fit_to_box(code_obj, 3.7, 0.55)
            visual.move_to(np.array([0, y, 0]))
            fit_to_box(visual, 3.5, 0.7)
            progress = Text(progress_text, font_size=19, color=SIGNAL_COLOR).move_to(np.array([4.3, y, 0]))
            fit_to_box(progress, 3.7, 0.55)
            self.play(FadeIn(code_obj), FadeIn(visual, scale=0.85), FadeIn(progress), run_time=0.38)
        self.wait(1.2)


class GeneralizationScene(TechnicalScene):
    """Show how the automation pattern generalizes to other EMT studies."""

    def construct(self):
        self.add_heading("Beyond the rectifier example", "The same architecture can automate many EMT studies")

        center = flow_block("PSCAD + Python", PYTHON_COLOR, 3.1, 0.9, 26).move_to(np.array([0, -0.3, 0]))
        topics = [
            "Harmonic filters",
            "Transformer inrush",
            "Capacitor switching",
            "Short circuits",
            "TRV",
            "Lines & cables",
            "Synchronous machines",
            "Parameter sweeps",
        ]
        angles = np.linspace(0, 2 * np.pi, len(topics), endpoint=False)
        nodes = VGroup()
        arrows = VGroup()
        for topic, angle in zip(topics, angles):
            pos = np.array([4.6 * np.cos(angle), 2.65 * np.sin(angle) - 0.3, 0])
            node = flow_block(topic, PSCAD_COLOR if "Parameter" not in topic else DATA_COLOR, 2.35, 0.62, 17).move_to(pos)
            nodes.add(node)
            arrows.add(boundary_arrow(center[0], node[0], color=GRAY_A))

        self.play(FadeIn(center))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.07), run_time=2.0)
        self.wait(1.0)


class PortabilityScene(TechnicalScene):
    """Show which source-script settings are machine-dependent and the portable-path recommendation."""

    def construct(self):
        self.add_heading("Portability", "Replace machine-specific paths with a project-relative directory")

        current = code_panel(
            '''OUTPUT_DIR = Path(
    r"C:\\Users\\z005b93y\\PycharmProjects"
    r"\\pscad-test-1\\PSCAD_Project"
)''',
            width=8.0,
            height=1.65,
        ).move_to(np.array([-2.25, 1.05, 0]))
        portable = code_panel(
            '''SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "PSCAD_Project"''',
            width=8.0,
            height=1.65,
        ).move_to(np.array([-2.25, -1.25, 0]))
        arrow = boundary_arrow(current, portable, color=SIGNAL_COLOR)
        label = Text("recommended", font_size=21, color=SIGNAL_COLOR).next_to(arrow, np.array([1, 0, 0]), buff=0.18)

        checks = VGroup(
            Text("PSCAD_VERSION = 5.1.0", font_size=21, color=PSCAD_COLOR),
            Text("PSCAD_X64 = True", font_size=21, color=PSCAD_COLOR),
            Text("mhi.pscad available in Python", font_size=21, color=PYTHON_COLOR),
            Text("License with Automation Library", font_size=21, color=ELECTRIC_COLOR),
        ).arrange(np.array([0, -1, 0]), buff=0.20).move_to(np.array([4.6, -0.2, 0]))

        fit_to_box(checks, 3.6, 3.4)
        self.play(FadeIn(current), FadeIn(portable), GrowArrow(arrow), FadeIn(label))
        self.play(LaggedStart(*[FadeIn(c, shift=np.array([0.12, 0, 0])) for c in checks], lag_ratio=0.14))
        self.wait(1.1)


class ConclusionScene(TechnicalScene):
    """Close the presentation with the full engineering automation message."""

    def construct(self):
        title = Text("From Python code to an automated\nelectromagnetic transient study", font_size=39, weight="BOLD")
        title.to_edge(np.array([0, 1, 0]), buff=0.85)

        pipeline = vertical_flow([
            flow_block("Python Code", PYTHON_COLOR, 4.2, 0.8, 25),
            flow_block("Automatic PSCAD Model", PSCAD_COLOR, 4.2, 0.8, 24),
            flow_block("EMT Simulation", ELECTRIC_COLOR, 4.2, 0.8, 25),
            flow_block("Engineering Results", SIGNAL_COLOR, 4.2, 0.8, 25),
        ], buff=0.34)
        pipeline.move_to(np.array([0, -0.65, 0]))


        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(obj) if not isinstance(obj, Arrow) else GrowArrow(obj) for obj in pipeline], lag_ratio=0.10), run_time=2.0)
        self.wait(1.5)


# Ordered list used by render_all.py.
SCENE_ORDER = [
    "IntroScene",
    "ManualVsAutomationScene",
    "ArchitectureScene",
    "ScriptOverviewScene",
    "WorkspaceScene",
    "ComponentLibraryScene",
    "CreateComponentScene",
    "CoordinateAndPortsScene",
    "SourceCreationScene",
    "RectifierConstructionScene",
    "RectifierOperationScene",
    "DCFilterScene",
    "MeasurementsAndChannelsScene",
    "SimulationSettingsScene",
    "ExecutionScene",
    "WaveformsScene",
    "OutputReadingScene",
    "FFTWindowScene",
    "FFTScene",
    "HarmonicsScene",
    "THDScene",
    "ResultsScene",
    "FullWorkflowScene",
    "GeneralizationScene",
    "PortabilityScene",
    "ConclusionScene",
]
