import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap

class CustomPlot:
    def __init__(self, title="Data Analysis", xlabel="X-axis", ylabel="Y-axis"):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def plot_line(self, x, y, label="Data"):
        self.ax.plot(x, y, label=label)

    def plot_bar(self, height, label=None, show_numbers=False, 
                map_max_space=1, cmap='winter', percentage=False, **kwargs):
        cmap = get_cmap(cmap)
        colors = cmap(np.linspace(0, map_max_space, len(height)))

        for index, value in enumerate(height):
            self.ax.bar(index, value, color=colors[index], **kwargs)

            if show_numbers:
                self._annotate_bar(value, index, colors[index], percentage)

        self._configure_axes(len(height))

        if not label is None:
            self.ax.set_xticklabels(label, rotation=45)


    def histogram_plot(self, values, title="Histogram", **kwargs):
        bins = kwargs.pop("bins", None)
        self.ax.hist(values, bins=bins, **kwargs)
        self.ax.set_title(title)

    def ax_legend_settings(self, **kwargs):
        self.ax.legend(**kwargs)

    def show_plot(self):
        plt.show()

    def save_plot(self, filename="plot.png"):
        self.fig.savefig(filename)

    def plot_pie(self, value, labels, show_numbers=False, autopct='%.2f%%'):
        if show_numbers:
            self.ax.pie(value, labels=labels, autopct=autopct)
        else:
            self.ax.pie(value, labels=labels)

    def _annotate_bar(self, value, index, color, percentage):
        if percentage:
            text = f'{value:.2f}%'
        else:
            text = str(value)
        self.ax.text(index, value, text, ha='center', va='bottom', color=color)

    def _configure_axes(self, num_heights):
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.ax.set_xticklabels(range(num_heights), rotation=45)
        self.ax.set_xticks(range(num_heights))

    def plot_histogram_non_numeric_data(self, data):
        counts = {}
        for item in data:
            counts[item] = counts.get(item, 0) + 1
        self.ax.bar(counts.keys(), counts.values())
        
