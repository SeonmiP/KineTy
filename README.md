<h1 align="center">Kinetic Typography Diffusion Model</h1>
<p align="center">
  <a href="https://scholar.google.com/citations?user=_jdAVpYAAAAJ"><strong>Seonmi Park</strong></a>
  ·  
  <a href="https://InhwanBae.github.io/"><strong>Inhwan Bae</strong></a>
  ·
  <a href="https://scholar.google.com/citations?user=o1kcenYAAAAJ"><strong>Seunghyun Shin</strong></a>
  ·
  <a href="https://scholar.google.com/citations?user=Ei00xroAAAAJ"><strong>Hae-Gon Jeon</strong></a>
  <br>
  ECCV 2024
</p>

<p align="center">
  <a href="https://seonmip.github.io/kinety"><strong><code>Project Page</code></strong></a>
  <a href="https://link.springer.com/chapter/10.1007/978-3-031-72754-2_10"><strong><code>ECCV Paper</code></strong></a>
  <a href="https://arxiv.org/abs/2407.10476"><strong><code>arXiv</code></strong></a>
  <a href="https://github.com/SeonmiP/KineTy/blob/main/dataset_construction/README.md"><strong><code>Dataset</code></strong></a>
</p>

<div align='center'>
  <br><img src="https://github.com/SeonmiP/KineTy/blob/main/img/edit.gif" width=70%>
  <br>Example of our generated videos.
</div>

## Source Code

We provide source codes of our KineTy model. Details are as follows.

### 🏢 Installation

#### Setup conda environment

```
git clone https://github.com/SeonmiP/KineTy.git
cd KineTy
conda env create -f environment.yaml
conda activate kinety
```

#### Download Stable Diffusion V1.5

```
git lfs install
git clone https://huggingface.co/runwayml/stable-diffusion-v1-5 models/StableDiffusion/
```

### 💾 Dataset
We provide how to make dataset [here](https://github.com/SeonmiP/KineTy/blob/main/dataset_construction)


### ⚽ Training
We trained our code on a machine with 8 NVIDIA A100 GPU.

```
torchrun --nnodes=1 --nproc_per_node=1 train.py --config configs/train.yaml
```


### 🎨 Inference
Our code is executed on an NVIDIA A100 GPU, but we also check if it runs on an NVIDIA GeForce 3090 Ti.

```
python -m inference --config configs/inference.yaml
```


## Acknowledgements
Part of our code is built upon [AnimateDiff](https://github.com/guoyww/AnimateDiff/tree/main) and [Tune-a-Video](https://github.com/showlab/Tune-A-Video). The visualization of the attention map refers to [FateZero](https://github.com/ChenyangQiQi/FateZero/tree/main) and [prompt-to-prompt](https://github.com/google/prompt-to-prompt/). Thanks to the authors for sharing their works.
