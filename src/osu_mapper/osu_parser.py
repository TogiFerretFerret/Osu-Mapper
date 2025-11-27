from typing import Optional, List
from .beatmap import Beatmap, TimingPoint, HitObject
import re

def parse_osu_file(file_path: str) -> Optional[Beatmap]:
    """
    Parses a .osu file and returns a Beatmap object.

    Args:
        file_path: The path to the .osu file.

    Returns:
        A Beatmap object if parsing is successful, otherwise None.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

    beatmap = Beatmap()
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('//'):
            continue
        
        if line.startswith('['):
            current_section = line
            continue

        if current_section == '[Metadata]':
            key, value = map(str.strip, line.split(':', 1))
            if hasattr(beatmap, key):
                setattr(beatmap, key, value)
            # For unicode variants, we'll just use the main ones for simplicity
            elif key == "TitleUnicode":
                beatmap.title = value
            elif key == "ArtistUnicode":
                beatmap.artist = value
            elif key == "Creator":
                beatmap.creator = value
            elif key == "Version":
                beatmap.version = value

        elif current_section == '[Difficulty]':
            key, value = map(str.strip, line.split(':', 1))
            if hasattr(beatmap, key):
                 try:
                    setattr(beatmap, key, float(value))
                 except (ValueError, TypeError):
                     print(f"Warning: Could not parse difficulty value for {key}: {value}")

        elif current_section == '[TimingPoints]':
            try:
                values = line.split(',')
                beatmap.timing_points.append(TimingPoint(
                    time=float(values[0]),
                    beat_length=float(values[1]),
                    meter=int(values[2]),
                    sample_set=int(values[3]),
                    sample_index=int(values[4]),
                    volume=int(values[5]),
                    uninherited=bool(int(values[6])),
                    effects=int(values[7])
                ))
            except (ValueError, IndexError) as e:
                print(f"Warning: Could not parse timing point line: {line} ({e})")

        elif current_section == '[HitObjects]':
            try:
                values = line.split(',')
                x, y, time, obj_type = int(values[0]), int(values[1]), int(values[2]), int(values[3])
                hit_sound = int(values[4])
                
                hit_obj = HitObject(x=x, y=y, time=time, obj_type=obj_type, hit_sound=hit_sound)

                # Check for slider
                if obj_type & 2:
                    curve_data = values[5].split('|')
                    hit_obj.curve_points = curve_data
                    hit_obj.slides = int(values[6])
                    hit_obj.length = float(values[7])
                
                # Check for spinner
                elif obj_type & 8:
                    hit_obj.end_time = int(values[5])

                beatmap.hit_objects.append(hit_obj)
            except (ValueError, IndexError) as e:
                print(f"Warning: Could not parse hit object line: {line} ({e})")
    
    return beatmap
