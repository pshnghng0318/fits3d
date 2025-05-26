import numpy as np
import pyvista as pv
import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

from astropy.io import fits

def smart_opacity(volume, percentile=95, alpha=0.7, steps=256):
    """
    根據給定的資料，生成一個 opacity transfer function。
    低於指定 percentile 的值為 0，超過的設為 alpha。
    """
    vmin = np.nanmin(volume)
    vmax = np.nanpercentile(volume, percentile)
    lut = np.linspace(vmin, vmax, steps)
    opacity = [0.0 if x < vmax else alpha for x in lut]
    return opacity

def load_fits_volume(filepath):
    with fits.open(filepath) as hdul:
        data = hdul[0].data.squeeze().astype(float)
        data = np.flip(data, axis=0)

    volume = np.transpose(data, (2, 1, 0))  # FREQ, DEC, RA
    volume[volume < 0] = 0.0
    return volume

def create_pv_grid(volume,naxis3):
    grid = pv.ImageData()
    grid.dimensions = np.array(volume.shape) + 1
    grid.spacing = (1, 1, naxis3/volume.shape[2])
    print(grid.spacing)
    grid.origin = (0, 0, 0)
    grid.cell_data["intensity"] = volume.flatten(order="F")
    return grid


cube1 = "so.fits"
cube2 = "sio87.fits"
cube3 = "co32f.fits"

vol1 = load_fits_volume(cube1)
vol2 = load_fits_volume(cube2)
vol3 = load_fits_volume(cube3)

naxis3 = max(vol1.shape[2], vol2.shape[2], vol3.shape[2])

grid1 = create_pv_grid(vol1,naxis3)
grid2 = create_pv_grid(vol2,naxis3)
grid3 = create_pv_grid(vol3,naxis3)

plotter = pv.Plotter()

threshold1 = 0.001
threshold2 = 0.005
threshold3 = 0.01

#opacity1 = [0.0 if x < threshold1 else 1 for x in np.linspace(np.nanmin(vol1), np.nanmax(vol1)/2., 256)]
#opacity2 = [0.0 if x < threshold2 else 1 for x in np.linspace(np.nanmin(vol2), np.nanmax(vol2)/2., 256)]
#opacity3 = [0.0 if x < threshold3 else 1 for x in np.linspace(np.nanmin(vol3), np.nanmax(vol3)/2., 256)]

opacity1 = smart_opacity(vol1, percentile=97, alpha=1.0)
opacity2 = smart_opacity(vol2, percentile=95, alpha=0.6)
opacity3 = smart_opacity(vol3, percentile=90, alpha=0.3) 


plotter = pv.Plotter(window_size=(screen_width, screen_height * 2))

plotter.add_volume(grid3, scalars="intensity", cmap="Blues", opacity=opacity3, opacity_unit_distance=0.05, shade=False)
plotter.add_volume(grid2, scalars="intensity", cmap="Greens", opacity=opacity2, opacity_unit_distance=0.05, shade=False)
plotter.add_volume(grid1, scalars="intensity", cmap="Reds", opacity=opacity1, opacity_unit_distance=0.05, shade=False)



#plotter.add_mesh(grid1.outline(), color="white", line_width=1)

plotter.add_axes()
plotter.show()
