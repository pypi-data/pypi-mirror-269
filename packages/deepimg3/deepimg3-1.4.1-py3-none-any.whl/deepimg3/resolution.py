from typing import List, Tuple, Optional


class Resolution:
    __good_resolutions = [
        {"size": (1024, 1024), "aspect_ratio": 1.0},
        {"size": (1032, 1016), "aspect_ratio": 1.016},
        {"size": (1040, 1008), "aspect_ratio": 1.032},
        {"size": (1048, 1000), "aspect_ratio": 1.048},
        {"size": (1120, 936), "aspect_ratio": 1.197},
        {"size": (1160, 904), "aspect_ratio": 1.283},
        {"size": (1192, 880), "aspect_ratio": 1.355},
        {"size": (1224, 856), "aspect_ratio": 1.43},
    ]

    def __init__(
        self,
        size: Optional[Tuple[int, int]] = None,
        aspect_ratio: Optional[float] = None,
    ):
        if not size and not aspect_ratio:
            self.size = (1024, 1024)
            self.aspect_ratio = 1.0
            return
        if aspect_ratio:
            data = self._data_from_aspect(aspect_ratio)
            if data:
                self.size = data["size"]
                self.aspect_ratio = data["aspect_ratio"]
                return
            self.size = None
            self.aspect_ratio = aspect_ratio
            return
        if isinstance(size, int):
            data = self._data_from_size((size, size))
        else:
            data = self._data_from_size(size)
        if data:
            self.size = data["size"]
            self.aspect_ratio = data["aspect_ratio"]
            return
        self.size = size
        self.aspect_ratio = round(size[0] / size[1], 3)

    @classmethod
    def get_good_resolutions(cls) -> List["Resolution"]:
        return [Resolution(**data) for data in cls.__good_resolutions]

    @classmethod
    def _data_from_aspect(cls, aspect: float) -> Optional[dict]:
        for data in cls.__good_resolutions:
            if abs(data["aspect_ratio"] - aspect) < 1e-4:
                return data
        return None

    @classmethod
    def _data_from_size(cls, size: Tuple[int, int]) -> Optional[dict]:
        for data in cls.__good_resolutions:
            if data["size"] == size:
                return data
        return None

    @classmethod
    def from_aspect(cls, aspect: float) -> Optional["Resolution"]:
        data = cls._data_from_aspect(aspect)
        if data:
            return Resolution(**data)
        return None

    @classmethod
    def from_size(cls, size: Tuple[int, int]) -> Optional["Resolution"]:
        data = cls._data_from_size(size)
        if data:
            return Resolution(**data)
        return None

    def is_good_resolution(self) -> bool:
        return any(
            res.size == self.size and abs(res.aspect_ratio - self.aspect_ratio) < 1e-4
            for res in self.get_good_resolutions()
        )

    def __repr__(self):
        return f"Resolution(size={self.size}, aspect_ratio={self.aspect_ratio:.3f})"
