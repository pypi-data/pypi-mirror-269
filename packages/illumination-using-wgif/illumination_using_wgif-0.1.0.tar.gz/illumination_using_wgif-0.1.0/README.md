# Illumination using WGIF

This repository features an implementation of the algorithm proposed in ["Low and non-uniform illumination color image enhancement using weighted guided image filtering" by Mu, Q., Wang, X., Wei, Y. et al. (2021)](https://doi.org/10.1007/s41095-021-0232-x)

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

## Results
Illuminated images from the [DARK FACE: Face Detection in Low Light Condition](https://flyywh.github.io/CVPRW2019LowLight/) dataset.
1. Column: original image
2. Column: illuminated greyscale values
3. Column: color restoration using linear transformation (slow)
4. Column: color restoration using hls manipulation (very slow)

![Illuminated images from the DARK FACE dataset](/assets/Illumination-result.png)

## Notes
The color restoration is terribly slow as of now, could be optimized