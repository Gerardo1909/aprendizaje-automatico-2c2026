# Mapa tema → capítulo

Para no citar de memoria. **Regla de oro: si el tema no está en esta tabla y no
estás seguro de la sección, citá el capítulo entero o no cites nada.** Una
referencia inventada es peor que ninguna: el alumno la va a buscar.

## Los tres libros

| Sigla | Libro | Rol |
|---|---|---|
| 📕 **ESL** | *The Elements of Statistical Learning* — Hastie, Tibshirani & Friedman (2ª ed.) | **Referencia principal.** La notación de la cátedra es la de este libro. [PDF](https://hastie.su.domains/ElemStatLearn/) |
| 📗 **ISL** | *An Introduction to Statistical Learning* — James, Witten, Hastie & Tibshirani | Primera aproximación, más suave y con menos álgebra. [Sitio](https://www.statlearning.com/) |
| 📘 **Bishop** | *Pattern Recognition and Machine Learning* — Christopher Bishop (2006) | Enfoque más bayesiano. Usa **otra notación** (ver abajo). [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf) |

## Traducción de notación ESL ↔ Bishop

Las clases mezclan las dos. Cuando eso pase, aclarálo y dale al alumno esta tabla.

| Concepto | ESL / cátedra | Bishop |
|---|---|---|
| Salida cualitativa | $G$, con valores en $\mathcal{G}$ | $\mathcal{C}_k$ (clases) |
| Clase $k$-ésima | $\mathcal{G}_k$ | $\mathcal{C}_k$ |
| Posterior de clase | $p(\mathcal{G}_k \mid X)$ | $p(\mathcal{C}_k \mid \mathbf{x})$ |
| Predicción de clase | $\hat{G}(x)$ | la región de decisión $\mathcal{R}_k$ |
| Pérdida | matriz $\mathbf{L}$, $L(k,\ell)$ | $L_{kj}$ |
| Riesgo | $EPE = E[L(G,\hat{G}(X))]$ | *expected loss* $\mathbb{E}[L]$ |
| Parámetros | $\beta$ | $\mathbf{w}$ |
| Diseño / atributos | $\mathbf{X}$ ($N \times p$) | $\Phi$ (matriz de diseño con bases $\phi_j$) |

Ojo con un choque real: para ESL, $p$ es el **número de predictores**; en muchas
fórmulas de Bishop, $p(\cdot)$ es una **densidad**. El contexto lo desambigua,
pero conviene decirlo la primera vez.

## Tema → sección

| Tema | 📕 ESL | 📘 Bishop | 📗 ISL |
|---|---|---|---|
| Notación ($X$, $G$, $x_i$, $\mathbf{X}$, $\mathbf{x}_j$) | §2.2 | — | — |
| Aprendizaje supervisado vs no supervisado | §2.1, cap. 14 | §1.1 | §2.1, cap. 12 |
| Inferencia vs predicción | — | — | §2.1.1 |
| Reglas de suma y producto, Bayes | — | §1.2 | — |
| Enfoque bayesiano vs frecuentista | cap. 8 (§8.3–8.4) | §1.2.3, §1.2.5–1.2.6 | — |
| **Teoría de la decisión** (EPE, pérdida 0-1, regla de Bayes) | **§2.4** | **§1.5** | §2.2 |
| $f(x)=E(Y\mid X=x)$ como predictor óptimo bajo pérdida cuadrática | §2.4 | §1.5.5 | §2.1 |
| Generativo / discriminativo / función discriminante | — | **§1.5.4** | — |
| Maldición de la dimensionalidad | §2.5 | §1.4 | §4.5 |
| Sesgo–varianza | §2.9, §7.2–7.3 | §3.2 | §2.2.2 |
| $k$-vecinos más cercanos | §2.3.2, cap. 13 | §2.5.2 | §3.5 |
| **Regresión lineal: formulación y OLS** | **§3.2** | **§3.1** | §3.1–3.2 |
| Geometría / proyección ortogonal / matriz *hat* | §3.2 (Fig. 3.2) | §3.1.2 | — |
| Insesgadez, $Var(\hat\beta)$, $Z$-score, estadístico $F$ | §3.2 | §3.1.1 | §3.1.2, §3.2.2 |
| Gauss–Markov | §3.2.2 | — | — |
| Ejemplo *Prostate Cancer* (Tablas 3.1 y 3.2) | §3.2.1 | — | — |
| Regresión simple → múltiple (ortogonalización) | §3.2.3 | — | §3.1 |
| Descenso por gradiente estocástico / LMS | — | **§3.1.3** (*sequential learning*) | — |
| Selección de subconjuntos | §3.3 | — | §6.1 |
| Ridge, Lasso, Elastic Net | §3.4 | §3.1.4 | §6.2 |
| Análisis discriminante (LDA/QDA) | §4.3 | §4.2 | §4.4 |
| Regresión logística | §4.4 | §4.3 | §4.3 |
| Validación cruzada, bootstrap | §7.10–7.11 | §1.3 | cap. 5 |
| Árboles / CART | §9.2 | §14.4 | cap. 8 |
| SVM | cap. 12 | cap. 7 | cap. 9 |
| Redes neuronales | cap. 11 | cap. 5 | cap. 10 |
| Bagging, boosting, random forests | §8.7, cap. 10, cap. 15 | §14.2–14.3 | cap. 8 |
| PCA, clustering | §14.5, §14.3 | cap. 12, §9.1 | cap. 12 |

## Cosas puntuales que sí podés citar con número

Verificadas, se pueden nombrar sin riesgo:

- **ESL Tabla 3.1** — correlaciones entre predictores del dataset *prostate*.
- **ESL Tabla 3.2** — coeficientes de mínimos cuadrados y sus $Z$-scores para *prostate*.
- **ESL Fig. 3.2** — la proyección ortogonal de $\mathbf{y}$ sobre el subespacio
  generado por las columnas de $\mathbf{X}$.

Para todo lo demás: **sección, no ecuación**. Y nunca un número de página.

## Papers que menciona la cátedra

- Hoerl & Kennard (1970), *Ridge Regression: Biased Estimation for Nonorthogonal Problems*.
- Tibshirani (1996), *Regression Shrinkage and Selection via the Lasso*.
- Zou & Hastie (2005), *Regularization and variable selection via the elastic net*.

---

*Ampliá esta tabla a medida que avanza la cursada, en vez de citar de memoria.*
