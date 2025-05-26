import numpy as np
import pyvista as pv
from astropy.io import fits

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

#cube1 = "co32f.fits"
cube1 = "so.fits"
cube2 = "sio87.fits"

vol1 = load_fits_volume(cube1)
#print(np.nanmin(vol1), np.nanmax(vol1))
vol2 = load_fits_volume(cube2)
#print(np.nanmin(vol2), np.nanmax(vol2))

naxis3 = max(vol1.shape[2],vol2.shape[2])
print(naxis3)
grid1 = create_pv_grid(vol1,naxis3)
#print(grid1)
grid2 = create_pv_grid(vol2,naxis3)
#print(grid2)
plotter = pv.Plotter()

threshold1 = 0.001
threshold2 = 0.005

opacity1 = [0.0 if x < threshold1 else 1 for x in np.linspace(np.nanmin(vol1), np.nanmax(vol1)/2., 256)]
opacity2 = [0.0 if x < threshold2 else 1 for x in np.linspace(np.nanmin(vol2), np.nanmax(vol2)/2., 256)]

plotter.add_volume(grid1, scalars="intensity", cmap="Reds", opacity=opacity1, opacity_unit_distance=0.05, shade=False)
plotter.add_volume(grid2, scalars="intensity", cmap="Blues", opacity=opacity2, opacity_unit_distance=0.05, shade=False)

#plotter.add_mesh(grid1.outline(), color="white", line_width=1)


plotter.add_axes()
plotter.show()
