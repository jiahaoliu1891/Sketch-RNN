import numpy as np
from PIL import Image, ImageDraw

class MetaData():
    def __init__(self, cate):
        self.cate_ = cate
        self.warning_ = True
        self.status_ = 'ABS' # absolute or relative data format

    def disable_warning(self):
        self.warning_ = False
    
    def enable_warning(self):
        self.warning_ = True

    def warn(self, content):
        if self.warning_:
            print(content)

    @property
    def status(self):
        return self.status_
    
    @property
    def cate(self):
        return self.cate_



class Stroke(MetaData):
    def __init__(self, data, cate='UNK', name='NONE'):
        assert data.shape[0] > 1  and data.shape[1] == 2, f"Data shape should be (length > 1, 2), but get {data.shape}"
        
        super().__init__(cate)

        self.data_ = data
        # Cluster Name as the Stroke Name 
        self.name_ = name       
        self.length_ = data.shape[0]
      
    def visualize(self, pil_img=None, canvas=None):
        """
            Visualize the Stroke
            if pil_img is None, create and return the pil_img
        """

        if pil_img is None:
            W, H = 256, 256
            pil_img = Image.new('RGB', (W, H), 'white')
            canvas = ImageDraw.Draw(pil_img)

        abs_data = self.get_absolute()
        __class__.draw_canvas(abs_data, canvas)

        return pil_img, canvas

    @staticmethod
    def draw_canvas(data, canvas, print_points=False):
        assert len(data) > 1 and len(data[0]) == 2 , "Data shape should be (length > 1, 2)"
        
        x, y = data[:, 0], data[:, 1]
        for i in range(1, len(x)):
            # NOTE: abs pos
            line = (x[i-1], y[i-1], x[i], y[i])
            if print_points:
                print(line)
            canvas.line(line, fill=0)

    @property        
    def data(self):
        return self.data_

    def __len__(self):
        return self.length_


class Sketch(MetaData):
    def __init__(self, data):
        self.data_ = [Stroke(s) for s in data]

    def visualize(self, pil_img=None, canvas=None):
        if pil_img is None:
            W, H = 256, 256
            pil_img = Image.new('RGB', (W, H), 'white')
            canvas = ImageDraw.Draw(pil_img)

        for d in self.data_:
            d.visualize(pil_img, canvas)

        return pil_img, canvas
