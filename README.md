#  Object Detection Dataset Analyzer for Tiny and Small Objects

The dataset Analyzer was developed to analyze different dataset to compare the representation of tiny and small objects in a datasets [1].

The size categories are:
- Large: > 96x96px
- Medium: < 96x96px, > 32x32px
- Small: < 32x32px & 16x16>
- Very Small: < 16x16px & > 32x32px
- Tiny: < 8x8px
## 1. Format of the Annotation Files
The annotation-file within the dataset folders need to be in the COCO-Format [2]. 

e.g.
```json
{
  "images": [
    {"id": "59198, "file_name": "3d9df7c0e.jpg", "width": 1024, "height": 768, "dataset-source": "TASOD", "license": "TBD"}, 
    {"id": "6925", "file_name": "224192aec.png", "width": 800, "height": 800, "dataset-source": "TASOD", "license": "TBD"}, 
    {"id": "10", "file_name": "9df54a644.png", "width": 800, "height": 800, "dataset-source": "TASOD", "license": "TBD"}],
  "annotations": [
    {"area": 520, "bbox": [308, 757, 52, 10], "category": "vehicle", "category_id": 2, "id": 608, "image_id": "59198"}, 
    {"area": 228, "bbox": [396, 761, 38, 6], "category": "vehicle", "category_id": 2, "id": 609, "image_id": "6925"}, 
    {"area": 611, "bbox": [459, 755, 47, 13], "category": "vehicle", "category_id": 2, "id": 610, "image_id": "10"}]
}
```

## 2. Potential Necessary Changes    
Change dataset name in dataAnalyzer.py and dataset_splits if necessary.
Change name of Dataset-Folder to your desired name. Same for the dataset folder in the Plot folder.

## 3. Usage 
Execute the python file dataAnalyzer.py and see the magic happen.

dataAnalyzer.py: Main-File edit and execute. Uses plotter.py, Image.py and ObjectInstance.py.

plotter.py: file to generate the plots

Image.py: Image-Class-file

ObjectInstance.py: ObjectInstance-Class-file

## 4. Output
The generated plots will be safed in the Plots folder. 
Depending on the plot pdf, png, scg and/or tex files will be generated.

These plots contain:

### 4.1 Size categorization
Categorizes the objects in the categories large, medium, small, very small and tiny.

- Large: > 96x96px
- Medium: < 96x96px, > 32x32px
- Small: < 32x32px & 16x16>
- Very Small: < 16x16px & > 32x32px
- Tiny: < 8x8px

![cate Image](Examples\TASODv1\size_categorization_TASODv1.png)
### 4.2 total object distribution on image
Distribution of the center of objects within the images with total values.

![distro Image](Examples\TASODv1\totalobjectdistributiononimage.png)

### 4.3 percentage image  distribution on image
Distribution of the center of objects within the images with percentages.

![distro Image](Examples\TASODv1\percentage_object_distribution_on_image.png)

### 4.4 complete bbox clean bbox distribution on image

![distro Image](Examples\TASODv1\complete_bbox_clean_bbox_distribution_on_image.png)
### 4.5 complete bbox bbox distribution on image
Distribution of the complete bounding box of objects within the images with percentages.

![distro Image](Examples\TASODv1\complete_bboxbbox_distribution_on_image.png)

### 4.6 boundingbox center clean bbox distribution on image
Distribution of the center of objects within the images with percentages.

![distro Image](Examples\TASODv1\bbox_center_clean_bbox_distribution_on_image.png)
### 4.7 boundingbox_width

![distro Image](Examples\TASODv1\boundingbox_width.png)
### 4.8 boundingbox_height

![distro Image](Examples\TASODv1\boundingbox_height.png)
### 4.9 boundingbox_size_overview

![distro Image](Examples\TASODv1\boundingbox_size_overview.png)



# 5. Acknowledgements
Special thanks to Dominik Erbacher for helping with the development.

# 6. References
[1] Lars Fichtel, Dominik Erbacher, Leon Heller, Alexander Frühwald, Leonhard Hösch, and Christian Bachmeir. "Analysis of Object Detection Datasets for Machine Learning with Small and Tiny Objects." In Eleventh International Conference on Engineering Computational Technology 2022 & the Fourteenth International Conference on Computational Structures Technology 2022, 2022.

[2] Tsung-Yi Lin, Michael Maire, Serge J. Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, C. Lawrence Zitnick: "Microsoft COCO: Common Objects in Context." ECCV (5) 2014: 740-755