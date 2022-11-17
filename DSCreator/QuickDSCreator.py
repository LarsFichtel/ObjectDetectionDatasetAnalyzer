import importlib
import cv2
import logging
import psycopg2
import tqdm

import Image
import dataset_Creator
from DSReader import dataset_Reader
import plotter
from dataset_Creator import *
from DSReader.dataset_Reader import *
from eval import *
from plotter import *

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][Bot] %(message)s',
    datefmt='%H:%M:%S'
)


# %%
# Library Reload Test - Pull changes from other Libs
def reload_libraries():
    importlib.reload(eval)
    importlib.reload(dataset_Creator)
    importlib.reload(dataset_Reader)
    importlib.reload(plotter)
    importlib.reload(psycopg2)
    importlib.reload(tqdm)


# %%

def show_categories(temp_image_list, bool):
    if bool:
        category_dictionary = eval.getObjectCategories(temp_image_list)
        print("Dataset categories (" + str(len(category_dictionary)) + ")")
        print(category_dictionary)


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
    plt.savefig('E:/Plots/' + dataset + '/example_picture.png',
                bbox_inches='tight',
                pad_inches=0)
    plt.savefig('E:/Plots/' + dataset + '/example_picture.pdf',
                bbox_inches='tight',
                pad_inches=0)
    plt.show()


def load_data_into_db(image_list):
    try:
        connection = psycopg2.connect("dbname=*INSERT dbname* user=*INSERTDBUSER* password=*INSERTPW*")
        cursor = connection.cursor()

        image_insert_query = """ INSERT INTO "Images" ("ID","Height", "Width" , "Folder", "location", "filename", "dataset") VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING "ID";"""
        for img in tqdm.tqdm(image_list):
            image_id = img.get_id()
            height = img.get_height()
            width = img.get_width()
            folder = img.get_folder()
            location = img.get_location()
            filename = img.get_filename()
            dataset = img.get_dataset()
            cursor.execute(image_insert_query, (image_id, height, width, folder, location, filename, dataset))

        # postgres_insert_query = """ INSERT INTO "Datasets" ("Name") VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING "Name";"""
        # record_to_insert = "testDataset"
        # cursor.execute(postgres_insert_query, (record_to_insert,))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    # %%

    try:
        connection = psycopg2.connect("dbname=*DATABSE* user=+USERNAME* password=*PASSWORD*")
        cursor = connection.cursor()

        image_insert_query = """ INSERT INTO "Objects" ("ObjectID","BoundingBox", "ImageID" , "CategoryName", "Size") VALUES (%s,%s,%s,%s,%s) RETURNING "ObjectID";"""
        for img in tqdm.tqdm(image_list):
            object_list = img.get_object_instances()
            for obj in object_list:
                obj_id = obj.get_object_id()
                bbox = obj.get_bbox()
                image_id = obj.get_image_id()
                category_name = obj.get_category_title()
                size = obj.get_object_size()
                cursor.execute(image_insert_query, (obj_id, bbox, image_id, category_name, size))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def load_data_from_db(dataset):
    db_image_list = []
    keystore = {}
    print("Trying to load image data from DB")
    try:
        connection = psycopg2.connect("dbname=*DBNAME* user=*user* password=*password*")
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
            postgres_query = """ SELECT * FROM "Objects" INNER JOIN "Images" ON "Objects"."ImageID" = "Images"."ID" WHERE "Images"."dataset" = (%s);"""
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


def createDatasetFromDB(object_size_criteria):
    db_image_list = []
    keystore = {}
    print("Trying to load image data from DB")
    try:
        connection = psycopg2.connect("dbname=*name* user=*user* password=*password*")
        cursor = connection.cursor()
        # Copy Table into New Table
        # Drop Images that are not matching criteria from above

        postgres_query = """ SELECT * FROM "Images" INNER JOIN "Objects" ON  "Objects"."ImageID" = "Images"."ID" WHERE "Objects"."Size" <= (%s) ORDER BY "ID" ;"""
        cursor.execute(postgres_query, (object_size_criteria,))

        db_rows = cursor.fetchall()
        print(str(len(db_rows)) + " Objects are suitable for import")

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to read record from table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    for db_image in tqdm.tqdm(db_rows):
        if db_image[0] in keystore:
            obj = ObjectInstance(db_image[8], [], db_image[9], db_image[10], db_image[11], db_image[13], db_image[14])
            parent_image = db_image_list.__getitem__(keystore.get(db_image[0]))
            parent_image.add_object_instance(obj)
        else:
            img = Image(db_image[0], db_image[5], db_image[1], db_image[2],
                        db_image[4], db_image[6], db_image[7])
            obj = ObjectInstance(db_image[8], [], db_image[9], db_image[10], db_image[11], db_image[13], db_image[14])
            img.add_object_instance(obj)

            db_image_list.append(img)
            keystore[db_image[0]] = len(db_image_list) - 1

    print("No. of Images: " + str(len(db_image_list)))
    return db_image_list


def createPlots():
    # get_percentage_object_sizes(image_object_list)
    create_object_percentage_size_histogram(get_percentage_object_sizes(image_list, dataset), dataset)

    object_size = get_object_size_comparison(get_percentage_object_sizes(image_list, dataset), dataset)
    if dataset == "tinyperson":
        create_object_size_comparison_chart_tinyperson(object_size, dataset)
    elif dataset == "mscoco":
        create_object_size_comparison_chart_mscoco(object_size, dataset)
    elif dataset == "imagenet" or dataset == "imagenet_Dummy" or dataset == "pascalvoc":
        create_object_size_comparison_chart_imagenet(object_size, dataset)

    size_comparison = get_size_comparison(image_list)
    create_size_comparison_chart(size_comparison, dataset)

    # zeigt relation zwischen number of objects (y achse) und (object instance height/width in pixeln)
    width_height_list = get_bbox_width_and_height_list(image_list, dataset)
    create_width_height_plot(width_height_list[0], "width", dataset)
    create_width_height_plot(width_height_list[1], "height", dataset)

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
    logger.info(arr)

    # Plotten jeweils mit und ohne Beschriftungen
    create_bbox_heatmap(arr, dataset, "complete bbox")
    no_axis_bbox_heatmap(arr, dataset, "complete bbox")


# %%
# dataset set you want to read: coco,tinyperson,imagenet,imagenet_Dummy, aitod , openimages , pascalvoc, exdark, all

dataset = "all"
image_list = load_data_from_db(dataset)

# %%
# Create New Dataset according to size criteria -
object_size_filter = 1024
strict_filtering = True  # bei FALSE, werden aktuell ALLE Datensätze gelesen

# Select how you want to distribute the images into the different sets (i.e. 80% training, 10% val, 10% test)
training = 80
test = 10
validation = 10

# Define seed for testing/traceability
seed = 100

def newDataset(temp_image_list, object_size_criteria, strict, training, test, validation, seed):
    suitableImages = getSuitableImages(temp_image_list, object_size_criteria, strict)
    datasets = beautifySetSplit(suitableImages, training, test, validation, seed)
    dataset_Creator.createDataset(datasets[0], object_size_filter, strict_filtering, "train")
    dataset_Creator.createDataset(datasets[1], object_size_filter, strict_filtering, "val")
    dataset_Creator.createDataset(datasets[2], object_size_filter, strict_filtering, "test")

newDataset(image_list, object_size_filter, strict_filtering, training, test, validation, seed)


