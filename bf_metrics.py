import pysepm
from scipy.io import wavfile
import os


filenames = [name for name in os.listdir('out')
            if os.path.isfile(os.path.join('out',name))]


with open("bf_results2.txt","a") as f:
    
    for file in filenames:
        print(file)
        fs, channel1_speech = wavfile.read("embedded/%s.CH1.wav"%file.split(".")[0])
        fs, beamformed_speech = wavfile.read("out/"+file)
        SNRseg = pysepm.SNRseg(channel1_speech,beamformed_speech,fs)
        stoi = pysepm.stoi(channel1_speech,beamformed_speech,fs)
        pesq = pysepm.pesq(channel1_speech[:10000],beamformed_speech[:10000],fs)
        print(SNRseg)
        print(stoi)
        print(pesq)
        f.write(file + "\n" + "SNRseg: %s \nSTOI: %s\nPESQ: %s \n"%(SNRseg,stoi,pesq))