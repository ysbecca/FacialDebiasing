import pickle
from PIL import Image
from torch.utils.data import Dataset

class CIFARDataset(Dataset):
	""" CIFAR 10-S, gray and colour adapted from Wang et al. """
	def __init__(
			self, 
			data_path="",
			label_path="",
			transform=None,
			target_transform=None,
		):
		super().__init__()


		self.transform 				= transform
		self.target_transform 		= target_transform

		with open(data_path, 'rb') as f:
			self.data = pickle.load(f)

		with open(label_path, 'rb') as f:
			self.targets = pickle.load(f)


	def __len__(self):
		return len(self.targets)


	def __getitem__(self, index):

		img, target = self.data[index], int(self.targets[index])

		img = Image.fromarray(img)		

		if self.transform is not None:
			img = self.transform(img)

		if self.target_transform is not None:
			target = self.target_transform(target)

		return img, target