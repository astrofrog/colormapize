import click
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap


COLORMAP_TEMPLATE_CODE = """
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import register_cmap

cdict = {cdict}

cmap = LinearSegmentedColormap('{cmap_name}', segmentdata=cdict, N=256)
register_cmap(name='{cmap_name}', cmap=cmap)
"""


class ImageColormapMaker:

    def __init__(self, image_file, cmap_name):

        self.image_file = image_file
        self.cmap_name = cmap_name

        image = Image.open(image_file)
        self.image_array = np.array(image)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.imshow(self.image_array)

        self.line = self.ax.plot([], [], 'o-')[0]

        self.x_values = []
        self.y_values = []
        self.n_values = 2

        self.colorbar = None

        self.fig.canvas.mpl_connect('button_press_event', self.button_press)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)

        plt.show()

    def button_press(self, event):

        if event.inaxes and self.fig.canvas.manager.toolbar._active is None:

            if len(self.x_values) >= 2:
                print("Resetting line")
                self.x_values.clear()
                self.y_values.clear()

            x, y = event.xdata, event.ydata
            print(f"Adding point at ({x},{y})")
            self.x_values.append(x)
            self.y_values.append(y)

            self.refresh_line()

    def get_xy(self):
        x = np.linspace(self.x_values[0], self.x_values[1], self.n_values)
        y = np.linspace(self.y_values[0], self.y_values[1], self.n_values)
        return x, y

    def refresh_line(self):

        if len(self.x_values) < 2:
            return

        x, y = self.get_xy()

        self.line.set_xdata(x)
        self.line.set_ydata(y)

        self.fig.canvas.draw()

    def key_press(self, event):
        if event.key == '+':
            self.n_values += 1
            self.refresh_line()
        elif event.key == '-' and self.n_values > 2:
            self.n_values -= 1
            self.refresh_line()
        elif event.key == 'enter':
            x, y = self.get_xy()
            x, y = x.astype(int), y.astype(int)
            colors = self.image_array[y, x, :]
            r, g, b = [], [], []

            for i in range(len(x)):
                frac = i / (len(x) - 1)
                r.append([frac, colors[i][0] / 255., colors[i][0] / 255.])
                g.append([frac, colors[i][1] / 255., colors[i][1] / 255.])
                b.append([frac, colors[i][2] / 255., colors[i][2] / 255.])

            cdict = {'red': r, 'green': g, 'blue': b}

            cmap = LinearSegmentedColormap('filename', segmentdata=cdict, N=256)

            s = self.ax.scatter([], [], c=[], cmap=cmap, vmin=0, vmax=1)
            if self.colorbar is None:
                self.colorbar = self.fig.colorbar(s)
            else:
                self.colorbar.on_mappable_changed(s)

            self.fig.canvas.draw()

            with open('cmap_' + self.cmap_name + '.py', 'w') as f:
                f.write(COLORMAP_TEMPLATE_CODE.format(cdict=cdict, cmap_name=self.cmap_name))

            print('Colorbar written to cmap_' + self.cmap_name + '.py')


@click.command()
@click.argument('image_file')
@click.argument('cmap_name')
def main(image_file, cmap_name):
    ImageColormapMaker(image_file, cmap_name)


plt.show()
