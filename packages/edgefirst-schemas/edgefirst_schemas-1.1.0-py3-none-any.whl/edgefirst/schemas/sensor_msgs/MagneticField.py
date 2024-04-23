# Measurement of the Magnetic Field vector at a specific location.
#
# If the covariance of the measurement is known, it should be filled in.
# If all you know is the variance of each measurement, e.g. from the datasheet,
# just put those along the diagonal.
# A covariance matrix of all zeros will be interpreted as "covariance unknown",
# and to use the data a covariance will have to be assumed or gotten from some
# other source.

from dataclasses import dataclass
from pycdr2 import IdlStruct
from pycdr2.types import float64, array
from ..std_msgs.Header import Header
from ..geometry_msgs.Vector3 import Vector3
from .. import default_field

@dataclass
class MagneticField(IdlStruct, typename='sensor_msgs/MagneticField'):
    header: Header = Header() # timestamp is the time the
                              # field was measured
                              # frame_id is the location and orientation
                              # of the field measurement

    magnetic_field: Vector3 = Vector3() # x, y, and z components of the
                                        # field vector in Tesla
                                        # If your sensor does not output 3 axes,
                                        # put NaNs in the components not reported.

    magnetic_field_covariance: array[float64, 9] = default_field([0] * 9) # Row major about x, y, z axes
                                                                          # 0 is interpreted as variance unknown