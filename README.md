# PSCAD Python Automation and Electromagnetic Transient Simulation Examples

A collection of Python-based automation examples for **PSCAD** focused on power-system studies, power electronics, electromagnetic transients, measurements, post-processing, FFT analysis, harmonic studies, and other engineering simulations.

Each simulation is intended to be self-contained and documented with its own `README.md`, so individual examples can be understood, executed, modified, and reused independently.

---

# Running This Repository on Another Computer

This section is intentionally placed near the beginning because portability is a primary goal of the repository.

## 1. Use portable paths

Avoid hard-coded paths that contain a specific Windows username or local project directory, for example:

```python
OUTPUT_DIR = Path(
    r"C:\Users\username\PycharmProjects\project\PSCAD_Project"
)
```

Prefer paths relative to the Python file:

```python
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = (
    SCRIPT_DIR
    / "PSCAD_Project"
)
```

This allows the repository to be cloned into almost any folder without editing machine-specific paths.

## 2. Check the PSCAD version used by each script

A script may contain configuration such as:

```python
PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True
```

If the target computer uses a different PSCAD version, update the version string accordingly.

If the PSCAD installation is 64-bit, keep:

```python
PSCAD_X64 = True
```

Each example-specific `README.md` should state the PSCAD version used during validation.

## 3. Check the Python interpreter

The Python interpreter used to run the scripts must be able to import the PSCAD Automation Library and the additional scientific packages required by the example.

A quick check is:

```powershell
python -c "import sys; print(sys.executable)"
```

For a typical example:

```powershell
python -c "import mhi.pscad; import numpy; import matplotlib; print('Environment OK')"
```

If required:

```powershell
python -m pip install numpy matplotlib
```

The PSCAD Automation Library must also be installed and accessible to the selected Python environment.

## 4. Run an example

Enter the directory of the desired simulation and execute its Python script.

Example:

```powershell
cd 01_three_phase_diode_rectifier
python three_phase_rectifier_fft_pscad.py
```

Some examples create their own PSCAD workspace and case automatically, while others may load existing PSCAD files.

Always check the example-specific `README.md`.

---

# PSCAD License Requirement

These examples require a PSCAD edition that supports the **Python Automation Library**.

The PSCAD **Free Edition does not support the Python Automation UI/Library**, so the automation scripts in this repository are not expected to run with the Free Edition.

In practice:

| PSCAD edition / license | Python Automation |
|---|---|
| Professional | Supported |
| Educational | Supported |
| Evaluation / Trial of a full-featured edition | Expected to work when Automation Library access is enabled |
| Free Edition | Not supported |

The exact capabilities available to a user may depend on the installed PSCAD version and license configuration.

Even when a model itself is small enough to fit within Free Edition model-size limits, the Python automation layer remains the relevant restriction for these scripts.

---

# Repository Purpose

The objective of this repository is to provide practical examples of automating PSCAD studies with Python.

Possible study categories include:

- power-electronic converters;
- diode and thyristor rectifiers;
- harmonic filters;
- FFT and harmonic analysis;
- synchronous machines;
- transformer energization;
- inrush current;
- transmission lines;
- cables;
- short-circuit studies;
- switching transients;
- TRV studies;
- capacitor banks;
- reactive compensation;
- electromagnetic transient simulations;
- automated measurements;
- automated graph creation;
- batch simulations;
- parameter sweeps;
- result extraction;
- CSV export;
- engineering post-processing in Python.

The repository is intended to grow over time as additional PSCAD automation examples are added.

---

# Recommended Repository Structure

A suggested organization is:

```text
pscad-python-automation-and-electromagnetic-transient-simulation-examples/
|
|-- README.md
|-- .gitignore
|
|-- 01_three_phase_diode_rectifier/
|   |-- README.md
|   |-- three_phase_rectifier_fft_pscad.py
|   `-- PSCAD_Project/
|
|-- 02_synchronous_machine/
|   |-- README.md
|   `-- ...
|
|-- 03_harmonic_filter/
|   |-- README.md
|   `-- ...
|
|-- 04_transmission_line/
|   |-- README.md
|   `-- ...
|
`-- 05_other_study/
    |-- README.md
    `-- ...
```

Each simulation should ideally have its own directory.

This avoids mixing:

- Python scripts;
- PSCAD cases;
- simulation results;
- figures;
- CSV files;
- documentation;
- temporary build files.

---

# Example-Specific README Files

Each example should contain its own `README.md` describing:

1. the purpose of the simulation;
2. the electrical model;
3. PSCAD version used;
4. Python dependencies;
5. main component definitions;
6. important parameters;
7. how to execute the script;
8. generated files;
9. expected results;
10. known limitations;
11. troubleshooting notes.

This top-level README describes the repository as a whole, while the individual READMEs document each simulation in detail.

---

# Typical Python Dependencies

The exact dependencies vary between examples.

Common packages may include:

```text
mhi.pscad
numpy
matplotlib
```

Other examples may also use:

```text
pandas
scipy
```

A future `requirements.txt` may be added for examples whose dependencies are fully installable with `pip`.

Note that `mhi.pscad` is associated with the PSCAD Automation Library and should be configured according to the PSCAD installation.

---

# Typical PSCAD Launch Pattern

Many examples use:

```python
import mhi.pscad

pscad = mhi.pscad.launch(
    version=PSCAD_VERSION,
    x64=True,
    minimize=False,
)
```

A common configuration block is:

```python
PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True
```

Keeping the PSCAD version in a clearly visible configuration section makes the scripts easier to adapt to another computer.

---

# Portable Project Folders

For examples that create files dynamically, the recommended pattern is:

```python
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = (
    SCRIPT_DIR
    / "PSCAD_Project"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
```

This avoids paths such as:

```text
C:\Users\specific_user\...
```

and makes GitHub clones much easier to run.

---

# PSCAD Master Library Components

Many examples rely on PSCAD Master Library definitions.

Typical examples include:

```python
SOURCE_DEFINITION = "master:source3"
BREAKOUT_DEFINITION = "master:breakout"
RESISTOR_DEFINITION = "master:resistor"
CAPACITOR_DEFINITION = "master:capacitor"
GROUND_DEFINITION = "master:ground"
AMMETER_DEFINITION = "master:ammeter"
OUTPUT_CHANNEL_DEFINITION = "master:pgb"
```

Not every example uses the same components.

Whenever possible, scripts should avoid inventing internal component or parameter names and should inspect the installed PSCAD Master Library when uncertainty exists.

Useful Automation Library methods may include:

```python
master.definitions()
component.parameters()
component.range()
component.ports()
```

---

# Generated Files

Different examples may produce:

```text
*.pswx
*.pscx
*.out
*.inf
*.csv
*.png
*.txt
```

Some examples may also generate other engineering reports or plots.

Generated simulation results should generally be separated from source code.

---

# Suggested `.gitignore`

A useful starting point is:

```gitignore
# Python
__pycache__/
*.pyc
.venv/
venv/

# IDE
.idea/
.vscode/

# PSCAD temporary/compiler directories
*.gf*/
*.if*/
*.x86/
*.x64/

# Temporary files
*.tmp
*.bak

# Generated results
**/PSCAD_Project/*.csv
**/PSCAD_Project/*.png
**/PSCAD_Project/*.txt
```

You may decide separately whether to version-control:

```text
*.pswx
*.pscx
```

Keeping PSCAD project files in Git can be useful when the repository is intended to provide ready-to-open examples.

---

# General Troubleshooting

## `ModuleNotFoundError: No module named 'mhi.pscad'`

The active Python interpreter cannot access the PSCAD Automation Library.

Check:

```powershell
python -c "import sys; print(sys.executable)"
```

Then test:

```powershell
python -c "import mhi.pscad; print('mhi.pscad OK')"
```

## PSCAD does not launch

Verify the script configuration:

```python
PSCAD_VERSION = "5.1.0"
PSCAD_X64 = True
```

These values must match the installation being used.

## NumPy or Matplotlib is missing

Install with:

```powershell
python -m pip install numpy matplotlib
```

## Script works on one computer but not another

Check, in this order:

1. PSCAD version;
2. PSCAD license type;
3. Python interpreter path;
4. availability of `mhi.pscad`;
5. installed Python packages;
6. hard-coded file paths;
7. compiler availability required by the PSCAD installation;
8. permissions for the output directory.

## PSCAD Free Edition

The Free Edition does not provide Python Automation UI/Library support.

If a script depends on `mhi.pscad`, use a PSCAD edition/license that includes Automation Library access.

---

# Version Compatibility

The examples in this repository may be developed using different PSCAD releases.

An example validated with:

```text
PSCAD 5.1.0 x64
```

may require small modifications when used with another release.

Potential differences include:

- Master Library definition names;
- component parameters;
- Automation Library methods;
- project runtime parameters;
- output-file handling;
- graph APIs;
- compiler configuration.

Always check the individual example README.

---

# Engineering Validation

These scripts automate model creation and result processing, but automation does not replace engineering validation.

Before using results in professional studies, independently verify:

- electrical parameters;
- units;
- source definitions;
- machine and transformer data;
- component orientation;
- network connections;
- simulation time step;
- initialization;
- steady-state conditions;
- FFT window;
- harmonic calculations;
- measurement scaling;
- result interpretation.

---

# Contribution Guidelines

Contributions are welcome.

When adding a new example, preferably:

1. create a dedicated folder;
2. include one main Python script;
3. add a dedicated `README.md`;
4. avoid machine-specific absolute paths;
5. document the PSCAD version;
6. document required Python packages;
7. explain the electrical model;
8. include important simulation parameters;
9. add troubleshooting notes;
10. avoid committing unnecessary PSCAD build directories.

---

# Naming Convention

A simple folder naming convention is:

```text
01_three_phase_diode_rectifier
02_synchronous_machine
03_harmonic_filter
04_transmission_line
05_transformer_inrush
```

Python scripts can use descriptive names such as:

```text
three_phase_rectifier_fft_pscad.py
synchronous_machine_startup_pscad.py
harmonic_filter_frequency_scan_pscad.py
transformer_inrush_pscad.py
```

---

# Intended Audience

This repository may be useful for:

- electrical engineers;
- power-system engineers;
- electromagnetic-transient specialists;
- PSCAD users;
- researchers;
- university professors;
- engineering students;
- developers working with simulation automation.

---

# Disclaimer

This repository is intended for:

- engineering study;
- research;
- education;
- automation development;
- PSCAD scripting examples.

Simulation results should be independently checked before being used for equipment ratings, protection settings, system design, compliance studies, contractual studies, or other engineering decisions.

---

# License

No software license is assumed by this README.

Before publishing the repository publicly, add an appropriate open-source license if desired, for example:

```text
MIT License
BSD-3-Clause
Apache-2.0
```

Choose the license according to how you want others to use, modify, and redistribute the code.


## Animated Manim presentation

An English-language presentation explains the rectifier automation and harmonic analysis workflow in 26 scenes. It renders independently of PSCAD using conceptual waveforms.

- [Installation, rendering and validation](README-manim.md)
- [Complete preview video, 480p at 15 fps](pscad_document_revision_480p.mp4)
- [PSCAD screenshot replacement guide](docs/PSCAD_SCREENSHOT_MAP.md)
- [Project continuity and validation](docs/CODEX_HANDOFF.md)

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python render_all.py --quality l --output pscad_document_revision_480p.mp4
```

The preview is silent, lasts 146.6 seconds, and is an educational visualization rather than a PSCAD numerical validation.
