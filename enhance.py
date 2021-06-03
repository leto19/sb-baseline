import os
import os.path
from enhance.noise_reduction import noise_reduction
import soundfile as sf

filenames = [name for name in os.listdir('out')
            if os.path.isfile(os.path.join('out',name))]

for file in filenames:
    noise_reduction("out/%s"%file,"out_enhanced/%s"%file.replace(".wav","_e.wav"))
