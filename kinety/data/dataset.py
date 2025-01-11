import os, io, csv, math, random
import numpy as np
from einops import rearrange
from decord import VideoReader

import torch
import torchvision.transforms as transforms
from torch.utils.data.dataset import Dataset
from kinety.utils.util import zero_rank_print

from PIL import Image


class KineticTypographyData_st8dy(Dataset):
    def __init__(
            self,
            csv_path, video_folder, mask_folder,
            sample_size=(198,352), sample_stride=4, sample_n_frames=16,
            is_image=False,
            is_kt=False
        ):
        zero_rank_print(f"loading annotations from {csv_path} ...")
        with open(csv_path, 'r') as csvfile:
            self.dataset = list(csv.DictReader(csvfile))
        self.length = len(self.dataset)
        zero_rank_print(f"data scale: {self.length}")

        self.video_folder    = video_folder
        self.sample_stride   = sample_stride
        self.sample_n_frames = sample_n_frames
        self.is_image        = is_image
        self.mask_folder     = mask_folder
        self.convert_to_tensor = transforms.ToTensor()
        
        sample_size = (int(sample_size[0]), int(sample_size[1])) if not isinstance(sample_size, int) else (sample_size, sample_size)
        self.pixel_transforms = transforms.Compose([
            transforms.Resize(sample_size),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], inplace=True),
        ])
        self.pixel_transforms_mask = transforms.Compose([
            transforms.Resize((64,64)),
            transforms.Resize(sample_size),
        ])
    
    def get_batch(self, idx):
        video_dict = self.dataset[idx]
        effect_num, word = video_dict['effect_num'], video_dict['word']
        caption_st, caption_dy, word_embed =  video_dict['caption_st'], video_dict['caption_dy'], video_dict['word_embed']
        
        video_dir    = os.path.join(self.video_folder, f"{int(effect_num):04d}/{word}.mp4")
        video_reader = VideoReader(video_dir)
        video_length = len(video_reader)
        
        if not self.is_image:
            clip_length = min(video_length, (self.sample_n_frames - 1) * self.sample_stride + 1)
            start_idx   = random.randint(0, video_length - clip_length)
            batch_index = np.linspace(start_idx, start_idx + clip_length - 1, self.sample_n_frames, dtype=int)
        else:
            batch_index = [23]

        pixel_values = torch.from_numpy(video_reader.get_batch(batch_index).asnumpy()).permute(0, 3, 1, 2).contiguous()
       
        pixel_values = pixel_values / 255.
        del video_reader

        mask_dir = os.path.join(self.mask_folder, f"{int(effect_num):04d}/{word}.png")
        mask_read = Image.open(mask_dir)
        pixel_values_mask = self.convert_to_tensor(mask_read)

        if self.is_image:
            pixel_values = pixel_values[0]
        
        return pixel_values, caption_st, caption_dy, word, pixel_values_mask, word_embed

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        while True:
            try:
                pixel_values, caption_st, caption_dy, word, pixel_values_mask, word_embed = self.get_batch(idx)
                break

            except Exception as e:
                idx = random.randint(0, self.length-1)

        pixel_values = self.pixel_transforms(pixel_values)
        pixel_values_mask = self.pixel_transforms_mask(pixel_values_mask)

        sample = dict(pixel_values=pixel_values, text_st=caption_st, text_dy=caption_dy, word=word, pixel_values_mask=pixel_values_mask, word_embed=word_embed)
        return sample



if __name__ == "__main__":
    from kinety.utils.util import save_videos_grid

    dataset = KineticTypographyData_st8dy(
        csv_path="data/dataset_584x1000/video_info_upper_short_st8dy_wordembed.csv",
        video_folder="data/dataset_584x1000/videos",
        sample_size=256,
        sample_stride=1, sample_n_frames=16,
        is_image=True,
    )
    import pdb
    pdb.set_trace()
    
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, num_workers=16,)
    for idx, batch in enumerate(dataloader):
        print(batch["pixel_values"].shape, len(batch["text"]))