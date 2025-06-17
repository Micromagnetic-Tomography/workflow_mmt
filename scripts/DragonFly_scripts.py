# copy-paste the following scripts into the script runner of DragonFly

####################### load numpy dataset Bz #######################
# code preparation
import numpy as np
from pathlib import Path
from ORSModel import createChannelFromNumpyArray

# main code
path = Path('C://Users//YOUR//PATH//HERE')
matrix = np.load(path / 'Bz_FILENAME.npy').astype(np.float32)
filtered = createChannelFromNumpyArray(matrix)
filtered.setTitle('Bz')
filtered.publish()

########################## load LED CSV/NPY ##########################
# code preparation
import numpy as np
from pathlib import Path
from ORSModel import createChannelFromNumpyArray

# main code
path = Path('C://Users//YOUR//PATH//HERE')
matrix = np.loadtxt(path / 'LED_FILENAME.csv', delimiter='\t').astype(np.uint8)
# or matrix = np.load(path / 'LED_FILENAME.npy').astype(np.uint8)
filtered = createChannelFromNumpyArray(matrix)
filtered.setTitle('LED')
filtered.publish()

######################### export data to NPY #########################
######################### use python console #########################
# code preparation
import numpy as np
from pathlib import Path
from config.pythonConsoleAutoImport import *
from OrsHelpers import arrayhelper

# main code
channel = DRAG_YOUR_CHANNEL_HERE
nparray = channel.getNDArray()
path = path = Path('C://Users//YOUR//SAVEPATH//HERE')
np.save(path / 'FILENAME.npy' , nparray)