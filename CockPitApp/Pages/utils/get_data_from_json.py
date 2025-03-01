import json 
import os 

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

PATH = os.path.join(parent_dir, 'Data', 'wood_25_01_2023_v2', 'data_1hz_full_speed') # "../Data/wood_25_01_2023_v2/data_1hz_full_speed/"


#PATH = "D:/Users/Tim/tubCloud/Shared/2022_23 WiSe KI Transferlabor 2/06 Daten/data_1hz_full_speed"
fileName = 'data.json'

def get_json_as_list():

    with open(os.path.join(PATH, fileName), "r") as read_file:
        data = json.load(read_file)
        measurements_list = data['measurements']
    return measurements_list

if __name__ == "__main__":
    print(get_json_as_list())
        
