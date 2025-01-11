from typing import Optional, Union, Tuple, List, Dict
import abc
import numpy as np
import copy
from einops import rearrange

import torch
import torch.nn.functional as F

from kinety.prompt_attention.attention_store import AttentionStore, AttentionControl
from kinety.prompt_attention.attention_register import register_attention_control
from kinety.prompt_attention.visualization import show_cross_attention, show_self_attention_comp





class EmptyControl:
    
    
    def step_callback(self, x_t):
        return x_t
    
    def between_steps(self):
        return
    
    def __call__(self, attn, is_cross: bool, place_in_unet: str):
        return attn