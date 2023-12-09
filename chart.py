import matplotlib.pyplot as plt
import os


class Chart:
    def __init__(self, title):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)
        self.x = []

    def set_x(self, x):
        self.x = x

    def add_elements(self, y, color, label):
        self.ax.plot(self.x, y, color, label=label)

    def show(self):
        self.ax.legend(loc='upper right')
        self.fig.show()

    def save_image(self, image):
        self.ax.legend(loc='upper right')
        image_dir = 'images'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_path = f"{image_dir}/{image}.png"
        self.fig.savefig(image_path)
        return image_path
