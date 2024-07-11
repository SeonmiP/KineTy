import os
import json



################ Set your path ################

# Path to your project folder
basedir = "~~~/dataset_construction"

################################################



basic_json_file = "basic_rendering_info.json"
text_names = open("word.csv", 'r')
file_settings = open("template_info.csv", 'r')

word_bags = []
for text in text_names:
    word_bags.append(text.rstrip())
# print("Number of Words:", len(word_bags))

lines = file_settings.readlines()
line_name = lines[0].strip().split(',') # id, template_name, composition_name, composition_text, layer_text
line_value = [line.strip().split(',') for line in lines[1:]]
# line_num = len(line_value)
# print("Number of Template:", line_num)

with open(basic_json_file) as json_file:
    json_data = json.load(json_file)

# Set a rendering information by utilizing 'basic_rendering_info.json'
for line in line_value:
    id, template_name, composition_name, composition_text, layer_text = line
    id = int(id)

    os.makedirs(f"./Rendering_info", exist_ok=True)
    os.makedirs(f"{basedir}/video/{id:04d}", exist_ok=True)

    # Set the rendering information
    json_data['template']['src'] = f"file:///{basedir}/template/{template_name}.aep"  # Set the path of the template
    json_data['template']['composition'] = composition_name  # Composition name of the kinetic typography template
    json_data['assets'][0]['composition'] = composition_text    # Composition name of the text box
    json_data['assets'][0]['layerName'] = layer_text    # layer name of the text box

    for k, word in enumerate(word_bags):

        # The text you want to print
        json_data['assets'][0]['value'] = word

        # Set output path of the video with the video name
        json_data['actions']['postrender'][1]['output'] = f"{basedir}/video/{id:04d}/{k:02d}.mp4"
        temp_json = f'./Rendering_info/{id:04d}_{k:02d}.json'

        # Save the rendering information in the json file
        with open(temp_json, "w") as temp_file:
            json.dump(json_data, temp_file)