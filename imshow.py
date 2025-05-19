import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from manim import TexTemplate

physics = TexTemplate()
physics.add_to_preamble(r"\usepackage{physics}")

amsmath = TexTemplate()
amsmath.add_to_preamble(r"\usepackage{amsmath}")

def construct_imshow(filename, function=None, extent=None, n_pixels=None, mapp='viridis'):
    x_vals = np.linspace(extent[0], extent[1], n_pixels)
    y_vals = np.linspace(extent[2], extent[3],
                         round(n_pixels*(extent[3]-extent[2])/(extent[1]-extent[0])))
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = function(X, Y)

    norm = Normalize(vmin=np.min(Z), vmax=np.max(Z))
    Z_normalized = norm(Z)

    # Get RGB using colormap
    colored_image = plt.get_cmap(mapp)(Z_normalized)
    print(X.shape)

    # Create a fading mask based on distance from center
    distances = np.zeros((4, y_vals.size, x_vals.size))
    distances[0,:,:] = np.abs(X-extent[0])
    distances[1,:,:] = np.abs(Y-extent[2])
    distances[2,:,:] = np.abs(extent[1]-X)
    distances[3,:,:] = np.abs(extent[3]-Y)
    alpha_mask = np.arctan(np.min(distances, axis=0) * 2) / np.pi
    # Apply mask to alpha channel
    colored_image[..., 3] = alpha_mask  # Set alpha channel


    window_2d = np.outer(np.hanning(x_vals.size), np.hanning(y_vals.size))
    Z *= window_2d
    # Compute the 2D Fourier Transform
    # Z -= np.mean(Z)  # Remove the DC component
    fft_result = np.fft.fft2(Z)  # Perform the 2D FFT
    fft_shifted = np.fft.fftshift(fft_result)  # Shift the zero frequency to the center
    # fft_result -= np.mean(fft_result)
    fftZ = np.abs(fft_shifted)  # Compute the magnitude of the FFT
    print(np.min(fftZ), np.max(fftZ))
    norm = Normalize(vmin=np.min(fftZ), vmax=np.max(fftZ))
    Z_normalized = norm(fftZ)
    fft_image = plt.get_cmap(mapp)(fftZ)
    fft_image[..., 3] = alpha_mask  # Set alpha channel


    plt.imsave("fft_"+filename, fft_image, cmap=mapp, origin='lower')
    plt.imsave(filename, colored_image, cmap=mapp, origin='lower')