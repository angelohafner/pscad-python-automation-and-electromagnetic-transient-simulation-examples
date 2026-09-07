# Manim document change plan

Source: `sugestoes-para-manim.docx`. Project: `E:/pscad-test-1`.
Goal: implement the supplied visual corrections, retaining the existing scene architecture and engineering inputs.
Execution: inline, with checkpoints in CODEX_HANDOFF.md. Original files backed up in docs/source_review/original_code.

- [x] Extract document text and all 18 embedded images; inspect contact sheets.
- [x] Global: remove repository credit from opening/closing; translate visible scene text into English.
- [x] Image 1: WorkspaceScene: separate yes/no branches.
- [x] Images 2-4: IntroScene, ManualVsAutomationScene, ArchitectureScene: add recognizable icons.
- [x] Image 5: ComponentLibraryScene: reserve separate areas for cards and creation example.
- [x] Image 6: CreateComponentScene: wrap code and enlarge font.
- [x] Images 7-10: document exact scene/helper locations for capacitor, bridge, source and DC load replacement with PSCAD screenshots.
- [x] Image 11: SourceCreationScene: separate specifications from waveforms.
- [x] Image 12: THDScene: separate brace label from formula.
- [x] Image 13: remove HannWindowScene from presentation.
- [x] Image 14: ResultsScene: fit all output files within frame.
- [x] Image 15: FullWorkflowScene: replace crowded miniature circuits with simple icons.
- [x] Image 16: GeneralizationScene: arrows connect box boundaries, with readable vertical arrows.
- [x] Image 17: PortabilityScene: stack code examples vertically with larger font.
- [x] Image 18: ConclusionScene: two-line title and icons.
- [x] Render all retained scenes at 480p / 15 fps; inspect frames, run tests, concatenate and verify MP4 metadata.
- [x] Update README, storyboard and screenshot replacement map; record final validation.

Assumptions: removal of GitHub refers to visible presentation credits; retain source attribution in documentation. English refers to visible animation text; Portuguese narration remains useful as a separate aid. Use local vector icons for offline reproducibility. No changes to PSCAD simulation or numerical assumptions.

Validation: 4 static tests passed; 26 scenes rendered; final MP4 146.599674 s, 2199 frames, 854x480 at 15 fps; full decode passed. See docs/source_review/video_validation.json.


## DC component alignment correction

2026-09-07: dc_parallel_load in pscad_visuals.py now positions unlabeled capacitor/resistor geometry before adding external labels. Wires use actual terminal coordinates; Idc remains horizontal. DCFilterScene re-rendered at 480p15, final frame inspected, full presentation re-concatenated and verified with verify_revision.py. Four static tests passed. Preview: docs/source_review/dc_alignment.png.
