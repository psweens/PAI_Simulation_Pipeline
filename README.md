# Photoacoustic Simulation Pipeline Using SIMPA, MCX, and k-Wave

This repository provides a simulation pipeline for generating synthetic photoacoustic imaging data using:
- [SIMPA](https://github.com/IMSY-DKFZ/simpa) for modeling **light transport and optical absorption**,
- [MCX](http://mcx.space/) as the **Monte Carlo simulation engine** for photon propagation,
- [k-Wave](http://www.k-wave.org/) for **acoustic propagation and image reconstruction**.

It operates on synthetic 3D segmentation masks of vasculature and produces reconstructed photoacoustic volumes.

---

## 🧠 Workflow Summary

1. 🧬 **Optical Simulation (`OpticalSimulations.py`)**
   - Uses SIMPA + MCX to simulate optical fluence and compute the initial pressure distribution.

2. 🔊 **Acoustic Reconstruction (`Reconstruction.m`)**
   - Uses k-Wave (in MATLAB) to simulate acoustic wave propagation and reconstruct photoacoustic images.

---

## 🌿 Synthetic Vasculature Input

The vascular segmentation masks used as input for simulation are generated using the  
[V-System](https://github.com/psweens/V-System) — a synthetic vessel generation framework.

This simulation pipeline was originally developed to support the **[VAN-GAN](https://github.com/psweens/VAN-GAN)** project, a deep learning framework for reconstructing vascular structures from photoacoustic data.

📄 **Citation**:  
If using this code, please cite the VAN-GAN research paper [here](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202402195). The codebase for VAN-GAN can be found [here](https://github.com/psweens/VAN-GAN)).

---

## 🧱 Requirements

### Python Environment

- Python 3.8+
- SIMPA Toolbox:
  ```bash
  pip install simpa
  ```
- Additional dependencies:
  ```bash
  pip install numpy scipy matplotlib h5py
  ```

### MCX (Monte Carlo eXtreme)

- Required by SIMPA for optical photon propagation.
- Install from: [http://mcx.space/](http://mcx.space/)
- Ensure it's accessible in your system PATH.

To test:
```bash
mcx --version
```

### MATLAB Environment

- MATLAB R2020a or later
- [k-Wave Toolbox](http://www.k-wave.org/)
  - Must be added to MATLAB path
  - GPU support is optional but recommended

---

## 📁 Repository Contents

| File                     | Description                                           |
|--------------------------|-------------------------------------------------------|
| `OpticalSimulations.py`  | Runs SIMPA + MCX to generate initial pressure maps    |
| `Reconstruction.m`       | Uses k-Wave in MATLAB to reconstruct the acoustic image |
| `*.mat` / `*.npy`        | Input and output data files                           |

---

## ▶️ How to Run

### Step 1: Optical Simulation (Python + SIMPA + MCX)

```bash
python OpticalSimulations.py
```

Ensure:
- A 3D vascular segmentation mask (`.npy` or `.mat`) is available.
- MCX is installed and accessible in the system path.
- SIMPA is set to use MCX as the photon transport backend.

### Step 2: Acoustic Reconstruction (MATLAB + k-Wave)

In MATLAB:

```matlab
Reconstruction
```

Make sure:
- The input `.mat` path matches the output from Python.
- k-Wave is correctly installed and functional.

---

## 📷 Output

- Output includes `.mat` files of reconstructed images.
- These can be visualized using MATLAB or Python tools.

---

## 🧪 Example Use Case

This pipeline is ideal for:
- Validating photoacoustic reconstruction methods
- Generating paired data for training deep learning models (e.g. VAN-GAN)
- Exploring the influence of vascular morphology on image contrast

---

## 🔗 References & Tools Used

- [SIMPA Toolbox](https://github.com/IMSY-DKFZ/simpa)
- [MCX: Monte Carlo eXtreme](http://mcx.space/)
- [k-Wave Toolbox](http://www.k-wave.org/)
- [V-System – Synthetic Vasculature](https://github.com/psweens/V-System)
- [VAN-GAN – Vascular Reconstruction with GANs](https://github.com/psweens/VAN-GAN)

---

## 🧑‍🎓 Attribution

This pipeline was developed for research and academic purposes using open-source tools.
Credit goes to the developers of SIMPA, MCX, k-Wave, and the V-System framework.

---

## 📬 Contact

For questions, please open an issue.
