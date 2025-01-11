import argparse
import datetime
import inspect
import os
from omegaconf import OmegaConf

import torch
import torchvision.transforms as transforms
import torch.nn.functional as F

import diffusers
from diffusers import AutoencoderKL, DDIMScheduler

from tqdm.auto import tqdm
from transformers import CLIPTextModel, CLIPTokenizer

from kinety.models.unet import UNet3DConditionModel
from kinety.pipelines.pipeline_kinety import KineTyPipeline
from kinety.utils.util import save_videos_grid, save_videos_mp4
from kinety.utils.util import load_weights
from diffusers.utils.import_utils import is_xformers_available

from einops import rearrange, repeat

import csv, pdb, glob, math
from pathlib import Path
from PIL import Image
import numpy as np


@torch.no_grad()
def main(args):
    *_, func_args = inspect.getargvalues(inspect.currentframe())
    func_args = dict(func_args)
    
    time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    savedir = f"samples/{Path(args.config).stem}-{time_str}"
    os.makedirs(savedir)

    config  = OmegaConf.load(args.config)
    samples = []

    # create validation pipeline
    tokenizer    = CLIPTokenizer.from_pretrained(args.pretrained_model_path, subfolder="tokenizer")
    text_encoder = CLIPTextModel.from_pretrained(args.pretrained_model_path, subfolder="text_encoder").cuda()
    vae          = AutoencoderKL.from_pretrained(args.pretrained_model_path, subfolder="vae").cuda()

    sample_idx = 0
    for model_idx, model_config in enumerate(config):
        model_config.W = model_config.get("W", args.W)
        model_config.H = model_config.get("H", args.H)
        model_config.L = model_config.get("L", args.L)

        model_config.disk_store = model_config.get("disk_store", args.disk_store) if model_config.get("disk_store", args.disk_store) is not None else None
        model_config.store_attention = model_config.get("store_attention", args.store_attention) if model_config.get("store_attention", args.store_attention) is not None else None

        inference_config = OmegaConf.load(model_config.get("inference_config", args.inference_config))
        unet = UNet3DConditionModel.from_pretrained_2d(args.pretrained_model_path,
        subfolder="unet", unet_additional_kwargs=OmegaConf.to_container(inference_config.unet_additional_kwargs),
        unet_pretrained=args.unet_checkpoint_path
        ).cuda()

        # set xformers
        if is_xformers_available() and (not args.without_xformers):
            unet.enable_xformers_memory_efficient_attention()

        pipeline = KineTyPipeline(
            vae=vae, text_encoder=text_encoder, tokenizer=tokenizer, unet=unet,
            disk_store = model_config.disk_store,
            scheduler=DDIMScheduler(**OmegaConf.to_container(inference_config.noise_scheduler_kwargs)),
        ).to("cuda")

        pipeline = load_weights(
            pipeline,
            motion_module_path         = model_config.get("motion_module", ""),
        ).to("cuda")

        prompts      = model_config.prompt
        n_prompts    = list(model_config.n_prompt) * len(prompts) if len(model_config.n_prompt) == 1 else model_config.n_prompt
        
        random_seeds = model_config.get("seed", [-1])
        random_seeds = [random_seeds] if isinstance(random_seeds, int) else list(random_seeds)
        random_seeds = random_seeds * len(prompts) if len(random_seeds) == 1 else random_seeds
        
        config[model_idx].random_seed = []
        for prompt_idx, (prompt, n_prompt, random_seed) in enumerate(zip(prompts, n_prompts, random_seeds)):

            prompt_word, prompt_st, prompt_dy = prompt.split('.', 2)

            # manually set random seed for reproduction
            if random_seed != -1: torch.manual_seed(random_seed)
            else: torch.seed()
            config[model_idx].random_seed.append(torch.initial_seed())
            
            print(f"current seed: {torch.initial_seed()}")
            print(f"sampling {prompt} ...")
            sample = pipeline(
                prompt_st,
                prompt_dy,
                prompt_word,
                negative_prompt     = n_prompt,
                num_inference_steps = model_config.steps,
                guidance_scale      = model_config.guidance_scale,
                width               = model_config.W,
                height              = model_config.H,
                video_length        = model_config.L,

                store_attention = model_config.store_attention,
                savedir = savedir,
            ).videos

            sample = F.interpolate(sample, size=[24,288,512])
            samples.append(sample)

            prompt = "-".join((prompt_st.replace("/", "").split(" ")[:10]))
            save_videos_mp4(sample, f"{savedir}/sample/{sample_idx}-{prompt}.mp4")
            print(f"save to {savedir}/sample/{prompt}.mp4")
            
            sample_idx += 1

    OmegaConf.save(config, f"{savedir}/config.yaml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretrained-model-path", type=str, default="models/StableDiffusion",)
    parser.add_argument("--inference-config",      type=str, default="configs/inference/inference-v1.yaml")    

    parser.add_argument("--unet_checkpoint_path", type=str, default="models/StableDiffusion/unet/unet-checkpoint.ckpt")
    parser.add_argument("--config", type=str, required=True)
    
    
    parser.add_argument("--L", type=int, default=16 )
    parser.add_argument("--W", type=int, default=512)
    parser.add_argument("--H", type=int, default=512)

    parser.add_argument("--disk_store", type=bool, default=False)
    parser.add_argument("--store_attention", type=bool, default=False)

    parser.add_argument("--without-xformers", action="store_true")

    args = parser.parse_args()
    main(args)
