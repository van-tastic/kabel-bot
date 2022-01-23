import numpy as np
from pathlib import Path

main_data = np.genfromtxt(Path("Data/TverrsnittCu.csv"), delimiter=';')
vern = np.array([6, 10, 15, 16, 20, 25, 32, 40, 50, 56, 63, 80, 100])
# Bryterkarakteristikk --> "Type": Koeffisient
karakter_i2 = {"A": 1.45, "B": 1.45, "C": 1.45, "D": 1.45, "K": 1.2, "Z": 1.2, "eff": {"hi": 1.25,"lo": 1.35}}
# Korreksjonsfaktorer dersom lagt i burde hentes og behandles eksternt
luft = np.array([1.22, 1.17, 1.12, 1.06, 1.00, 0.94, 0.87, 0.79, 0.71, 0.61, 0.60])
jord = np.array([1.10, 1.05, 1.00, 0.95, 0.89, 0.84, 0.77, 0.71, 0.63, 0.55, 0.45])
kfaktor_nf = np.array([[100, 80, 70, 65, 60, 57, 50],
                    [100, 85, 79, 75, 73, 72, 70],
                    [95, 81, 72, 68, 66, 64, 61]], dtype=float)

rim =  {"A1": main_data[:,1:3], 
        "A2": main_data[:,3:5],
        "B1": main_data[:,5:7],
        "B2": main_data[:,7:9],
        "C" : main_data[:,9:11],
        "D2": main_data[:,11:13],
        "E" : main_data[:,13:15],
        "F" : main_data[:,15:17],
        "F3": main_data[:,17:18],
        "G" : main_data[:,18:20]}
Areal = main_data[:,0]    # Kabeltverrsnitt
