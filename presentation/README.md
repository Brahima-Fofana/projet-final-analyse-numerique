# Présentation LaTeX - Analyse Numérique

## Structure du projet

```
presentation/
├── main.tex              # Fichier principal de la présentation Beamer
├── figures/              # Dossier contenant toutes les figures générées
│   ├── edo_*.pdf/png     # Figures équations différentielles
│   └── int_*.pdf/png     # Figures intégration numérique
└── README.md             # Ce fichier
```

## Compilation

### Méthode 1 : Compilation manuelle (Windows)

Ouvrez PowerShell dans le dossier `presentation/` et exécutez :

```powershell
pdflatex main.tex
pdflatex main.tex  # Seconde compilation pour les références
```

### Méthode 2 : Avec latexmk (recommandé)

```powershell
latexmk -pdf main.tex
```

Pour nettoyer les fichiers auxiliaires :

```powershell
latexmk -c
```

### Méthode 3 : Avec un éditeur LaTeX

Ouvrez `main.tex` avec :
- **TeXstudio** (recommandé)
- **TeXmaker**
- **Overleaf** (en ligne)
- **VS Code** avec extension LaTeX Workshop

## Prérequis

Vous devez avoir une distribution LaTeX installée :

### Windows
- **MiKTeX** (https://miktex.org/) - recommandé
- **TeX Live** (https://tug.org/texlive/)

### Installation des packages nécessaires

Les packages suivants seront installés automatiquement par MiKTeX lors de la première compilation :

- `beamer` - Classe de présentation
- `amsmath`, `amssymb`, `amsfonts` - Symboles mathématiques
- `graphicx` - Inclusion d'images
- `pgfplots`, `tikz` - Graphiques
- `babel` - Support français
- `booktabs` - Tableaux professionnels
- `algorithm`, `algpseudocode` - Algorithmes

## Génération des figures

Avant de compiler la présentation, assurez-vous que toutes les figures ont été générées en exécutant :

```powershell
cd ..  # Revenir à la racine du projet
python analyse_complete.py
```

Cela génère automatiquement toutes les figures dans `presentation/figures/`.

## Structure de la présentation

1. **Introduction** - Contexte et objectifs
2. **Fondements Théoriques** - Base mathématique
3. **Méthodes pour Équations Différentielles**
   - Euler
   - Heun
   - Runge-Kutta 4
4. **Méthodes d'Intégration Numérique**
   - Quadratures de Gauss (Laguerre, Legendre, Chebyshev)
   - Simpson
   - Splines Quadratiques
5. **Résultats Expérimentaux** - Figures et analyses
6. **Analyse Comparative** - Synthèse
7. **Conclusion** - Recommandations et perspectives

## Format de sortie

- **Sortie principale** : `main.pdf`
- **Format** : Beamer (diapositives 16:9 par défaut)
- **Qualité** : Figures en PDF (vectoriel, haute qualité)

## Personnalisation

### Modifier le thème

Dans `main.tex`, ligne ~30 :
```latex
\usetheme{Madrid}  % Changer pour : Berlin, Copenhagen, Warsaw, etc.
```

### Modifier les couleurs

Ligne ~31 :
```latex
\usecolortheme{default}  % Changer pour : whale, beaver, crane, etc.
```

### Activer LaTeX pour les formules (si disponible)

Ligne ~14 :
```latex
rc('text', usetex=True)  % Dans le script Python
```

## Résolution de problèmes

### Erreur : "File not found"
- Vérifiez que les figures sont dans `presentation/figures/`
- Vérifiez les chemins relatifs

### Erreur : "Package not found"
- MiKTeX : Acceptez l'installation automatique des packages
- TeX Live : Exécutez `tlmgr install <package_name>`

### Erreur de compilation
- Compilez deux fois (pour les références)
- Vérifiez les logs dans `main.log`

### Figures trop grandes/petites
- Ajustez `width=0.95\textwidth` dans les commandes `\includegraphics`

## Visualisation

Après compilation réussie, ouvrez `main.pdf` avec :
- Adobe Acrobat Reader
- SumatraPDF
- Navigateur web
- Visionneuse PDF intégrée à votre éditeur

## Mode présentation

Dans un lecteur PDF :
- **F5** ou **Ctrl+L** : Mode plein écran
- **Flèches** : Navigation
- **Échap** : Quitter le mode plein écran

## Contact et Support

Pour toute question sur la présentation LaTeX :
- Consultez la documentation Beamer : https://ctan.org/pkg/beamer
- Forum TeX : https://tex.stackexchange.com/

## Licence

Ce document fait partie du projet d'analyse numérique - Master 2 GI.

