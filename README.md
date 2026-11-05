EDST (Elastic Dynamics of Space-Time) - Cosmological Validation
This repository contains the computational Python pipeline used to empirically validate the Elastic Dynamics of Space-Time (EDST) theory—originally formulated as the Teoria do Tecido Escuro (Dark Fabric Theory).
The scripts in this repository apply the mechanical and structural principles of EDST to the official NASA/SPARC catalog (comprising 175 galactic systems) to demonstrate that galactic rotation curves can be analytically modeled through the strict elastic resistance of the space-time continuum, without the need for hypothetical dark matter particles.

Repository Contents

This repository features two main Python scripts designed for different stages of the validation process:
1. LinearFabricMiner_Imbativel.py
This script executes an adaptive Monte Carlo deep search to isolate and stabilize the absolute geometric constants of the spacetime mesh:

K_cosmo: Local Deformation Rigidity (Substitutes the Dark Matter effect).
T_cosmo: Cosmological Stretching Tension (Substitutes the Dark Energy effect).

The algorithm enforces a regime of strict linear elasticity ($L=1.0$) and implements rigorous biological and thermodynamic constraints regarding Stellar Mass-to-Light ratios ($\Upsilon_*$), strictly anchored in the standard stellar population synthesis (SPS) models defined by Lelli, McGaugh, and Schombert. It automatically funnels the search window around the lowest global mean errors to find the exact absolute minimum.

2. Table_Generator_Deet.py
This script applies the exact, calibrated EDST equations to the NASA/SPARC catalog. It processes all 175 galaxies and outputs a comprehensive CSV file (Detailed_Table_SPARC_DEET.csv).
The generated table provides a detailed, radius-by-radius breakdown comparing the real observed rotational velocity (V_obs) against the theoretical velocity calculated by the EDST elastic mesh (V_calc). It also records the specific dynamic gas fluctuations and Mass-to-Light ratios optimally selected by the algorithm within the physically allowed bounds.

Requirements
To run these scripts, you need:

Python 3.x installed on your system.
NumPy library.
An active internet connection (the scripts are programmed to automatically fetch the official SPARC .mrt database directly from the servers upon first run).
You can install the required dependency via pip:

pip install numpy

Usage
You can run the scripts directly from your terminal or command prompt.
To start the adaptive deep search for the universal elastic constants:

python LinearFabricMiner_Imbativel.py

(Note: This is a continuous search algorithm. You can stop it at any time by pressing Ctrl+C)To generate the full detailed CSV table with the radius-by-radius EDST calculations:python Table_Generator_Deet.py