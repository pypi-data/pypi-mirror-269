class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False

        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
