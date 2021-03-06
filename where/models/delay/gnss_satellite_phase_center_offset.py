"""Correct for the satellite phase center offset

Description:
------------

Correct satellite phase center offset, that means apply vector between satellite center-of-mass (CoM) and antenna
phase center (APC).

The precise orbits has to be related to the satellite antenna phase center by comparing broadcast with precise orbits.
That means the precise orbits has to be corrected by offset between satellite center of mass and antenna phase center.
In this case the satellite antenna phase offset of the first frequency is used as default.
"""

# External library imports
import numpy as np

# Midgard imports
from midgard.dev import plugins

# Where imports
from where import apriori
from where.lib import gnss


@plugins.register
def gnss_satellite_phase_center_offset(dset):
    """Determine satellite phase center offset correction

    Satellite phase center offset corrections are given in line of sight, that means in direction from satellite to
    receiver.

    Args:
        dset (Dataset):   Model data.

    Returns:
        numpy.ndarray: Satellite phase center offset correction in meter
    """
    ant_corr = apriori.get("gnss_antenna_correction")
    pco_itrs = ant_corr.satellite_phase_center_offset(dset)
    line_of_sight = gnss.get_line_of_sight(
        dset
    )  # TODO: Check if this can be replaced by direction, vector, ... properties of posvel_table()
    correction = np.einsum("ij,ij->i", line_of_sight, pco_itrs)  # dot product

    return correction
