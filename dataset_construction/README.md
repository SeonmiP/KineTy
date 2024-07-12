<h2 align="center">Kinetic Typography Diffusion Model</h2>
<h3 align="center">Instruction for the dataset construction</h3>

<br>
Here, we will explain how to construct the kinetic typography dataset. Due to the IP license issues of the templates, we provide a source code for a post-processing and video rendering.

## Preliminaries
To construct the dataset, you need to subscribe to the Adobe After Effects program, as our dataset is constructed using Adobe After Effects templates.

### Adobe After Effect
You can subscribe to the software here: [Adobe After Effect](https://www.adobe.com/products/aftereffects.html).


### Nexrender
We use only 'nexrender-cli-win64.exe' from [Nexrender Installation link](https://github.com/inlife/nexrender/releases). This is for window and we use version 1.46.6. For more information, you can find here: [Nexrender](https://github.com/inlife/nexrender)


### Templates
We will provide you with templates, but you can download more templates from the site below.

- [MotionArray](https://motionarray.com/)
- [Artlist](https://artlist.io/)
- [EnvatoElement](https://elements.envato.com/)
- [Pixflow](https://pixflow.net/)
- [Videohive](https://videohive.net/)
- [motion elements](https://www.motionelements.com/ko/)



## Settings for Running Code

### Text

Write down the words you want to print out in the video to [word.csv](https://github.com/SeonmiP/KineTy/blob/main/dataset_construction/word.csv)

### Video setting

Edit rendering information such as resolution and frame number in [basic_rendering_info.json](). You can add or change the other elements in reference to [Nexrender](https://github.com/inlife/nexrender).

### Template setting
Record the below information in [template_info.csv](https://github.com/SeonmiP/KineTy/blob/main/dataset_construction/template_info.csv).
- id: just a number of the template
- template_name: template file name
- composition_name: a composition name what you want to render
- composition_text: the composition name where the text layer is
- layer_text: a text layer name which has a 'source text'


## Video Rendering

For using nexrender:
```sh
pip install ffmpeg
```

Then, set your path to dataset construction folder in [render_set.py](https://github.com/SeonmiP/KineTy/blob/main/dataset_construction/render_set.py):
```
# Path to your project folder
basedir = "~~~/dataset_construction"
```

Lastly, designate your path to nexrender software and aerender software in [render.py](https://github.com/SeonmiP/KineTy/blob/main/dataset_construction/render.py):
```
# Path to your nexrender-cli-win64.exe
nexrender_cli_path = "~~~\\nexrender-cli-win64.exe"

# Path to your Adobe After Effects aerender.exe
aerender_path = "~~~\\aerender.exe"
```

Prepare [rendering information](https://github.com/SeonmiP/KineTy/tree/main/dataset_construction#settings-for-running-code) with each video:
```sh
python render_set.py
```

Render the template:
```sh
python render.py
```


