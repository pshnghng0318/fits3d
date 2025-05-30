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

    vmin, vmax = np.nanmin(volume), np.nanmax(volume)
    print(vmin,vmax)

    # 建立 binary opacity curve：< threshold → 0, >= threshold → 1
    opacity = [0.0 if val < threshold else 1.0 for val in np.linspace(vmin, vmax, 256)]

    # 建立 PyVista ImageData
    grid = pv.ImageData()
    grid.dimensions = np.array(volume.shape) + 1
    grid.spacing = (1, 1, 1)
    grid.origin = (0, 0, 0)
    grid.cell_data["intensity"] = volume.flatten(order="F")
    print(grid)
    # 繪製
    plotter = pv.Plotter()
    plotter.add_volume(
        grid,
        scalars="intensity",
        cmap="rainbow",
        opacity=opacity,
        opacity_unit_distance=0.1,
        shade=True
    )
    plotter.add_axes()
    plotter.show()

# 範例：將低於 1e-3 的值完全透明
visualize_fits_3d_volume("sio87.fits", threshold=1e-2)

