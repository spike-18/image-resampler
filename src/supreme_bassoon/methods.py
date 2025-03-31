import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift

def nearest_neighbor(image, scale):
    in_h, in_w = image.shape[:2]
    out_h, out_w = int(in_h * scale), int(in_w * scale)
    
    if image.ndim == 3:
        out_image = np.zeros((out_h, out_w, image.shape[2]), dtype=image.dtype)
    else:
        out_image = np.zeros((out_h, out_w), dtype=image.dtype)
        
    for i in range(out_h):
        for j in range(out_w):
            src_i = int(i / scale)
            src_j = int(j / scale)
            out_image[i, j] = image[src_i, src_j]
    
    return out_image

def bilinear_interpolation(image, scale):
    in_h, in_w = image.shape[:2]
    out_h, out_w = int(in_h * scale), int(in_w * scale)
    
    if image.ndim == 3:
        out_image = np.zeros((out_h, out_w, image.shape[2]), dtype=image.dtype)
    else:
        out_image = np.zeros((out_h, out_w), dtype=image.dtype)
    
    for i in range(out_h):
        for j in range(out_w):
            x = i / scale
            y = j / scale

            x0 = int(np.floor(x))
            x1 = min(x0 + 1, in_h - 1)
            y0 = int(np.floor(y))
            y1 = min(y0 + 1, in_w - 1)
            
            dx = x - x0
            dy = y - y0
            
            if image.ndim == 3:
                top = (1 - dy) * image[x0, y0] + dy * image[x0, y1]
                bottom = (1 - dy) * image[x1, y0] + dy * image[x1, y1]
                value = (1 - dx) * top + dx * bottom
            else:
                top = (1 - dy) * image[x0, y0] + dy * image[x0, y1]
                bottom = (1 - dy) * image[x1, y0] + dy * image[x1, y1]
                value = (1 - dx) * top + dx * bottom
            
            out_image[i, j] = value
    return out_image

def piecewise_linear_interpolation(image, scale):
    in_h, in_w = image.shape[:2]
    new_h = int(in_h * scale)
    temp = np.zeros((new_h, in_w) + (() if image.ndim == 2 else (image.shape[2],)), dtype=image.dtype)
    
    row_indices = np.arange(new_h) / scale
    for j in range(in_w):
        if image.ndim == 2:
            col_data = image[:, j]
            temp[:, j] = np.interp(row_indices, np.arange(in_h), col_data)
        else:
            for c in range(image.shape[2]):
                col_data = image[:, j, c]
                temp[:, j, c] = np.interp(row_indices, np.arange(in_h), col_data)
    
    new_w = int(in_w * scale)
    if image.ndim == 2:
        out_image = np.zeros((new_h, new_w), dtype=image.dtype)
    else:
        out_image = np.zeros((new_h, new_w, image.shape[2]), dtype=image.dtype)
    
    col_indices = np.arange(new_w) / scale
    for i in range(new_h):
        if image.ndim == 2:
            row_data = temp[i, :]
            out_image[i, :] = np.interp(col_indices, np.arange(in_w), row_data)
        else:
            for c in range(image.shape[2]):
                row_data = temp[i, :, c]
                out_image[i, :, c] = np.interp(col_indices, np.arange(in_w), row_data)
    
    return out_image

def l2_optimal_interpolation(image, scale):
    if not float(scale).is_integer():
        raise ValueError("L2 optimal interpolation via Fourier zero-padding requires an integer scale factor.")
    scale = int(scale)
    
    def fourier_upscale(channel):
        h, w = channel.shape
        f = fftshift(fft2(channel))
        
        new_h, new_w = h * scale, w * scale
        
        f_up = np.zeros((new_h, new_w), dtype=complex)
        
        h_center, w_center = new_h // 2, new_w // 2
        h_half, w_half = h // 2, w // 2
        
        f_up[h_center - h_half:h_center - h_half + h, w_center - w_half:w_center - w_half + w] = f
        
        upscaled = np.real(ifft2(ifftshift(f_up)))
        return upscaled * (scale**2)
    
    if image.ndim == 2:
        return fourier_upscale(image)
    else:
        channels = []
        for c in range(image.shape[2]):
            channels.append(fourier_upscale(image[..., c]))
        return np.stack(channels, axis=-1)
