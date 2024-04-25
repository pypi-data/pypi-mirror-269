from setuptools import setup

setup(
    name='illumination_using_wgif',
    version='0.1.0',
    description='A Python implementation of https://doi.org/10.1007/s41095-021-0232-x',
    long_description_content_type='text/markdown',
    long_description='''This repository features an implementation of the algorithm proposed in ["Low and non-uniform illumination color image enhancement using weighted guided image filtering" by Mu, Q., Wang, X., Wei, Y. et al. (2021)](https://doi.org/10.1007/s41095-021-0232-x)

## Installation
```cmd
pip install illumination_using_wgif
```

## Usage

```python
from PIL import Image
from illumination_using_wgif import illuminate

# load_image
image = Image.open("./<YOUR_IMAGE_HERE>")

rgb_image_data = np.reshape(image.getdata(), (image.size[1], image.size[0], 3))
greyscale_image_data = np.reshape(image.convert('L').getdata(), (image.size[1], image.size[0]))

# greyscale
illuminated_greyscale_data = illuminate(rgb_image_data)
# or: illuminated_greyscale_data = illuminate(greyscale_image_data)
illuminated_greyscale = Image.fromarray(illuminated_greyscale_data)

# linear color restoration
illuminated_linear_data = illuminate(rgb_image_data, 'linear')
illuminated_linear = Image.fromarray(illuminated_linear_data)

# hls color restoration
illuminated_hls_data = illuminate(rgb_image_data, 'hls')
illuminated_hls = Image.fromarray(illuminated_hls_data)
```

## Github
For more info see [https://github.com/muelphil/illumination_using_wgif](https://github.com/muelphil/illumination_using_wgif)

## Notes
The color restoration is terribly slow as of now, could be optimized''',
    url='https://github.com/muelphil/illumination_using_wgif',
    author='Philip Müller',
    author_email='muellers.philp@googlemail.com',
    license='CC BY 4.0 DEED',
    packages=['illumination_using_wgif'],
    install_requires=['numpy>=1.26.3','scipy>=1.11.4','Pillow>=10.2.0'],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ],
)