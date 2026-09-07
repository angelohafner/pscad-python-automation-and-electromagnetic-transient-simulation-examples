"""Static tests that do not require Manim to be installed."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "pscad_rectifier_presentation.py"
VISUALS = ROOT / "pscad_visuals.py"

EXPECTED_SCENES = [
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


def parse(path: Path) -> ast.Module:
    """Parse one Python module without importing runtime dependencies."""
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_python_sources_parse() -> None:
    parse(MAIN)
    parse(VISUALS)


def test_all_expected_scenes_exist() -> None:
    module = parse(MAIN)
    class_names = {node.name for node in module.body if isinstance(node, ast.ClassDef)}
    assert set(EXPECTED_SCENES).issubset(class_names)


def test_scene_order_matches_expected_scenes() -> None:
    module = parse(MAIN)
    order = next(node.value for node in module.body if isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id == "SCENE_ORDER"
                         for target in node.targets))
    assert ast.literal_eval(order) == EXPECTED_SCENES


def test_no_pscad_runtime_dependency_in_animation() -> None:
    text = MAIN.read_text(encoding="utf-8") + VISUALS.read_text(encoding="utf-8")
    assert "import mhi.pscad" not in text
