import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Connexion à la base de données (créera un fichier SQLite s'il n'existe pas)
conn = sqlite3.connect('todolist.db')
cursor = conn.cursor()

# Création des tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tache (
        Libelle TEXT,
        Date_Creation DATE,
        Date_Realisation DATE,
        Date_Fixee DATE,
        Code_Etat TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Etat (
        Code_Etat TEXT PRIMARY KEY,
        Nom TEXT
    )
''')

# Insertion des états possibles
cursor.executemany('INSERT OR IGNORE INTO Etat VALUES (?, ?)', [('AFAIRE', 'À faire'), ('ENCOURS', 'En cours'), ('TERMINEE', 'Terminée')])

# Fonction pour afficher la liste de tâches à faire et en cours
def afficher_taches():
    cursor.execute('SELECT * FROM Tache WHERE Code_Etat IN ("AFAIRE", "ENCOURS")')
    taches = cursor.fetchall()
    for tache in taches:
        liste_taches.insert(tk.END, f"{tache[0]} - {tache[4]}\n")

# Fonction pour ajouter une nouvelle tâche
def ajouter_tache():
    libelle = entry_libelle.get()
    date_creation = datetime.now().strftime('%Y-%m-%d')
    date_fixee = entry_date_fixee.get()
    code_etat = 'AFAIRE'
    
    if libelle and date_fixee:
        cursor.execute('INSERT INTO Tache VALUES (?, ?, NULL, ?, ?)', (libelle, date_creation, date_fixee, code_etat))
        conn.commit()
        rafraichir_liste_taches()
        entry_libelle.delete(0, tk.END)
        entry_date_fixee.delete(0, tk.END)
    else:
        messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs.")

# Fonction pour rafraîchir la liste des tâches
def rafraichir_liste_taches():
    liste_taches.delete(1.0, tk.END)
    afficher_taches()

# ...

# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Gestion de Tâches")

# Création des widgets Tkinter
label_libelle = tk.Label(fenetre, text="Libellé de la tâche:")
entry_libelle = tk.Entry(fenetre)

label_date_fixee = tk.Label(fenetre, text="Date fixée (YYYY-MM-DD):")
entry_date_fixee = tk.Entry(fenetre)

liste_taches = tk.Text(fenetre, height=10, width=50)

# Bouton pour ajouter une tâche
bouton_ajouter = tk.Button(fenetre, text="Ajouter Tâche", command=ajouter_tache)

# Placement des widgets
label_libelle.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
entry_libelle.grid(row=0, column=1, padx=10, pady=10)

label_date_fixee.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
entry_date_fixee.grid(row=1, column=1, padx=10, pady=10)

liste_taches.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

bouton_ajouter.grid(row=3, column=0, columnspan=2, pady=10)

# Rafraîchir la liste des tâches au démarrage
rafraichir_liste_taches()

# Lancer la boucle Tkinter
fenetre.mainloop()

# Fermeture de la connexion
conn.close()
