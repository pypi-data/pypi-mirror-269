from scipy import ndimage

def edgeaware(img, radius):
    (height, width) = img.shape
    L = img.max()-img.min()
    eps = (0.001*L)**2
    mean_I = ndimage.uniform_filter(img, size=radius, mode='mirror') # calc_mean(image, radius, N)
    corr_I = ndimage.uniform_filter(img*img, size=radius, mode='mirror') # calc_mean(img .* img, r, N)
    var_I = corr_I - mean_I * mean_I
    gamma = (var_I + eps) * sum(1 / (var_I + eps)) / (height*width)
    return gamma

# https://github.com/wjymonica/WGIF-and-GIF
def wgif(img, guide, radius, llambda):
    gamma = edgeaware(img, 1)
    (height, width) = img.shape
    #step 1:
    mean_img = ndimage.uniform_filter(img, size=radius, mode='mirror') #calc_mean(img, r, N)
    mean_guide = ndimage.uniform_filter(guide, size=radius, mode='mirror') #calc_mean(guide, r, N)
    corr_img = ndimage.uniform_filter(img*img, size=radius, mode='mirror') #calc_mean(img .*img, r, N)
    corr_Ip = ndimage.uniform_filter(img*guide, size=radius, mode='mirror') #calc_mean(img .*guide, r, N)

    #step 2:
    var_I = corr_img - mean_img * mean_img
    cov_Ip = corr_Ip - mean_img * mean_guide

    #step 3:
    a = cov_Ip / (var_I + llambda / gamma)
    b = mean_guide - a * mean_img

    #step 4:
    mean_a = ndimage.uniform_filter(a, size=radius, mode='mirror') #calc_mean(a, r, N)
    mean_b = ndimage.uniform_filter(b, size=radius, mode='mirror') #calc_mean(b, r, N)

    q = mean_a * img + mean_b

    return q