from units.measurement_system import physical_measurement_system
from .physical_LTM import LTM

SI = physical_measurement_system(LTM)

(m,s,kg) = SI.base_quantities()

N = kg*m/(s**2)
Pa = N/(m**2)
J = kg*(m/s)**2
W = J/s
Hz = s**-1
