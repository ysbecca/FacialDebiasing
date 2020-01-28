import torch
from torch.utils.data import Dataset as TorchDataset, ConcatDataset, DataLoader, Dataset, Sampler, WeightedRandomSampler, BatchSampler, SequentialSampler
from torch.utils.data.dataset import Subset
from torch.utils.data.sampler import RandomSampler
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder

from setup import config
import numpy as np
import pandas as pd
from PIL import Image
from typing import Callable, Optional
from enum import Enum
from torch import float64

from .data_utils import DatasetOutput, default_transform, DataLabel, slide_windows_over_img

class ImagenetDataset(ImageFolder):
    def __init__(
        self,
        path_to_images: str,
        transform: Callable = default_transform,
        nr_windows: int = 10,
        batch_size: int = -1,
        stride: float = 0.2,
        get_sub_images: bool = False
    ):
        super().__init__(path_to_images, transform)

        self.nr_windows: int = nr_windows
        self.batch_size: Optional[int] = None if batch_size < 0 else batch_size
        self.stride: float = stride
        self.get_sub_images = get_sub_images

    def __getitem__(self, idx: int):
        img, _ = super().__getitem__(idx)

        if self.get_sub_images:
            sub_images = slide_windows_over_img(img, min_win_size=config.eval_min_size,
                                          max_win_size=config.eval_max_size,
                                          nr_windows=self.nr_windows,
                                          stride=self.stride)
            sub_images = torch.split(sub_images, self.batch_size)
        else:
            sub_images = torch.tensor(0)

        return DatasetOutput(
            image=img,
            label=DataLabel.NEGATIVE.value,
            idx=idx,
            sub_images=sub_images
        )

    def sample(self, amount: int):
        max_idx: int = len(self)
        idxs: np.array = np.random.choice(np.linspace(0, max_idx - 1), amount)

        return [self.__getitem__(idx) for idx in idxs]
