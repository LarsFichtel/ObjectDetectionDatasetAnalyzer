import csv
import os
import json
from os.path import basename

from Image import Image
from ObjectInstance import ObjectInstance
from xml.dom import minidom
from PIL import Image as ImagePIL


def loadCategories(category_dict):
    # Careful!! Change directory if needed!!

    with open('E:/ImageNet ILSVRC/Annotations/classes_in_imagenet.csv') as csvfile:
        categoryReader = csv.DictReader(csvfile)
        for row in categoryReader:
            category_dict[row['synid']] = row['class_name']
    return category_dict


def xmlReader(image_list, keystore, imagePath, path, current_dataset):
    print("Loading " + current_dataset)
    # Crawl through directory
    image_counter = 0
    category_dict = {}

    # Load Imagenet object categories from CSV
    if current_dataset == "imagenet" or current_dataset == "imagenet_Dummy":
        category_dict = loadCategories(category_dict)

    for root, subDirs, files in os.walk(path):
        # print(root)
        # print("Files: " + str(files))
        for file in files:
            filePath = os.path.join(root, file)
            # print("FilePath: " + str(filePath))
            xmldoc = minidom.parse(filePath)
            fileName = xmldoc.getElementsByTagName('filename')[0].firstChild.data
            folder = str(xmldoc.getElementsByTagName('folder')[0].firstChild.data)
            imageID = ''

            # Format FileName and Location according to xml schema
            if current_dataset == "imagenet" or current_dataset == "imagenet_Dummy":
                imageID = current_dataset + "_" + fileName
                fileName += ".jpeg"
                location = imagePath + folder + "/" + fileName
            else:
                imageID = (current_dataset + "_" + fileName).replace(".jpg", "")
                location = imagePath + fileName
            width = int(xmldoc.getElementsByTagName('width')[0].firstChild.data)
            height = int(xmldoc.getElementsByTagName('height')[0].firstChild.data)

            # Create new Image Object
            newImage = Image(imageID, str(fileName), height, width, location,
                             current_dataset)  # evtl: '+ ".xml"' hinter filename?
            newImage.set_folder(folder)
            image_list.append(newImage)

            # Iterate through objects for each image annotation xml file
            objects = xmldoc.getElementsByTagName('object')
            for obj in objects:

                # BBOX Reader & Formatter
                bbox = [int(obj.getElementsByTagName('xmin')[0].firstChild.data),
                        int(obj.getElementsByTagName('ymin')[0].firstChild.data),
                        int(obj.getElementsByTagName('xmax')[0].firstChild.data) - int(
                            obj.getElementsByTagName('xmin')[0].firstChild.data),
                        int(obj.getElementsByTagName('ymax')[0].firstChild.data) - int(
                            obj.getElementsByTagName('ymin')[0].firstChild.data)]
                category_id = xmldoc.getElementsByTagName('folder')[0].firstChild.data
                new_object_instance = ObjectInstance(newImage.get_object_amount() + 1, [], bbox,
                                                     imageID,
                                                     category_id)

                if current_dataset == 'pascalvoc':
                    category_title = str(obj.getElementsByTagName('name')[0].firstChild.data)
                    if category_title not in category_dict:
                        cat_id = len(category_dict) + 1
                        category_dict[category_title] = cat_id
                        new_object_instance.set_category_title(category_title)
                        new_object_instance.set_category_id(cat_id)
                        # print("New Category added: " + str(cat_id) + " " + str(category_title))
                    else:
                        new_object_instance.set_category_title(category_title)
                        new_object_instance.set_category_id(category_dict.get(category_title))
                else:
                    category_id = folder
                    category_title = category_dict.get(folder)
                    new_object_instance.set_category_title(category_title)
                    new_object_instance.set_category_id(category_id)

                newImage.add_object_instance(new_object_instance)
            # Save List position and Image ID in dictionary
            keystore[imageID] = len(image_list) - 1
            # print(fileName)
            # print(keystore[fileName])
            image_counter += 1
            # if image_counter % 500000 == 0:
            #     print("XML Dateien eingelesen: " + str(image_counter))

    amount_bboxes = 0
    for image in image_list:
        amount_bboxes += image.get_object_amount()

    output(current_dataset, image_list, keystore)


def output(dataset, image_list, keystore):
    print(dataset + " loaded.\tImages: " + str(len(image_list)) + " Dictionary: " + str(
        len(keystore)))


# %%
def read_dataset(dataset):
    # Create empty list for incoming Objects from json/xml file
    image_list = []
    # Create dictionary for identification (list position <-> image id)
    keystore = {}

    if dataset == "mscoco" or dataset == "all":
        print("Loading COCO2017")
        # Select Json file
        # Careful!! Change directory if needed!!

        with open('../annotations/instances_train2017.json') as json_file:
            # Load Json file
            data = json.load(json_file)
            # Iterate through all 'images' in json file
            for p in data['images']:
                # Create Image Object and add to object list
                image_id = 'coco_' + str(p['id'])
                image_list.append(
                    Image(image_id, p['file_name'], p['height'], p['width'],
                          'E:/COCO/train2017/' + p['file_name'],
                          "mscoco"))
                # Save List position and Image ID in dictionary
                keystore[image_id] = len(image_list) - 1

            for a in data['annotations']:
                image_id = 'coco_' + str(a['image_id'])
                # Check if object instance is single object or RLE of multiple objects
                if a['iscrowd'] == 0:
                    # Create to ObjectInstance
                    new_object_instance = ObjectInstance(a['id'], a['segmentation'], a['bbox'], image_id,
                                                         a['category_id'])
                    parent_image = image_list.__getitem__(keystore.get(image_id))
                    # Map ObjectInstance to Image (Parent)
                    parent_image.add_object_instance(new_object_instance)
                    for cat in data['categories']:
                        if cat['id'] == a['category_id']:
                            new_object_instance.set_category_title(cat['name'])

        temp_list = []
        for img in image_list:
            # Falls keine Annotation vorhanden, lösche Bild aus image list -> Keine weitere Verarbeitung
            if img.get_object_amount() > 0:
                temp_list.append(img)
            else:
                del keystore[img.get_id()]
        image_list = temp_list
        output("COCO2017", image_list, keystore)

    if dataset == "imagenet" or dataset == "imagenet_Dummy" or dataset == "pascalvoc" or dataset == "all":

        if dataset == "imagenet_Dummy":
            #   Dummy version with ~7000 XML Files
            # Careful!! Change directory if needed!!

            path = 'E:/ImageNet ILSVRC/Annotations/dummyTest'
            imagePath = "E:/ImageNet ILSVRC/Data/train/"
            current_dataset = "imagenet_Dummy"
            xmlReader(image_list, keystore, imagePath, path, current_dataset)

        if dataset == "imagenet" or dataset == "all":
            #   Main version with ~1.000.000 XML Files
            # Careful!! Change directory if needed!!

            path = 'E:/ImageNet ILSVRC/Annotations/train'
            imagePath = "E:/ImageNet ILSVRC/Data/train/"
            current_dataset = "imagenet"
            xmlReader(image_list, keystore, imagePath, path, current_dataset)

        if dataset == "pascalvoc" or dataset == "all":
            # Pascal Voc (XML)
            # Careful!! Change directory if needed!!

            path = 'E:/Pascal VOC/Annotations'
            imagePath = "E:/Pascal VOC/JPEGImages/"
            current_dataset = "pascalvoc"
            xmlReader(image_list, keystore, imagePath, path, current_dataset)

    if dataset == "tinyperson" or dataset == "all":
        current_dataset = "tinyperson"
        # Careful!! Change directory if needed!!

        with open(
                'E:/TinyPerson/annotations/tiny_set_train_with_dense.json') as json_file:
            print("Loading TinyPerson")
            # Load Json file
            data = json.load(json_file)
            # Iterate through all 'images' in json file
            for p in data['images']:
                # Create Image Object and add to object list
                fileName = p['file_name'].split("/", 1)[1]
                image_list.append(
                    Image('tinyperson_' + str(p['id']), fileName, p['height'], p['width'],
                          "E:/TinyPerson/train/" + p['file_name'],
                          current_dataset))
                # Save List position and Image ID in dictionary
                keystore['tinyperson_' + str(p['id'])] = len(image_list) - 1

            for a in data['annotations']:
                image_id = 'tinyperson_' + str(a['image_id'])
                # Check if object instance is single object or RLE of multiple objects
                if a['iscrowd'] == 0 and not a['ignore']:
                    # Create Object of Type ObjectInstance
                    new_object_instance = ObjectInstance(a['id'], a['segmentation'], a['bbox'], image_id,
                                                         a['category_id'])
                    parent_image = image_list.__getitem__(keystore.get(image_id))
                    # Map ObjectInstance to Image (Parent)
                    parent_image.add_object_instance(new_object_instance)
                    for cat in data['categories']:
                        if cat['id'] == a['category_id']:
                            new_object_instance.set_category_title(cat['name'])
        output("TinyPerson", image_list, keystore)

    if dataset == "aitod" or dataset == "all":
        current_dataset = "aitod"
        # Careful!! Change directory if needed!!

        with open(
                'E:/AI-TOD/annotations/aitod_train_v1.json') as json_file:
            print("Loading AI-TOD")
            # Load Json file
            data = json.load(json_file)
            # Iterate through all 'images' in json file
            for p in data['images']:
                # Create Image Object and add to object list
                image_id = 'aitod_' + str(p['id'])
                image_list.append(
                    Image(image_id, p['file_name'], p['height'], p['width'],
                          "E:/AI-TOD/images/" + p['file_name'],
                          current_dataset))
                # Save List position and Image ID in dictionary
                keystore[image_id] = len(image_list) - 1

            for a in data['annotations']:
                image_id = 'aitod_' + str(a['image_id'])
                # Check if object instance is single object or RLE of multiple objects
                if a['iscrowd'] == 0:
                    # Create Object of Type ObjectInstance
                    new_object_instance = ObjectInstance(a['id'], a['segmentation'], a['bbox'], image_id,
                                                         a['category_id'])
                    parent_image = image_list.__getitem__(keystore.get(image_id))
                    # Map ObjectInstance to Image (Parent)
                    parent_image.add_object_instance(new_object_instance)
                    for cat in data['categories']:
                        if cat['id'] == a['category_id']:
                            new_object_instance.set_category_title(cat['name'])

        output("AI-TOD", image_list, keystore)
    if dataset == "exdark" or dataset == "all":
        print("Loading exDark")
        # Careful!! Change directory if needed!!

        path = "E:/exDark/imageclasslist.txt"
        images = []
        exDark_SizeKeystore = {}
        categories = {'Bicycle': '1', 'Boat': '2', "Bottle": "3", "Bus": "4", "Car": "5", "Cat": "6", "Chair": "7",
                      "Cup": "8",
                      "Dog": "9", "Motorbike": "10", "People": "11", "Table": "12"}

        imagePath = "E:/exDark/images"
        for root, subDirs, files in os.walk(imagePath):
            for file in files:
                filePath = os.path.join(root, file)
                img = ImagePIL.open(filePath)
                dimensions = [img.width, img.height]
                exDark_SizeKeystore[file] = dimensions

        with open(path) as file:
            for line in file:
                formattedLine = line.split()
                if formattedLine[4] == '1':
                    images.append(formattedLine[0])
                    dimensions = exDark_SizeKeystore.get(formattedLine[0])
                    image_id = 'exdark_' + str(formattedLine[0])
                    image_list.append(
                        Image(image_id, formattedLine[0], dimensions[0], dimensions[1], "",
                              "exDark"))
                    keystore[image_id] = len(image_list) - 1
                    # print('exdark_' + str(formattedLine[0]))

        # print("Ausgewählte Bilder: " + str(len(image_list)))

        # Careful!! Change directory if needed!!

        annotationPath = "E:/exDark/annotation"
        for root, subDirs, files in os.walk(annotationPath):
            for file in files:
                if file.replace(".txt", "") in images:
                    filePath = os.path.join(root, file)
                    with open(filePath) as textFile:
                        lineCounter = 0
                        for line in textFile:
                            lineCounter += 1
                            formattedLine = line.split()
                            if formattedLine[0] != "%":
                                image_id = 'exdark_' + file.replace(".txt", "")
                                new_object_instance = ObjectInstance(lineCounter, [],
                                                                     [int(formattedLine[1]), int(formattedLine[2]),
                                                                      int(formattedLine[3]), int(formattedLine[4])],
                                                                     image_id,
                                                                     categories.get(str(formattedLine[0])))
                                new_object_instance.set_category_title(str(formattedLine[0]))
                                parent_image = image_list.__getitem__(keystore.get(image_id))
                                parent_image.add_object_instance(new_object_instance)
                                parent_image.set_folder(basename(root.replace(os.sep, "/")))
                                parent_image.set_location(
                                    imagePath + "/" + parent_image.get_folder() + "/" + parent_image.get_filename())
        output("exDark", image_list, keystore)

    if dataset == "openimages" or dataset == "all":
        current_dataset = "openimages"
        print("Loading OpenImages")
        # Careful!! Change directory if needed!!

        with open('E:/OpenImages/json/annotation.json') as json_file:
            # Load Json file
            data = json.load(json_file)
            print("Creating Image Objects from json file...")
            image_counter = 0
            imagePath = "E:/OpenImages/data/train/"
            # Iterate through all 'images' in json file
            for p in data['images']:
                # Create Image Object and add to object list
                image_id = 'openimages_' + str(p['id'])
                image_list.append(
                    Image(image_id, p['file_name'], p['height'], p['width'],
                          imagePath + p['file_name'], current_dataset))
                # Save List position and Image ID in dictionary
                keystore[image_id] = len(image_list) - 1
                image_counter += 1
                if image_counter % 100000 == 0:
                    print("Open Images Bild-Annotationen eingelesen: " + str(image_counter))
            print("Analysing Annotations...")

            # %%
            object_counter = 0
            for a in data['annotations']:
                image_id = 'openimages_' + str(a['image_id'])
                # Check if object instance is single object or RLE of multiple objects
                if a['iscrowd'] == 0 or a['iscrowd'] == 'false':
                    # Create to ObjectInstance
                    new_object_instance = ObjectInstance(a['id'], [], a['bbox'], image_id,
                                                         a['category_id'])
                    parent_image = image_list.__getitem__(keystore.get(image_id))
                    # Map ObjectInstance to Image (Parent)
                    parent_image.add_object_instance(new_object_instance)
                    for cat in data['categories']:
                        if cat['id'] == a['category_id']:
                            new_object_instance.set_category_title(cat['name'])
                    object_counter += 1
                if object_counter % 250000 == 0:
                    print("Open Images Objects Read: " + str(object_counter) + " Progress: " + str(
                        (object_counter / 14000000) * 100) + "%")
        output("OpenImages", image_list, keystore)

    # Output & Return
    # return image_list, keystore
    return image_list
