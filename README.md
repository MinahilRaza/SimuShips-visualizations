# SimuShips - A High Resolution Simulation Dataset for Ship Detection with Precise Annotations
Available at: https://zenodo.org/record/7003924

SimuShips is a high-resolution, simulation-based dataset for maritime environments consisting of images resembling the real world. Our dataset incorporates diversity of objects, weather, illumination, visible proportion and scale. This package provides Jupyter notebooks that assists in generating and visualizing the annotations in SimuShips. The full dataset and annotations can be downloaded from Zenodo.

| Characteristics| Value |
|:--------------------------------------|:------------------------|
| Total number of images                | 6756 + 2715 = 9471 |
| Images (without weather augmentation) | 2715 |
| Range of number of objects in images  | [1, 10] |     
| Categories                            | Dynamic (0), Static (1) | 

## Requirements
- Python3
- Jupyter
- OpenCV
- Pillow
- Matplotlib

## How to Get Started
Clone the repo

```bash
         git clone https://github.com/MinahilRaza/SimuShips-visualizations.git
```
Sample images have been provided in this repository. In order to generate annotations, run `Generate_Annotations.ipynb`
The annotations get stored in `annotated_images/annotations`. Run `TestBoundingBox.ipynb` to visualize the annotations.

## Results
One example of a succesful run is shown below:

<img src="https://user-images.githubusercontent.com/30044227/191004455-de4bffb8-13e2-4157-b7a5-031fb619c5f2.png" width="290"> <img src="https://user-images.githubusercontent.com/30044227/191004478-7daea630-0935-45b9-a9c8-a2f0fee7b13d.png" width="290"> <img src="https://user-images.githubusercontent.com/30044227/191004502-17158a85-5d8a-48b7-b8b6-2a1fb1cde762.png" width="290">
