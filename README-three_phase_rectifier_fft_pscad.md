# Three-Phase Rectifier Automation for PSCAD

Python automation script for **PSCAD 5.1.0 x64** that builds, simulates, and post-processes a three-phase six-pulse diode rectifier with a DC capacitor filter.

The script automatically creates the PSCAD schematic, measures the phase and DC currents, runs the EMTDC simulation, exports results, calculates the FFT of the Phase-A current, extracts harmonic components up to the 25th order, and calculates current THD.

---

# Running on Another Computer

This is the most important section if you clone or download this project from GitHub.

## 1. Use portable paths

Do **not** keep a machine-specific path such as:

```python
OUTPUT_DIR = Path(
    r"C:\Users\z005b93y\PycharmProjects\pscad-test-1\PSCAD_Project"
)
```

Use a path relative to the Python script:

```python
SCRIPT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = (
    SCRIPT_DIR
    / "PSCAD_Project"
)
```

This makes the project independent of the Windows username and of the folder where the repository is cloned.

Recommended structure:

```text
three-phase-rectifier-pscad/
|
|-- three_phase_rectifier_fft_pscad.py
|-- README.md
|
`-- PSCAD_Project/
    |-- ThreePhaseRectifier.pswx
    |-- ThreePhaseRectifier.pscx
    |-- rectifier_currents.csv
    |-- phase_a_fft_spectrum.png
    |-- phase_a_harmonics.png
    |-- phase_a_harmonics.csv
    `-- phase_a_harmonic_summary.txt
```

The `PSCAD_Project` directory is created automatically by the script.

## 2. Check the PSCAD version

The current script uses:

```python
PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True
```

If the other computer also has **PSCAD 5.1.0 x64**, no change is needed.

If another version is installed, change:

```python
PSCAD_VERSION = "5.1.0"
```

to the installed version.

## 3. Check the Python environment

The Python interpreter must be able to import:

```text
mhi.pscad
numpy
matplotlib
```

Test with:

```powershell
python -c "import mhi.pscad; import numpy; import matplotlib; print('Environment OK')"
```

If necessary, install NumPy and Matplotlib with:

```powershell
python -m pip install numpy matplotlib
```

The PSCAD Automation Library must also be installed and accessible to the Python interpreter being used.

## 4. Confirm that PSCAD launches correctly

The script uses:

```python
pscad = mhi.pscad.launch(
    version=PSCAD_VERSION,
    x64=PSCAD_X64,
    minimize=False,
)
```

If PSCAD does not launch, verify:

- the installed PSCAD version;
- whether the installation is 64-bit;
- whether `mhi.pscad` is available in the active Python environment;
- whether the intended Python interpreter is actually being used.

Check the interpreter with:

```powershell
python -c "import sys; print(sys.executable)"
```

## 5. Run the script

From PowerShell or Command Prompt:

```powershell
python three_phase_rectifier_fft_pscad.py
```

---

# Main Features

The script automatically:

1. launches PSCAD;
2. loads or creates the workspace and project;
3. clears the previous schematic;
4. creates a three-phase voltage source;
5. creates a six-pulse diode bridge;
6. measures `Ia`, `Ib`, `Ic` and `Idc`;
7. creates a parallel DC capacitor and resistor;
8. places `C_FILTER` to the left of `R_LOAD`;
9. aligns the source ground horizontally with the source;
10. creates PSCAD Output Channels;
11. sets **Use Signal Name as Title? = YES**;
12. creates PSCAD time-domain graphs;
13. runs the simulation;
14. exports PSCAD output data;
15. reads the Phase-A current;
16. calculates its FFT;
17. extracts harmonic components up to the 25th order;
18. calculates current THD;
19. saves tables and plots automatically.

---

# Electrical Model

Default values:

| Parameter | Default value |
|---|---:|
| Source voltage | 480 V line-line RMS |
| Fundamental frequency | 60 Hz |
| DC load resistance | 10 ohm |
| Filter capacitance | 2200 uF |
| Rectifier | Three-phase six-pulse diode bridge |

DC-side arrangement:

```text
                 +Vdc
                   |
            +------+------+
            |             |
        C_FILTER         Idc
            |             |
            |           R_LOAD
            |             |
            +------+------+
                   |
                 -Vdc
```

The capacitor is intentionally placed to the **left** of the resistor.

---

# PSCAD Master Library Components

The current implementation uses:

```python
SOURCE_DEFINITION = "master:source3"
BREAKOUT_DEFINITION = "master:breakout"

DIODE_DEFINITION = "master:peswitch"

RESISTOR_DEFINITION = "master:resistor"
CAPACITOR_DEFINITION = "master:capacitor"

GROUND_DEFINITION = "master:ground"

AMMETER_DEFINITION = "master:ammeter"

OUTPUT_CHANNEL_DEFINITION = "master:pgb"
DATA_LABEL_DEFINITION = "master:datalabel"
```

The semiconductor switches are configured as diodes with:

```python
Type="DIODE"
```

---

# Output Channels

The recorded signals are:

```text
Ia
Ib
Ic
Idc
```

To avoid the generic label `Value`, the Output Channels use:

```python
UseSignalName="YES"
```

The current implementation also scales the current channels to amperes.

---

# Simulation Settings

Default runtime configuration:

```python
SIMULATION_DURATION_S = 0.60

SOLUTION_TIME_STEP_US = 50.0
CHANNEL_PLOT_STEP_US = 50.0
```

The 0.60 s simulation time helps the capacitor charging transient decay before the FFT window is selected.

---

# FFT and Harmonic Analysis

The fundamental frequency is:

```python
FUNDAMENTAL_FREQUENCY_HZ = 60.0
```

The maximum analyzed order is:

```python
MAX_HARMONIC_ORDER = 25
```

Therefore:

```text
25 x 60 Hz = 1500 Hz
```

The FFT processing:

- uses the final steady-state cycles of `Ia`;
- removes the DC component;
- applies a Hann window when enabled;
- calculates a one-sided FFT;
- converts the spectral magnitude to RMS current;
- extracts integer harmonic orders;
- calculates each harmonic as a percentage of the fundamental;
- calculates Phase-A current THD.

The default FFT window uses:

```python
FFT_ANALYSIS_CYCLES = 12
```

At 60 Hz, this corresponds to approximately 0.2 s.

---

# Generated Files

After a successful run:

```text
PSCAD_Project/
|
|-- ThreePhaseRectifier.pswx
|-- ThreePhaseRectifier.pscx
|-- rectifier_currents.csv
|-- phase_a_fft_spectrum.png
|-- phase_a_harmonics.png
|-- phase_a_harmonics.csv
`-- phase_a_harmonic_summary.txt
```

## `rectifier_currents.csv`

Contains the exported time-domain channels:

```text
TIME
Ia
Ib
Ic
Idc
```

## `phase_a_fft_spectrum.png`

Frequency-domain spectrum of the Phase-A current.

## `phase_a_harmonics.png`

Bar chart of harmonic components by order.

## `phase_a_harmonics.csv`

Contains:

```text
Harmonic Order
Frequency [Hz]
Current RMS [A]
Percent of Fundamental [%]
```

## `phase_a_harmonic_summary.txt`

Contains the fundamental current and THD summary.

---

# Main Parameters to Modify

## PSCAD

```python
PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True
```

## Source

```python
SOURCE_VLL_KV = 0.480
SOURCE_FREQUENCY_HZ = 60.0
SOURCE_BASE_MVA = 1.0
```

## DC Load

```python
LOAD_RESISTANCE_OHM = 10.0
FILTER_CAPACITANCE_UF = 2200.0
```

## Simulation

```python
SIMULATION_DURATION_S = 0.60
SOLUTION_TIME_STEP_US = 50.0
CHANNEL_PLOT_STEP_US = 50.0
```

## Harmonic Analysis

```python
FUNDAMENTAL_FREQUENCY_HZ = 60.0
MAX_HARMONIC_ORDER = 25
FFT_ANALYSIS_CYCLES = 12
USE_HANN_WINDOW = True
```

---

# Recommended Portable Path Configuration

For GitHub, use:

```python
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = (
    SCRIPT_DIR
    / "PSCAD_Project"
)
```

Avoid committing machine-specific information such as:

- Windows usernames;
- absolute local paths;
- company-specific folders;
- temporary build directories;
- IDE-specific local configuration.

---

# Suggested `.gitignore`

```gitignore
# Python
__pycache__/
*.pyc
.venv/
venv/

# IDE
.idea/
.vscode/

# PSCAD temporary/compiler folders
*.gf*/
*.if*/
*.x86/
*.x64/

# Generated numerical results
PSCAD_Project/*.csv
PSCAD_Project/*.png
PSCAD_Project/*.txt

# Optional:
# Uncomment if you do not want to version generated PSCAD files.
# PSCAD_Project/*.pswx
# PSCAD_Project/*.pscx
```

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'mhi.pscad'`

The active Python interpreter cannot access the PSCAD Automation Library.

Check:

```powershell
python -c "import sys; print(sys.executable)"
python -c "import mhi.pscad; print('mhi.pscad OK')"
```

## PSCAD does not launch

Check:

```python
PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True
```

These must match the installed PSCAD version and architecture.

## `OSError: Already open`

When using `OutFile`, close it before calling `toCSV()`.

Correct pattern:

```python
output.open()

try:
    columns = output.columns()
finally:
    output.close()

output.toCSV(
    str(PSCAD_CSV_FILE)
)
```

`toCSV()` opens the output file internally.

## Graphs show `Value` instead of signal names

Ensure:

```python
UseSignalName="YES"
```

is configured on the Output Channels.

## FFT results look incorrect

Check:

- whether the system has reached steady state;
- whether the capacitor charging transient has decayed;
- whether enough cycles are used in the FFT window;
- whether the time step is sufficiently small;
- whether `Ia` is the signal actually being analyzed.

If necessary, increase:

```python
SIMULATION_DURATION_S
```

---

# Initial Validation Environment

The script was initially developed and tested with:

```text
PSCAD 5.1.0 x64
Python 3.11
NumPy
Matplotlib
PSCAD Automation Library
```

---

# GitHub Checklist

Before publishing:

1. replace fixed absolute paths with the portable `SCRIPT_DIR` configuration;
2. remove personal or corporate paths;
3. include a `.gitignore`;
4. decide whether `.pswx` and `.pscx` should be version-controlled;
5. include representative result images if useful;
6. state which PSCAD version was used for validation.

Suggested repository structure:

```text
three-phase-rectifier-pscad/
|
|-- README.md
|-- .gitignore
|-- three_phase_rectifier_fft_pscad.py
|
|-- docs/
|   `-- images/
|
`-- PSCAD_Project/
```

---

# Disclaimer

This project is intended for engineering study, automation development, and educational use.

Simulation results should be independently checked before being used for equipment ratings, protection settings, design decisions, compliance studies, or other engineering decisions.
