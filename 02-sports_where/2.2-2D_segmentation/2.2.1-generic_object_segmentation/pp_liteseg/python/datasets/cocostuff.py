# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import glob

from python.datasets import Dataset
from python.cvlibs import manager
from python.transforms import Compose


@manager.DATASETS.add_component
class CocoStuff(Dataset):
    """
    COCO-Stuff dataset `https://github.com/nightrome/cocostuff`.
    The folder structure is as follow:

        cocostuff
        |
        |--images
        |  |--train2017
        |  |--val2017
        |
        |--annotations
        |  |--train2017
        |  |--val2017


    Args:
        transforms (list): Transforms for image.
        dataset_root (str): Cityscapes dataset directory.
        mode (str): Which part of dataset to use. it is one of ('train', 'val'). Default: 'train'.
        edge (bool, optional): Whether to compute edge while training. Default: False
    """
    NUM_CLASSES = 171

    def __init__(self, transforms, dataset_root, mode='train', edge=False):
        self.dataset_root = dataset_root
        self.transforms = Compose(transforms)
        self.file_list = list()
        mode = mode.lower()
        self.mode = mode
        self.num_classes = self.NUM_CLASSES
        self.ignore_index = 255
        self.edge = edge

        if mode not in ['train', 'val']:
            raise ValueError(
                "mode should be 'train', 'val', but got {}.".format(mode))

        if self.transforms is None:
            raise ValueError("`transforms` is necessary, but it is None.")

        img_dir = os.path.join(self.dataset_root, 'images')
        label_dir = os.path.join(self.dataset_root, 'annotations')
        if self.dataset_root is None or not os.path.isdir(
                self.dataset_root) or not os.path.isdir(
                    img_dir) or not os.path.isdir(label_dir):
            raise ValueError(
                "The dataset is not Found or the folder structure is nonconfoumance."
            )

        label_files = sorted(
            glob.glob(os.path.join(label_dir, mode + '2017', '*.png')))

        img_files = sorted(
            glob.glob(os.path.join(img_dir, mode + '2017', '*.jpg')))

        self.file_list = [
            [img_path, label_path]
            for img_path, label_path in zip(img_files, label_files)
        ]
