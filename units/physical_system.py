'''Fundamental physical objects
'''

from numbers import Number

class PhysicalSystem:
    """A PhysicalSystem is the abstract data of a number of a number of quantities and a list of physical constants which define what 1 unit is in this system
    """
    def __init__(self,quantities):
        """quantities_and_units: list of (str,str)"""
        for q, u in quantities:
            assert isinstance(q,str)
            assert isinstance(u,str)

        self.quantities = quantities

class Dimension(tuple):
    """List of exponents that express the dimension of a quantity in a given system. Can be added and subtracted together, and multiplied or divided by numbers"""
    def __add__(self,other):
        return Dimension([x+y for x,y in zip(self,other)])
    def __sub__(self, other):
        return Dimension([x - y for x, y in zip(self, other)])
    def __neg__(self):
        return Dimension([-x for x in self])
    def __mul__(self, other):
        return Dimension(x*other for x in self)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __truediv__(self,other):
        return Dimension(x/other for x in self)

class PhysicalQuantity:
    """A PhysicalQuantity is a quantity expressed in a PhysicalSystem. It is the data of a physical dimension(a product of powers of elementary quantities expressed as a list of floats) and of a value (float)"""
    def __init__(self,value,dimension,system):
        assert isinstance(value,Number)
        self.value = value

        assert isinstance(system,PhysicalSystem)
        self.system = system

        assert len(dimension) == len(system.quantities)
        self.dimension = Dimension(dimension)



    def __mul__(self, other):
        if isinstance(other,Number):
            return PhysicalQuantity(self.value*other,self.dimension,self.system)
        else:
            assert other.system == self.system
            return PhysicalQuantity(self.value*other.value,self.dimension+other.dimension,self.system)

    def __rmul__(self, other):
        assert isinstance(other,Number)
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other,Number):
            return PhysicalQuantity(self.value/other,self.dimension,self.system)
        else:
            assert other.system == self.system
            return PhysicalQuantity(self.value/other.value,self.dimension-other.dimension,self.system)

    def __rtruediv__(self, other):
        assert isinstance(other,Number)
        return PhysicalQuantity(other/self.value,-self.dimension,self.system)

    def __add__(self, other):
        assert other.system == self.system
        assert self.dimension == other.dimension
        return PhysicalQuantity(self.value + other.value, self.dimension, self.system)

    def __sub__(self, other):
        assert other.system == self.system
        assert self.dimension == other.dimension
        return PhysicalQuantity(self.value - other.value, self.dimension, self.system)