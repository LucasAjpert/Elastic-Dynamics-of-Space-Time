"""
DEET (Elastic Dynamics of Space-Time) - Linear Fabric Miner (Adaptive Deep Search)
Author: Lucas Vinicius Ajpert Cosmo
Description: Busca profunda e contínua pelas constantes absolutas Kcosmo e X_void.
O algoritmo afunila a busca automaticamente em torno dos recordes para achar o erro mínimo exato.
"""

import os
import urllib.request
import numpy as np
import random

def ensure_nasa_catalog():
    filename = "catalogo_nasa_175_galaxias.txt"
    url = "https://astroweb.cwru.edu/SPARC/MassModels_Lelli2016c.mrt"
    if not os.path.exists(filename):
        print(f"📥 Baixando banco de dados oficial NASA/SPARC...")
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

def run_deep_miner():
    systems_data = load_systems()
    valid_systems = []
    
    for name, points in systems_data.items():
        if len(points) < 5: 
            continue
            
        arr = np.array(points)
        v_obs_max = np.max(arr[:, 1])
        v_dsk_max = np.max(arr[:, 3])
        v_bul_max = np.max(arr[:, 4])

        # Travas Biológicas e Estruturais do Modelo DEET
        if v_bul_max > (0.6 * v_dsk_max) and v_obs_max > 190:
            y_bounds = np.linspace(0.5, 1.0, 15)
        elif v_obs_max >= 180:
            y_bounds = np.linspace(0.5, 1.0, 15)
        elif v_obs_max >= 95:
            y_bounds = np.linspace(0.3, 0.8, 15)
        else:
            y_bounds = np.linspace(0.2, 0.5, 15)
            
        valid_systems.append({
            'name': name,
            'arr': arr,
            'y_bounds': y_bounds
        })

    print("="*75)
    print(" 🚀 DEET MINER IMBATÍVEL - MODO DE BUSCA PROFUNDA ADAPTATIVA (X2 = 1.0)")
    print(" (O código vai rodar para sempre afinando os valores. Pressione Ctrl+C para parar)")
    print("="*75)
    
    best_global_error = float('inf')
    best_constants = (0, 0)
    X2_FIXED = 1.0
    
    # Janela de busca inicial ampla
    K_min, K_max = 1.20e-10, 1.50e-10
    Xv_min, Xv_max = 6.00e-12, 9.00e-12
    
    iteration = 0
    try:
        while True:
            iteration += 1
            
            # Sorteia valores dentro da janela dinâmica
            test_Kcosmo = random.uniform(K_min, K_max)
            test_X_void = random.uniform(Xv_min, Xv_max)
            
            systemic_errors = []
            
            for sys in valid_systems:
                best_sys_err = float('inf')
                
                for y_est in sys['y_bounds']:
                    for f_gas in [0.75, 1.0, 1.25]:
                        err_pts = []
                        for p in sys['arr']:
                            r_m = p[0] * 3.086e19
                            g_gas = (-1 if p[2] < 0 else 1) * ((p[2] * 1000.0)**2) / r_m
                            g_dsk = ((p[3] * 1000.0)**2) / r_m
                            g_bul = ((p[4] * 1000.0)**2) / r_m
                            
                            g_bar = max((f_gas * g_gas) + (y_est * g_dsk) + (1.25 * y_est * g_bul), 1e-15)
                            
                            # Nova Equação Exata com Kcosmo
                            g_sink = g_bar * np.sqrt(1.0 + (test_Kcosmo / g_bar))
                            g_stretch = test_X_void * (test_Kcosmo / (g_bar + test_Kcosmo))
                            
                            v_calc = np.sqrt(max(g_sink - g_stretch, 0.0) * r_m) / 1000.0
                            err_pts.append(abs(v_calc - p[1]))
                        
                        if np.mean(err_pts) < best_sys_err:
                            best_sys_err = np.mean(err_pts)
                
                systemic_errors.append(best_sys_err)
                
            current_global_error = np.mean(systemic_errors)
            
            # Se encontrar um novo recorde, registra e AFUNILA a janela de busca
            if current_global_error < best_global_error:
                best_global_error = current_global_error
                best_constants = (test_Kcosmo, test_X_void)
                
                print(f"🎉 NOVO RECORDE NA ITERAÇÃO {iteration:,}! Erro: {best_global_error:.4f} km/s")
                print(f"   Kcosmo: {test_Kcosmo:.4e} | X2: STRICTLY {X2_FIXED:.1f} | X_void: {test_X_void:.4e}\n")
                
                # Afunilamento: a nova busca será 5% para cima e para baixo do novo recorde
                # Isso cria um efeito "zoom" focado na calibração microscópica absoluta
                K_margin = best_constants[0] * 0.05
                Xv_margin = best_constants[1] * 0.05
                
                K_min = best_constants[0] - K_margin
                K_max = best_constants[0] + K_margin
                Xv_min = best_constants[1] - Xv_margin
                Xv_max = best_constants[1] + Xv_margin

    except KeyboardInterrupt:
        print("\n" + "="*75)
        print(" 🏁 MINERAÇÃO INTERROMPIDA PELO USUÁRIO! VALORES IMBATÍVEIS ENCONTRADOS:")
        print("="*75)
        print(f" Erro Médio Global Mínimo:{best_global_error:.4f} km/s")
        print(f" Rigidez (Kcosmo):        {best_constants[0]:.5e} m/s²")
        print(f" Expoente (X2):           STRICTLY 1.0 (Exact Law)")
        print(f" Tensão de Vazio (X_void):{best_constants[1]:.5e} m/s²")
        print("="*75)

if __name__ == "__main__":
    run_deep_miner()