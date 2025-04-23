import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Fenêtre de sélection du fichier Excel
def choisir_fichier_excel():
    root = Tk()
    root.withdraw()
    fichier = askopenfilename(title="Sélectionner un fichier Excel", filetypes=[("Fichiers Excel", "*.xlsx")])
    return fichier

# Chargement des données
chemin_fichier = choisir_fichier_excel()
df = pd.read_excel(chemin_fichier)

# Variables explicatives : F1 à F8 + NIR
X_data = df[["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "NIR"]].values
X = np.hstack([np.ones((X_data.shape[0], 1)), X_data])  # Ajout de l'intercept

# Cibles
y_r = df["PPFD-R"].values
y_b = df["PPFD-B"].values
y_g = df["PPFD-G"].values
y_fr = df["PPFD-FR"].values if "PPFD-FR" in df.columns else None

# Entraînement
model_r = LinearRegression(fit_intercept=False).fit(X, y_r)
model_b = LinearRegression(fit_intercept=False).fit(X, y_b)
model_g = LinearRegression(fit_intercept=False).fit(X, y_g)
model_fr = LinearRegression(fit_intercept=False).fit(X, y_fr) if y_fr is not None else None

# Affichage JS
def print_coeffs(name, coef):
    print(f"\nconst coeffs{name} = [")
    print(",\n".join([f"  {v:.4f}" for v in coef]) + "]; // Intercept + F1 à F8 + NIR")

print_coeffs("R", model_r.coef_)
print_coeffs("B", model_b.coef_)
print_coeffs("G", model_g.coef_)
if model_fr:
    print_coeffs("FR", model_fr.coef_)


