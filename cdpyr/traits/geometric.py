class Cuboid(object):

    def __init__(self, width: float = None, height: float = None, depth:
    float = None, mass: float = None):
        self.width = width
        self.height = height
        self.depth = depth
        self.mass = mass

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if width is not None and width <= 0:
            raise ValueError('width must be positive')

        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if height is not None and height <= 0:
            raise ValueError('height must be positive')

        self._height = height

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        if depth is not None and depth <= 0:
            raise ValueError('depth must be positive')

        self._depth = depth

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        if mass is not None and mass <= 0:
            raise ValueError('mass must be positive')

        self._mass = mass

    @property
    def inertia(self):
        return 1. / 12 * self.mass * (self.height ** 2 + self.depth ** 2), \
               1. / 12 * self.mass * (self.width ** 2 + self.depth ** 2), \
               1. / 12 * self.mass * (self.height ** 2 + self.width ** 2)


class Cylindric(object):

    def __init__(self, radius: float = None, length: float = None,
                 mass: float = None, diameter: float = None):
        self.diameter = diameter
        self.radius = radius
        self.length = length
        self.mass = mass

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius is not None and radius <= 0:
            raise ValueError('radius must be positive')

        self._radius = radius

    @property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, diameter):
        self._radius = diameter / 2. if diameter is not None else diameter

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if length is not None and length <= 0:
            raise ValueError('length must be positive')

        self._length = length

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        if mass is not None and mass <= 0:
            raise ValueError('mass must be positive')

        self._mass = mass

    @property
    def inertia(self):
        return 1. / 12 * self.mass * (3 * self.radius ** 2 + self.length ** 2), \
               1. / 12 * self.mass * (3 * self.radius ** 2 + self.length ** 2), \
               1. / 2. * self.mass * self.radius ** 2
