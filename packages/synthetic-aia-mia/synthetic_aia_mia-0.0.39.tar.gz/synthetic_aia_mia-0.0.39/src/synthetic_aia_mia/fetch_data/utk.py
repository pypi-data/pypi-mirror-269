"""Downlaod and manages train / test split for UTKFaces dataset."""

from cv2 import pyrDown, pyrUp
from sklearn.model_selection import StratifiedKFold
import aia_fairness.dataset_processing as dp
import numpy as np
from PIL import Image
from pathlib import Path
import os
import kaggle
from zipfile import ZipFile
import copy

import matplotlib.pyplot as plt


from . import split

class StorageData:
    """A dataset structure that loads images from storage.
    On initialisation """
    def __init__(self):
        path = Path(os.getcwd(),"data_raw", "UTK")
        os.makedirs(path, exist_ok=True)
        #Toggle this switch to download or use predownload utk 
        imgpath = Path(path,"utkface_aligned_cropped","crop_part1")
        if not(os.path.exists(imgpath)):
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files("jangedoo/utkface-new", path)
            with ZipFile(Path(path, "utkface-new.zip")) as z:
                z.extractall(path=path)


        files = os.listdir(imgpath)
        #Parse file name to obtain labels and attributes 
        self.x = []
        self.race = []
        self.sex = []
        self.y = []
        for file in files:
            a = file.find("_")
            age = int(int(file[:a])>50)
            b = 1+a+file[a+1:].find("_")
            sex = int(file[a+1:b])
            c = 1+b+file[b+1:].find("_")
            try:
                race = int(file[b+1:c])
            except:
                race = 3
            if race==0 or race==1:
                self.x += [Path(imgpath,file)]
                self.y += [age]
                self.race += [race]
                self.sex += [sex]

        self.x =np.array(self.x)
        self.y =np.array(self.y)
        self.race =np.array(self.race)
        self.sex =np.array(self.sex)

    def __getitem__(self,i):
        """return ith element in the following order : image, y, sex, race."""

        x = np.asarray(Image.open(self.x[i]))
        x = pyrDown(pyrDown(x))
        x = np.moveaxis(x,2,0)
        x = x.astype(float)/255.0
        return x,self.y[i],self.sex[i],self.race[i]

    def __len__(self):
        return len(self.y)

    def __str__(self):
        pass
                

    def extraction(self, i):
        """Create a new smallest StorageDataset.

        :param i: List in indicies.
        :type i: list of int
        """
        new = copy.deepcopy(self)
        new.x = new.x[i]
        new.y = new.y[i]
        new.sex = new.sex[i]
        new.race = new.race[i]
        return new



def load(k=0):
    data = StorageData()
    skf = StratifiedKFold(random_state=123, shuffle=True)
    for i,(tmp_train,tmp_test) in enumerate(skf.split(data,data.y)):
        if i==k:
            train = tmp_train
            test = tmp_test


    data_split = {}
    data_split["train"] = data.extraction(train)
    data_split["test"] = data.extraction(test)
    return data_split


