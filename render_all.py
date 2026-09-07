"""Render all Manim scenes and concatenate them into one MP4 file."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from pscad_rectifier_presentation import SCENE_ORDER


QUALITY_FOLDER = {
    "l": "480p15",
    "m": "720p30",
    "h": "1080p60",
    "p": "1440p60",
    "k": "2160p60",
}


def run_command(command: list[str]) -> None:
    """Run a subprocess and stop immediately if it fails."""
    print("+", " ".join(command))
    subprocess.run(command, check=True, cwd=Path(__file__).resolve().parent)


def render_scenes(project_dir: Path, quality: str) -> list[Path]:
    """Render every scene using the selected Manim quality preset."""
    script = project_dir / "pscad_rectifier_presentation.py"
    for scene_name in SCENE_ORDER:
        run_command(
            [
                sys.executable,
                "-m",
                "manim",
                f"-q{quality}",
                "--disable_caching",
                str(script),
                scene_name,
            ]
        )

    video_dir = (
        project_dir
        / "media"
        / "videos"
        / "pscad_rectifier_presentation"
        / QUALITY_FOLDER[quality]
    )
    videos = [video_dir / f"{scene_name}.mp4" for scene_name in SCENE_ORDER]
    missing = [path for path in videos if not path.is_file()]
    if missing:
        missing_text = "\n".join(str(path) for path in missing)
        raise FileNotFoundError(f"Expected rendered scene files were not found:\n{missing_text}")
    return videos


def concatenate(videos: list[Path], output_file: Path) -> None:
    """Concatenate equal-format Manim MP4 files with FFmpeg."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("FFmpeg was not found on PATH. Install FFmpeg before concatenation.")

    concat_file = output_file.with_suffix(".concat.txt")
    with concat_file.open("w", encoding="utf-8") as handle:
        for video in videos:
            escaped = video.resolve().as_posix().replace("'", "'\\''")
            handle.write(f"file '{escaped}'\n")

    try:
        run_command(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output_file),
            ]
        )
    except subprocess.CalledProcessError:
        # Re-encode as a robust fallback if stream-copy concatenation fails.
        run_command(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(output_file),
            ]
        )
    finally:
        concat_file.unlink(missing_ok=True)


def main() -> None:
    """Parse command-line options and render the complete presentation."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quality",
        choices=sorted(QUALITY_FOLDER),
        default="l",
        help="Manim quality preset: l, m, h, p, or k (default: l, 480p at 15 fps).",
    )
    parser.add_argument(
        "--output",
        default="pscad_python_automation_presentation.mp4",
        help="Final concatenated MP4 filename.",
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    videos = render_scenes(project_dir, args.quality)
    output_file = project_dir / args.output
    concatenate(videos, output_file)
    print(f"Complete presentation: {output_file}")


if __name__ == "__main__":
    main()
