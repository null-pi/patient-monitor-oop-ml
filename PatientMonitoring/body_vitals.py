import enum
from .cholesterol import Cholesterol
from .blood_pressure import BloodPressure

#contains specific class to be created
class BodyVitals(enum.Enum):
    CHOLESTEROL = Cholesterol
    BLOOD_PRESSURE = BloodPressure