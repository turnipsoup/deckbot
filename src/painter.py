import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from . import setup_logger

logger = setup_logger.logger


class Painter:
    def __init__(self, maketype, paintdata):
        self.maketype = maketype
        self.paintdata = paintdata

        