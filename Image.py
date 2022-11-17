import statistics  # Berechnung von Median
from operator import attrgetter

class Image:

    def __init__(self, image_id, filename, height, width, location, dataset, image_license):
        self.id = image_id
        self.filename = filename
        self.folder = ''
        self.location = location
        self.width = width
        self.height = height
        self.dataset = dataset
        self.object_instances = []
        self.license = image_license

    def get_dataset(self):
        return self.dataset

    def get_id(self):
        return self.id

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_folder(self, folder):
        self.folder = folder

    def get_license(self):
        return self.license

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_folder(self):
        return self.folder

    def get_size(self):
        return self.height * self.width

    def get_size_each(self):
        size = str(self.get_height()) + "x" + str(self.get_width())
        return size

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def add_object_instance(self, object_instance):
        self.object_instances.append(object_instance)

    def get_object_instances(self):
        return self.object_instances

    def remove_object_instance(self, object_instance):
        self.object_instances.remove(object_instance)

    def get_object_amount(self):
        return len(self.object_instances)

    def get_smallest_object(self):
        smallest_object = min(self.object_instances, key=attrgetter('area'))
        return smallest_object.get_object_size()

    def get_biggest_object(self):
        biggest_object = max(self.object_instances, key=attrgetter('area'))
        return biggest_object.get_object_size()

    def get_average_object_size(self):
        temp_list = []
        for oi in self.object_instances:
            temp_list.append(oi.get_object_size())
        return sum(temp_list) / len(self.object_instances)

    def get_median_object_size(self):
        temp_list = []
        for oi in self.object_instances:
            temp_list.append(oi.get_object_size())
        return statistics.median(temp_list)

    def get_object_to_image_ratio(self, object_size):
        return object_size / (self.width * self.height)

    def get_image_info(self):
        return "ID: {0}\nAuflösung: {1}x{2}\nObjektinstanzen:{3}".format(
            str(self.id), str(self.width), str(self.height), str(len(self.object_instances)))
