from pygan._torch.ebgan_image_generator import EBGANImageGenerator
import copy
from pathlib import Path
import pickle
import numpy as np
import os
from PIL import Image
import uuid
import torch

from ..predictor.utk import UtkNN

class _StorageDataset:
    def __init__(self, imgpath):
        files = os.listdir(imgpath)
        self.x = []
        self.y = []
        for file in files:
            self.x += [Path(imgpath,file)]
            self.y += [0]

    def __len__(self):
        return len(self.x)

    def __getitem__(self,i):
        x = np.asarray(Image.open(self.x[i]))
        x = x.astype(float)/255.0
        x = np.moveaxis(x,2,0)
        return x,self.y[i]
        

def _pathmaker(i):
    path = Path("dataset_for_pygan")
    os.makedirs(path, exist_ok=True)
    return Path(path, f"{str(i)}.bmp")

def gan(dataset,iter_n=1000):
    """Generate image using pygan.

    :param dataset: Image dataset used to train the gan.
    :type dataset: fetch_data.utk.StorageDataset
    :param iter_n: (Optional default=1000) Number of iterations.
    :type iter_n: int
    :return: A dataset with generated images.
    :rtype : fetch_data.utk.StorageDataset
    """

    #Saving 50x50 images from the train dataset
    for i in range(len(dataset)):
        x = dataset[i][0]
        x = x*255
        x = np.moveaxis(x,0,2).astype(int)
        image = Image.fromarray(x.astype('uint8'), 'RGB')
        image.save(_pathmaker(i), "bmp")
        

    ctx = "cuda:0" if torch.cuda.is_available() else "cpu"

    gan_image_generator = EBGANImageGenerator(
        # `list` of path to your directories.
        dir_list=["dataset_for_pygan"],
        # `int` of image width.
        width=50,
        # `int` of image height.
        height=50,
        # `int` of image channel.
        channel=3,
        # `int` of batch size.
        batch_size=40,
        # `float` of learning rate.
        learning_rate=1e-06,
        ctx=ctx
    )

    gan_image_generator.learn(
        # `int` of the number of training iterations.
        iter_n=iter_n,
        # `int` of the number of learning of the discriminative model.
        k_step=10,
    )

    
    path = Path("synthetic_data",str(uuid.uuid4()))
    os.makedirs(path,exist_ok=True)
    
    arr = gan_image_generator.EBGAN.generative_model.draw()
    arr = arr.detach().cpu().numpy()
    
    #arr shape is:
    #batch
    #channel
    #height
    #width

    #save generate images 
    for i in range(np.shape(arr)[0]):
        image_path = Path(path,f"{str(i)}.bmp")
        img = np.moveaxis(arr[i],0,2)*255
        image = Image.fromarray(img.astype('uint8'), 'RGB')
        image.save(image_path, "bmp")

    #Generating labels
    utknn = UtkNN()
    utknn.fit(dataset)
    synthetic = _StorageDataset(path)
    synthetic = utknn.predict(synthetic)
    synthetic.y = copy.deepcopy(synthetic.hard)
    del synthetic.hard
    del synthetic.soft0
    del synthetic.soft1

    return synthetic
