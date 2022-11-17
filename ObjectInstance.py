class ObjectInstance:
    def __init__(self, object_id, segmentation, bbox, image_id, category_title, category_id, supercategory):
        self.object_id = object_id
        self.segmentation = segmentation
        self.bbox = bbox
        self.size = bbox[2]*bbox[3]
        self.image_id = image_id
        self.category_id = category_id
        self.category_title = category_title
        self.parent_category = ""
        self.supercategory = supercategory

    def get_object_id(self):
        return self.object_id

    def set_segmentation(self, segmentation):
        self.segmentation = segmentation

    def get_segmentation(self):
        return self.segmentation

    def get_segmentation_values(self):
        # print("Self Segmentation")
        # print(self.segmentation)
        for segmentation in self.get_segmentation():
            if len(segmentation) == 1:
                [segmentation] = segmentation
            x_list = []
            y_list = []
            for i in range(0, len(segmentation) - 1, 2):
                x_list.append(segmentation[i])
                y_list.append(segmentation[i + 1])
            return [x_list, y_list]

    def get_supercategory(self):
        return self.supercategory

    def get_center(self, xy_list):
        x_list = xy_list[0]
        y_list = xy_list[1]

        if (len(x_list)) == 1:
            [x_list] = y_list
            [y_list] = y_list

        length = len(x_list)
        # print(x_list)
        # print(y_list)
        try:
            x = sum(x_list) / length
            y = sum(y_list) / length
        except:
            print("Error bei x_list: " + str(x_list) + "und länge: " + str(len(x_list)))
            x = 0
            y = 0
        return x, y

    def get_bbox_center(self):
        bbox = self.bbox
        x_top_left = bbox[0]
        y_top_left = bbox[1]
        width = bbox[2]
        height = bbox[3]

        x = x_top_left + width*0.5
        y = y_top_left + height*0.5

        # print("BBox: " + str(bbox) + " Center: " + str(x) + " " + str(y))
        return x, abs(y)

    def set_bbox(self, bbox):
        self.bbox = bbox

    def get_bbox(self):
        return self.bbox

    def get_size(self):
        return self.size

    def set_category_id(self, category_id):
        self.category_id = category_id

    def set_category_title(self, category_title):
        self.category_title = category_title

    def get_category_title(self):
        return self.category_title

    def get_category_id(self):
        return self.category_id

    def get_object_size(self):
        return self.size

    def get_image_id(self):
        return self.image_id

    def get_segmentation_info(self):
        return str(self.segmentation) + " " + str(self.bbox) + " " + str(self.size)

    def get_object_instance_info(self):
        return "Kategorie: {3} (id:{2})\nSegmentierung: {0}\nBbox: {1}".format(
            str(self.segmentation), str(self.bbox), str(self.category_id), self.category_title, self.parent_category)
