from .wgif import wgif
import numpy as np
from math import isinf
import colorsys

def adjust_lighting(rgb, new_lighting):
    hls = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    rgb = colorsys.hls_to_rgb(hls[0], new_lighting, hls[2])
    return [int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)]

def rgb_to_greyscale(rgb):
    return 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]

# https://link.springer.com/article/10.1007/s41095-021-0232-x
def illuminate(image_data, color_restoration=None): # TODO
    """Illuminates the given image

    Parameters
    ----------
    image : array
        The image that is to be illuminated, given as array with shape (width, height, 3) for an rgb image and (width, height) for an greyscale image. The image data should be in the range of [0, 255].
    color_restoration : boolean, optional
        Wheter the color should be restored after illumination, only applicable for rgb input images
    Returns
    -------
    array
        The illuminated image values. The output depends on the type of image (rgb or greyscale) and color_restoration.
    """
    if color_restoration not in [None, 'linear', 'hls']:
        raise Exception("The provided color restoration method not supported, supported color restoration methods: [None, 'linear', 'hls']")
    
    image_data = image_data.astype(np.uint8)
    is_greyscale = len(image_data.shape) == 2
    height, width = image_data.shape[0:2]
    
# 1) Load original RGB color image S(x, y), convert to HSI color model, select intensity image SI (x, y).
    S_I = image_data if is_greyscale\
        else np.apply_along_axis(rgb_to_greyscale, 2, image_data)\
            .reshape(height, width)\
            .astype(np.uint8)
    
# 2) Enhance intensity image
    # Compute and process illumination component
    # 1. Use WGIF to estimate illumination component of intensity: SILi(x, y) = aiSIi(x, y) + bi
    S_IL_PRE = wgif(S_I, S_I, 3, 0.001)
    S_IL_PRE = np.clip(S_IL_PRE,0.1,255)
    S_IL = S_IL_PRE / 255
    #  Adaptive brightness equalization
    #   2. Correct the illumination component using adaptive gamma function: SILG(x, y) = SIL(x, y))f(x,y)
    a = 1 - (np.mean(S_IL))
    gamma = (S_IL + a)/(1+a)
    S_ILG = np.abs(S_IL) ** gamma
    
    #   3. Perform global linear stretching: SILGf (x, y) = SILG(x,y)-min(SILG(x,y)) / max(SILG(x,y))-min(SILG(x,y))
    S_ILGf = (S_ILG - np.min(S_ILG)) / (np.max(S_ILG) - np.min(S_ILG))
    # Compute and process reflection component image
    #   4. Compute the reflection component: SIR(x, y) = SI (x, y)/SIL(x, y)
    S_IR = S_I / S_IL_PRE
    #   5. Denoise the reflection component using WGIF: SIRHi(x, y) = aiSIR(x, y) + bi
    S_IRH = wgif(S_IR*255, S_IR*255, 3, 0.001) / 255
    
    
# 3) Image fusion
    # Fuse the processed illumination component and reflection component
    # 1. Compute the enhanced intensity image: SIE(x, y) = SILGf (x, y)SIRH(x, y)
    S_IE = S_ILGf * S_IRH
    # 2.Improve the brightness of the fused image using the S-hyperbolic tangent function:
    b = np.mean(S_IE)
    S_IEf = 1 / (1 + np.exp(-8* (S_IE-b)))
    if is_greyscale or color_restoration is None:
        return (S_IEf * 255).astype(np.uint8)
        
# 4) Color restoration
    # 1. Calculate the brightness gain coefficient: a(x, y) = S_IEf (x, y)/S_I (x, y)
    alpha = 255 * S_IEf / S_I # *255 since S_IEf is in range [0,1]

    # 2. Convert the enhanced HSI image to RGB by linear color restoration RGB(x, y) = a(x, y)RGB(x, y)
    new_image_data = np.copy(image_data)
    if color_restoration == 'linear':
        for i in range(height): # for every pixel:
            for j in range(width):
                if not isinf(alpha[i][j]):
                    new_image_data[i][j] = tuple(map(lambda x: int(np.clip(x* alpha[i,j], 0, 255)), new_image_data[i][j]))
    elif color_restoration == 'hls':
        for i in range(height): # for every pixel:
            for j in range(width):
                if not isinf(alpha[i][j]):
                    new_image_data[i][j] = tuple(map(lambda x: int(np.clip(x, 0, 255)), adjust_lighting(new_image_data[i][j], S_IEf[i][j])))
    return new_image_data