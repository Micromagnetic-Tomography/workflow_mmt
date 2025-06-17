import numpy as np
from pathlib import Path
from MMT_protocol_selection import mmt_inversion

dpath = Path('/home/5649404/Codes/MMT_codes/Martha_30mu')
qdm_data = 'magnetic_field_top.txt'
grain_data = 'position_grains_rev.txt'
dqdm = 1.2e-6
Hz = 2.5e-6

output = mmt_inversion(dpath, np.loadtxt(dpath / qdm_data), np.loadtxt(dpath / grain_data), dqdm, Hz,
                       save_name='dipole', exp_limit='dipole')