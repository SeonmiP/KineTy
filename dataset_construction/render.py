import os
import multiprocessing
import natsort
import json



################ Set your path ################

# Path to your nexrender-cli-win64.exe
nexrender_cli_path = "~~~\\nexrender-cli-win64.exe"

# Path to your Adobe After Effects aerender.exe
aerender_path = "~~~\\aerender.exe"

################################################



def execute_command(json_file):

    with open(json_file) as jf:
        json_data = json.load(jf)
    
    if os.path.exists(json_data['actions']['postrender'][1]['output']):
        # If the video is already rendered
        print('already rendered:', json_data['actions']['postrender'][1]['output'])
        return
    else:
        # Render the video
        command = f"{nexrender_cli_path} --file {json_file} --binary=\"{aerender_path}\""
        os.system(command)


def main():

    json_files = [f'./Rendering_info/{ff}' for ff in sorted(os.listdir(f'./Rendering_info'))]  # Replace with your JSON file names
    json_files = natsort.natsorted(json_files)

    # Create a pool of workers equal to the number of CPU cores
    pool = multiprocessing.Pool(processes=2)

    # Map the execution function to the list of json files
    # This will distribute the execution of the command across multiple processes
    pool.map(execute_command, json_files)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()