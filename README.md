# Méthodes Numériques pour la Résolution d’Équations Différentielles et d'Intégration Numérique


## Méthodes Numériques pour la Résolution d’Équations Différentielles

Ce projet implémente trois méthodes numériques à pas séparés pour résoudre d’Équations Différentielles Ordinaires:

- Euler
- Heun
- Runge-Kunta

suivant (exemple principal utilisé dans les tests) :

$$
\begin{cases}
z'(x) = \pi \cos(\pi x) \cdot z(x), & \forall x \in [0, 6] \\
z(0) = 1
\end{cases}
$$

**Solution exacte connue :**

$$
z(x) = e^{\sin(\pi x)}
$$


## Méthodes Implémentées et Formules Mathématiques

### 1. Méthode d’Euler

**Formule itérative :**

$$
y_{n+1} = y_n + h \cdot f(x_n, y_n)
$$

**Description :**  
Méthode élémentaire : on avance d’un pas \( h \) en suivant la pente donnée par $$f(x_n, y_n)$$ au point courant.  
L’approximation obtenue est une ligne brisée (polygénale).  

### 2. Méthode de Heun

**Formules itératives :**

$$
\begin{align*}
k_1 &= f(x_n, y_n) \\
k_2 &= f\left(x_n + \frac{h}{2}, \, y_n + \frac{h}{2} k_1 \right) \\
y_{n+1} &= y_n + h \cdot k_2
\end{align*}
$$

**Description :**  
Méthode prédicteur-correcteur améliorée :  
- $k_1$ représente la pente au début de l’intervalle (identique à Euler).  
- $k_2$ estime la pente au milieu de l’intervalle grâce à une prédiction intermédiaire.  
- La mise à jour finale utilise uniquement $k_2$, ce qui améliore sensiblement la précision.  


### 3. Méthode de Runge-Kutta

**Formules itératives :**

$$
\begin{align*}
k_1 &= f(x_n, y_n) \\
k_2 &= f\left(x_n + \frac{h}{2}, \, y_n + \frac{h}{2} k_1 \right) \\
k_3 &= f\left(x_n + \frac{h}{2}, \, y_n + \frac{h}{2} k_2 \right) \\
k_4 &= f\left(x_n + h, \, y_n + h k_3 \right) \\[10pt]
y_{n+1} &= y_n + \frac{h}{6} (k_1 + 2k_2 + 2k_3 + k_4)
\end{align*}
$$

**Description :**  
Méthode de référence pour sa précision et sa robustesse :  
- Quatre évaluations de $f$ par pas : au début $k_1$, deux fois au milieu $k_2$, k_3$, et à la fin $k_4$.  
- Combinaison pondérée optimale des pentes qui élimine les termes d’erreur jusqu’à l’ordre 4 inclus.  

---

# Méthodes d'Intégration Numérique

Ce projet implémente et compare plusieurs méthodes d'intégration numérique en Python :

- Gauss-Laguerre
- Gauss-Legendre
- Gauss-Chebyshev
- Règle de Simpson (composite)
- Intégration par spline quadratique (interpolation + intégration analytique)

Le script exécute 6 exemples et affiche pour chacun :
- L'erreur absolue en fonction du paramètre *n*
- Le temps d'exécution

## Méthodes Implémentées et Formules Mathématiques

### 1. Quadrature de Gauss-Laguerre

Utilisée pour les intégrales semi-infinies avec poids exponentiel :

$$
\int_0^{+\infty} e^{-x} f(x) \, dx \approx \sum_{i=1}^n w_i f(x_i)
$$

où $x_i$ sont les racines du polynôme de Laguerre $L_n(x)$ et $w_i$ les poids associés.

### 2. Quadrature de Gauss-Legendre

Pour les intégrales sur un intervalle fini $[a, b]$ :

$$
\int_a^b f(x) \, dx \approx \frac{b-a}{2} \sum_{i=1}^n w_i \, f\left( \frac{b-a}{2} x_i + \frac{a+b}{2} \right)
$$

où $x_i$ et $w_i$ sont les nœuds et poids de Gauss-Legendre sur $[-1, 1]$.

### 3. Quadrature de Gauss-Chebyshev

Pour les intégrales avec poids singulier aux extrémités :

$$
\int_{-1}^{1} \frac{f(x)}{\sqrt{1 - x^2}} \, dx \approx \sum_{i=1}^n w_i f(x_i) = \frac{\pi}{n} \sum_{i=1}^n f\left( \cos \left( \frac{(2i-1)\pi}{2n} \right) \right)
$$

Les poids sont tous égaux à \(\pi/n\).

### 4. Règle de Simpson Composite

Sur \([a, b]\) divisé en \(n\) sous-intervalles pairs (\(n\) pair) :

$$
\int_a^b f(x) \, dx \approx \frac{h}{3} \left[ f(a) + f(b) + 4 \sum_{k=1}^{n/2} f(a + (2k-1)h) + 2 \sum_{k=1}^{n/2-1} f(a + 2kh) \right]
$$

avec $ h = \frac{b - a}{n} $.

### 5. Intégration par Spline Quadratique

1. **Interpolation** : On évalue \(f\) en \(m\) points équidistants sur \([a, b]\) et on construit une spline quadratique \(S(x)\) (degré 2 par morceaux, continue en valeur et dérivée première \(C^1\)).

Sur chaque intervalle $[x_i, x_{i+1}]$ :

$$
S(x) = a_i (x - x_i)^2 + b_i (x - x_i) + c_i
$$

2. **Intégration analytique exacte** de la spline :

$$
\int_a^b f(x) \, dx \approx \int_a^b S(x) \, dx = \sum_{i=0}^{m-2} \left( \frac{a_i h_i^3}{3} + \frac{b_i h_i^2}{2} + c_i h_i \right)
$$

## Formules des Coefficients de la Spline Quadratique

Pour chaque sous-intervalle $[x_i, x_{i+1}]$, les coefficients du polynôme quadratique

$$
S_i(x) = a_i (x - x_i)^2 + b_i (x - x_i) + c_i
$$

sont donnés par les relations suivantes :

$$
\boxed{
\begin{aligned}
c_i &= y_i \\[0.5em]
b_i &= 2\,a_{i-1}\,h_{i-1} + b_{i-1} \\[0.5em]
a_i &= \frac{y_{i+1} - y_i - b_i\,h_i}{h_i^2}
\end{aligned}
}
$$

**où :**

- $h_i = x_{i+1} - x_i$ est la longueur du sous-intervalle,
- $y_i = f(x_i)$ est la valeur de la fonction au point $x_i$.

**Ces relations assurent :**

- l'interpolation des points,
- la continuité de la fonction,
- la continuité de la dérivée première.

Cette méthode est très précise car l’intégration de la spline est exacte (pas d’erreur de discrétisation supplémentaire).