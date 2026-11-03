# Mapa del 2do parcial: por dónde entra

> **PROVISIONAL.** Sale de la slide de temario de la cátedra. Puede cambiar por días
> sin clase, y todavía faltan las slides con la explicación del profesor. Cuando se
> procese cada clase con `/clase`, actualizá la fila correspondiente. Si el profesor
> dice otra cosa en clase, gana el profesor.
>
> Lectura del alumno: entra con foco del punto 1 al 4; el punto 5 (no supervisado) se da
> como bonus **pero se evalúa**.

Las secciones de ESL salen de `clase/referencias/bibliografia.md`; donde no está
cubierto ahí, figura "verificar" y hay que confirmarlo antes de citar.

**Leyenda:** 🧮 derivar en frío · 📌 saber como resultado · ⚠️ trampa típica

## 1. Intermezzo: Newton-Raphson

- **Material:** `books/explained/cap4_metodos_lineales_clasificacion.ipynb`, §4.4.1 (Newton e IRLS); `src/figuras/Methode_newton.png`. ESL §4.4 (logística). Clase propia: `src/notebooks/explained/6_metodos_lineales_clasificacion.ipynb` §6 (Newton) y §9 (IRLS).
- 🧮 La iteración `x_{n+1} = x_n − f(x_n)/f'(x_n)` y su versión para optimizar: `θ ← θ − H⁻¹ ∇`. Por qué Newton es una aproximación cuadrática.
- 📌 Converge rápido cerca del óptimo; cada paso cuesta invertir el Hessiano.
- ⚠️ Confundir buscar raíces de `f` con buscar el mínimo (raíces de `f'`).

## 2. Clasificación: logística, regularización, LDA, Naive Bayes

- **Material:** cap. 4 de ESL en `books/explained/cap4_metodos_lineales_clasificacion.ipynb` (§4.3 LDA/QDA, §4.4 logística, §4.4.4 logística L1). Clase propia: `src/notebooks/explained/6_metodos_lineales_clasificacion.ipynb` §2–§3 (Bayes y frontera de LDA), §7–§10 (logística, IRLS, regularizada). ESL §4.3, §4.4. Naive Bayes: no está en el capítulo armado (**verificar** dónde lo ubica la cátedra). Enfoque generativo vs discriminativo: Bishop §1.5.4 (en la tabla de bibliografía).
- 🧮 Log-verosimilitud logística, su gradiente `Xᵀ(y − p)` y el Hessiano `−Xᵀ W X`; un paso de Newton como mínimos cuadrados ponderados (IRLS). 🧮 Frontera de decisión de LDA igualando posteriores con covarianza común (queda lineal). 🧮 Por qué logística + separabilidad perfecta diverge.
- 📌 Logística L1 (Lasso para clasificación); LDA vs logística (§4.4.5 en la notebook); Naive Bayes asume independencia condicional.
- ⚠️ Ajustar logística con mínimos cuadrados; creer que LDA necesita datos gaussianos *para usarse* (lo necesita para ser óptimo); que los coeficientes de logística se lean como en OLS (son log-odds).

## 3. Árboles y ensambles: Bagging, Random Forest, Boosting, XGBoost

> **FUERA DEL TEMARIO** (confirmado por el alumno el 2026-11-03: sacaron ensambles de la materia). Se deja la fila como referencia.

- **Material:** sin notebook todavía. ESL §9.2 (árboles/CART), §8.7 (bagging), cap. 15 (random forests), cap. 10 (boosting). XGBoost: fuera de ESL (**verificar**).
- 🧮 (probable) Criterio de corte con Gini/entropía/RSS. 🧮 Por qué promediar `B` modelos reduce la varianza: `Var = ρσ² + (1−ρ)σ²/B`; es la fórmula que explica por qué random forest decorrelaciona.
- 📌 Boosting ajusta sobre residuos / gradientes; bagging vs boosting ataca varianza vs sesgo.
- ⚠️ Decir que bagging reduce el sesgo; creer que más árboles sobreajusta en random forest.

## 4. Evaluación: sesgo-varianza, nº efectivo de parámetros, CV, bootstrap

- **Material:** `src/notebooks/explained/1_intro_teoria_decision.ipynb` y `src/figuras/Bias-Variance.png` (ya hay intro). Clase propia: `src/notebooks/explained/7_evaluacion_modelos.ipynb` §2 (EPE y media condicional), §3 (sesgo-varianza), §4 (OLS y Ridge con df), §6 (K-fold). ESL §2.9 y §7.2–7.3 (sesgo-varianza), §7.10–7.11 (CV y bootstrap). Número efectivo de parámetros: ESL §7.6 (**verificar**); `df(λ)` de Ridge está derivado en la clase 7 §4 (traza de la matriz sombrero vía la SVD de la clase 3).
- 🧮 Descomposición `EPE(x₀) = σ² + Sesgo² + Var`. 🧮 `df` de Ridge desde la SVD (enlaza con la clase 3). 🧮 Por qué K-fold con K chico sesga y K grande tiene varianza alta.
- 📌 Bootstrap: muestreo con reemplazo, ~63,2 % de observaciones únicas por réplica.
- ⚠️ Estimar el error con el mismo conjunto en el que se seleccionó el modelo; hacer selección de variables *antes* de la CV.

## 5. No supervisado (bonus, pero se evalúa)

- **Material:** Clase propia: `src/notebooks/explained/8_aprendizaje_no_supervisado.ipynb` — §1 (supervisado vs no supervisado, $P(X)$), §2 (reducción de dimensión y clustering como modas de $P(X)$), §3 (mezcla de dos gaussianas), §4 (MV directa: log de una suma, punto fijo, degeneración $\sigma\to0$), §5 (verosimilitud completa con $\Delta_i$ conocidas), §6 (responsabilidades por Bayes), §7 (algoritmo EM, monotonía de $\ell$, inicialización, sklearn), §8 ($K$ componentes y multivariado, $\pi_k$ por Lagrange). PCA: la clase solo lo nombra (celda 4); el desarrollo está en `books/explained/cap14_5_pca_componentes_principales.ipynb`, `notes/descomposicion-matrices-svd.md` y la clase 3 (SVD). ESL §8.5 (EM), §14.5 (PCA), §14.3 (clustering); Bishop cap. 9.
- 🧮 MV de la mezcla: derivar $\ell$ respecto de $\mu_2$ ⇒ $\mu_2=\sum\gamma_i y_i/\sum\gamma_i$ con $\gamma_i$ que depende de $\mu_2$ (punto fijo ⇒ EM). 🧮 Estimadores con $\Delta_i$ conocidas desde $\ell_0$ y por qué el M-step cambia $\Delta_i$ por $\gamma_i$ ($\ell_0$ lineal en $\Delta_i$). 🧮 Responsabilidad $\gamma_i=E[\Delta_i\mid y_i]$ por Bayes (2 y $K$ componentes). 🧮 $\pi_k=N_k/N$ por Lagrange. 🧮 PCA desde SVD (`X = UDVᵀ` centrada ⇒ componentes = columnas de `V`, varianzas `d_j²/N`) y desde la matriz de covarianza (autovectores de `XᵀX/N`): mostrar que dan lo mismo — **no se dio en la clase 8**, está en el material de PCA.
- 📌 EM no baja nunca $\ell$ pero converge a un máximo local; la inicialización importa (ESL: dos datos al azar, varianza total, $\pi=0{,}5$); $\ell$ no está acotada (una $\sigma_k\to0$ sobre un dato); cluster = $\operatorname{argmax}_k\gamma_{ik}$; EM ≈ QDA sin etiquetas; K-means = límite duro. K-means y jerárquico **no se dieron en la clase 8** (solo como puente); reducción no lineal tampoco (**a confirmar** si la cátedra los toma).
- ⚠️ Confundir $\gamma_i$ (por dato) con $\pi$ (global); aplicar $\log(a+b)=\log a+\log b$; los dos $\pi$ (peso vs. $3{,}14$); creer que EM da el máximo global; elegir $K$ maximizando $\ell$; *label switching* al comparar. PCA: no centrar; no estandarizar cuando las escalas difieren.

## Derivaciones en frío, en una lista

1. Un paso de Newton y su forma para logística (IRLS). — M9, M1, M10
2. Gradiente y Hessiano de la log-verosimilitud logística. — M10, M1
3. Frontera de LDA (covarianza común). — M3
4. `EPE = σ² + Sesgo² + Var`. — M2, M3
5. ~~`Var` del promedio de `B` estimadores correlacionados. — M4~~ (ensambles fuera del temario)
6. `df(λ)` de Ridge con la SVD. — M4, M5
7. PCA: SVD ≡ autovectores de la covarianza. — M5, M8
8. MV de la mezcla de gaussianas ⇒ punto fijo con responsabilidades (EM). — M10, M1
9. M-step: estimadores con $\Delta_i$ conocidas y $\pi_k = N_k/N$. — M10, M1, M8
10. Responsabilidad por Bayes. — (Bayes; candidata a movida)

Reglas de práctica: el ciclo de días y el criterio de "estudiado" están en
`tutor/README.md`; las movidas (`M#`), en `tutor/movidas.md`.
