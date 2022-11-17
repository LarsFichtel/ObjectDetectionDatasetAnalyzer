import json
import random

# temp image list holder
image_list = []
keystore = {}
# Insert Path to selected, downloaded dataset annotation file

# Careful!! Change directory if needed!!

annotaion_folder = "E:/newDS/images_256a/annotations/"
annotation_file = "E:/newDS/images_256a/annotations/annotation.json"

# Select how you want to distribute the images into the different sets (i.e. 80% training, 10% val, 10% test)
training = 80
test = 10
validation = 10

# Define seed for testing/traceability
random.seed(100)

with open(annotation_file) as json_file:
    data = json.load(json_file)
    # Iterate through all 'images' in json file
    for p in data['images']:
        image_list.append(p['id'])
print(str(len(image_list)) + " Pictures loaded from source annotation file.")

if training + test + validation == 100 and training > 0 and test > 0 and validation > 0:
    # int cast to avoid no of pics > image_list length
    # if no of pics < image list -> add 1 img to training data set
    amount_training = int(len(image_list) * training / 100)
    amount_test = int(len(image_list) * test / 100)
    amount_val = int(len(image_list) * validation / 100)

    if amount_training + amount_test + amount_val < len(image_list):
        missing_no_of_pics = len(image_list) - (amount_training + amount_test + amount_val)
        amount_training += missing_no_of_pics

    training_data = random.sample(image_list, k=amount_training)
    rest_data = list(set(image_list) - set(training_data))
    validation_data = random.sample(rest_data, k=amount_val)
    test_data = list(set(rest_data) - set(validation_data))

    for img in training_data:
        keystore[img] = 0
    for img in validation_data:
        keystore[img] = 1
    for img in test_data:
        keystore[img] = 2

    print("Writing " + str(len(keystore)) + " entries in json file.")
    json.dump(keystore, open(annotaion_folder + "train_val_test_distribution.json", "w", encoding='utf-8'), )
else:
    print("Please make sure to only use positive numbers and that you have exactly 100% total...")
