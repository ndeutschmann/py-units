from units.measurement_system import MeasurementSystem
from units.prefixes import giga
from .SI import m,s,kg

c_SI = 299792458 * m / s
hbar_SI = 1.0545718e-34*(m**2)/s *kg
eV_SI = 1.602176634e-19*kg*((m/s)**2)
GeV_SI = giga*eV_SI

HEP_def = (
("E","GeV",GeV_SI),
("V","c",c_SI),
("J","hbar",hbar_SI),
)

HEP = MeasurementSystem(HEP_def)
(GeV,c,hbar) = HEP.base_quantities()