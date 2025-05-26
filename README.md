# FITS 3D Volume Visualizer

This Python script visualizes 3D astronomical data stored in a FITS file using [PyVista](https://github.com/pyvista/pyvista) for interactive volume rendering.

## Features

- Reads 3D FITS data cubes (e.g., ALMA data)
- Automatically squeezes singleton dimensions (e.g., shape (1, N1, N2, N3) → (N1, N2, N3))
- Transposes cube axes to (FREQ, DEC, RA) so that frequency becomes the vertical axis (Z)
- Visualizes the volume using opacity and color mapping
- Thresholding for showing only signal above a certain value

## Requirements

- Python 3.8+
- `astropy`
- `pyvista`
- `numpy`

e.g., 
# 1. 建立虛擬環境
python3 -m venv astroenv

# 2. 啟用虛擬環境
source astroenv/bin/activate

# 3. 安裝所需的 Python 套件（包括 astropy）
pip install astropy numpy matplotlib

Install dependencies:

```bash
pip install astropy pyvista numpy

## Usage

- python fits3d.py

## Notes

- FITS files with shape like (1, FREQ, DEC, RA) will be auto-squeezed.
- PyVista expects data in (Z, Y, X) → so cube is transposed to (FREQ, DEC, RA).
- Adjust threshold to hide noise.
- Use a suitable colormap (e.g., "rainbow", "turbo", "inferno").
