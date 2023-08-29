import json
from dataclasses import dataclass, field
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


class SomeClass:
    def __init__(self):
        self.methods = {
            'method1': self.__method_1
        }

    def __method_1(self, payload):
        print(payload)

    def call_method_1(self):
        self.methods["method1"]('alalal')


if __name__ == '__main__':
    # coords = Coordinate3D(1, 2, 3)
    # lidar_offset = 50
    # offsets = LidarOffsets(lidar_offset=50, axis=coords).as_dict()
    # f = open('offsets.json', 'w')
    # json.dump(offsets, f)
    # f.close()

    f = open('offsets.json', 'r')
    offsets = json.load(f)
    f.close()
    print(offsets)

# if __name__ == '__main__':
# coords_1 = FanucCoords(x=1, y=2, z=3, w=0, p=0, r=0)
# coords_2 = FanucCoords(x=5, y=6, z=3, w=0, p=0, r=0)
# current_render = CurrentRender(z=3)
# current_render.points.append(coords_1)
# current_render.points.append(coords_2)
# print(current_render.as_dict())
