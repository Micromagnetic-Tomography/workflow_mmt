import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from mmt_multipole_inversion import plot_tools
import mmt_multipole_inversion.magnetic_sample as msp
import mmt_multipole_inversion.multipole_inversion as minv

def mmt_inversion(datapath: Path,
                  qdm_data: np.array,
                  grain_data: np.array,
                  dqdm: float,
                  Hz: float,
                  mask: np.array = None,
                  save_name: str = 'MMT',
                  exp_limit: str = 'dipole',
		  verbose: bool = True):
    """ Function to calculate the magnetic moments

    Parameters
    ----------
    datapath
        Path-object pointing to all files
    qdm_data
        Bz data in tesla
    grain_data
        grain data. first three columns position, fourth column volume. all in m or m3
    dqdm
        pixel size qdm (think of binning)
    Hz
        distance between sensor and sample.
    mask
        poopmask
    save_name
        save name of the multipole moment file
    exp_limit
        expansion limit of MMT, defaults to quadrupole
    verbose
        verbosity flag, defaults to no output (False)
    """
    domainsize = np.array([[0, 0], [(len(qdm_data)-1)*dqdm, (len(qdm_data)-1)*dqdm]])
    max_depth = 60e-6  # max depth where grains can be found
    dxy_s = dqdm / 2
    pos_grain = grain_data[:, :3]
    
    print(f'There are {len(pos_grain)} grains present')
    volumes = grain_data[:, :]
    dip_mom = np.zeros_like(pos_grain)

    # Get derived parameters
    sensors_x = int(
        (domainsize[1, 0] - domainsize[0, 0]) / dqdm) + 1
    sensors_y = int(
        (domainsize[1, 1] - domainsize[0, 1]) / dqdm) + 1
    sensor_area = 4 * dxy_s **2
    Sx = domainsize[1,0] - domainsize[0,0] + dqdm
    Sy = domainsize[1,1] - domainsize[0,1] + dqdm
    Sdx = dqdm
    Sdy = dqdm
    Lx = Sx * 1.0
    Ly = Sy * 1.0

    # Initiate a Forward model
    sample = msp.MagneticSample(Hz, Sx, Sy, Sdx, Sdy, Lx, Ly, max_depth,
                                bz_field_module='spherical_harmonics_basis'
                                )
    # Load the files
    sample.generate_particles_from_array(pos_grain, dip_mom, volumes)
    # Construct the Greens matrix and make magnetic field
    sample.generate_measurement_mesh()
    sample.Bz_array = qdm_data
    # save the data
    sample.save_data(filename = save_name, basedir = datapath, noised_array=False)

    json_file = datapath / f"MetaDict_{save_name}.json"
    npz_file = datapath / f"MagneticSample_{save_name}.npz"
    dir_model = minv.MultipoleInversion(
            json_file, npz_file,
            expansion_limit=exp_limit,
            sus_functions_module='spherical_harmonics_basis',
            verbose=verbose)
    # dir_model.compute_inversion(mask=mask)
    dir_model.compute_inversion(method='direct')
    dir_model.save_multipole_moments(basedir=datapath, save_name=save_name)

    fig, ax = plt.subplots()
    cf, c1, c2 = plot_tools.plot_inversion_Bz(ax, dir_model, imshow_args=dict(vmin=-1e-4, vmax=1e-4, cmap='RdBu'), scatter_args=dict(s=3, color='black'))
    cl = fig.colorbar(cf)
    cl.set_label('Tesla')
    plt.savefig(datapath / 'plot_forward.png')

    return dir_model
