import json
from dataclasses import dataclass
from typing import List


@dataclass
class FanucCoords:
    x: float
    y: float
    z: float
    w: float
    p: float
    r: float


@dataclass
class FanucPoint:
    layer_height: float
    coords: FanucCoords

    def as_dict(self):
        return {
            "layer_height": self.layer_height,
            "coords": self.coords.__dict__
        }


@dataclass
class CurrentRender:
    z: float
    points: List[FanucPoint]

    def as_dict(self):
        points = []
        for point in self.points:
            points.append(point.as_dict())
        return {
            "z": self.z,
            "points": points
        }


@dataclass
class Coordinate3D:
    x: float
    y: float
    z: float


@dataclass
class LidarOffsets:
    axis: Coordinate3D
    lidar_offset: float

    def as_dict(self):
        return {
            "axis": self.axis.__dict__,
            "lidar_offset": self.lidar_offset
        }
