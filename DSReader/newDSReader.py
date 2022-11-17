import json
import random
from pathlib import Path

import cv2
from matplotlib import pyplot as plt

from PIL import Image
#from ObjectInstance import ObjectInstance
from ..eval import display_result, avg_object_size_from_bbox, get_object_size_comparison, get_percentage_object_sizes, \
    get_size_comparison, get_bbox_width_and_height_list, get_object_position_distribution, \
    get_percentage_object_position_distribution, get_object_distribution_new, get_total_object_sizes, \
    get_object_size_comparison_for_newDS
from ..plotter import create_object_percentage_size_histogram, create_object_size_comparison_chart_tinyperson, \
    create_object_size_comparison_chart_mscoco, create_object_size_comparison_chart_imagenet, \
    create_size_comparison_chart, create_width_height_plot, create_object_position_heatmap, no_axis_bbox_heatmap, \
    create_bbox_heatmap, create_bbox_size_plot, create_object_size_comparison_chart


def load_example_picture():
    # Select Picture and draw Bounding Boxes
    # logger.info("Trying to open Example Image at:")
    # logger.info(random_image.get_location())

    """
    # Get Information for file (Debug)
    wantedImg = 'n04074963_2603.jpeg'

    for img in image_list:
        if img.get_filename() == wantedImg:
            logger.info("Bild: " + wantedImg)
            logger.info("Anzahl Objekte: " + str(img.get_object_amount()))
            # random_image = img
    """
    random_image = random.choice(image_list)
    location = random_image.get_location()
    filename = random_image.get_filename()

    try:
        # Careful!! Change directory if needed!!

        color_img = cv2.imread(location + "train/images/" + filename, 1)
        # Iterate through object instances of selected Image
        for obj in random_image.get_object_instances():
            bbox = obj.get_bbox()
            # Mark beginning and end of bounding box
            startX = int(bbox[0])
            startY = int(bbox[1])
            endX = startX + int(bbox[2])  # width
            endY = startY + int(bbox[3])  # height
            # choose bounding box color (in this case random)
            random_rgb = [255, 0, 0]
            random.shuffle(random_rgb)
            # draw bounding box
            cv2.rectangle(color_img, (startX, startY), (endX, endY), random_rgb, 2)

        # select picture
        plt.imshow(cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        # show picture via matplotlib pyplot
        plt.savefig('/Plots/' + dataset + '/example_picture.png',
                    bbox_inches='tight',
                    pad_inches=0)
        plt.savefig('/Plots/' + dataset + '/example_picture.pdf',
                    bbox_inches='tight',
                    pad_inches=0)
        plt.show()
    except:
        print("")

    try:
        color_img = cv2.imread(location + "test/images/" + filename, 1)
        # Iterate through object instances of selected Image
        for obj in random_image.get_object_instances():
            bbox = obj.get_bbox()
            # Mark beginning and end of bounding box
            startX = int(bbox[0])
            startY = int(bbox[1])
            endX = startX + int(bbox[2])  # width
            endY = startY + int(bbox[3])  # height
            # choose bounding box color (in this case random)
            random_rgb = [255, 0, 0]
            random.shuffle(random_rgb)
            # draw bounding box
            cv2.rectangle(color_img, (startX, startY), (endX, endY), random_rgb, 2)

        # select picture
        plt.imshow(cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        # show picture via matplotlib pyplot
        # Careful!! Change directory if needed!!

        plt.savefig('/Plots/' + dataset + '/example_picture.png',
                    bbox_inches='tight',
                    pad_inches=0)
        plt.savefig('/Plots/' + dataset + '/example_picture.pdf',
                    bbox_inches='tight',
                    pad_inches=0)
        plt.show()
    except:
        print("")

    try:
        color_img = cv2.imread(location + "val/images/" + filename, 1)
        # Iterate through object instances of selected Image
        for obj in random_image.get_object_instances():
            bbox = obj.get_bbox()
            # Mark beginning and end of bounding box
            startX = int(bbox[0])
            startY = int(bbox[1])
            endX = startX + int(bbox[2])  # width
            endY = startY + int(bbox[3])  # height
            # choose bounding box color (in this case random)
            random_rgb = [255, 0, 0]
            random.shuffle(random_rgb)
            # draw bounding box
            cv2.rectangle(color_img, (startX, startY), (endX, endY), random_rgb, 2)

        # select picture
        plt.imshow(cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        # show picture via matplotlib pyplot
        plt.savefig('/Plots/' + dataset + '/example_picture.png',
                    bbox_inches='tight',
                    pad_inches=0)
        plt.savefig('/Plots/' + dataset + '/example_picture.pdf',
                    bbox_inches='tight',
                    pad_inches=0)
        plt.show()
    except:
        print("")
def createPlots():
    # get_percentage_object_sizes(image_object_list)
    create_object_percentage_size_histogram(get_percentage_object_sizes(image_list, dataset), dataset)

    object_size = get_object_size_comparison(get_percentage_object_sizes(image_list, dataset), dataset)
    if dataset == "tinyperson":
        create_object_size_comparison_chart_tinyperson(object_size, dataset)
    elif dataset == "coco":
        create_object_size_comparison_chart_mscoco(object_size, dataset)
    elif dataset == "imagenet" or dataset == "imagenet_Dummy" or dataset == "pascalvoc":
        create_object_size_comparison_chart_imagenet(object_size, dataset)

    size_comparison = get_size_comparison(image_list)
    create_size_comparison_chart(size_comparison, dataset)

    # zeigt relation zwischen number of objects (y achse) und (object instance height/width in pixeln)
    width_height_list = get_bbox_width_and_height_list(image_list, dataset)
    create_width_height_plot(width_height_list[0], "width", dataset)
    create_width_height_plot(width_height_list[1], "height", dataset)

    bbox_size_list = get_total_object_sizes(image_list)
    create_bbox_size_plot(bbox_size_list, dataset)

    object_size = get_object_size_comparison_for_newDS(get_percentage_object_sizes(image_list, dataset), dataset)
    create_object_size_comparison_chart(object_size, dataset)

    # Verteiltungsheatmap basierend auf Zentrum der Bounding Boxen!!!

    # zeigt "totale" verteilung der objekte auf dem bild an (9 tiles -> konkrete objektanzahl pro Tile))
    total_distribution_bboxcenter = get_object_position_distribution(image_list)
    create_object_position_heatmap(total_distribution_bboxcenter, dataset, "total")
    # by bbox center ohne beschriftung
    no_axis_bbox_heatmap(total_distribution_bboxcenter, dataset, "bbox_center")

    # zeigt prozentuale verteilung der objekte auf dem bild an (9 tiles -> konkrete objektanzahl pro Tile/gesamtzahl d objekte))
    percentage_distribution_bboxcenter = get_percentage_object_position_distribution(image_list)
    create_object_position_heatmap(percentage_distribution_bboxcenter, dataset, "percentage")

    # Verteilungsheatmap basierend auf gesamter Bounding Box!!
    arr = get_object_distribution_new(image_list)
    print(arr)

    # Plotten jeweils mit und ohne Beschriftungen
    create_bbox_heatmap(arr, dataset, "complete bbox")
    no_axis_bbox_heatmap(arr, dataset, "complete bbox")


# which dataset would you like to import
dataset = "TASODv1"
# which dataset split would you like to import
dataset_splits = ["train", "val", "test"]

# Create empty list for incoming Objects from json/xml file
image_list = []
# Create dictionary for identification (list position <-> image id)
keystore = {}
for split in dataset_splits:
    # path to dataset i.e. "E:/newDS/images_" + dataset + "/" + split +  "/annotation.json"
    # Careful!! Change directory if needed!!

    dataset_path = "/" + dataset + "/" + split + "/annotation.json"
    print("Loading Dataset from " + dataset_path)
    # Select Json file
    with open(dataset_path) as json_file:
        # Load Json file
        data = json.load(json_file)
        # Iterate through all 'images' in json file
        for p in data['images']:
            # Create Image Object and add to object list
            image_list.append(
                Image(p['id'], p['file_name'], p['height'], p['width'],
                      'E:/newDS/images_' + dataset + '/',
                      p['dataset-source'], p['license']))
            # Save List position and Image ID in dictionary
            keystore[p['id']] = len(image_list) - 1

        for a in data['annotations']:
            # Create to ObjectInstance
            new_object_instance = ObjectInstance(a['id'], [], a['bbox'], a['image id'],
                                                 a['category'], a['category_id'], '')
            parent_image = image_list.__getitem__(keystore.get(a['image id']))
            # Map ObjectInstance to Image (Parent)
            parent_image.add_object_instance(new_object_instance)

print("Overall Image Information:")
result = avg_object_size_from_bbox(image_list)
display_result(result, dataset)

# %%
# Careful!! Change directory if needed!!

Path("/Plots/" + dataset).mkdir(parents=True, exist_ok=True)
Path("/Errors/" + dataset).mkdir(parents=True, exist_ok=True)

createPlots()


# %%
load_example_picture()
