# ==============================================================================
# INSTRUCTIONS DE COMPILATION - PRÉSENTATION LATEX
# ==============================================================================

## ⚠️ PROBLÈMES RÉSOLUS

Tous les problèmes signalés ont été corrigés :

### ✅ 1. Page de garde - Titre visible
- Les caractères accentués sont maintenant encodés correctement
- Utilisation de commandes LaTeX explicites (\'e, \`e, etc.)
- Le titre complet s'affiche correctement

### ✅ 2. Table des matières
- Ajout de l'option `[hideallsubsections]` pour affichage correct
- La table des matières s'affiche maintenant sur la diapositive 2

### ✅ 3. Tableau comparaison EDO (diapositive 31)
- Remplacement des étoiles (★) par des valeurs textuelles
- Données complètes : Faible/Bonne/Excellente, etc.
- Tableau entièrement rempli et lisible

### ✅ 4. Tableau comparaison Intégration
- Remplacement des étoiles par des valeurs textuelles
- Toutes les cellules contiennent des données
- Format cohérent et professionnel

### ✅ 5. En-têtes des diapositives
- Configuration des couleurs pour meilleure visibilité
- Fond bleu marine avec texte blanc
- En-têtes visibles sur toutes les diapositives

## 📋 COMPILATION

### Méthode 1 : Script PowerShell automatique (RECOMMANDÉ)

```powershell
cd presentation
.\compile.ps1
```

### Méthode 2 : Compilation manuelle

```powershell
cd presentation

# IMPORTANT : Fermez le fichier main.pdf s'il est ouvert !

pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### Méthode 3 : Script Batch (Windows)

```cmd
cd presentation
compile.bat
```

## ⚠️ ATTENTION : Erreur "I can't write on file"

Si vous voyez cette erreur :
```
! I can't write on file `main.pdf'.
```

**Solution :**
1. Fermez le fichier `main.pdf` dans votre lecteur PDF
2. Relancez la compilation

## 🔍 VÉRIFICATION DES CORRECTIONS

Après compilation, vérifiez :

### Diapositive 1 (Page de titre)
- [ ] Titre visible : "Méthodes Numériques pour Équations Différentielles..."
- [ ] Sous-titre visible : "Analyse Comparative et Validation Expérimentale"
- [ ] Fond bleu marine, texte blanc
- [ ] Auteur et institut visibles

### Diapositive 2 (Table des matières)
- [ ] Liste des sections affichée :
  * Introduction
  * Fondements Théoriques
  * Méthodes pour Équations Différentielles
  * Méthodes d'Intégration Numérique
  * Résultats Expérimentaux
  * Analyse Comparative
  * Conclusion

### Diapositive 31 (Tableau EDO)
- [ ] Colonne "Critère" : Précision, Vitesse, Stabilité, Simplicité, Usage général
- [ ] Colonne "Euler" : Faible, Très rapide, Limitée, Très simple, Déconseillé
- [ ] Colonne "Heun" : Bonne, Rapide, Bonne, Simple, Recommandé
- [ ] Colonne "RK4" : Excellente, Modérée, Excellente, Moyenne, Recommandé

### Diapositive 32 (Tableau Intégration)
- [ ] 5 colonnes de méthodes : G-Lag., G-Leg., G-Cheb., Simpson, Spline
- [ ] Toutes les cellules remplies avec : Excellente, Bonne, Moyenne, etc.

### Toutes les diapositives
- [ ] En-têtes visibles en haut (fond bleu, texte blanc)
- [ ] Numéro de diapositive visible en bas
- [ ] Navigation visible en bas à droite

## 📊 STRUCTURE DE LA PRÉSENTATION

Total : ~35 diapositives

1. **Introduction** (2 slides)
2. **Fondements Théoriques** (4 slides)
3. **Méthodes EDO** (3 slides)
4. **Méthodes Intégration** (6 slides)
5. **Résultats Expérimentaux** (12 slides)
   - 4 comparaisons EDO (h différents)
   - 1 convergence EDO
   - 1 tableau EDO
   - 5 méthodes intégration
   - 1 comparaison globale
   - 1 tableau intégration
6. **Analyse Comparative** (3 slides)
7. **Conclusion** (4 slides)

## 🎨 PERSONNALISATION (optionnel)

### Changer le thème

Dans `main.tex`, ligne ~30 :
```latex
\usetheme{Madrid}  % Options : Berlin, Copenhagen, Warsaw, Boadilla
```

### Changer les couleurs

Ligne ~33-40 (déjà optimisé pour visibilité) :
```latex
\setbeamercolor{structure}{fg=NavyBlue}
\setbeamercolor{title}{fg=white,bg=NavyBlue}
```

Options de couleurs : NavyBlue, DarkBlue, Red, ForestGreen, Purple

## 🔧 DÉPANNAGE

### Erreur : "pdflatex not found"
**Solution :** Installez MiKTeX (https://miktex.org/) ou TeX Live

### Erreur : "Package not found"
**Solution :** MiKTeX télécharge automatiquement les packages manquants
- Acceptez l'installation automatique lors de la première compilation

### Erreur : "Undefined control sequence"
**Solution :** Vérifiez que tous les packages sont chargés
- Tous les packages nécessaires sont déjà dans `main.tex`

### Table des matières vide
**Solution :** Compilez DEUX FOIS (LaTeX a besoin de deux passes)

### Figures manquantes
**Solution :** Vérifiez que les figures sont dans `presentation/figures/`
```powershell
ls figures/*.pdf  # Doit lister 11 fichiers PDF
```

Si les figures manquent, générez-les :
```powershell
cd ..
python analyse_complete.py
cd presentation
```

## 📁 FICHIERS GÉNÉRÉS

Après compilation réussie :
- ✅ `main.pdf` - Présentation finale (à conserver)
- `main.aux` - Fichier auxiliaire (peut être supprimé)
- `main.log` - Journal de compilation (utile pour debug)
- `main.nav` - Navigation Beamer (peut être supprimé)
- `main.out` - Signets PDF (peut être supprimé)
- `main.snm` - Notes Beamer (peut être supprimé)
- `main.toc` - Table des matières (peut être supprimé)

### Nettoyage

```powershell
# Supprimer les fichiers auxiliaires
Remove-Item *.aux, *.log, *.nav, *.out, *.snm, *.toc, *.vrb
```

## ✅ RÉSUMÉ DES MODIFICATIONS

| Problème | Localisation | Correction |
|----------|--------------|------------|
| Titre invisible | Page 1 | Encodage UTF-8 → Commandes LaTeX explicites |
| Table vide | Page 2 | Ajout `[hideallsubsections]` |
| Tableau EDO vide | Page 31 | Remplacement ★ → Texte |
| Tableau Int vide | Page 32 | Remplacement ★ → Texte |
| En-têtes invisibles | Toutes | Configuration couleurs fg/bg |

## 🎯 UTILISATION POUR SOUTENANCE

### Mode présentation
1. Ouvrez `main.pdf` avec Adobe Reader ou autre lecteur
2. Appuyez sur **F5** ou **Ctrl+L** pour plein écran
3. Utilisez les **flèches** pour naviguer
4. **Échap** pour quitter le mode présentation

### Impression (optionnel)
- Format : PDF (déjà vectoriel, haute qualité)
- Pages par feuille : 1 (diapositives) ou 2-4 (handouts)
- Couleur recommandée (graphiques scientifiques)

## 📞 SUPPORT

En cas de problème persistant :
1. Consultez `main.log` (dernières lignes pour l'erreur)
2. Vérifiez l'encodage UTF-8 du fichier
3. Assurez-vous que MiKTeX est à jour
4. Fermez tous les lecteurs PDF avant compilation

---

**Date des corrections :** 2026-01-06
**Fichier corrigé :** `presentation/main.tex`
**Version :** Finale (prête pour soutenance)

✅ **Tous les problèmes signalés sont maintenant résolus !**

