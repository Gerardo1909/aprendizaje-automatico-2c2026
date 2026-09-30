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

- **Material:** `books/explained/cap4_metodos_lineales_clasificacion.ipynb`, §4.4.1 (Newton e IRLS); `src/figuras/Methode_newton.png`. ESL §4.4 (logística). Clase propia: pendiente.
- 🧮 La iteración `x_{n+1} = x_n − f(x_n)/f'(x_n)` y su versión para optimizar: `θ ← θ − H⁻¹ ∇`. Por qué Newton es una aproximación cuadrática.
- 📌 Converge rápido cerca del óptimo; cada paso cuesta invertir el Hessiano.
- ⚠️ Confundir buscar raíces de `f` con buscar el mínimo (raíces de `f'`).

## 2. Clasificación: logística, regularización, LDA, Naive Bayes

- **Material:** cap. 4 de ESL en `books/explained/cap4_metodos_lineales_clasificacion.ipynb` (§4.3 LDA/QDA, §4.4 logística, §4.4.4 logística L1). ESL §4.3, §4.4. Naive Bayes: no está en el capítulo armado (**verificar** dónde lo ubica la cátedra). Enfoque generativo vs discriminativo: Bishop §1.5.4 (en la tabla de bibliografía).
- 🧮 Log-verosimilitud logística, su gradiente `Xᵀ(y − p)` y el Hessiano `−Xᵀ W X`; un paso de Newton como mínimos cuadrados ponderados (IRLS). 🧮 Frontera de decisión de LDA igualando posteriores con covarianza común (queda lineal). 🧮 Por qué logística + separabilidad perfecta diverge.
- 📌 Logística L1 (Lasso para clasificación); LDA vs logística (§4.4.5 en la notebook); Naive Bayes asume independencia condicional.
- ⚠️ Ajustar logística con mínimos cuadrados; creer que LDA necesita datos gaussianos *para usarse* (lo necesita para ser óptimo); que los coeficientes de logística se lean como en OLS (son log-odds).

## 3. Árboles y ensambles: Bagging, Random Forest, Boosting, XGBoost

- **Material:** sin notebook todavía. ESL §9.2 (árboles/CART), §8.7 (bagging), cap. 15 (random forests), cap. 10 (boosting). XGBoost: fuera de ESL (**verificar**).
- 🧮 (probable) Criterio de corte con Gini/entropía/RSS. 🧮 Por qué promediar `B` modelos reduce la varianza: `Var = ρσ² + (1−ρ)σ²/B`; es la fórmula que explica por qué random forest decorrelaciona.
- 📌 Boosting ajusta sobre residuos / gradientes; bagging vs boosting ataca varianza vs sesgo.
- ⚠️ Decir que bagging reduce el sesgo; creer que más árboles sobreajusta en random forest.

## 4. Evaluación: sesgo-varianza, nº efectivo de parámetros, CV, bootstrap

- **Material:** `src/notebooks/explained/1_intro_teoria_decision.ipynb` y `src/figuras/Bias-Variance.png` (ya hay intro). ESL §2.9 y §7.2–7.3 (sesgo-varianza), §7.10–7.11 (CV y bootstrap). Número efectivo de parámetros: ESL §7.6 (**verificar**); `df(λ)` de Ridge no aparece con ese nombre en la notebook de la clase 4 (**verificar**), pero se deduce de la SVD de la clase 3.
- 🧮 Descomposición `EPE(x₀) = σ² + Sesgo² + Var`. 🧮 `df` de Ridge desde la SVD (enlaza con la clase 3). 🧮 Por qué K-fold con K chico sesga y K grande tiene varianza alta.
- 📌 Bootstrap: muestreo con reemplazo, ~63,2 % de observaciones únicas por réplica.
- ⚠️ Estimar el error con el mismo conjunto en el que se seleccionó el modelo; hacer selección de variables *antes* de la CV.

## 5. No supervisado (bonus, pero se evalúa)

- **Material:** `notes/descomposicion-matrices-svd.md` y la clase 3 (SVD). ESL §14.5 (PCA), §14.3 (clustering). SVD → PCA enlaza directo con la clase 3.
- 🧮 PCA desde SVD (`X = UDVᵀ` centrada ⇒ componentes = columnas de `V`, varianzas `d_j²/N`) y desde la matriz de covarianza (autovectores de `XᵀX/N`): mostrar que dan lo mismo.
- 📌 K-means: alterna asignación y centroides, converge a mínimo local; clustering jerárquico: enlaces simple/completo/promedio. Reducción no lineal: saber cuál dio la cátedra (**a confirmar**).
- ⚠️ No centrar antes de PCA; no estandarizar cuando las escalas difieren; K-means sensible a la inicialización.

## Derivaciones en frío, en una lista

1. Un paso de Newton y su forma para logística (IRLS).
2. Gradiente y Hessiano de la log-verosimilitud logística.
3. Frontera de LDA (covarianza común).
4. `EPE = σ² + Sesgo² + Var`.
5. `Var` del promedio de `B` estimadores correlacionados.
6. `df(λ)` de Ridge con la SVD.
7. PCA: SVD ≡ autovectores de la covarianza.

Reglas de práctica: cada semana, derivar a mano **sin mirar** las de la clase del
momento; corregir con `/tutor corregir`; registrar en el diario.
