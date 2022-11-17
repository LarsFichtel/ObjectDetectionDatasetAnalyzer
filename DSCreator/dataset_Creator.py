import json
import math
import os.path
import random
import shutil
from collections import Counter
from pathlib import Path

# Suche alle geeigneten Bilder, hier z.B. alle Bilder, bei denen ALLE Objekte <= 256px sind
import eval


def beautifyDatasetAffiliation(dataset_occurence):
    dataset_Dict = Counter(dataset_occurence)
    affiliation = [(i, "{:.2f}".format(dataset_Dict[i] / len(dataset_occurence) * 100.0)) for i, count in
                   dataset_Dict.most_common()]
    temp_result = ""
    for tuple in affiliation:
        temp_result += str(tuple) + "%\n"
    result = temp_result.replace("(", "").replace(")", "").replace(",", ":").replace("'", "")
    return result


def beautifyCategoryAffiliation(category_occurence):
    categories = Counter(category_occurence).most_common()
    temp_result = ""
    for tuple in categories:
        temp_result += str(tuple) + "\n"
    result = temp_result.replace("(", "").replace(")", "").replace(",", ":").replace("'", "")
    return result


def getSuitableImages(image_list, object_size_criteria, strict):
    print("Searching for Images with objects < " + str(object_size_criteria) + "px. Strict? " + str(strict))
    suitable_images = []
    if strict:
        for img in image_list:
            is_suitable = True
            objects = img.get_object_instances()
            for obj in objects:
                if obj.get_object_size() > object_size_criteria:
                    is_suitable = False
                    # print(obj.get_object_size())
                # else:
                # print(obj.get_object_size())
            if is_suitable:
                suitable_images.append(img)
    else:
        for img in image_list:
            objects = img.get_object_instances()
            for obj in objects:
                if obj.get_object_size() > object_size_criteria:
                    img.remove_object_instance(obj)
                else:
                    suitable_images.append(img)
    result = eval.avg_object_size_from_bbox(suitable_images)
    eval.display_result(result)
    return suitable_images


def beautifySetSplit(image_list, training, test, validation, rnd_seed):
    print("Verteilung: " + str(training) + " " + str(test) + " " + str(validation))
    amount_training = int(len(image_list) * training / 100)
    amount_val = int(len(image_list) * validation / 100)
    amount_test = int(len(image_list) * test / 100)

    if amount_training + amount_test + amount_val < len(image_list):
        missing_no_of_pics = len(image_list) - (amount_training + amount_test + amount_val)
        amount_training += missing_no_of_pics

    print("Anzahl pro Split: " + str(amount_training) + " " + str(amount_val) + " " + str(amount_test))

    random.seed(rnd_seed)
    random.shuffle(image_list)
    training_data = image_list[0:amount_training]
    validation_data = image_list[amount_training:amount_training + amount_val]
    test_data = image_list[amount_training + amount_val:amount_training + amount_val + amount_test]

    return [training_data, validation_data, test_data]


# Kopiere die geeigneten Bilder aus ihren Quellordnern in neuen Dataset Ordner &
# Erstelle in Abhängigkeit von ausgewählten Bildern und neuem Datensatz eine Annotationsdatei

def createDataset(image_list, object_size, strict_filtering, split):
    version = ""
    strict = ""
    if strict_filtering:
        strict = "enabled"
        version = "a"
    else:
        strict = "disabled"
        version = "b"
    # Copy Images
    # Copying Images to new Dataset

    # Careful!! Change directory if needed!!
    target = 'E:/newDS/images_' + str(object_size) + version + '/' + split + '/'

    imageFolder = target + 'images/'
    Path(target).mkdir(parents=True, exist_ok=True)
    Path(imageFolder).mkdir(parents=True, exist_ok=True)

    img_counter = 0
    oi = {}
    # Annotation
    images = []
    annotations = []
    category_list = []
    dataset_occurence = []
    category_occurence = []
    category_dict = {}
    supercategory_dict = {}
    supercategory_occurence = []

    #     for img in image_list[1:5000]:
    for img in image_list:
        img_counter += 1
        # Copy Images to target directory
        if img.get_location() != '':
            if not os.path.isfile(imageFolder + img.get_filename()):
                shutil.copyfile(img.get_location(), imageFolder + img.get_filename())

        # Image annotations
        tempImg = {'id': img.get_id(), 'file_name': img.get_filename(), 'width': img.get_width(),
                   'height': img.get_height(), 'dataset-source': img.get_dataset(), 'license': img.get_license()}
        images.append(tempImg)

        # object annotations
        for obj in img.get_object_instances():
            tempObj = {'id': obj.get_object_id(), 'area': obj.get_object_size(), 'image id': obj.get_image_id(),
                       'bbox': obj.get_bbox(), 'category': obj.get_category_title(),
                       'category_id': obj.get_category_id()}
            annotations.append(tempObj)
            category_occurence.append(obj.get_category_title() + " [id " + str(obj.get_category_id()) + "]")
            category_dict[obj.get_category_id()] = obj.get_category_title()
            supercategory_dict[obj.get_category_id()] = obj.get_supercategory()
            supercategory_occurence.append(obj.get_supercategory())


        # DatasetAffiliation
        dataset_occurence.append(img.get_dataset())

    print(str(img_counter) + " Bilder kopiert.")

    # category annotation
    # Which categories occure? LATER ( category_occurences: how many for each category!!)
    occuring_categories = eval.getObjectCategories(image_list)
    for key in category_dict:
        category_list.append(
            {'id': str(key), 'name': category_dict.get(key), 'supercategory': supercategory_dict.get(key)})

    oi['images'] = images
    oi['annotations'] = annotations
    oi['categories'] = category_list

    # Write Annotations in Json file
    filename = target + 'annotation.json'.format('v6', 'train', 'bbox')
    print('Writing annotation file to {}'.format(filename))
    json.dump(oi, open(filename, "w", encoding='utf-8'), )

    datasets = beautifyDatasetAffiliation(dataset_occurence)
    categories = beautifyCategoryAffiliation(category_occurence)
    supercategories = beautifyCategoryAffiliation(supercategory_occurence)

    print(supercategories)
    # Create ReadMe
    # Careful!! Change directory if needed!!

    readme_file = open(target + "readme.txt", "w+")
    readme_file.write("This dataset was generated by gathering the matching images with suitable object sizes.\n"
                      "The images in this new dataset only have object instances that are smaller than "
                      + str(object_size) + "px.\nStrict Filtering has been " + strict + ".\n\nThere are " + str(
        img_counter)
                      + " images with " + str(
        len(annotations)) + " objects in total.\nThe images belong to the following"
                            " datasets:\n"
                      + str(datasets) + "\n\nSupercategories: \n" + supercategories + "\n\nDifferent categories: " + str(
        len(category_list)) + "\nOccurence of categories:\n" + categories)

    readme_file.close()

    # Careful!! Change directory if needed!!

    license_file = open(target + "license.txt", "w+")
    license_file.write(
        "The license for each indiviual image can be found in the annotation file as image attribute.\n\n"
        "AI TOD:\nAttribution-NonCommercial CC BY-NC-SA 2.0 http://creativecommons.org/licenses/by-nc-sa/2.0/\n\nexDark: \nBSD 3 Clause license: (New or Revised)"
        "\nhttps://github.com/cs-chan/Exclusively-Dark-Image-Dataset\n\nPascalVoc:\nThe VOC data includes images obtained from the flickr website.\n"
        "Use of these images must respect the corresponding terms of use: flickr terms of use.\nurl: http://host.robots.ox.ac.uk/pascal/VOC/\n\n"
        "ImageNet:\nImageNet doesn't own the copyright for any of the images.\nFor non-commercial or educational purpose: Flickr terms of use\n\n"
        "Open Images:\nAnnotations: CC BY 4.0 license.\nImages:  CC BY 2.0 license\n\n"
        "TinyPerson:\nhttps://github.com/ucas-vg/TinyBenchmark\nThe images in TinyPerson 'are collected from Internet. "
        "Firstly, videos with a high resolution are collected from different websites.\nSecondly, we sample images from video every 50 frames.'\n\n"
        "Coco:\nObjects: Creative Commons Attribution 4.0 License.\nImages:"
        "\nhttp://creativecommons.org/licenses/by-nc-sa/2.0/ Attribution-NonCommercial-ShareAlike License,"
        "\nhttp://creativecommons.org/licenses/by-nc/2.0/ Attribution-NonCommercial License"
        "\nhttp://creativecommons.org/licenses/by-nc-nd/2.0/ Attribution-NonCommercial-NoDerivs License"
        "\nhttp://creativecommons.org/licenses/by/2.0/ Attribution License"
        "\nhttp://creativecommons.org/licenses/by-sa/2.0/ Attribution-ShareAlike License"
        "\nhttp://creativecommons.org/licenses/by-nd/2.0/ Attribution-NoDerivs License"
        "\nhttp://flickr.com/commons/usage/  No known copyright restrictions"
        "\nhttp://www.usa.gov/copyright.shtml United States Government Work")
    license_file.close()
