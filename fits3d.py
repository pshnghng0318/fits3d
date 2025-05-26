import numpy as np
import pyvista as pv
from astropy.io import fits

def visualize_fits_3d_volume(filepath, threshold=0.0):
    with fits.open(filepath) as hdul:
        data = hdul[0].data.squeeze().astype(float)

    if data.ndim != 3:
        raise ValueError("FITS 檔案不是三維資料")

    volume = np.transpose(data, (2, 1, 0))  # (FREQ, DEC, RA)
    volume[volume < 0] = 0.0

    #print("資料範圍：", np.nanmin(volume), "到", np.nanmax(volume))
    #print("NaN 數量：", np.isnan(volume).sum())
    #print("資料 shape：", volume.shape)

    grid = pv.ImageData()
    grid.dimensions = np.array(volume.shape) + 1
    grid.spacing = (1, 1, 1)
    grid.origin = (0, 0, 0)
    grid.cell_data["intensity"] = volume.flatten(order="F")

    plotter = pv.Plotter()
    plotter.add_volume(grid, scalars="intensity",
                       cmap="rainbow", 
                       opacity="sigmoid",
                       opacity_unit_distance=2.0,
                       shade=True)
    plotter.add_axes()
    plotter.show()

visualize_fits_3d_volume("sio87.fits", threshold=1e-3)

