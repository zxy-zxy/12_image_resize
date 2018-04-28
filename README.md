# Image Resizer
A Python script for image resizing. 

## Requirements
Python >= 3.5 required. 

[Python Imaging Library](https://github.com/python-pillow/Pillow) is also required.

For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

You can use  
```bash
pip install -r requirements.txt
```
to install dependencies.

## Usage

### There are 2 modes of the script:
1.  Resizing image by providing a scale parameter.
2.  Resizing image by providing height and with of desired result. 
Also you can specify only one indicator and the second one will be calculated by the given.

### Example input
```bash
python image_resize.py scale 2 original_image.jpg
```
```bash
python image_resize.py resize --width 600  original_image.jpg
```

### Output
Desired output also can be provided as an argument:
```bash
python image_resize.py scale 2 image.jpg --output=/home/username/scaled.jpg
```

# Project Goals
The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)


