import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging

class Painter:
    def __init__(self, maketype, paintdata):
        self.maketype = maketype
        self.paintdata = paintdata

        