"""
DEET (Elastic Dynamics of Space-Time) - Detailed Output Generator
Author: Lucas Vinicius Ajpert Cosmo
Description: Applies the Exact Linear Mesh on 175 galaxies and generates a CSV 
with detailed radius-by-radius output.
"""

import os
import urllib.request
import numpy as np
import csv

# ==========================================
# UNIVERSAL CONSTANTS OF THE DARK FABRIC
# ==========================================
Kcosmo = 1.5605e-10       # Local Deformation Rigidity (m/s^2)
L = 1.0                   # STRICTLY LINEAR ELASTICITY (L)
Tcosmo = 4.7642e-12       # Cosmological Stretching Tension (m/s^2)

def ensure_nasa_catalog():
    filename = "catalogo_nasa_175_galaxias.txt"
    url = "https://astroweb.cwru.edu/SPARC/MassModels_Lelli2016c.mrt"
    if not os.path.exists(filename):
        print(f"📥 Downloading official NASA/SPARC database...")
        urllib.request.urlretrieve(url, filename)
    return filename

def load_systems():
    filename = ensure_nasa_catalog()
    systems = {}
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 8:
                try:
                    name = parts[0]
                    r_kpc, v_obs = float(parts[2]), float(parts[3])
                    v_gas, v_dsk, v_bul = float(parts[5]), float(parts[6]), float(parts[7])
                    if r_kpc > 0 and v_obs > 0:
                        systems.setdefault(name, []).append([r_kpc, v_obs, v_gas, v_dsk, v_bul])
                except ValueError:
                    continue
    return systems

def run_detailed_pipeline():
    systems_data = load_systems()
    csv_filename = "Detailed_Table_SPARC_DEET.csv"
    
    print("="*75)
    print(" 🚀 STARTING DEET DETAILED TABLE GENERATION...")
    print("="*75)

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # English Headers for the CSV
        writer.writerow([
            'Galactic System', 'Structural Classification', 'Radius (kpc)', 
            'V_obs (km/s)', 'V_calc DEET (km/s)', 'Error per Radius (km/s)', 
            'Mean Galaxy Error (km/s)', 'Mass-to-Light Ratio (Y*)', 'Gas Fluctuation (f_gas)'
        ])
                         
        global_errors = []
        
        for name, points in systems_data.items():
            arr = np.array(points)
            v_obs_max = np.max(arr[:, 1])
            v_dsk_max = np.max(arr[:, 3])
            v_bul_max = np.max(arr[:, 4])
            
            # Structural and Biological Classification
            if v_bul_max > (0.6 * v_dsk_max) and v_obs_max > 190:
                group = "Ultra-Deep Well System"
                y_bounds = np.linspace(0.5, 1.0, 30)
            elif v_obs_max >= 180:
                group = "Deep Well System"
                y_bounds = np.linspace(0.5, 1.0, 30)
            elif v_obs_max >= 95:
                group = "Intermediate Deformation System"
                y_bounds = np.linspace(0.3, 0.8, 30)
            else:
                group = "Shallow Basin System"
                y_bounds = np.linspace(0.2, 0.5, 30)
            
            best_err_sys = float("inf")
            best_y = 0
            best_f_gas = 0
            best_radii_data = [] 
            
            for y_est in y_bounds:
                for f_gas in [0.75, 1.0, 1.25]:
                    err_points = []
                    current_radii_data = []
                    
                    for p in arr:
                        r_kpc, v_obs = p[0], p[1]
                        r_m = r_kpc * 3.086e19
                        
                        g_gas = (-1 if p[2] < 0 else 1) * ((p[2] * 1000.0)**2) / r_m
                        g_dsk = ((p[3] * 1000.0)**2) / r_m
                        g_bul = ((p[4] * 1000.0)**2) / r_m
                        
                        g_bar = max((f_gas * g_gas) + (y_est * g_dsk) + (1.25 * y_est * g_bul), 1e-15)
                        
                        # Exact DEET Equation
                        g_sink = g_bar * np.sqrt(1.0 + (Kcosmo / g_bar))
                        g_stretch = Tcosmo * (Kcosmo / (g_bar + Kcosmo))
                        
                        v_calc = np.sqrt(max(g_sink - g_stretch, 0.0) * r_m) / 1000.0
                        err = abs(v_calc - v_obs)
                        
                        err_points.append(err)
                        current_radii_data.append([r_kpc, v_obs, v_calc, err])
                        
                    mean_err = np.mean(err_points)
                    
                    if mean_err < best_err_sys:
                        best_err_sys = mean_err
                        best_y = y_est
                        best_f_gas = f_gas
                        best_radii_data = current_radii_data
            
            global_errors.append(best_err_sys)
            
            for data in best_radii_data:
                r_kpc, v_obs, v_calc, err = data
                writer.writerow([
                    name, group, f"{r_kpc:.3f}", f"{v_obs:.2f}", 
                    f"{v_calc:.2f}", f"{err:.4f}", f"{best_err_sys:.4f}", 
                    f"{best_y:.3f}", f"{best_f_gas:.2f}"
                ])
                
    print(f"✅ DONE! Detailed table saved as: '{csv_filename}'")
    print(f"📊 Official Global Mean Error: {np.mean(global_errors):.4f} km/s")
    print("="*75)

if __name__ == "__main__":
    run_detailed_pipeline()