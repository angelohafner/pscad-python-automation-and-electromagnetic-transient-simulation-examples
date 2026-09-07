# PSCAD Python Automation — Manim Presentation

Animated technical presentation explaining how the public example
`three_phase_rectifier_fft_pscad.py` builds and simulates a three-phase
six-pulse diode rectifier in PSCAD and then performs Phase-A FFT, harmonic
extraction, and THD calculation in Python.

The presentation is designed as an engineering lesson rather than a sequence
of static slides. It repeatedly applies the pattern:

**Code → Meaning → Visual Action**

## Source material

The content was derived from:

- `https://github.com/angelohafner/pscad-python-automation-and-electromagnetic-transient-simulation-examples`
- `three_phase_rectifier_fft_pscad.py`
- `README-three_phase_rectifier_fft_pscad.md`
- repository-level `README.md`
- attached `pscad_component_catalog.csv`
- attached `pscad_component_catalog.json`

The animation does **not** import or run `mhi.pscad`. It is therefore
renderable on a computer that does not have PSCAD installed. PSCAD is the
subject of the explanation, not a runtime dependency of the Manim project.

---

## Project files

```text
pscad_manim_presentation/
|
|-- pscad_rectifier_presentation.py   # 26 Manim scenes
|-- pscad_visuals.py                  # reusable schematic/diagram helpers
|-- technical_analysis.md             # source-script technical analysis
|-- storyboard_and_narration.md       # storyboard + Brazilian Portuguese narration
|-- render_all.py                     # render all scenes and concatenate them
|-- requirements.txt
|-- manim.cfg
|-- README.md
|
`-- tests/
    `-- test_static.py
```

---

## Manim version

This project targets **Manim Community Edition 0.20.1**.

The validated local Manim installation accepts the standard command:

```powershell
manim [OPTIONS] FILE [SCENES]
```

and also supports the explicit form:

```powershell
manim render [OPTIONS] FILE [SCENE_NAMES]
```

The presentation uses the current `Code(code_string=..., language="python")`
API and does not rely on the deprecated foreground-color override behavior of
older `Code` versions.

---

## 1. Recommended environment on Windows

Use an isolated Python environment with `uv` or ordinary `venv`/`pip`. The revision was rendered with Python 3.13 and Manim 0.20.1.

### Option A — `uv`

Install `uv` if needed, then from this project folder:

```powershell
uv venv --python 3.12
uv pip install -r requirements.txt
```

Activate the environment if desired, or prefix commands with `uv run`.

Example:

```powershell
uv run manim -pql pscad_rectifier_presentation.py IntroScene
```

### Option B — standard Python virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify:

```powershell
python -m manim --version
```

Expected major target:

```text
Manim Community v0.20.1
```

---

## 2. LaTeX requirement

Several scenes use `MathTex`, including the FFT-interval, harmonic-order, and THD equations. A working LaTeX installation is therefore
required for the complete presentation.

On Windows, use a normal TeX distribution such as TeX Live or MiKTeX and make
sure its executables are available on `PATH`.

A useful check is:

```powershell
latex --version
```

If ordinary text scenes render but mathematical scenes fail, the LaTeX setup
is the first item to check.

---

## 3. FFmpeg

Manim requires FFmpeg for video creation. The helper `render_all.py` also uses
FFmpeg to concatenate the 26 rendered scene files into a single MP4.

Check:

```powershell
ffmpeg -version
```

---

## 4. Render one scene quickly

Low-quality preview:

```powershell
manim -pql pscad_rectifier_presentation.py IntroScene
```

Equivalent with the Python module entry point:

```powershell
python -m manim -pql pscad_rectifier_presentation.py IntroScene
```

Another useful test scene:

```powershell
manim -pql pscad_rectifier_presentation.py RectifierConstructionScene
```

FFT explanation:

```powershell
manim -pql pscad_rectifier_presentation.py FFTScene
```

---

## 5. Render Full HD

Manim high quality (`-qh`) is the optional Full-HD preset. The default preview is 480p at 15 fps.
It produces the 1080p/60-fps output directory used by `render_all.py`.

Render one scene:

```powershell
manim -pqh pscad_rectifier_presentation.py FullWorkflowScene
```

Without automatically opening the result:

```powershell
manim -qh pscad_rectifier_presentation.py FullWorkflowScene
```

---

## 6. Render every scene and create one complete video

Full HD:

```powershell
python render_all.py --quality h
```

This renders every scene in `SCENE_ORDER` and concatenates the videos into:

```text
pscad_python_automation_presentation.mp4
```

Fast preview version:

```powershell
python render_all.py --quality l --output pscad_preview.mp4
```

Quality values accepted by the helper:

```text
l -> 480p15
m -> 720p30
h -> 1080p60
p -> 1440p60
k -> 2160p60
```

---

## 7. Render multiple selected scenes

Manim accepts one or more scene names after the Python file. For example:

```powershell
manim -ql pscad_rectifier_presentation.py WorkspaceScene ComponentLibraryScene CreateComponentScene
```

They are rendered as separate scene videos. Use `render_all.py` when a single
concatenated presentation file is desired.

---

## 8. Scene order

The complete presentation contains 26 scenes:

```text
01  IntroScene
02  ManualVsAutomationScene
03  ArchitectureScene
04  ScriptOverviewScene
05  WorkspaceScene
06  ComponentLibraryScene
07  CreateComponentScene
08  CoordinateAndPortsScene
09  SourceCreationScene
10  RectifierConstructionScene
11  RectifierOperationScene
12  DCFilterScene
13  MeasurementsAndChannelsScene
14  SimulationSettingsScene
15  ExecutionScene
16  WaveformsScene
17  OutputReadingScene
18  FFTWindowScene
19  FFTScene
20  HarmonicsScene
21  THDScene
22  ResultsScene
23  FullWorkflowScene
24  GeneralizationScene
25  PortabilityScene
26  ConclusionScene
```

The list is also stored as `SCENE_ORDER` in
`pscad_rectifier_presentation.py`.

---

## 9. Important source-script facts represented in the animation

The presentation intentionally reflects the current GitHub example:

```text
PSCAD version              5.1.0 x64
source                     480 V line-line RMS
frequency                  60 Hz
source base                1 MVA
DC resistor                10 ohm
filter capacitor           2200 uF
simulation duration        0.60 s
solution time step         50 us
channel plot step          50 us
FFT analysis cycles        12
maximum harmonic order     25
Hann window                enabled
```

The animation also represents the exact Master Library identifiers used by the
script, including:

```text
master:source3
master:breakout
master:peswitch
master:resistor
master:capacitor
master:ground
master:ammeter
master:pgb
master:datalabel
```

---

## 10. Conceptual waveforms versus real PSCAD results

The public repository currently contains the automation script and
documentation, but not a complete exported numerical PSCAD result set from a
specific run. For this reason, the Manim scenes use deterministic **conceptual
waveforms** to explain:

- distorted phase current;
- six-pulse rectification;
- smoothing by the DC capacitor;
- FFT transformation;
- representative spectral components.

They are not presented as measured or simulated numerical results from the
current PSCAD case.

If real `rectifier_currents.csv` and harmonic result files are later added to
the repository, the project can be extended to read them and animate the
actual curves.

---

## 11. Why the presentation does not run PSCAD

The original automation requires `mhi.pscad`, a compatible PSCAD installation,
and a license with Python Automation support. A Manim educational video should
not depend on those requirements merely to render a diagram.

Therefore:

```text
original engineering script:
Python -> mhi.pscad -> PSCAD -> EMTDC -> output -> Python FFT

Manim presentation:
Python/Manim -> visual explanation of that chain
```

This separation also makes the presentation suitable for GitHub, classrooms,
and machines that only have the animation toolchain installed.

---

## 12. Portability discussion included in the presentation

The current PSCAD Python file contains a machine-specific absolute output path.
Its own README recommends changing it to:

```python
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "PSCAD_Project"
```

`PortabilityScene` explicitly teaches this distinction and also reminds the
viewer to check:

- PSCAD version;
- x64 setting;
- Python interpreter;
- availability of `mhi.pscad`;
- PSCAD license support for Automation Library.

---

## 13. Validate the generated project without Manim

The included static tests parse the Python sources with `ast`, verify all
expected scenes, and confirm that the animation has no `mhi.pscad` runtime
import.

Run:

```powershell
pytest -q
```

A Python syntax-only check is also possible:

```powershell
python -m py_compile pscad_visuals.py pscad_rectifier_presentation.py render_all.py
```

---

## 14. Recommended development workflow

For fast iteration:

```powershell
manim -pql pscad_rectifier_presentation.py SceneName
```

When the scene is visually correct:

```powershell
manim -pqh pscad_rectifier_presentation.py SceneName
```

Only after individual scenes are stable, render the complete video:

```powershell
python render_all.py --quality h
```

---

## 15. Suggested next improvements

A second version could add:

1. actual PSCAD screenshots used only as brief contextual references;
2. real `rectifier_currents.csv` data when a validated result set is published;
3. exact harmonic bars calculated from that result file;
4. synchronized recorded narration;
5. subtitles generated from `storyboard_and_narration.md`;
6. a side-by-side animation comparing the PSCAD schematic with its Python
   construction calls;
7. a detailed animation of `DN`/`DP`, `N1`/`N2`/`N3`, and signal-port types;
8. a final parameter-sweep example demonstrating how the automation pattern
   grows beyond a single simulation.

---

## Engineering disclaimer

This presentation explains the operation of an automation example. Conceptual
waveforms in the animation are pedagogical and must not be interpreted as
validated equipment-design results. Engineering decisions should be based on
independently validated PSCAD cases and numerical outputs.


## Document revision 2026-09-07

The requests in `sugestoes-para-manim.docx` are tracked in `docs/CHANGE_PLAN.md`.
Visible animation text is now English. The opening/closing repository credits and
HannWindowScene were removed; the numerical script still uses its original Hann
window setting. Source attribution remains in this README. No PSCAD simulation
inputs or calculations were changed.

Revised layouts separate workspace branches, library cards and the creation
example, source parameters and waveforms, and the THD annotation and equation.
Portability examples are stacked vertically. Code uses Consolas with wrapped
lines. Offline vector icons replace crowded workflow miniatures. Radial arrows
connect box boundaries. The final heading uses two lines.

Render the complete revised presentation:

```powershell
python render_all.py --quality l --output pscad_document_revision_480p.mp4
python -m pytest -q
```

The helper defaults to low quality (480p, 15 fps), uses its own project directory,
and includes only the 26 retained scenes. The MP4 has no narration audio; the
storyboard narration is a separate Portuguese aid.

See `docs/PSCAD_SCREENSHOT_MAP.md` for exact source locations and instructions for
replacing the four requested drawings with PSCAD screenshots. See
`docs/CODEX_HANDOFF.md` for the current validation and resume checkpoint.
Original source backups and extracted document images are in
`docs/source_review/`; pytest is restricted to `tests/` to exclude these backups.

Validated revision output: `pscad_document_revision_480p.mp4`, 26 scenes, 146.599674 seconds, 2199 frames, 854 x 480 at 15 fps. Four static tests passed and full FFmpeg decoding succeeded. Media metadata is saved in `docs/source_review/video_validation.json`.


## DC component alignment correction

2026-09-07: dc_parallel_load in pscad_visuals.py now positions unlabeled capacitor/resistor geometry before adding external labels. Wires use actual terminal coordinates; Idc remains horizontal. DCFilterScene re-rendered at 480p15, final frame inspected, full presentation re-concatenated and verified with verify_revision.py. Four static tests passed. Preview: docs/source_review/dc_alignment.png.
