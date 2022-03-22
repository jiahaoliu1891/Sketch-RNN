import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import pickle 
from utils import convert_to_PIL

def load_file(filepath):
    """
        Load a .ndjson file from the input filepath
        Return category name and list of sketches
    """
    df = pd.read_json(filepath, lines=True)
    category = df.iloc[0]['word']
    sketches = df['drawing']
    sketch_list = []

    for i, sketch in enumerate(sketches):
        # Map the list data into numpy array
        # NOTE: shape of each stroke array: (2, stroke_lenght)
        sketch_np = list(map(lambda stroke: np.array(stroke), sketch))
        sketch_list.append(sketch_np)

    return category, sketch_list


def test_load_file():
    DATA_ROOT = os.path.join(os.path.abspath('./'), 'data')
    origin_data_path = os.path.join(DATA_ROOT, 'origin')
    example_filepath = os.path.join(origin_data_path, 'example.ndjson')
    category, sketch_list = load_file(example_filepath)
    print(f'------ CATEGORY:{category} ------')
    # random select a skecth
    i_sketch = 2
    sketch = sketch_list[i_sketch]
    print(f'# Select {i_sketch}th Sketch')
    print(f'# Number of Strokes: {len(sketch)}')
    # random select a stroke from the sketch
    i_stroke = 0    
    stroke = sketch[i_stroke]
    print(f'# {i_stroke}th Stroke:\n{stroke}')
    print(f'# Shape of {i_stroke}th Stroke: {stroke.shape}')



def load_data_to_numpy(origin_path, numpy_path):
    """
        Load original data and convert it into numpy array 
    """
    
    if not os.path.exists(origin_path):
        print(f'{origin_path} not exists!')
        assert False

    if not os.path.exists(numpy_path):
        print(f'{numpy_path} not exists!')
        assert False
        
    print('Start Converting data into numpy format...')

    for filename in tqdm(list(os.listdir(origin_path))):
        filepath = os.path.join(origin_path, filename)
        category, sketch_list = load_file(filepath)
        with open(f'{numpy_path}/{category}.npy', 'wb') as f:
            pickle.dump(sketch_list, f)

def test_load_data_to_numpy():
    DATA_ROOT = os.path.join(os.path.abspath('./'), 'data')
    origin_path = os.path.join(DATA_ROOT, 'origin')
    numpy_path = os.path.join(DATA_ROOT, 'numpy')
    load_data_to_numpy(origin_path, numpy_path)


if __name__ == '__main__':
    # test_load_data_to_numpy()
    DATA_ROOT = os.path.join(os.path.abspath('./'), 'data')
    numpy_path = os.path.join(DATA_ROOT, 'numpy')
    with open(f'{numpy_path}/brain.npy', 'rb') as f:
        brain_list = pickle.load(f)
        # select first brain in the list
        brain = brain_list[0]
        pil_img = convert_to_PIL(brain)
        pil_img.show()
