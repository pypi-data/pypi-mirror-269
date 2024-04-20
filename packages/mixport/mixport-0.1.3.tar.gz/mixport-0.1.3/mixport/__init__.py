import argparse
import sys

from dataclasses import replace
from pathlib import Path
from typing import Optional
from tracklist.format.cuesheet import CuesheetFormat

from mixport.transcode import transcode

RECORDINGS_PATH = Path.home() / 'Music' / 'Mixxx' / 'Recordings'
CUESHEET_FORMAT = CuesheetFormat()

def find_latest_recording() -> Optional[Path]:
    '''Fetches the path to the latest recording's .cue file.'''
    return next((path for path in sorted(RECORDINGS_PATH.iterdir(), reverse=True) if path.name.endswith('.cue')), None)

def main():
    parser = argparse.ArgumentParser(description='CLI tool for transcoding Mixxx recordings')
    parser.add_argument('-o', '--output', required=True, type=Path, help='The output directory.')
    parser.add_argument('-f', '--format', default='opus', help='The file extension of the output format. Has to be a format that ffmpeg supports.')
    parser.add_argument('--trim-duration', type=float, default=None, help='Trims to the given duration in seconds.')
    parser.add_argument('--fade-in', type=float, default=None, help='Adds the given fade-in in seconds.')
    parser.add_argument('--fade-out', type=float, default=None, help='Adds the given fade-out in seconds.')
    parser.add_argument('input', type=Path, nargs=argparse.OPTIONAL, help='The input cue file. Defaults to the latest Mixxx recording.')

    args = parser.parse_args()

    in_cue_path = args.input or find_latest_recording()
    out_dir = args.output
    format = args.format
    trim_duration = args.trim_duration
    fade_in = args.fade_in
    fade_out = args.fade_out

    if not in_cue_path:
        print(f'No recording (.cue file) found in recordings: {RECORDINGS_PATH}')
        sys.exit(1)

    print(f'==> Parsing {in_cue_path}')
    with open(in_cue_path, 'r') as f:
        in_tracklist = CUESHEET_FORMAT.parse(f.read())

    if not in_tracklist.file:
        print(f'No audio file referenced in {in_cue_path}!')
        sys.exit(1)
    
    in_audio_path = RECORDINGS_PATH / in_tracklist.file

    print(f'==> Checking {in_audio_path}')
    if not in_audio_path.exists():
        print(f'Non-existent audio file {in_audio_path} referenced in {in_cue_path}!')
        sys.exit(1)

    out_cue_path = out_dir / in_cue_path.name
    out_audio_path = out_dir / in_cue_path.with_suffix(f'.{format}').name

    print(f'==> Creating {out_dir} if needed')
    out_dir.mkdir(parents=True, exist_ok=True)

    out_tracklist = replace(in_tracklist, file=out_audio_path.name)

    print(f'==> Copying to {out_cue_path}')
    with open(out_cue_path, 'w') as f:
        f.write(CUESHEET_FORMAT.format(out_tracklist))

    print(f'==> Transcoding to {out_audio_path}')
    transcode(
        in_audio_path=in_audio_path,
        out_audio_path=out_audio_path,
        trim_duration=trim_duration,
        fade_in=fade_in,
        fade_out=fade_out,
    )
