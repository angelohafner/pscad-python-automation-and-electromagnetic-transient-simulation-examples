# Validation of the Manim revision

Validated on 2026-09-07 with Python 3.13 and Manim 0.20.1.

- `python -m pytest -q`: 4 passed.
- All 26 retained scenes rendered at 854 x 480 and 15 fps.
- Final and intermediate frames visually inspected.
- Final MP4: 146.599674 seconds, 2199 frames; H.264, no audio.
- Full FFmpeg decode passed; concatenated frame count equals the sum of the scene frame counts.
- DC capacitor and resistor geometry is positioned before labels; connections use actual terminal coordinates and Idc stays horizontal.

Detailed local QA images, logs and original backups are intentionally untracked in docs/source_review. The final video and reproducible source are versioned. Numerical PSCAD inputs and the original simulation script are unchanged from the remote baseline.

```powershell
python -m pytest -q
ffprobe -v error -show_streams -show_format pscad_document_revision_480p.mp4
ffmpeg -v error -i pscad_document_revision_480p.mp4 -f null -
```
