"""Defines measurement systems and related objects
A measurement system is a specific unit system in a given physical system.
It has a complete set of defining quantities, which are not necessarily aligned with the defining quantities
of the underlying physical system

For example, one can choose the SI system to describe all of physics and the defining physical quantities.
An example of derived system is the HEP system, in which one has action (with defining unit hbar) and velocity
(with defining unit c) as defining quantities.
"""
# External imports
from sympy import Matrix,det

# Internal imports
from .physical_system import PhysicalQuantity,Dimension


class MeasurementSystem:
    def __init__(self,defining_quantities,physical_system):
        for q in defining_quantities:
            assert q.system == physical_system

        # No zero value can be used
        assert all([q.value != 0 for q in defining_quantities])

        # Load data
        self.defining_quantities = defining_quantities
        self.physical_system = physical_system

        # Build the transfer matrix, check that it is invertible
        self.matrix = Matrix([q.dimension for q in defining_quantities])
        assert det(self.matrix) != 0
        # Build the inverse transfer matrix
        self.inverse_matrix = self.matrix.inv()


class MeasurementQuantity(PhysicalQuantity):
    """A MeasurementQuantity is a quantity expressed in a MeasurementSystem. It is the data of a physical dimension(a product of powers of elementary quantities expressed as a list of floats) and of a value (float)"""
    def __init__(self,value,dimension,system,name=None):
        assert isinstance(system,MeasurementSystem)
        PhysicalQuantity.__init__(self,value,dimension,system,name=name)

    def underlying_quantity(self):
        """Generate a PhysicalQuantity expressed in the underlying PhysicalSystem

        quantity = value * defining_quantity_1**n_1 * ... * defining_quantity_N**n_N
        where N = len(self.dimension)
        defining_quantity has a similar expression in terms of a value and the defining quantities of the underlying
        system
        """
        underlying_value = self.value
        underlying_dimension = Dimension([0]*len(self.dimension))

        for i,q in enumerate(self.system.defining_quantities):
            underlying_value *= q.value**self.dimension[i]
            underlying_dimension = underlying_dimension + self.dimension[i]*q.dimension

        return PhysicalQuantity(underlying_value,underlying_dimension,self.system.physical_system,name=self.name)

def physical_measurement_system(physical_system):
    """Build a measurement system from the defining quantities of a physical system"""
    N = len(physical_system.quantities)
    defining_quantities = []
    for i,q in enumerate(physical_system.quantities):
        d = [0 if j != i else 1 for j in range(N) ]
        defining_quantities.append(PhysicalQuantity(1,d,physical_system))

    return MeasurementSystem(defining_quantities,physical_system)

