"""
OpticalSimulations.py

This script performs optical simulations on multi-class segmentation masks using SIMPA and MCX.
It supports tissue type mapping and layered background simulation, and outputs the resulting
initial pressure distributions as .mat files.

Requirements:
- SIMPA (https://github.com/IMSY-DKFZ/simpa)
- MCX installed and accessible in system PATH
"""

import os
import argparse
import numpy as np
import simpa as sp
import skimage.io as skio
from simpa import Tags
from scipy.io import savemat

# --- Command-line Arguments ---
parser = argparse.ArgumentParser(description="Run SIMPA + MCX optical simulations on multi-class segmentations.")
parser.add_argument("--segmentation_path", type=str, required=True, help="Path to 3D segmentation image (TIFF stack).")
parser.add_argument("--background_path", type=str, required=True, help="Path to background segmentation (TIFF stack).")
parser.add_argument("--output_dir", type=str, required=True, help="Directory to save .mat output files.")
parser.add_argument("--spacing_mm", type=float, default=0.02, help="Voxel spacing in mm.")
parser.add_argument("--random_seed", type=int, default=3500, help="Random seed for reproducibility.")
args = parser.parse_args()

# --- Simulation Parameters ---
SPACING = args.spacing_mm
SEED = args.random_seed
WAVELENGTH = 532  # nm
VOLUME_NAME = f"SIMPA_MC_{SEED}"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Workaround for Intel MKL bug

# --- Load and Combine Segmentations ---
seg = skio.imread(args.segmentation_path)
bg = skio.imread(args.background_path)

# Shape and orientation corrections
seg = np.swapaxes(np.swapaxes(np.abs(seg), 0, 1), 1, 2)
bg = np.swapaxes(np.swapaxes(np.abs(bg), 0, 1), 1, 2)
vol = seg + bg
vol = np.where(vol % 2 == 1, 1, vol)  # Binarise overlapping regions
vol = np.pad(vol, 1, mode='constant', constant_values=0)  # Padding to avoid boundary issues

# --- Tissue Class Mapping ---
def segmentation_class_mapping():
    mapping = dict()
    mapping[0] = sp.TISSUE_LIBRARY.muscle(background_oxy=0.7, blood_volume_fraction=0.02)
    mapping[1] = sp.TISSUE_LIBRARY.blood(oxygenation=0.7)
    mapping[2] = sp.TISSUE_LIBRARY.ultrasound_gel()
    mapping[3] = sp.TISSUE_LIBRARY.epidermis()
    mapping[4] = sp.TISSUE_LIBRARY.muscle(background_oxy=0.7, blood_volume_fraction=0.03)
    mapping[6] = sp.TISSUE_LIBRARY.muscle(background_oxy=0.7, blood_volume_fraction=0.04)
    mapping[8] = sp.TISSUE_LIBRARY.muscle(background_oxy=0.7, blood_volume_fraction=0.05)
    mapping[10] = sp.TISSUE_LIBRARY.muscle(background_oxy=0.7, blood_volume_fraction=0.06)
    mapping[12] = sp.TISSUE_LIBRARY.muscle(background_oxy=0.7, blood_volume_fraction=0.07)
    return mapping

# --- Simulation Settings ---
volume_dims = vol.shape
settings = {
    Tags.RANDOM_SEED: SEED,
    Tags.VOLUME_NAME: VOLUME_NAME,
    Tags.SIMULATION_PATH: args.output_dir,
    Tags.SPACING_MM: SPACING,
    Tags.DIM_VOLUME_X: volume_dims[0],
    Tags.DIM_VOLUME_Y: volume_dims[1],
    Tags.DIM_VOLUME_Z: volume_dims[2],
    Tags.WAVELENGTH: WAVELENGTH,
    Tags.SIMULATION_PIPELINE: [Tags.OPTICAL_MODEL],
    Tags.OPTICAL_MODEL: Tags.MCX_DO_NOT_GPU_ACCELERATE,
    Tags.DO_FILE_COMPRESSION: False
}

# --- Build Simulation Domain ---
os.makedirs(args.output_dir, exist_ok=True)
sp.DomainBuilder(settings).create_from_segmentation_volume(
    segmentation_volume=vol,
    segmentation_class_mapping=segmentation_class_mapping(),
    background_label=0
)

# --- Run SIMPA Optical Simulation ---
simulation = sp.Simulation(settings)
simulation.run()

# --- Save Initial Pressure Output ---
initial_pressure = simulation.data_field[Tags.DATA_FIELD_INITIAL_PRESSURE]
output_file = os.path.join(args.output_dir, f"{VOLUME_NAME}_p0.mat")
savemat(output_file, {"initial_pressure": initial_pressure})
print(f"Saved initial pressure to: {output_file}")
