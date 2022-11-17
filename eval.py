import statistics
from pathlib import Path

from shapely.geometry import Polygon

# CHANGE DIRECTORIES TO SAVE YOUR ErrorFiles !!!!


# Abhängig von auftretenden Objekten im Bild (und jeweiliger Größe) werden geeignete Bilder für neues DS ausgewählt
from DSCreator.dataset_Creator import beautifyDatasetAffiliation


def get_images_for_dataset(image_list):
    for image in image_list:
        for obj in image.get_object_instances():
            print()


def avg_object_size_from_bbox(image_list):
    #  Größenverhältnis für jedes Objekt in Bezug auf Image speichern
    size_in_pixels = []
    size_percentage = []
    categories = []
    dataset_affiliation = []
    for image in image_list:
        image_size = image.get_size()
        dataset_affiliation.append(image.get_dataset())
        for obj in image.get_object_instances():
            bbox = obj.get_bbox()
            object_size = bbox[2] * bbox[3]
            size_in_pixels.append(object_size)
            size_percentage.append(object_size / image_size)
            categories.append(obj.get_category_title())

    return [len(image_list), len(size_in_pixels), size_in_pixels, size_percentage, categories, dataset_affiliation]


def get_size_comparison(image_list):
    size_comparison = [0, 0, 0, 0, 0]
    for image in image_list:
        for obj in image.get_object_instances():
            object_size = obj.get_object_size()
            if object_size < 64:
                size_comparison[0] += 1
            elif 64 <= object_size < 256:
                size_comparison[1] += 1
            elif 256 <= object_size <= 1024:
                size_comparison[2] += 1
            elif 1024 < object_size < 9216:
                size_comparison[3] += 1
            elif object_size >= 9216:
                size_comparison[4] += 1
    return size_comparison


def get_object_size_comparison(relative_object_size_list, dataset):
    if dataset == "tinyperson" or dataset == "aitod":
        # size_categories = ["<0.01%", "0.01-0.02%", "0.02-0.03%", "0.03-0.04%", "0.04-0.05%", ">0.05%"]
        size_comparison = [0, 0, 0, 0, 0, 0]

        for percentage in relative_object_size_list:
            if percentage < 0.01:
                size_comparison[0] += 1
                # break
            elif 0.01 <= percentage < 0.02:
                size_comparison[1] += 1
                # break
            elif 0.02 <= percentage < 0.03:
                size_comparison[2] += 1
                # break
            elif 0.03 <= percentage < 0.04:
                size_comparison[3] += 1
                # break
            elif 0.04 <= percentage < 0.05:
                size_comparison[4] += 1
                # break
            elif percentage >= 0.05:
                size_comparison[5] += 1
                # break
    elif dataset == "coco" or dataset == "exdark" or dataset == "openimages":
        # size_categories = ["<0.1%", "0.1-1%", "1-3%", "3-5%", "5-10%", "10-25%", ">25"]
        size_comparison = [0, 0, 0, 0, 0, 0, 0]

        for percentage in relative_object_size_list:
            if percentage < 0.1:
                size_comparison[0] += 1
                # break
            if 0.1 <= percentage < 1:
                size_comparison[1] += 1
                # break
            elif 1 <= percentage < 3:
                size_comparison[2] += 1
                # break
            elif 3 <= percentage < 5:
                size_comparison[3] += 1
                # break
            elif 5 <= percentage < 10:
                size_comparison[4] += 1
                # break
            elif 10 <= percentage < 25:
                size_comparison[5] += 1
                # break
            elif percentage >= 25:
                size_comparison[6] += 1
                # break
    else:
        # size_categories = ["<1%", "1-5%", "5-10%", "10-25%", "25-50%", "50-75%", "75-90%", ">90%"]
        size_comparison = [0, 0, 0, 0, 0, 0, 0, 0]

        for percentage in relative_object_size_list:
            if percentage < 1:
                size_comparison[0] += 1
                # break
            elif 1 <= percentage < 5:
                size_comparison[1] += 1
                # break
            elif 5 <= percentage < 10:
                size_comparison[2] += 1
                # break
            elif 10 <= percentage < 25:
                size_comparison[3] += 1
                # break
            elif 25 <= percentage < 50:
                size_comparison[4] += 1
                # break
            elif 50 <= percentage < 75:
                size_comparison[5] += 1
                # break
            elif 75 <= percentage < 90:
                size_comparison[6] += 1
                # break
            elif percentage >= 90:
                size_comparison[7] += 1
    # print("Size Comparison data: " + str(len(relative_object_size_list)) + " objects.")

    # counter = 0
    # for entry in size_comparison:
    #     print(size_categories[counter] + "\t\t" + str(entry))
    #     counter += 1
    # print()
    return size_comparison

def get_object_size_comparison_for_newDS(relative_object_size_list, dataset):
    if dataset == '1024a':
        size_comparison = [0, 0, 0, 0, 0, 0, 0]
        for percentage in relative_object_size_list:
            if percentage < 0.01:
                size_comparison[0] += 1
                # break
            elif 0.01 <= percentage < 0.015:
                size_comparison[1] += 1
                # break
            elif 0.015 <= percentage < 0.02:
                size_comparison[2] += 1
                # break
            elif 0.02 <= percentage < 0.025:
                size_comparison[3] += 1
                # break
            elif 0.025 <= percentage < 0.03:
                size_comparison[4] += 1
                # break
            elif 0.03 <= percentage < 0.035:
                size_comparison[5] += 1
                # break
            elif percentage >= 0.035:
                size_comparison[6] += 1
                # break
    else:
        size_comparison = [0, 0, 0, 0, 0, 0, 0]
        for percentage in relative_object_size_list:
            if percentage < 0.02:
                size_comparison[0] += 1
                # break
            elif 0.02 <= percentage < 0.04:
                size_comparison[1] += 1
                # break
            elif 0.04 <= percentage < 0.06:
                size_comparison[2] += 1
                # break
            elif 0.06 <= percentage < 0.08:
                size_comparison[3] += 1
                # break
            elif 0.08 <= percentage < 0.1:
                size_comparison[4] += 1
                # break
            elif 0.1 <= percentage < 0.12:
                size_comparison[5] += 1
                # break
            elif percentage >= 0.12:
                size_comparison[6] += 1
                # break
    return size_comparison

def display_result(result, dataset):

    categories = beautifyDatasetAffiliation(result[5])
    print("Anzahl Bilder: " + str(result[0]))
    print("Anzahl Objekte: " + str(result[1]))
    print("Anzahl Kategorien: " + str(len(set(result[4]))))
    print("Avg. Größe: " + str(statistics.mean(result[2])))
    print("Median Größe: " + str(statistics.median(result[2])))
    print("Avg. Größe (%): " + str("{:.2f}".format(statistics.mean(result[3]) * 100)) + "%")
    print("Median Größe (%): " + str("{:.2f}".format(statistics.median(result[3]) * 100)) + "%")
    print("Kategorie-Verteilung: " + categories)

    print()

    Path("/Plots/" + dataset).mkdir(parents=True, exist_ok=True)

    info_file = open("/Plots/" + dataset + "/info.txt", "w+")
    info_file.write(
        "Anzahl Bilder: " + str(result[0]) + "\n" + "Anzahl Objekte: " + str(result[1]) + "\n" +
        "Anzahl Kategorien: " + str(len(set(result[4]))) + "\n" +
        "Avg. Größe: " + str(statistics.mean(result[2])) + "\n" +
        "Median Größe: " + str(statistics.median(result[2])) + "\n" +
        "Avg. Größe (%): " + str("{:.2f}".format(statistics.mean(result[3]) * 100)) + "%" + "\n" +
        "Median Größe (%): " + str("{:.2f}".format(statistics.median(result[3]) * 100)) + "%"+ "\n" +
        "Kategorie-Verteilung: " + categories
        )
    info_file.close()
    print("Kategorie-Verteilung: " + categories)


def get_total_object_sizes(image_list):
    objects = []
    for image in image_list:
        for obj in image.get_object_instances():
            if obj.get_object_id() != 391362:
                objects.append(obj.get_object_size())

    return objects


def get_percentage_object_sizes(image_list, dataset):
    objects = []
    ErrorLog = []
    for image in image_list:
        image_size = image.get_size()
        for obj in image.get_object_instances():
            object_size = obj.get_object_size()
            objects.append((object_size / image_size) * 100)
            # print(str((object_size / image_size) * 100))
            if (object_size / image_size) > 0.95:
                ErrorLog.append("Image: " + str(
                    image.get_id()) + "\tObjectInstance: " + str(
                    obj.get_object_id()) + "\t Object Size in relation to Image Size: " + str(
                    (object_size / image_size) * 100) + "\tFilename: " + str(image.get_filename()) + "\n")
            if dataset == "tinyperson" and (object_size / image_size) > 0.05:
                ErrorLog.append("Image: " + str(
                    image.get_id()) + "\tObjectInstance: " + str(
                    obj.get_object_id()) + "\t Object Size in relation to Image Size: " + str(
                    (object_size / image_size) * 100) + "\tFilename: " + str(image.get_filename()) + "\n")
    # with open("E:/Errors/" + dataset + "/ExtremelyLargeObjects.txt", 'w+') as textFile1:
    #    for error in ErrorLog:
    #        textFile1.write(error)

    return objects


def get_object_position_distribution(image_object_list):
    counter = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    # Bild in 8x8 Tiles aufteilen
    for image in image_object_list:
        width = image.get_width()
        height = image.get_height()
        part_width = int(width / 8)
        part_height = int(height / 8)
        # Nacheinander die Objekte für jedes Bild durchgehen
        for obj in image.get_object_instances():
            # x und y liste des objekt polygons direkt an center methode übergeben
            bbox_center = obj.get_bbox_center()
            x_value = bbox_center[0]
            y_value = bbox_center[1]
            for x in range(8):
                if (x * part_width) <= x_value < ((x + 1) * part_width):
                    column = x
            for y in range(8):
                if (y * part_height) <= y_value < ((y + 1) * part_height):
                    row = y
            # print("Objekt-Mittelpunk in Zeile: " + str(row) + " Spalte: " + str(column))
            counter[row][column] += 1
    return counter


def get_percentage_object_position_distribution(image_object_list):
    counter = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    for image in image_object_list:
        width = image.get_width()
        height = image.get_height()
        part_width = int(width / 8)
        part_height = int(height / 8)
        for obj in image.get_object_instances():
            # x und y liste des objekt polygons direkt an center methode übergeben
            bbox_center = obj.get_bbox_center()
            x_value = bbox_center[0]
            y_value = bbox_center[1]
            for x in range(8):
                if (x * part_width) <= x_value < ((x + 1) * part_width):
                    column = x
            for y in range(8):
                if (y * part_height) <= y_value < ((y + 1) * part_height):
                    row = y
            # print("Objekt-Mittelpunk in Zeile: " + str(row) + " Spalte: " + str(column))
            counter[row][column] += 1
    summe = sum(counter[0]) + sum(counter[1]) + sum(counter[2]) + sum(counter[3]) + sum(counter[4]) + sum(
        counter[5]) + sum(counter[6]) + sum(counter[7])
    for i in range(8):
        for result in counter:
            result[i] = float(int((result[i] / summe) * 10000) / 100)
    return counter


def get_percentage_of_bbox(image_list):
    objects = []
    for image in image_list:
        image_size = image.get_size()
        for obj in image.get_object_instances():
            object_size = obj.get_object_size()
            bbox = obj.get_bbox()
            bbox_size = bbox[2] * bbox[3]
            if bbox_size != 0:
                objects.append((object_size / bbox_size) * 100)
                # if (object_size / bbox_size) > 0.95:
                #   print(str(image.get_id()) + " " + str((object_size / image_size) * 100))
            else:
                print("Bbox 0 für: " + str(image.get_id()) + " und Objekt: " + str(obj.get_object_id()))

    return objects


def get_object_distribution_by_bbox_area(image_object_list):
    counter = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    image_tracker = 0
    for image in image_object_list:
        image_tracker += 1
        if image_tracker % 1 == 0:
            print("Berechnete Bilder: " + str(image_tracker))
        width = image.get_width()
        height = image.get_height()
        part_width = int(width / 3)
        part_height = int(height / 3)
        # Create Bounding Box
        bbox1 = [0, 0, part_width, part_height]
        bbox2 = [part_width, 0, part_width, part_height]
        bbox3 = [2 * part_width, 0, part_width, part_height]
        bbox4 = [0, part_height, part_width, part_height]
        bbox5 = [part_width, part_height, part_width, part_height]
        bbox6 = [2 * part_width, part_height, part_width, part_height]
        bbox7 = [0, 2 * part_height, part_width, part_height]
        bbox8 = [part_width, 2 * part_height, part_width, part_height]
        bbox9 = [2 * part_width, 2 * part_height, part_width, part_height]
        bbox_list = [bbox1, bbox2, bbox3, bbox4, bbox5, bbox6, bbox7, bbox8, bbox9]

        for obj in image.get_object_instances():
            temp_area = 0
            biggest_intersection_bbox = 0
            for i in range(9):
                bbox_intersection = bb_intersection_over_union(height, bbox_list[i], obj.get_bbox())
                # print("Image_Bbox " + str(i) + ": " + str(bbox_list[i]) + "Object Bbox : " + str(obj.get_bbox()) +
                # "Intersection: " + str(bbox_intersection))
                if bbox_intersection > temp_area:
                    temp_area = bbox_intersection
                    biggest_intersection_bbox = i
            # print("Biggest Intersection at " + str(biggest_intersection_bbox) + " with Value: " + str(temp_area))
            if temp_area > 0:
                counter[biggest_intersection_bbox] += 1
    print(counter)

    summe = sum(counter)
    for i in range(9):
        counter[i] = float(int((counter[i] / summe) * 10000) / 100)
    # print(counter)
    chunks = [counter[x:x + 3] for x in range(0, len(counter), 3)]  # splitten der liste (nach x,y koordinaten)
    # print(chunks)
    return chunks


def get_object_distribution_new(image_object_list):
    counter = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    # Bild in 8x8 Tiles aufteilen
    for image in image_object_list:
        width = image.get_width()
        height = image.get_height()
        part_width = int(width / 8)
        part_height = int(height / 8)
        # Nacheinander die Objekte für jedes Bild durchgehen
        for obj in image.get_object_instances():
            bbox = obj.get_bbox()
            # 4 Eckpunkte der Bounding Box bestimmen
            # top left
            x1 = bbox[0]
            y1 = bbox[1]

            # bottom right
            x4 = abs(bbox[0] + bbox[2])
            y4 = abs(bbox[1] + bbox[3])
            # print(obj.get_image_id())
            # print("Bounding Box = " + str(bbox))
            bbox_coordinates = [[x1, y1], [x4, y4]]
            # print("Top Left Corner: " + str(bbox_coordinates[0]))
            # print("Bottom Right Corner: " + str(bbox_coordinates[1]))

            bbox_corner_rc = []
            for value in bbox_coordinates:
                # print(value)
                for x in range(8):
                    if (x * part_width) <= value[0] < ((x + 1) * part_width):
                        column = x
                for y in range(8):
                    if (y * part_height) <= value[1] < ((y + 1) * part_height):
                        row = y
                # print("Coordinate in row " + str(row) + " column " + str(column))
                bbox_corner_rc.append(row)
                bbox_corner_rc.append(column)
            rows = list(range(bbox_corner_rc[0], bbox_corner_rc[2] + 1))
            columns = list(range(bbox_corner_rc[1], bbox_corner_rc[3] + 1))
            # print("Rows " + str(rows) + " columns " + str(columns))

            for r in rows:
                for c in columns:
                    counter[r][c] += 1
    return counter


def bb_intersection_over_union(image_height, bb1, bb2):
    # Siehe Lösung von Uzzal Podder
    # @https://stackoverflow.com/questions/25349178/calculating-percentage-of-bounding-box-overlap-for-image-detector-evaluation
    poly_1 = Polygon([[bb1[0], bb1[1]], [bb1[2], bb1[1]], [bb1[2], bb1[3]], [bb1[0], bb1[3]]])
    poly_2 = Polygon([[bb2[0], bb2[1]], [bb2[2], bb2[1]], [bb2[2], bb2[3]], [bb2[0], bb2[3]]])
    if poly_1.union(poly_2).area != 0:
        iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
        return iou
    else:
        return 0


def getObjectCategories(image_list):
    category_list = []
    category_dict = {}
    for img in image_list:
        for obj in img.get_object_instances():
            obj_category_id = obj.get_category_id()
            if obj_category_id not in category_list:
                category_dict[obj_category_id] = obj.get_category_title()
    return category_dict


def get_bbox_width_and_height_list(image_object_list, dataset):
    width_list = []
    height_list = []
    object_counter = 0
    ErrorLog = []
    for image in image_object_list:
        for obj in image.get_object_instances():
            object_counter += 1
            bbox = obj.get_bbox()
            bbox_width = bbox[2]
            bbox_height = bbox[3]
            width_list.append(bbox_width)
            height_list.append(bbox_height)
            if bbox_width > image.get_width() or bbox_height > image.get_height():
                ErrorLog.append("Image: " + str(
                    image.get_id()) + "Size: " + str(image.get_size_each()) + "\tObjectInstance: " + str(
                    obj.get_object_id()) + "\tBbox Width: " + str(
                    bbox_width) + "\tBbox Height: " + str(
                    bbox_height) + "\tFilename: " + str(image.get_filename()) + "\n")
    with open("/Errors/" + dataset + "/wrong bbox size.txt", 'w+') as textFile:
        for error in ErrorLog:
            textFile.write(error)

    # print(object_counter)
    # print(len(width_list))
    # print(len(height_list))
    # print(width_list)

    return [width_list, height_list]

