# Technical Analysis — PSCAD Python Automation Example

## Source basis

This analysis is based on the public repository:

`angelohafner/pscad-python-automation-and-electromagnetic-transient-simulation-examples`

Primary script:

`three_phase_rectifier_fft_pscad.py`

Supporting documentation:

- `README-three_phase_rectifier_fft_pscad.md`
- repository-level `README.md`
- attached `pscad_component_catalog.csv`
- attached `pscad_component_catalog.json`

The attached catalog identifies PSCAD 5.1.0 and contains 426 component definitions. The CSV and JSON contain the same component-level fields: project, project type, definition, scoped name, description, group, tags, URL, and module status.

---

## 1. What the script actually does

The script is a complete automation chain rather than only a model builder. Its responsibilities are:

1. launch PSCAD 5.1.0 x64;
2. load an existing workspace or create a new workspace and case;
3. configure simulation/output parameters;
4. access and clear the `Main` canvas;
5. instantiate PSCAD Master Library definitions;
6. inspect ports and component geometry;
7. rotate two-terminal components when required;
8. connect components with PSCAD wires;
9. construct a three-phase six-pulse diode rectifier;
10. create a parallel capacitor/resistor DC load;
11. create current measurements and output channels;
12. create PSCAD time-domain graphs;
13. save and run the PSCAD case;
14. locate generated PSCAD INF/OUT files;
15. convert PSCAD output to CSV with `OutFile`;
16. read time and Phase-A current into NumPy arrays;
17. select the final steady-state FFT window;
18. remove DC, optionally apply a Hann window, and compute a one-sided FFT;
19. scale the FFT to RMS magnitude;
20. extract the 1st through 25th harmonics;
21. calculate THD from the 2nd through 25th harmonics;
22. save tables, figures, and a text summary.

The core conceptual split is therefore:

**Python automation → PSCAD EMT simulation → Python post-processing**.

---

## 2. Main configuration values

| Category | Parameter | Value in the current script | Meaning |
|---|---|---:|---|
| PSCAD | `PSCAD_VERSION` | `5.1.0` | PSCAD release requested by `mhi.pscad.launch()` |
| PSCAD | `PSCAD_X64` | `True` | 64-bit PSCAD instance |
| Source | `SOURCE_VLL_KV` | `0.480` | 480 V line-line RMS |
| Source | `SOURCE_FREQUENCY_HZ` | `60.0` | source frequency |
| Source | `SOURCE_BASE_MVA` | `1.0` | source base power parameter |
| DC load | `LOAD_RESISTANCE_OHM` | `10.0` | load resistance |
| DC filter | `FILTER_CAPACITANCE_UF` | `2200.0` | PSCAD capacitor value in microfarads |
| Simulation | `SIMULATION_DURATION_S` | `0.60` | total simulated time |
| Simulation | `SOLUTION_TIME_STEP_US` | `50.0` | EMT solution time step |
| Output | `CHANNEL_PLOT_STEP_US` | `50.0` | output/plot sampling step |
| FFT | `FUNDAMENTAL_FREQUENCY_HZ` | `60.0` | harmonic reference frequency |
| FFT | `MAX_HARMONIC_ORDER` | `25` | last integer harmonic extracted |
| FFT | `FFT_ANALYSIS_CYCLES` | `12` | final cycles used for FFT |
| FFT | `USE_HANN_WINDOW` | `True` | enables Hann window |

At 60 Hz, 12 cycles correspond to 0.2 s. The script therefore uses approximately the interval 0.4–0.6 s when the full 0.60 s run is available.

---

## 3. PSCAD Master Library definitions used

| Script constant | Scoped definition | Catalog description | Catalog group | How the script uses it |
|---|---|---|---|---|
| `SOURCE_DEFINITION` | `master:source3` | Three Phase Voltage Source Model 1 | Sources | three-phase source |
| `BREAKOUT_DEFINITION` | `master:breakout` | 3 Phase to SLD Electrical Wire Converter | Passive | separates/handles phase conductors |
| `DIODE_DEFINITION` | `master:peswitch` | Power electronic switch | HVDC FACTS PE | instantiated with `Type="DIODE"` |
| `RESISTOR_DEFINITION` | `master:resistor` | Resistor | Passive | DC load resistor |
| `CAPACITOR_DEFINITION` | `master:capacitor` | Capacitor | Passive | DC smoothing capacitor |
| `GROUND_DEFINITION` | `master:ground` | Ground Symbol | Passive / Sources / Breakers Faults / HVDC FACTS PE | source-neutral ground |
| `AMMETER_DEFINITION` | `master:ammeter` | Current Meter | Meters | Ia, Ib, Ic and Idc |
| `OUTPUT_CHANNEL_DEFINITION` | `master:pgb` | Output Channel | I/O Devices | records signals to PSCAD output |
| `DATA_LABEL_DEFINITION` | `master:datalabel` | Data signal label | Meters / Breakers Faults / Machines / Miscellaneous | connects named signals to output channels |

Important distinction for the animation:

`master:capacitor` is a **library definition identifier**. It becomes a placed schematic instance only after a call such as `canvas.create_component(...)`.

---

## 4. Function-by-function mapping

| Stage | Python function / code | Action in PSCAD | Electrical / computational meaning | Proposed Manim action |
|---|---|---|---|---|
| Launch | `launch_pscad()` | calls `mhi.pscad.launch(version=..., x64=...)` | starts the PSCAD application controlled by Python | Python block sends command to PSCAD block |
| Workspace | `create_or_load_project()` | loads `.pswx` or creates workspace and case | creates the simulation container | decision flow: exists? load / create |
| Runtime | `configure_project()` | sets duration, time step, sample step, OUT filename | controls EMT integration and data sampling | animated time line with Δt |
| Canvas | `get_main_canvas()` | opens `Main` canvas | accesses schematic drawing area | PSCAD project → Main Canvas |
| Cleanup | `clear_canvas()` | deletes graph frames and components | guarantees a deterministic rebuild | previous circuit fades away |
| Generic creation | `create_component()` | `canvas.create_component(definition, x, y, ...)` | converts a Master Library definition into a placed instance | library card → component at coordinate |
| Port inspection | `get_ports()`, `resolved_port()`, `port_xy()` | queries component ports | obtains real connection coordinates | terminal dots appear with `(x,y)` |
| Electrical-port test | `electrical_ports()` | filters type 3 ports | distinguishes electrical terminals from signal ports | electrical ports highlighted |
| Orientation | `ensure_horizontal()`, `ensure_vertical()` | may call `canvas.rotate_right()` | aligns two-terminal components before wiring | symbol rotates until ports line up |
| Wires | `create_wire()` | calls `canvas.create_wire(*points)` | creates PSCAD electrical/signal interconnections | line grows from port to port |
| Source | `create_source()` | creates `master:source3`, sets source parameters | 480 V L-L RMS, 60 Hz three-phase supply | source appears; three phase waves animate |
| Source ground | `create_and_connect_ground()` | creates/mirrors/repositions ground and wires neutral | grounds the source neutral | ground symbol flips and snaps into place |
| Diode | `create_diode()` | creates `master:peswitch` with `Type="DIODE"` | power-electronic switch becomes a diode | generic library switch becomes diode |
| Bridge | `create_bridge()` | creates D1, D3, D5 / D2, D4, D6; creates DC buses and AC phase nodes | six-pulse Graetz bridge | six diodes appear, then buses and phase nodes |
| AC measurements | `connect_ac_side()` | creates Ia/Ib/Ic ammeters and connects source → breakout → bridge | measures phase currents | meters inserted into each phase |
| DC load | `create_dc_load()` | creates capacitor left branch and Idc + resistor right branch | parallel C-R DC load | C_FILTER left, R_LOAD right; parallel buses close |
| Data label | `create_data_label()` | creates named signal label | makes a named signal accessible | tag leaves meter and enters output chain |
| Output channel | `configure_output_channel()` | sets signal title, scale 1000, units A when supported | avoids generic `Value`, converts kA to A | label → Output Channel → A |
| Channel creation | `create_output_channel(s)` | wires Data Labels to `master:pgb` | records Ia, Ib, Ic, Idc | four signal pipelines appear |
| Graphs | `create_pscad_graphs()` | creates phase-current and DC-current graphs | visual monitoring in PSCAD | waveforms emerge in graph frames |
| Save | `save_project()` | saves case/workspace | persists generated model | disk icon / PSCAD files |
| Run | `run_simulation()` | calls `project.run()` and checks messages | PSCAD/EMTDC performs the numerical simulation | progress bar on PSCAD solver |
| Locate output | `find_pscad_output_basename()` | scans `project.temp_folder` for `.inf` | identifies generated result set | search animation in temp folder |
| OUT → CSV | `convert_output_to_csv()` | uses `OutFile`, then `toCSV()` | converts PSCAD channel data into tabular form | `.out` → `OutFile` → `.csv` |
| Read Ia | `read_phase_a_current()` | no PSCAD action | reads TIME and Ia into NumPy arrays | CSV columns turn into two arrays |
| FFT window | `calculate_fft()` | no PSCAD action | chooses final 12 cycles, removes mean | final 0.2 s region is highlighted |
| Window | `np.hanning()` | no PSCAD action | reduces truncation discontinuities | Hann envelope multiplies signal |
| FFT | `np.fft.rfft()` | no PSCAD action | computes one-sided DFT efficiently | time waveform transforms into spectrum |
| Frequency grid | `np.fft.rfftfreq()` | no PSCAD action | associates FFT bins with frequency | x-axis labels appear |
| RMS scaling | coherent-gain formula in `calculate_fft()` | no PSCAD action | converts windowed FFT magnitudes to RMS | formula builds step-by-step |
| Harmonics | `extract_harmonics()` | no PSCAD action | picks nearest bin to `h f1`, h=1…25 | spectral lines selected one-by-one |
| THD | `extract_harmonics()` | no PSCAD action | RMS ratio of harmonics 2…25 to fundamental | squares → sum → root → divide by I1 |
| Save data | `save_harmonic_results()` | no PSCAD action | creates harmonic CSV and text summary | output files enter project folder |
| Plots | `create_fft_spectrum_plot()`, `create_harmonic_bar_plot()` | no PSCAD action | Matplotlib exports spectrum and harmonic bar chart | figures appear as generated assets |
| Finish | `print_final_summary()` | no PSCAD action | reports parameters, fundamental, THD, files | final engineering pipeline closes |

---

## 5. Electrical topology of the generated model

The automated schematic contains:

- a three-phase voltage source;
- a breakout component;
- three series phase-current meters;
- a six-pulse diode bridge;
- a positive and a negative DC bus;
- a capacitor connected across the DC buses;
- a resistor branch connected across the same DC buses;
- an Idc meter in series with the resistor branch;
- source-neutral grounding;
- signal labels and PSCAD output channels.

The script intentionally places `C_FILTER` to the **left** of `R_LOAD`.

The bridge is built in the following naming pattern:

- upper row: D1, D3, D5;
- lower row: D2, D4, D6.

The script reads diode ports `DN` and `DP`, then builds the DC buses and the three AC phase nodes from those actual coordinates.

---

## 6. FFT implementation details

### Sample interval and sample rate

The script calculates:

`dt = median(diff(time_array))`

and then:

`sampling_frequency = 1 / dt`

This is robust to tiny floating-point variations in exported time values.

### Window length

The requested duration is:

`FFT_ANALYSIS_CYCLES / FUNDAMENTAL_FREQUENCY_HZ`

which is:

`12 / 60 = 0.2 s`

The corresponding sample count is rounded from duration divided by `dt`, then clipped to the available number of samples.

### Mean removal

The selected current segment is copied and its arithmetic mean is subtracted. This explicitly removes the DC component before the FFT.

### Window selection

When `USE_HANN_WINDOW = True`, the code uses `np.hanning(sample_count)`; otherwise it uses a rectangular window of ones.

### One-sided FFT

The script uses:

- `np.fft.rfft(windowed_current)`;
- `np.fft.rfftfreq(sample_count, d=dt)`.

Because the input is real, `rfft` returns the non-negative-frequency half of the DFT.

### RMS scaling

The implemented scale is:

`2 / sum(window) / sqrt(2)`

so the one-sided FFT magnitude is corrected for coherent gain and converted from peak amplitude to RMS magnitude.

### Harmonic extraction

For each integer order from 1 to 25:

1. calculate `target_frequency = order * 60`;
2. find the frequency bin with minimum absolute frequency error;
3. record the corresponding RMS spectrum value;
4. express it as a percentage of the fundamental.

### THD

The implementation sums the squared ratios of harmonics 2 through 25:

`THD = 100 * sqrt(sum((Ih/I1)^2))`

The 1st harmonic is therefore the denominator only; it is not included in the distortion sum.

---

## 7. Important accuracy notes for the animation

1. The presentation must not imply that Python numerically solves the EMT model. `project.run()` delegates the actual network solution to PSCAD/EMTDC.
2. `master:*` strings are library definitions, not visual instances.
3. Component placement is not enough: the script actively inspects ports and corrects orientation before making connections.
4. `master:peswitch` is a generic power-electronic switch definition; the script configures each instance with `Type="DIODE"`.
5. The Output Channel code conditionally sets `UseSignalName`, `Scale`, and `Units` only when those parameters exist.
6. `OutFile.toCSV()` opens the data internally, so the script deliberately closes the manually opened `OutFile` before calling `toCSV()`.
7. The animation uses conceptual/synthetic waveforms because the public repository does not contain the numerical PSCAD result files used to derive exact harmonic magnitudes.
8. The theoretical six-pulse relation `h = 6k ± 1` should be presented as the characteristic ideal relationship, not as a guarantee that every simulated spectrum contains only those orders.

---

## 8. Portability issue in the current script

The current Python file contains a machine-specific absolute `OUTPUT_DIR`. The example-specific README explicitly recommends replacing this with a path relative to the script:

```python
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "PSCAD_Project"
```

Other environment-dependent items are:

- PSCAD version string;
- x64 selection;
- availability of `mhi.pscad` in the active Python environment;
- PSCAD license support for Python Automation;
- compiler/runtime requirements of the installed PSCAD environment.

The presentation includes a dedicated portability scene because this is central to publishing the example on GitHub.
