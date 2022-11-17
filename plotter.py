import codecs
import statistics
from pathlib import Path

import numpy
import numpy as np
import tikzplotlib
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 11})
plt.rc('xtick', labelsize=11)
plt.rc('ytick', labelsize=11)

example_list = [[0, 1], [3, 2], [5, 6], [2, 6], [10, 9]]

# CHANGE DIRECTORY IF NEEDED!!

pathToPlots = "Plots/"

# also check directories for all the saved plots!!! strg + f for "savefig" and "tikzplotlib.save"

# tikzplozlib plotter

def tikzplotlib_plot(name, fig):
    # %%
    filepath = pathToPlots + name + ".tex"
    code = tikzplotlib.get_tikz_code(fig, extra_axis_parameters=[], filepath=filepath)

    ylimpos = code.index("\nymin=") + 5 + 1
    ylimend = code.index(",", ylimpos + 5)
    ylim = code[ylimpos:ylimend]

    ytickpos = code.index("\nytick=") + 1
    ytickend = code.index("}", ytickpos) + 1 + 2  # add +1 for comma, and +1 for newline
    code = code[:ytickpos] + code[ytickend:]

    ytickpos = code.index("\nyticklabels=")
    ytickend = code.index("]", ytickpos)
    code = code[:ytickpos - 1] + "\n" + code[ytickend:]

    code = code \
        .replace(",0) r", "," + ylim + ") r") \
        .replace(",0);", "," + ylim + ");")

    file_handle = codecs.open(filepath, "w")
    file_handle.write(code)
    file_handle.close()


# line plot
def plot1(xylist):
    x = []
    y = []
    for points in xylist:
        x.append(points[0])
        y.append(points[1])
        print("x: " + str(x) + "  y: " + str(y))

    plt.title("Plot 1")
    plt.xlabel("x-Achse")
    plt.ylabel("y-Achse")
    plt.plot(x, y)
    plt.show()
    plt.hist(x)
    plt.show()


# histrogram plot
def create_object_percentage_size_histogram(xlist, dataset):
    # plt.style.use('fivethirtyeight')
    median = statistics.median(xlist)
    mean = statistics.mean(xlist)
    plt.title("Object instances in relation to % size of image" + "\nmedian ≈ " + "{:.2f}".format(
        median) + "%, mean ≈ " + "{:.2f}".format(mean) + "%")
    plt.xlabel("% size of image")
    plt.ylabel("Number of Objects")
    # y achsenabstände
    plt.xticks((10, 20, 30, 40, 50, 60, 70, 80, 90))
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    plt.hist(xlist, bins=bins, edgecolor='black')
    plt.yscale('log')
    # Creating vector pdf plot for easy latex import (problem: font size)
    plt.savefig(pathToPlots + dataset + '/log_object_percentage_size.png')
    plt.savefig(pathToPlots + dataset + '/log_object_percentage_size.pdf')

    # Creating .txt file for manual plotting in latex:
    with open(pathToPlots + dataset + "/percentage_size_text.txt", 'w') as textFile:
        for item in xlist:
            textFile.write(str(item) + "\n")

    # tikzplotlib.save("C:/Users/Dominik/Downloads/plots/tex/" + dataset + "/object_percentage_size.tex")
    plt.show()


'''
def create_area_pixel_histogram(image_list, dataset):
    median = round(statistics.median(image_list))
    mean = round(statistics.mean(image_list))
    plt.title("Object instance segmentation area in pixels" + "\nmedian ≈ " + str(median) + " pixels, mean ≈ " + str(
        mean) + " pixels")
    plt.xlabel("Segmentation area in pixels")
    plt.ylabel("Number of Objects")
    # y achsenabstände
    # plt.xlim(0, max(object_size_list))
    plt.xticks([100000, 200000, 300000, 400000])
    # bins = [0,10000, 100000, 200000, 300000, 400000]
    plt.hist(image_list, bins=200)
    plt.yscale('log')
    plt.savefig(pathToPlots + dataset + '/object_instance_size_in_pixel.pdf')
    plt.savefig(pathToPlots + dataset + '/object_instance_size_in_pixel.png')

    plt.show()
'''


def create_size_comparison_chart(size_comparison, dataset):
    x1 = size_comparison[0] / sum(size_comparison) * 100
    x2 = size_comparison[1] / sum(size_comparison) * 100
    x3 = size_comparison[2] / sum(size_comparison) * 100
    x4 = size_comparison[3] / sum(size_comparison) * 100
    x5 = size_comparison[4] / sum(size_comparison) * 100

    percentages = [x1, x2, x3, x4, x5]
    get_max_percentage = max(percentages)
    print(get_max_percentage)
    ypos = np.arange(len(percentages))
    plt.title(" Size categorization")
    plt.xlabel("Size Categories")
    sizes = ["tiny\n<8x8 px", "very small\n>8x8 &\n <16x16 px", "small\n>16x16 &\n <32x32 px",
             "medium\n>32x32 px &\n <96x96 px", "large\n>96x96 px"]
    plt.ylabel("Percentage of all objects")
    plt.ylim(0, get_max_percentage + 10)
    plt.xticks(ypos, sizes)
    plt.bar(ypos, percentages, edgecolor='black')
    for i in range(len(percentages)):
        plt.text(i, percentages[i] + 0.5, str(("{:.2f}".format(percentages[i]))) + "%", horizontalalignment='center')

    plt.savefig(pathToPlots + dataset + '/size_categorization_' + dataset + '.png')
    plt.savefig(pathToPlots + dataset + '/size_categorization_' + dataset + '.pdf')
    tikzplotlib.save(pathToPlots + dataset + '/size_categorization_' + dataset + '.tex')
    plt.show()


def create_object_size_comparison_chart_imagenet(size_comparison, dataset):
    x1 = size_comparison[0] / sum(size_comparison) * 100
    x2 = size_comparison[1] / sum(size_comparison) * 100
    x3 = size_comparison[2] / sum(size_comparison) * 100
    x4 = size_comparison[3] / sum(size_comparison) * 100
    x5 = size_comparison[4] / sum(size_comparison) * 100
    x6 = size_comparison[5] / sum(size_comparison) * 100
    x7 = size_comparison[6] / sum(size_comparison) * 100
    x8 = size_comparison[7] / sum(size_comparison) * 100

    percentages = [x1, x2, x3, x4, x5, x6, x7, x8]
    get_max_percentage = max(percentages)
    print("Creating Object Size comparison chart. Max. Percentage: ")
    print(get_max_percentage)
    ypos = np.arange(len(percentages))
    plt.title("Object to Image Size comparison for " + dataset)
    plt.xlabel("Percentage of Image Size")
    sizes = ["<1%", "1-5%", "5-10%", "10-25%", "25-50%", "50-75%", "75-90%", ">90%"]
    plt.ylabel("Percentage of objects")
    plt.ylim(0, get_max_percentage + 10)
    plt.xticks(ypos, sizes)
    plt.bar(ypos, percentages, edgecolor='black')
    for i in range(len(percentages)):
        plt.text(i, percentages[i] + 0.5, str(("{:.2f}".format(percentages[i]))) + "%", horizontalalignment='center')

    # Creating vector pdf plot for easy latex import (problem: font size)
    plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.pdf")
    plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.png")
    tikzplotlib.save(filepath=pathToPlots + dataset + "/newdistro/relative object size.tex")
    plt.show()


def create_object_size_comparison_chart_mscoco(size_comparison, dataset):
    x1 = size_comparison[0] / sum(size_comparison) * 100
    x2 = size_comparison[1] / sum(size_comparison) * 100
    x3 = size_comparison[2] / sum(size_comparison) * 100
    x4 = size_comparison[3] / sum(size_comparison) * 100
    x5 = size_comparison[4] / sum(size_comparison) * 100
    x6 = size_comparison[5] / sum(size_comparison) * 100
    x7 = size_comparison[6] / sum(size_comparison) * 100

    percentages = [x1, x2, x3, x4, x5, x6, x7]
    get_max_percentage = max(percentages)
    print("Creating Object Size comparison chart. Max. Percentage: ")
    print(get_max_percentage)
    ypos = np.arange(len(percentages))
    plt.title("Object to Image Size comparison for " + dataset)
    plt.xlabel("Percentage of Image Size")
    sizes = ["<0.1%", "0.1-1%", "1-3%", "3-5%", "5-10%", "10-25%", ">25%"]
    plt.ylabel("Percentage of objects")
    plt.ylim(0, get_max_percentage + 10)
    plt.xticks(ypos, sizes)
    plt.bar(ypos, percentages, edgecolor='black')
    for i in range(len(percentages)):
        plt.text(i, percentages[i] + 0.5, str(("{:.2f}".format(percentages[i]))) + "%", horizontalalignment='center')

    # Creating vector pdf plot for easy latex import (problem: font size)
    Path(pathToPlots + dataset + "/newdistro/").mkdir(parents=True, exist_ok=True)
    plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.pdf")
    plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.png")
    tikzplotlib.save(filepath=pathToPlots + dataset + "/newdistro/relative object size.tex")
    plt.show()


def create_object_size_comparison_chart_tinyperson(size_comparison, dataset):
    x1 = size_comparison[0] / sum(size_comparison) * 100
    x2 = size_comparison[1] / sum(size_comparison) * 100
    x3 = size_comparison[2] / sum(size_comparison) * 100
    x4 = size_comparison[3] / sum(size_comparison) * 100
    x5 = size_comparison[4] / sum(size_comparison) * 100
    x6 = size_comparison[5] / sum(size_comparison) * 100

    percentages = [x1, x2, x3, x4, x5, x6]
    get_max_percentage = max(percentages)
    print("Creating Object Size comparison chart. Max. Percentage: ")
    print(get_max_percentage)
    ypos = np.arange(len(percentages))
    plt.title("Object to Image Size comparison for " + dataset)
    plt.xlabel("Percentage of Image Size")
    sizes = ["<0.01%", "0.01-0.02%", "0.02-0.03%", "0.03-0.04%", "0.04-0.05%", ">0.05%"]
    plt.ylabel("Percentage of objects")
    plt.ylim(0, get_max_percentage + 10)
    plt.xticks(ypos, sizes)
    plt.bar(ypos, percentages, edgecolor='black')
    for i in range(len(percentages)):
        plt.text(i, percentages[i] + 0.5, str(("{:.2f}".format(percentages[i]))) + "%", horizontalalignment='center')

    # Creating vector pdf plot for easy latex import (problem: font size)
    Path(pathToPlots + dataset + "/newdistro/").mkdir(parents=True, exist_ok=True)
    plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.pdf")
    plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.png")
    tikzplotlib.save(filepath=pathToPlots + dataset + "/newdistro/relative object size.tex")
    plt.show()


def create_object_size_comparison_chart(size_comparison, dataset):
    if dataset == "1024a":
        x1 = size_comparison[0] / sum(size_comparison) * 100
        x2 = size_comparison[1] / sum(size_comparison) * 100
        x3 = size_comparison[2] / sum(size_comparison) * 100
        x4 = size_comparison[3] / sum(size_comparison) * 100
        x5 = size_comparison[4] / sum(size_comparison) * 100
        x6 = size_comparison[5] / sum(size_comparison) * 100
        x7 = size_comparison[6] / sum(size_comparison) * 100

        percentages = [x1, x2, x3, x4, x5, x6, x7]
        get_max_percentage = max(percentages)
        print("Creating Object Size comparison chart. Max. Percentage: ")
        print(get_max_percentage)
        ypos = np.arange(len(percentages))
        plt.title("Object to Image Size comparison for " + dataset)
        plt.xlabel("Percentage of Image Size")
        sizes = ["<0.01%", "0.01-0.015%", "0.015-0.02%", "0.02-0.025%", "0.025-0.03%", "0.03-0.035%", ">0.035%"]
        plt.ylabel("Percentage of objects")
        plt.ylim(0, get_max_percentage + 10)
        plt.xticks(ypos, sizes)
        plt.bar(ypos, percentages, edgecolor='black')
        for i in range(len(percentages)):
            plt.text(i, percentages[i] + 0.5, str(("{:.2f}".format(percentages[i]))) + "%",
                     horizontalalignment='center')

        # Creating vector pdf plot for easy latex import (problem: font size)
        Path(pathToPlots + dataset + "/newdistro/").mkdir(parents=True, exist_ok=True)
        plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.pdf")
        plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.png")
        tikzplotlib.save(filepath=pathToPlots + dataset + "/newdistro/relative object size.tex")
        plt.show()
    else:
        x1 = size_comparison[0] / sum(size_comparison) * 100
        x2 = size_comparison[1] / sum(size_comparison) * 100
        x3 = size_comparison[2] / sum(size_comparison) * 100
        x4 = size_comparison[3] / sum(size_comparison) * 100
        x5 = size_comparison[4] / sum(size_comparison) * 100
        x6 = size_comparison[5] / sum(size_comparison) * 100
        x7 = size_comparison[6] / sum(size_comparison) * 100

        percentages = [x1, x2, x3, x4, x5, x6, x7]
        get_max_percentage = max(percentages)
        print("Creating Object Size comparison chart. Max. Percentage: ")
        print(get_max_percentage)
        ypos = np.arange(len(percentages))
        plt.title("Object to Image Size comparison for " + dataset)
        plt.xlabel("Percentage of Image Size")
        sizes = ["<0.02%", "0.02-0.04%", "0.04-0.06%", "0.06-0.08%", "0.08-0.1%", "0.1-0.12%", ">0.12%"]
        plt.ylabel("Percentage of objects")
        plt.ylim(0, get_max_percentage + 10)
        plt.xticks(ypos, sizes)
        plt.bar(ypos, percentages, edgecolor='black')
        for i in range(len(percentages)):
            plt.text(i, percentages[i] + 0.5, str(("{:.2f}".format(percentages[i]))) + "%",
                     horizontalalignment='center')

        # Creating vector pdf plot for easy latex import (problem: font size)
        Path(pathToPlots + dataset + "/newdistro/").mkdir(parents=True, exist_ok=True)
        plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.pdf")
        plt.savefig(pathToPlots + dataset + "/newdistro/relative object size.png")
        tikzplotlib.save(filepath=pathToPlots + dataset + "/newdistro/relative object size.tex")
        plt.show()


def create_bbox_size_comparison_chart(xlist, dataset):
    # plt.style.use('fivethirtyeight')
    median = statistics.median(xlist)
    mean = statistics.mean(xlist)
    plt.title("Object segmentation area in % relation to bounding box size" + "\nmedian ≈ " + "{:.2f}".format(
        median) + "%, mean ≈ " + "{:.2f}".format(mean) + "%")
    plt.xlabel("% size of bounding box")
    plt.ylabel("Number of Objects")
    # y achsenabstände
    plt.xticks((10, 20, 30, 40, 50, 60, 70, 80, 90))
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    plt.hist(xlist, bins=bins, edgecolor='black')
    plt.yscale('log')
    plt.savefig(pathToPlots + dataset + '/bbox_comparison.pdf')
    plt.savefig(pathToPlots + dataset + '/bbox_comparison.png')
    plt.show()


def destribution_heatmap(imageList):
    for image in imageList:
        width = image.get_width()
        height = image.get_height()
        tempXdiv = width / 300
        tempYdiv = height / 300
        for obj in image.get_object_instances():
            bbox = obj.get_bbox()
            bbox_startX = bbox[0] / tempXdiv
            bbox_startY = bbox[1] / tempYdiv
            bbox_endX = bbox_startX + bbox[2] / tempXdiv
            bbox_endY = bbox_startY + bbox[3] / tempYdiv
            bbox_width = bbox[2] / tempXdiv
            bbox_height = bbox[3] / tempYdiv

            newBbox = [bbox]

    print()


def create_object_position_heatmap(xlist, dataset, keyword):
    sum = numpy.sum(xlist)
    # print("Heatmap Elemente eingelesen:")
    # print(sum)
    vegetables = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
    farmers = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]
    harvest = np.array(xlist)
    fig, ax = plt.subplots()
    im = ax.imshow(harvest, cmap="YlOrRd")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(farmers)))
    ax.set_yticks(np.arange(len(vegetables)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(farmers)
    ax.set_yticklabels(vegetables)
    # plt.axis('off')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), ha="center", )

    # Loop over data dimensions and create text annotations.

    for i in range(len(vegetables)):
        for j in range(len(farmers)):
            text = ax.text(j, i, harvest[i, j],
                           ha="center", va="center", color="black")

    # ax.set_title("Object Distribution on Image for " + dataset)
    fig.tight_layout()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig(pathToPlots + dataset + "/" + keyword + " object distribution on image.pdf",
                bbox_inches='tight',
                pad_inches=0)
    plt.savefig(pathToPlots + dataset + "/" + keyword + " object distribution on image.png",
                bbox_inches='tight',
                pad_inches=0)
    plt.show()


def create_bbox_heatmap(xlist, dataset, keyword):
    sum = numpy.sum(xlist)
    # print("Heatmap Elemente eingelesen:")
    # print(sum)
    vegetables = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
    farmers = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]
    harvest = np.array(xlist)
    fig, ax = plt.subplots()

    im = ax.imshow(harvest, cmap="YlOrRd")

    # Create colorbar
    ax.figure.colorbar(im, ax=ax)
    ax.set_ylabel("", rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(farmers)))
    ax.set_yticks(np.arange(len(vegetables)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(farmers)
    ax.set_yticklabels(vegetables)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), ha="center", )

    # Loop over data dimensions and create text annotations.
    for i in range(len(vegetables)):
        for j in range(len(farmers)):
            text = ax.text(j, i, harvest[i, j],
                           ha="center", va="center", color="black")

    ax.set_title("Object Distribution on Image for " + dataset)
    fig.tight_layout()
    plt.savefig(pathToPlots + dataset + "/" + keyword + " bbox distribution on image.pdf")
    plt.savefig(pathToPlots + dataset + "/" + keyword + " bbox distribution on image.png")
    plt.show()


def no_axis_bbox_heatmap(xlist, dataset, keyword):
    sum = numpy.sum(xlist)
    # print("Heatmap Elemente eingelesen:")
    # print(sum)
    vegetables = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
    farmers = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]
    harvest = np.array(xlist)
    fig, ax = plt.subplots()
    im = ax.imshow(harvest, cmap="YlOrRd")
    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.tick_params(labelsize=15)
    # ax.set_ylabel("legendenbeschriftung", rotation=-90, va="bottom")

    # plt.axis('off')

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(farmers)))
    ax.set_yticks(np.arange(len(vegetables)))
    # ... and label them with the respective list entries

    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.tight_layout()
    plt.savefig(pathToPlots + dataset + "/" + keyword + " clean bbox distribution on image.pdf",
                bbox_inches='tight',
                pad_inches=0)
    plt.savefig(pathToPlots + dataset + "/" + keyword + " clean bbox distribution on image.png",
                bbox_inches='tight',
                pad_inches=0)
    plt.show()


def create_width_height_plot(list, keyword, dataset):
    median = round(statistics.median(list))
    mean = round(statistics.mean(list))
    plt.title("Bounding Box " + keyword + " pixel overview" + "\nmedian = " + str(median) + " pixels, mean = " + str(
        mean) + " pixels")
    plt.xlabel("object instance bounding box " + keyword)
    plt.ylabel("number of objects")
    plt.hist(list, bins=200)
    plt.yscale('log')
    plt.savefig(pathToPlots + dataset + '/boundingbox_' + keyword + '.pdf')
    plt.savefig(pathToPlots + dataset + '/boundingbox_' + keyword + '.png')
    tikzplotlib.save(filepath=pathToPlots + dataset + '/boundingbox_' + keyword + '.tex')
    plt.savefig(pathToPlots + dataset + '/boundingbox_' + keyword + '.svg', format="svg")
    plt.show()


def create_bbox_size_plot(list, dataset):
    median = round(statistics.median(list))
    mean = round(statistics.mean(list))
    plt.title("Bounding Box size overview" + "\nmedian = " + str(median) + " pixels, mean = " + str(
        mean) + " pixels")
    plt.xlabel("object instance bounding box")
    plt.ylabel("number of objects")
    plt.hist(list, bins=200)
    plt.yscale('log')
    plt.savefig(pathToPlots + dataset + '/boundingbox_size_overview.pdf')
    plt.savefig(pathToPlots + dataset + '/boundingbox_size_overview.png')
    tikzplotlib.save(filepath=pathToPlots + dataset + '/boundingbox_size_overview.tex')
    plt.savefig(pathToPlots + dataset + '//boundingbox_size_overview.svg', format="svg")
    plt.show()
