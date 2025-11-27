from dataclasses import dataclass, field
from typing import List

@dataclass
class HitObject:
    """Represents a single hit object (circle, slider, or spinner)."""
    x: int
    y: int
    time: int
    obj_type: int
    hit_sound: int
    # For sliders
    curve_points: List[str] = field(default_factory=list)
    slides: int = 0
    length: float = 0.0
    # For spinners
    end_time: int = 0

@dataclass
class TimingPoint:
    """Represents a timing control point."""
    time: float
    beat_length: float
    meter: int
    sample_set: int
    sample_index: int
    volume: int
    uninherited: bool
    effects: int

@dataclass
class Beatmap:
    """Represents a full Osu! beatmap."""
    # Metadata
    title: str = ""
    artist: str = ""
    creator: str = ""
    version: str = ""
    
    # Difficulty
    hp_drain_rate: float = 5.0
    circle_size: float = 5.0
    overall_difficulty: float = 5.0
    approach_rate: float = 5.0
    slider_multiplier: float = 1.4
    slider_tick_rate: float = 1.0

    timing_points: List[TimingPoint] = field(default_factory=list)
    hit_objects: List[HitObject] = field(default_factory=list)
