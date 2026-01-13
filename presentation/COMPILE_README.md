# Compilation de la présentation LaTeX

## 📋 Prérequis

- **Windows PowerShell 5.1** ou supérieur
- **MiKTeX** ou **TeX Live** installé
- Le fichier `main.tex` doit être présent dans le répertoire

## 🚀 Utilisation

### Méthode 1 : Double-clic (Recommandé)

1. Double-cliquez sur le fichier **`compile.ps1`**
2. Si Windows bloque l'exécution, faites un **clic droit** → **"Exécuter avec PowerShell"**

### Méthode 2 : Ligne de commande

Ouvrez PowerShell dans le dossier `presentation` et exécutez :

```powershell
.\compile.ps1
```

## 🔧 Résolution des problèmes

### Erreur : "L'exécution de scripts est désactivée"

Si vous obtenez cette erreur, autorisez l'exécution de scripts PowerShell (à faire une seule fois) :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessayez :

```powershell
.\compile.ps1
```

### Erreur : "pdflatex n'est pas installé"

Installez une distribution LaTeX :
- **MiKTeX** : https://miktex.org/download (recommandé pour Windows)
- **TeX Live** : https://www.tug.org/texlive/

### Erreur : "Le fichier main.tex est introuvable"

Assurez-vous que :
1. Vous êtes dans le bon répertoire (celui contenant `main.tex`)
2. Le fichier `main.tex` existe bien

## ✨ Fonctionnalités du script

Le script `compile.ps1` effectue automatiquement :

- ✅ Vérification de la présence de `pdflatex`
- ✅ Vérification de la présence de `main.tex`
- ✅ Nettoyage des fichiers temporaires avant compilation
- ✅ Fermeture automatique du PDF s'il est ouvert
- ✅ **Compilation en 2 passes** (pour les références et la table des matières)
- ✅ Vérification que le PDF a bien été généré
- ✅ Nettoyage des fichiers temporaires après compilation
- ✅ **Ouverture automatique du PDF** à la fin
- ✅ Affichage du temps de compilation et de la taille du fichier

## 📂 Fichiers générés

Après compilation réussie :
- ✅ **`main.pdf`** - Votre présentation (conservé)
- ❌ `main.aux`, `main.log`, `main.nav`, etc. - Fichiers temporaires (supprimés automatiquement)

## 📊 Sortie du script

Le script affiche des messages colorés :
- 🟢 **[✓]** Succès
- 🔵 **[i]** Information
- 🟡 **[!]** Avertissement
- 🔴 **[✗]** Erreur

## 🎯 Utilisation avancée

### Compilation sans ouverture automatique

Modifiez la variable `$AutoOpen` au début du script :

```powershell
$AutoOpen = $false
```

### Conserver les fichiers temporaires

Commentez la ligne de nettoyage final dans le script.

## 📞 Support

En cas de problème :
1. Vérifiez que LaTeX est installé : `pdflatex --version`
2. Consultez le fichier `main.log` pour les erreurs de compilation
3. Assurez-vous que tous les packages LaTeX sont à jour

---

**Auteur :** BRAHIMA FOFANA  
**Date :** 13 janvier 2026  
**Version :** 1.0

