import torch

from speechbrain.dataio.dataio import read_audio_multichannel,write_audio,read_audio
from speechbrain.processing.features import STFT, ISTFT
from speechbrain.processing.multi_mic import Covariance
from speechbrain.processing.multi_mic import GccPhat
from speechbrain.processing.multi_mic import DelaySum
import os
import os.path
import numpy as np

def beamformer(x,fs):
    """computes the delay sum beamformer output of an input multichannel signal 
    
    Arguments
    ---------
    x : 
        multichannel input audio signal
    fs : int
        sample rate of signal, used for Fourier transforms 
    """
    stft = STFT(sample_rate=fs)
    cov = Covariance()
    gccplat= GccPhat()
    delaysum = DelaySum()
    istft = ISTFT(sample_rate=fs) 
    
    X = stft(x) #take the fourier transform 
    #print(X)
    XX = cov(X) #calculate the covarience matrix
    #print(XX)
    tdoas = gccplat(XX) # delay estimation
    #print(tdoas)
    Y = delaysum(X,tdoas) #delay sum beamformer 
    y = istft(Y) # inverse fourier transform 
    return y 


filenames = [name for name in os.listdir('embedded')
            if os.path.isfile(os.path.join('embedded',name))]
#print(filenames)

file_channel_dict = {}
for file in filenames:
    path = os.path.join('embedded',file)
    prefix = "".join(file.split(".")[:-2]) #finds the base name of the file 
    print(prefix)
    if prefix not in file_channel_dict.keys(): # finds all paths to the channels for this recording
        file_channel_dict[prefix] = [path] 
        #print(file_channel_dict)
    else:
        file_channel_dict[prefix].append(path)

for key,element in zip(file_channel_dict,file_channel_dict.values()): #for each recording
    element = sorted(element) # sort in accending channel number 
    channel0 = element.pop(0) #pop off the 0th channel, it's the close talking one 

    print(sorted(element))
    #audio = read_audio_multichannel({"files":file_channel_dict[key],"start":0,"stop":len(read_audio(element[0]))})
    
    #read the list of files as a single multichannel signal 
    audio = read_audio_multichannel({"files":element,"start":0}) 
    audio = audio.unsqueeze(0) # formatting 
    print(audio.shape) 
    #perform beamforming 
    out = beamformer(audio,16000)
    out = out.flatten()
    print(out.shape)

    write_audio("out/%s"%key+".wav",out,16000)
    
 