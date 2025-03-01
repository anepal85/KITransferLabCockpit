import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as mpl


class MyFigureCanvas(FigureCanvas):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x, y:list, y_label_name:list) -> None:
        super().__init__(mpl.figure())

        self.x = x 
        self.y = y 
        self.y_label_name = y_label_name
        
        # Store a figure ax
        
        self._ax_ = self.figure.subplots() 
        #self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1]) # added
        
        color = ['blue','green','red','orange','cyan']
        

        if len(self.y)>1 and len(color) >= len(self.y):
            for i, diff_y in enumerate(self.y):
                self._line_, = self._ax_.plot(self.x, diff_y, color[i])
                self._line_.set_label(self.y_label_name[i])
                self._line_.set_ydata(diff_y)

                self._ax_.draw_artist(self._ax_.patch)
                self._ax_.draw_artist(self._line_)

        self._ax_.set_xlabel('Time')
        self._ax_.set_ylabel('Value')
        self._ax_.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
             borderaxespad=0, mode="expand", ncol=len(self.y))
        self.draw()  
        