# 🍽️ Système de Contrôle d'Accès au Restaurant Scolaire - RecoFacial

## 📋 Description du Projet

Application Python de contrôle d'accès au restaurant scolaire basée sur la **reconnaissance faciale**. Le système permet de :
- Enregistrer de nouveaux étudiants avec leur photo
- Reconnaître automatiquement les étudiants devant la caméra
- Gérer les comptes et soldes des étudiants
- Débiter automatiquement ou manuellement le prix du repas

**Projet réalisé dans le cadre du cours Python BSI-DSN - Institut Limayrac**

---

## 🎯 Fonctionnalités

### ✅ Fonctionnalités Principales
- **Mode "Ajout de nouveaux étudiants"** : Capture de 30 photos par étudiant pour l'entraînement du modèle
- **Mode "Contrôle d'accès"** : Reconnaissance faciale en temps réel avec débit automatique ou manuel
- **Gestion des comptes** : Création, modification, suppression et consultation des comptes étudiants
- **Gestion des soldes** : Débit automatique (1x par jour) ou manuel, ajout de crédit
- **Interface graphique** : IHM intuitive avec Tkinter

### 🔧 Fonctionnalités Optionnelles
- Mode automatique/manuel pour le débit
- Limitation d'un débit par jour par étudiant
- Historique complet des transactions
- Réinitialisation des limites quotidiennes (pour tests)

---

## 📦 Prérequis

- **Python** : Version 3.8 ou supérieure
- **Caméra** : Webcam intégrée ou externe (ou smartphone en alternative)
- **Système d'exploitation** : Windows, Linux ou macOS

---

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
git clone https://github.com/GeorgeKhita/RecoFaciale.git
cd RecoFaciale
```

### 2. Installer les dépendances Python

Le projet nécessite les bibliothèques suivantes. Vous pouvez les installer de deux façons :

**Option 1 : Utiliser le fichier requirements.txt (recommandé)**
```bash
pip install -r requirements.txt
```

**Option 2 : Installer manuellement**
```bash
pip install opencv-contrib-python numpy pillow
```

**Détail des dépendances :**

| Bibliothèque | Version recommandée | Usage |
|-------------|---------------------|-------|
| **opencv-contrib-python** | 4.8.1+ | Capture vidéo, détection et reconnaissance faciale (Haar Cascade + LBPH) |
| **numpy** | 1.26+ | Manipulation de matrices pour le traitement d'images |
| **pillow** (PIL) | 10.1+ | Conversion d'images pour l'affichage dans Tkinter |
| **tkinter** | Built-in | Interface graphique (inclus avec Python) |

**Note** : `opencv-contrib-python` est nécessaire (et non `opencv-python`) car il inclut les modules de reconnaissance faciale (`cv2.face`).

**Note importante** : Sur certaines distributions Linux, `tkinter` n'est pas inclus par défaut. Si vous obtenez une erreur `ModuleNotFoundError: No module named 'tkinter'`, installez-le :
- **Ubuntu/Debian** : `sudo apt-get install python3-tk`
- **Fedora** : `sudo dnf install python3-tkinter`
- **macOS** : Généralement inclus avec Python

### 3. Vérifier l'installation

```bash
python -c "import cv2; import numpy; import PIL; import tkinter; print('✅ Toutes les dépendances sont installées')"
```

---

## 🎮 Utilisation

### Premier lancement

Lors du premier lancement, l'application va :
1. Créer automatiquement le dossier `face_samples/` (s'il n'existe pas)
2. Démarrer la caméra (assurez-vous qu'elle est disponible)
3. Afficher "⚠️ Aucun utilisateur enregistré" dans le panneau vidéo (normal au premier lancement)

**Les fichiers de données** (`accounts.json`, `names.pkl`, `face_recognizer.yml`) seront créés automatiquement lors du **premier ajout d'un utilisateur**.

**Aucune configuration supplémentaire n'est nécessaire !** L'application est prête à être utilisée dès l'installation.

### Lancer l'application

```bash
python canteen_system.py
```

**Note** : Si vous utilisez Python 3 explicitement, utilisez `python3` au lieu de `python`.

### Interface Utilisateur

L'interface se compose de deux panneaux :

#### **Panneau de gauche** : Flux vidéo
- Affichage en temps réel de la caméra
- Détection et reconnaissance des visages
- Messages d'information (reconnaissance, débit, erreurs)

#### **Panneau de droite** : Contrôles
- **Prix du repas** : Montant configurable (par défaut 3.50€)
- **Mode AUTO/MANUEL** : Bascule entre débit automatique et manuel
- **Bouton "DÉBITER MAINTENANT"** : Débit manuel (actif en mode MANUEL uniquement)
- **Nouvel Utilisateur** : Ajouter un étudiant au système
- **Ajouter Crédit** : Recharger le compte d'un étudiant
- **Voir Comptes** : Consulter tous les comptes et soldes
- **Supprimer un utilisateur** : Retirer un étudiant du système
- **Réinitialiser limites** : Réinitialiser les dates de débit (pour tests)

### Scénarios d'utilisation

#### 1. Ajouter un nouvel étudiant
1. Cliquer sur "➕ Nouvel Utilisateur"
2. Saisir le nom de l'étudiant
3. Saisir le solde initial (ex: 50.00€)
4. Se placer face à la caméra et bouger légèrement
5. Attendre la capture automatique de 30 photos
6. L'étudiant est ajouté et le modèle est réentraîné

#### 2. Reconnaissance et débit automatique
1. Activer le mode AUTO (bouton bleu)
2. L'étudiant se place face à la caméra
3. Le système reconnaît l'étudiant
4. Le débit est effectué automatiquement (1x par jour maximum)
5. Le solde est mis à jour

#### 3. Reconnaissance et débit manuel
1. Activer le mode MANUEL (bouton orange)
2. L'étudiant se place face à la caméra
3. Le système reconnaît l'étudiant
4. Cliquer sur "💳 DÉBITER MAINTENANT" pour débiter

#### 4. Ajouter du crédit
1. Cliquer sur "💰 Ajouter Crédit"
2. Sélectionner l'étudiant dans la liste
3. Saisir le montant à ajouter
4. Valider

---

## 📁 Structure du Projet

```
RecoFacial/
├── canteen_system.py          # Code source principal
├── accounts.json              # Base de données des comptes (généré automatiquement)
├── names.pkl                  # Liste des noms des étudiants (généré automatiquement)
├── face_recognizer.yml        # Modèle de reconnaissance entraîné (généré automatiquement)
├── face_samples/              # Dossier contenant les photos des étudiants
│   ├── Etudiant1/
│   │   ├── sample_0.jpg
│   │   ├── sample_1.jpg
│   │   └── ... (30 photos)
│   └── Etudiant2/
│       └── ...
├── Doc/                       # Documentation
│   └── SCENARIOS_TESTS.md            # Scénarios de tests
└── README.md                  # Ce fichier
```

### Fichiers générés automatiquement

L'application crée automatiquement les fichiers suivants lors de la première utilisation :

- **`accounts.json`** : Stocke les comptes, soldes et transactions (créé au premier ajout d'utilisateur)
- **`names.pkl`** : Liste sérialisée des noms des étudiants (créé au premier ajout d'utilisateur)
- **`face_recognizer.yml`** : Modèle LBPH entraîné pour la reconnaissance (créé au premier ajout d'utilisateur)
- **`face_samples/`** : Dossier créé automatiquement, contient les sous-dossiers avec les 30 photos par étudiant

**Important** : Ces fichiers ne sont pas dans le dépôt GitHub (voir `.gitignore`). Ils seront créés automatiquement lors du premier lancement de l'application.

---

## 🔧 Technologies Utilisées

### Reconnaissance Faciale
- **Haar Cascade** : Détection des visages dans l'image
- **LBPH (Local Binary Patterns Histograms)** : Algorithme de reconnaissance faciale
- **OpenCV** : Bibliothèque de traitement d'images et de vision par ordinateur

### Interface Graphique
- **Tkinter** : Bibliothèque graphique native Python

### Stockage des Données
- **JSON** : Stockage des comptes et transactions
- **Pickle** : Sérialisation des listes Python
- **YAML** : Format du modèle de reconnaissance (via OpenCV)

---

## ⚙️ Configuration

### Paramètres modifiables dans le code

- **Seuil de confiance** : Ligne 207 dans `canteen_system.py`
  ```python
  if confidence < 70:  # Modifier cette valeur (plus bas = plus permissif)
  ```

- **Nombre de photos par étudiant** : Ligne 294 dans `canteen_system.py`
  ```python
  text = f"{len(self.capture_samples)}/30"  # Modifier 30 si nécessaire
  ```

- **Prix du repas par défaut** : Ligne 92 dans `canteen_system.py`
  ```python
  self.price_entry.insert(0, "3.50")  # Modifier le prix par défaut
  ```

---

## 🐛 Dépannage

### La caméra ne fonctionne pas
- Vérifier que la caméra n'est pas utilisée par une autre application
- Essayer de changer l'index de la caméra (ligne 160) : `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`
- Utiliser un fichier image en alternative (modifier le code pour lire une image au lieu de la caméra)

### Erreur "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-contrib-python
```

### Erreur "ModuleNotFoundError: No module named 'tkinter'"
- **Windows** : Réinstaller Python avec l'option "tcl/tk" cochée
- **Linux** : Installer `python3-tk` (voir section Installation)
- **macOS** : Généralement inclus, vérifier la version de Python

### Erreur "AttributeError: module 'cv2' has no attribute 'face'"
Vous avez installé `opencv-python` au lieu de `opencv-contrib-python`. Désinstallez et réinstallez :
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-contrib-python
```

### La reconnaissance ne fonctionne pas bien
- S'assurer d'avoir capturé 30 photos de bonne qualité
- Vérifier l'éclairage (doit être suffisant et uniforme)
- Ajuster le seuil de confiance si nécessaire
- Réentraîner le modèle après suppression d'utilisateurs

### Erreur lors de l'ajout d'un utilisateur
- Vérifier que le nom n'existe pas déjà
- S'assurer qu'il y a assez d'espace disque pour les photos
- Vérifier les permissions d'écriture dans le dossier `face_samples/`

---

## 📚 Documentation Complémentaire

Consultez les fichiers dans le dossier `Doc/` pour plus de détails :

- **`SCENARIOS_TESTS.md`** : Scénarios de tests pour valider le fonctionnement du système

---

## 👤 Auteur

**Projet réalisé par** : [Votre Nom]  
**Établissement** : Institut Limayrac - BSI-DSN  
**Année** : 2025-2026  
**Cours** : Python Commun

---

## 📝 Licence

Ce projet est réalisé dans le cadre d'un projet scolaire.

---

## 🔗 Liens

- **Dépôt distant** : https://github.com/GeorgeKhita/RecoFaciale.git
- **Vidéo de démonstration** : [URL_DRIVE_GOOGLE]

---

## 📌 Notes Importantes

- Les données sont stockées localement dans des fichiers JSON/Pickle
- Le modèle de reconnaissance est entraîné localement
- Aucune donnée n'est envoyée sur Internet
- Pour un usage en production, considérer l'ajout d'une authentification administrateur

---

**Dernière mise à jour** : Décembre 2025

