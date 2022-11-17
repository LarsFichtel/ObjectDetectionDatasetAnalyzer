import json
import random
from pathlib import Path

import cv2
import psycopg2
from matplotlib import pyplot as plt
import tqdm

from Image import Image
from ObjectInstance import ObjectInstance
from eval import display_result, avg_object_size_from_bbox, get_object_size_comparison, get_percentage_object_sizes, \
    get_size_comparison, get_bbox_width_and_height_list, get_object_position_distribution, \
    get_percentage_object_position_distribution, get_object_distribution_new, get_total_object_sizes
from plotter import create_object_percentage_size_histogram, create_object_size_comparison_chart_tinyperson, \
    create_object_size_comparison_chart_mscoco, create_object_size_comparison_chart_imagenet, \
    create_size_comparison_chart, create_width_height_plot, create_object_position_heatmap, no_axis_bbox_heatmap, \
    create_bbox_heatmap, create_bbox_size_plot


def load_example_picture():
    # Select Picture and draw Bounding Boxes
    # logger.info("Trying to open Example Image at:")
    # logger.info(random_image.get_location())
    random_image = random.choice(image_list)
    """
    # Get Information for file (Debug)
    wantedImg = 'n04074963_2603.jpeg'

    for img in image_list:
        if img.get_filename() == wantedImg:
            logger.info("Bild: " + wantedImg)
            logger.info("Anzahl Objekte: " + str(img.get_object_amount()))
            # random_image = img
    """

    color_img = cv2.imread(random_image.get_location(), 1)
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

    plt.savefig('E:/Plots/' + dataset + '/example_picture.png',
                bbox_inches='tight',
                pad_inches=0)
    plt.savefig('E:/Plots/' + dataset + '/example_picture.pdf',
                bbox_inches='tight',
                pad_inches=0)
    plt.show()


def createPlots():
    # get_percentage_object_sizes(image_object_list)
    create_object_percentage_size_histogram(get_percentage_object_sizes(image_list, dataset), dataset)

    object_size = get_object_size_comparison(get_percentage_object_sizes(image_list, dataset), dataset)
    if dataset == "tinyperson" or dataset == "aitod":
        create_object_size_comparison_chart_tinyperson(object_size, dataset)
    elif dataset == "coco" or dataset == "exdark" or dataset == "openimages":
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

def load_data_from_db(dataset):
    db_image_list = []
    keystore = {}
    print("Trying to load image data from DB")
    try:
        connection = psycopg2.connect("dbname=*dbname* user=*user* password=*password*")
        cursor = connection.cursor()
        # Copy Table into New Table
        # Drop Images that are not matching criteria from above

        if dataset == "all":
            postgres_query = """ SELECT * FROM "Images" ORDER BY "ID";"""
            cursor.execute(postgres_query)
        else:
            postgres_query = """ SELECT * FROM "Images" WHERE "Images"."dataset" = (%s) ORDER BY "ID" ;"""
            cursor.execute(postgres_query, (dataset,))

        db_images = cursor.fetchall()
        print(str(len(db_images)) + " images selected for import")

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to read record from table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    for db_image in tqdm.tqdm(db_images):
        db_image_list.append(
            Image(db_image[0], db_image[5], db_image[1], db_image[2],
                  db_image[4], db_image[6], db_image[7]))
        keystore[db_image[0]] = len(db_image_list) - 1

    try:
        print("Trying to load object data from DB")
        connection = psycopg2.connect("dbname=*dbname* user=*user* password=*password*")
        cursor = connection.cursor()
        # Copy Table into New Table
        # Drop Images that are not matching criteria from above

        if dataset == "all":
            postgres_query = """ SELECT * FROM "Objects";"""
            cursor.execute(postgres_query)
        else:
            postgres_query = """ SELECT * FROM "Objects" INNER JOIN "Images" ON "Objects"."imageID" = "Images"."ID" WHERE "Images"."dataset" = (%s);"""
            cursor.execute(postgres_query, (dataset,))

        db_objects = cursor.fetchall()
        print(str(len(db_objects)) + " objects selected for import")

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to read record from table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    for db_obj in tqdm.tqdm(db_objects):
        new_object_instance = ObjectInstance(db_obj[0], [], db_obj[1], db_obj[2],
                                             db_obj[3], db_obj[5], db_obj[6])
        parent_image = db_image_list.__getitem__(keystore.get(db_obj[2]))
        # Map ObjectInstance to Image (Parent)
        parent_image.add_object_instance(new_object_instance)

    print("Done! DB Data loaded.")
    return db_image_list

# dataset set you want to read: coco,tinyperson,imagenet,imagenet_Dummy, aitod , openimages , pascalvoc, exdark, all

dataset = "openimages"

# Create empty list for incoming Objects from json/xml file
image_list = load_data_from_db(dataset)

print("Overall Image Information:")
result = avg_object_size_from_bbox(image_list)
display_result(result, dataset)

# %%
"dbname=*dbname* user=*user* password=*password*"
Path("E:/Plots/" + dataset).mkdir(parents=True, exist_ok=True)
Path("E:/Errors/" + dataset).mkdir(parents=True, exist_ok=True)

createPlots()

# %%
load_example_picture()
