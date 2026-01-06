# 📘 Guide de Compilation - Présentation LaTeX

Ce document explique comment compiler la présentation `main.tex` pour générer le fichier PDF.

---

## 📋 Table des matières

1. [Méthode Rapide (Script)](#méthode-1--script-automatique-recommandé)
2. [Méthode Manuelle (Terminal)](#méthode-2--terminal-manuel)
3. [Méthode PyCharm](#méthode-3--pycharm-avec-texify)
4. [Méthode Éditeur LaTeX](#méthode-4--éditeur-latex-dédié)
5. [Méthode en Ligne](#méthode-5--overleaf-en-ligne)
6. [Prérequis](#-prérequis)
7. [Résolution de problèmes](#-résolution-de-problèmes)

---

## ✅ Méthode 1 : Script Automatique (Recommandé)

### La plus simple et la plus rapide

**Windows (PowerShell)** :
```powershell
cd presentation
.\compile.ps1
```

**Windows (Invite de commandes)** :
```cmd
cd presentation
compile.bat
```

Le script fait automatiquement :
- ✅ Suppression de l'ancien PDF
- ✅ Première compilation
- ✅ Deuxième compilation (pour les références)
- ✅ Nettoyage des fichiers temporaires
- ✅ Ouverture automatique du PDF

**Résultat** : `main.pdf` (38 diapositives, ~1 MB)

---

## ✅ Méthode 2 : Terminal Manuel

### Compilation pas à pas

1. **Ouvrir le terminal** (PowerShell, Invite de commandes, ou Terminal dans PyCharm)

2. **Se placer dans le dossier** :
   ```bash
   cd "D:\MASTER 2 GI\MODEL DE CALCUL NUMERIQUE\PROJET ANALYSE NUMERIQUE\projet_final\presentation"
   ```

3. **Compiler** (deux fois pour les références) :
   ```bash
   pdflatex main.tex
   pdflatex main.tex
   ```

4. **Ouvrir le PDF** :
   ```bash
   # Windows PowerShell
   start main.pdf
   
   # Windows CMD
   main.pdf
   
   # Linux/Mac
   open main.pdf
   ```

### Version courte (une seule ligne)
```bash
cd presentation && pdflatex main.tex && pdflatex main.tex && start main.pdf
```

---

## ✅ Méthode 3 : PyCharm avec TeXiFy

### Installation du plugin

1. **Dans PyCharm** : `File` → `Settings` (ou `Ctrl+Alt+S`)
2. Aller dans **`Plugins`**
3. Rechercher **"TeXiFy IDEA"**
4. Cliquer sur **Install**
5. **Redémarrer PyCharm**

### Configuration

1. `File` → `Settings` → `Languages & Frameworks` → `TeXiFy`
2. Vérifier que le chemin vers `pdflatex.exe` est détecté
   - Exemple : `C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe`

### Compilation

**Trois méthodes au choix** :

1. **Clic droit** sur `main.tex` → **"Compile LaTeX file"**
2. **Raccourci clavier** : `Shift + F10`
3. **Bouton vert** ▶️ en haut à droite

Le PDF s'ouvre automatiquement dans le visualiseur intégré.

---

## ✅ Méthode 4 : Éditeur LaTeX Dédié

### TeXstudio (Recommandé pour débutants)

#### Installation

1. **Télécharger** : [https://www.texstudio.org/](https://www.texstudio.org/)
2. **Installer** (après avoir installé MiKTeX)

#### Utilisation

1. Ouvrir **TeXstudio**
2. `File` → `Open` → Sélectionner `main.tex`
3. **Compiler** :
   - Appuyer sur **F5**
   - Ou cliquer sur le bouton ▶️ vert "Build & View"
4. Le PDF s'affiche automatiquement à droite

**Avantages** :
- ✅ Interface visuelle intuitive
- ✅ Aperçu PDF en temps réel
- ✅ Détection automatique des erreurs
- ✅ Autocomplétion des commandes LaTeX
- ✅ Vérification orthographique

### Autres éditeurs LaTeX

- **TeXmaker** : [https://www.xm1math.net/texmaker/](https://www.xm1math.net/texmaker/)
- **LyX** : [https://www.lyx.org/](https://www.lyx.org/) (WYSIWYG)
- **Visual Studio Code** avec extension **LaTeX Workshop**

---

## ✅ Méthode 5 : Overleaf (En ligne)

### Sans installation locale

1. Aller sur **[https://www.overleaf.com/](https://www.overleaf.com/)**
2. **Créer un compte gratuit**
3. **Importer le projet** :
   - Clic sur **"New Project"** → **"Upload Project"**
   - Zipper le dossier `presentation/` (avec le dossier `figures/`)
   - Uploader le fichier ZIP
4. Le PDF se compile **automatiquement** à chaque modification

**Avantages** :
- ✅ Aucune installation requise
- ✅ Fonctionne sur n'importe quel ordinateur/tablette
- ✅ Collaboration en temps réel
- ✅ Historique des versions automatique
- ✅ Sauvegarde cloud

**Inconvénients** :
- ❌ Nécessite une connexion internet
- ❌ Version gratuite limitée (1 collaborateur, timeout de compilation)

---

## 🔧 Prérequis

### Distribution LaTeX (obligatoire)

Vous devez avoir une distribution LaTeX installée sur votre machine.

#### Windows

**MiKTeX** (Recommandé) :
1. Télécharger : [https://miktex.org/download](https://miktex.org/download)
2. Installer (version 64-bit)
3. ⚠️ **Important** : Cocher **"Always install missing packages on-the-fly"**
4. Redémarrer le terminal après installation

**TeX Live** (Alternative) :
- Télécharger : [https://tug.org/texlive/](https://tug.org/texlive/)
- Installation complète (~7 GB)

#### Vérifier l'installation

Ouvrir un terminal et taper :
```bash
pdflatex --version
```

Vous devriez voir quelque chose comme :
```
pdfTeX 3.141592653-2.6-1.40.24 (MiKTeX 23.10)
```

Si la commande n'est pas reconnue, ajoutez MiKTeX au PATH Windows :
- Panneau de configuration → Système → Paramètres système avancés
- Variables d'environnement → Path
- Ajouter : `C:\Program Files\MiKTeX\miktex\bin\x64\`

---

## 📦 Packages LaTeX utilisés

La présentation utilise les packages suivants (installés automatiquement par MiKTeX) :

- `beamer` - Classe de présentation
- `amsmath`, `amssymb`, `amsfonts`, `amsthm` - Symboles mathématiques
- `mathtools` - Outils mathématiques avancés
- `graphicx` - Inclusion d'images
- `booktabs` - Tableaux professionnels
- `array` - Tableaux avancés
- `xcolor` - Couleurs
- `algorithm`, `algpseudocode` - Algorithmes
- `tikz`, `pgfplots` - Graphiques et diagrammes
- `babel[french]` - Support français
- `hyperref` - Hyperliens

**MiKTeX les installe automatiquement lors de la première compilation.**

---

## 📁 Structure du projet

```
presentation/
├── main.tex              # Fichier source LaTeX principal
├── main.pdf              # Présentation générée (38 pages)
├── compile.ps1           # Script PowerShell de compilation
├── compile.bat           # Script Batch de compilation
├── README.md             # Ce fichier
└── figures/              # Dossier des figures (11 fichiers PDF)
    ├── edo_comparaison_h0.500.pdf
    ├── edo_comparaison_h0.300.pdf
    ├── edo_comparaison_h0.150.pdf
    ├── edo_comparaison_h0.060.pdf
    ├── edo_convergence.pdf
    ├── int_gauss_laguerre.pdf
    ├── int_gauss_legendre.pdf
    ├── int_gauss_chebyshev.pdf
    ├── int_simpson.pdf
    ├── int_spline.pdf
    └── int_comparaison_globale.pdf
```

---

## ⚠️ Résolution de problèmes

### Erreur : "pdflatex n'est pas reconnu"

**Cause** : LaTeX n'est pas installé ou pas dans le PATH

**Solution** :
1. Installer MiKTeX : [https://miktex.org/download](https://miktex.org/download)
2. Redémarrer le terminal
3. Si ça ne fonctionne toujours pas, ajouter manuellement au PATH Windows

---

### Erreur : "File 'beamer.cls' not found"

**Cause** : Package LaTeX manquant

**Solution automatique** (MiKTeX) :
- MiKTeX devrait proposer d'installer automatiquement
- Accepter l'installation

**Solution manuelle** :
```bash
# Ouvrir MiKTeX Console
# Aller dans "Packages"
# Rechercher et installer le package manquant
```

Ou via ligne de commande :
```bash
mpm --install=beamer
```

---

### Erreur : "figures/xxx.pdf not found"

**Cause** : Les figures sont manquantes

**Solution** :
1. Vérifier que le dossier `figures/` existe
2. Générer les figures en exécutant le script Python :
   ```bash
   cd ..
   python analyse_complete.py
   cd presentation
   ```

---

### PDF ne se génère pas / Compilation bloquée

**Solution** :
1. Supprimer les fichiers auxiliaires :
   ```bash
   # PowerShell
   Remove-Item *.aux, *.log, *.nav, *.out, *.snm, *.toc, *.vrb
   
   # CMD
   del *.aux *.log *.nav *.out *.snm *.toc *.vrb
   ```

2. Recompiler :
   ```bash
   pdflatex main.tex
   pdflatex main.tex
   ```

---

### Erreur : "I can't write on file 'main.pdf'"

**Cause** : Le fichier PDF est ouvert dans un lecteur

**Solution** :
1. **Fermer** le fichier `main.pdf` dans votre lecteur PDF
2. Recompiler

---

### Table des matières vide

**Cause** : Une seule compilation effectuée

**Solution** :
- Compiler **deux fois** :
  ```bash
  pdflatex main.tex
  pdflatex main.tex
  ```
- LaTeX a besoin de deux passes pour générer les références et la table des matières

---

### Caractères accentués mal affichés

**Cause** : Problème d'encodage

**Solution** :
- Le fichier `main.tex` utilise déjà l'encodage correct avec des commandes LaTeX explicites (`\'{e}`, `\`{a}`, etc.)
- Si vous modifiez le fichier, utilisez un éditeur avec encodage UTF-8

---

## 📊 Comparaison des méthodes

| Méthode | Facilité | Vitesse | Installation | Recommandé pour |
|---------|----------|---------|--------------|-----------------|
| **Script (compile.ps1)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Aucune | Utilisation rapide |
| **Terminal manuel** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Aucune | Contrôle total |
| **PyCharm + TeXiFy** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Plugin | Développeurs Python |
| **TeXstudio** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Application | Débutants LaTeX |
| **Overleaf** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Aucune | Collaboration, mobilité |

---

## 🎯 Recommandation

### Pour vous (utilisateur du projet)

**Méthode recommandée** : **Script PowerShell** `.\compile.ps1`

**Pourquoi ?**
- ✅ Le plus simple (une seule commande)
- ✅ Le plus rapide (tout automatisé)
- ✅ Aucune configuration supplémentaire
- ✅ Gère automatiquement les erreurs courantes

### Pour des modifications fréquentes

**Utilisez TeXstudio** :
- Interface visuelle intuitive
- Aperçu en temps réel
- Détection d'erreurs
- Parfait pour éditer et tester

### Pour travailler en déplacement

**Utilisez Overleaf** :
- Pas d'installation
- Accessible partout
- Sauvegarde automatique

---

## 🎓 Utilisation pour la soutenance

### Mode présentation

1. Ouvrir `main.pdf`
2. Appuyer sur **F5** ou **Ctrl+L** (plein écran)
3. Naviguer avec les **flèches** ou clic souris
4. **Échap** pour quitter le mode plein écran

### Astuces

- **Page spécifique** : Taper le numéro puis Entrée
- **Vue d'ensemble** : Mode mosaïque du lecteur PDF
- **Zoom** : Ctrl + molette (si besoin de détails)
- **Notes** : Utilisez un second écran pour vos notes

---

## 📞 Support

### Ressources officielles

- **Documentation Beamer** : [https://ctan.org/pkg/beamer](https://ctan.org/pkg/beamer)
- **MiKTeX Documentation** : [https://docs.miktex.org/](https://docs.miktex.org/)
- **TeXstudio Manual** : [https://texstudio.sourceforge.net/manual/current/usermanual_en.html](https://texstudio.sourceforge.net/manual/current/usermanual_en.html)
- **Forum TeX** : [https://tex.stackexchange.com/](https://tex.stackexchange.com/)

### Contact

Pour toute question sur ce projet spécifique, consultez les autres fichiers de documentation :
- `CORRECTIONS.md` - Détails des corrections appliquées
- `RESUME_CORRECTIONS.md` - Historique technique
- `../CAHIER_DES_CHARGES.md` - Documentation complète du projet

---

## ✅ Checklist avant compilation

- [ ] MiKTeX ou TeX Live installé
- [ ] Commande `pdflatex` accessible dans le terminal
- [ ] Dossier `figures/` présent avec les 11 fichiers PDF
- [ ] Fichier `main.tex` présent
- [ ] Aucun fichier `main.pdf` ouvert dans un lecteur

---

## 🎉 Résultat attendu

Après compilation réussie :
- ✅ Fichier `main.pdf` créé (environ 1 MB)
- ✅ 38 diapositives
- ✅ Titre : "Méthodes Numériques pour Équations Différentielles et Intégration"
- ✅ Auteur : "Fofana Brahima"
- ✅ Toutes les figures affichées correctement
- ✅ Tableaux comparatifs remplis

---

**Bonne compilation et bonne soutenance ! 🎓**

*Dernière mise à jour : 6 janvier 2026*

