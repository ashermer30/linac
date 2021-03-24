import numpy as np
import math
import pandas as pd
from root_pandas import read_root, to_root
import uproot
from scipy import stats
# from matplotlib import pylab as plt
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--density', help='foo help')
parser.add_argument('--entries', help='foo help')
parser.add_argument('--jobID', help='foo help')
args = parser.parse_args()
air_density=args.density
file_num=int(args.jobID)
ents_gen=int(args.entries)

filename=f"/work/jo17631/PhaseSpaces/PhS2_10x10_p1_Elec/EverestAir.root"
print(f"input file: {filename}")
ur=uproot.pandas.iterate(filename, "PhaseSpace", ['X','Y','dX','dY','Ekine'])
mylist=list(ur)
dftot=pd.concat(mylist, ignore_index=True, sort=False  ,copy = False)

print("read files")

nparr=dftot.to_numpy()
values=nparr.T

bandwidth=0.025
events_to_be_generated=ents_gen   #1000000

kde = stats.gaussian_kde(values,bw_method=bandwidth)
print("generated KDE")

for i in range(file_num,file_num+1):
        newsample = stats.gaussian_kde.resample(kde,events_to_be_generated)
        print("resampled KDE",i)

        newsample=newsample.T
        newdf=pd.DataFrame(newsample,columns=['X','Y','dX','dY','Ekine'])

        newdfsub=newdf[(newdf['Ekine']>0)]
        newdfsub['dZ']=-1*pow(1.0-newdfsub['dX']*newdfsub['dX']-newdfsub['dY']*newdfsub['dY'],0.5)
        newdfsub["Z"]=-0.0000005
        newdfsub=newdfsub.dropna(axis='index')
        newdfsub=newdfsub.astype('float32')
        newdfsub.to_root(f"/work/as17540/PhaseSpaces/Generated_PhS2_10x10_Electrons/Jo_generatedElectron_PhS2_10x10_{air_density}.root", key='PhaseSpace')
        print("root file saved",i)

print("Finished")
