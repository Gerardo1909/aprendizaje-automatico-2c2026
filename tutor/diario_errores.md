# Diario de errores

Lo mantiene el tutor (`/tutor corregir`, `/tutor diario`). Una entrada por error o laguna.
**Estados:** `pendiente` → `repasar` → `dominado (fecha)`.

**Formato:**

```
## <tema> — <fecha>
- Qué pasó:
- Causa: concepto | álgebra | hipótesis oculta | lectura del enunciado | no reconoció la herramienta
- Regla para reconocerlo:
- Estado:
```

---

## 1P Ej. 2 — pérdida absoluta ⇒ mediana — 2026-09-30
- Qué pasó: respondió "imposible porque el módulo no es derivable" y cerró ahí.
- Causa: concepto. No derivable en un punto ≠ no minimizable; hay que partir en tramos. Además, `E[|Y−c|]` **es** una integral.
- Regla para reconocerlo: pérdida absoluta ⇒ mediana, y la condición de óptimo es `P(Y≤c|x)=½`. Argumento sin integrales: correr `c` en `δ` cambia el costo en `δ·(P(Y<c) − P(Y>c))`; el óptimo equilibra las dos masas.
- Estado: pendiente

## 1P Ej. 4 — coordinate descent con predictores idénticos — 2026-09-30
- Qué pasó: eligió la opción correcta (el primero se lleva todo) pero no pudo justificarla; le costó el residuo parcial.
- Causa: hipótesis oculta. `xᵀx/N = 1` por estandarización ⇒ `a₂ = a − c = λ`, y soft-thresholding manda a 0 lo que no supera `λ`.
- Regla para reconocerlo: "barrido cíclico en ese orden + `β=0`" vuelve determinista el algoritmo. Residuo parcial = lo que **falta explicar** de `y` tras descontar a los demás. Ridge reparte, Lasso elige.
- Estado: pendiente

## 1P Ej. 5 — OLS con predictores estandarizados — 2026-09-30
- Qué pasó: derivó e igualó a 0 (correcto) pero no llegó a la fórmula; eligió la opción 2 por intuición de estadística inferencial. La resolución da la opción 5 (2 y 3).
- Causa: hipótesis oculta + álgebra. No usó `Σx = 0` (estandarizar ⇒ media 0 ⇒ suma 0) para desacoplar `β0` y no resolvió el 2×2 en `β1, β2`.
- Regla para reconocerlo: derivar e igualar a 0 **es** la ecuación normal `XᵀXβ = Xᵀy`. Que el enunciado defina `ρ` anticipa `1/(1−ρ²)`. `β0 = 0` si `y` viene centrado, `β0 = ȳ` si no; si hay ambigüedad, pensar en la opción que agrupa a las dos.
- Estado: pendiente

## ESL 4.2 — de E[Y|x]=posterior a "importa el orden, no el valor" — 2026-10-01
- Qué pasó: al leer la notebook del cap. 4, se perdió después de "¿Con qué justificación? Esperanza condicional": la pregunta "¿importa que los f̂_k sean posteriores?" queda abierta y las secciones siguientes (suman 1, objetivos t_k, masking) no parecen conectadas.
- Causa: concepto (falta el hilo) — en parte, defecto de la notebook, no solo del alumno.
- Regla para reconocerlo: Bayes ⇒ argmax del posterior; E(Y_k|x)=Pr(G=k|x) justifica el objetivo; OLS da la mejor aproximación lineal L2, no el posterior; para clasificar solo importa el ORDEN de los f̂_k, y se rompe cuando la aproximación lineal lo invierte (masking).
- Estado: pendiente

## Clase 6 §5 — para qué sirve descomponer Σ = UDUᵀ — 2026-10-07
- Qué pasó: leyó la descomposición espectral como un método para *estimar* las covarianzas de LDA/QDA, y la cuenta de la inversa y del determinante (celda 27 de la notebook explicada) no le dejó claro el objetivo.
- Causa: concepto (en parte, defecto de la notebook: la verificación aparece antes del motivo). La estimación es el plug-in de §4; la descomposición sirve para *usar* Σ̂ una vez estimada.
- Regla para reconocerlo: en los ejes de la elipse, Mahalanobis = Σ z_l²/λ_l y log|Σ| = Σ log λ_l. Para qué sirve: (1) geometría (|Σ| es el volumen² de la elipse, de ahí el −½log|Σ_k|), (2) estabilidad numérica (det directo da 0 o ∞ con p grande), (3) se ven los λ chicos que RDA levanta. No es más rápido que invertir: las dos cosas cuestan O(p³).
- Estado: pendiente

## Clase 6 §6 — Newton-Raphson aplicado a la derivada — 2026-10-08
- Qué pasó: leyó "aplicarlo a la derivada" como "hacer Newton sobre f''". Interpretó f'' como regla de parada (parar si el paso sube; converger cuando f''→0) y no vio cómo un método de raíces encuentra máximos/mínimos.
- Causa: concepto. El puente es "óptimo ⇒ f'=0": Newton se aplica a g=f', y f'' aparece solo porque es g' (la pendiente de la tangente). Se para cuando f'(x)≈0 (el paso se anula); f''≈0 es la zona peligrosa (vértice en el infinito), no el criterio de convergencia. El signo de f'' decide hacia qué tipo de punto crítico va, no si se frena.
- Regla para reconocerlo: "optimizar con Newton" = "Newton de raíces sobre el gradiente". Reemplazá f→f', f'→f''. En varias variables: f'→∇f, f''→H.
- Estado: pendiente

## PCA (ESL 14.5) — lagunas de base al leer la derivación — 2026-10-10
- Qué pasó: al leer §1–§2 del notebook de PCA no pudo seguir cuatro pasos: por qué cada $\lambda_i$ se optimiza por separado, la regla $\partial_b\|a-Mb\|^2=-2M^T(a-Mb)$, por qué $\mathbf V_q\mathbf V_q^T$ es una proyección, y los multiplicadores de Lagrange (nunca los vio).
- Causa: no reconoció la herramienta (en los tres primeros: es la ecuación normal y la matriz hat de la clase 2 con $\mathbf X^T\mathbf X=I$) + concepto (Lagrange).
- Regla para reconocerlo: "optimizar con restricción de igualdad" ($\|v\|=1$) ⇒ Lagrange ⇒ $\nabla f=\gamma\nabla g$; con $f=v^TAv$ da $Av=\gamma v$ y el objetivo vale $\gamma$. "Suma de términos que no comparten incógnitas" ⇒ se minimiza cada uno por separado. "$\mathbf V\mathbf V^T$ con columnas ortonormales" ⇒ matriz hat.
- Estado: pendiente (repasar con la derivación en frío de PCA: Pitágoras → forma cuadrática → Lagrange → autovector)

## PCA — qué representa V de la SVD (puente con clase 3) — 2026-10-20
- Qué pasó: entendía que V "pondera" las variables en los scores, pero no por qué *esa* V; seguía la derivación por Lagrange del cap14_5 sin conectarla con el "rotar–estirar–rotar" de la clase 3. (Antes: confundía qué se permuta en la línea base; se aclaró que se mezclan valores dentro de cada columna de Z, no los scores.)
- Causa: no reconoció la herramienta. Es la misma SVD de la clase 3 §5 leída sobre la matriz de datos.
- Regla para reconocerlo: ‖Zw‖² = Σᵢ(zᵢᵀw)² = N·var(proyección sobre w) ⇒ "cuánto estira Z a w" = "cuánto se dispersan los países sobre w". v₁ = dirección de máximo estiramiento = PC1. De Z = UDVᵀ sale ZV = UD (scores) y Z = (UD)Vᵀ (reconstrucción): la fila k de V da el peso de la variable k en cada componente, y también de cada componente en la variable k.
- Estado: pendiente
## PCA (ESL 14.5) §1 — la búsqueda por ángulos vs. la SVD — 2026-10-15
- Qué pasó: al leer la celda 6 (búsqueda en grilla de θ) creyó que $(\cos\theta,\sin\theta)$ tenía que salir de la SVD, y no distinguió "probar todos los candidatos" de "la fórmula cerrada". También dudó de si `mean(0)`/`std(0)` estandarizan por columna.
- Causa: concepto (parametrizar la restricción $\|v\|=1$ en 2D) + lectura de numpy (`axis=0` = un valor por columna).
- Regla para reconocerlo: en $\mathbb R^2$, "vector unitario" ⇔ $(\cos\theta,\sin\theta)$; barrer θ es fuerza bruta sobre el mismo problema que la SVD resuelve de una (§2). Recta por el origen en dirección $v$ = $\{t\,v\}$, con $t$ haciendo de $\lambda$; pie de la perpendicular = $(v^Tx)\,v = Hx$.
- Estado: pendiente
## PCA (ESL 14.5) §2 Paso 3 — Vᵀv_j = e_j, D²e_j y el camino de la covarianza — 2026-10-22
- Qué pasó: leyó $v_j$ como "un vector unitario cualquiera que se multiplica a derecha" (no como la columna $j$ de $\mathbf V$), no vio por qué $\mathbf D^2e_j=d_j^2e_j$, y creyó que la SVD era una solución distinta de "autovectores de la covarianza $\mathbf X^T\mathbf X/N$".
- Causa: concepto (producto matriz × vector canónico = sacar una columna) + falta el hilo (Lagrange ya da la respuesta; la SVD solo la calcula).
- Regla para reconocerlo: $\mathbf A e_j$ = columna $j$ de $\mathbf A$; $\mathbf V^Tv_j$ = productos punto de $v_j$ con cada columna ⇒ $e_j$ solo porque $v_j$ ES una de ellas. Problema → Lagrange → autovectores de $\mathbf X^T\mathbf X$ (= de la covarianza, dividir por $N$ no mueve autovectores) → la SVD de $\mathbf X$ los entrega sin formar $\mathbf X^T\mathbf X$.
- Estado: pendiente

## Clase 7 §3 — de dónde salen sesgo², varianza y el "integrar contra p(x)" — 2026-10-25
- Qué pasó: siguió §1–§2 (selección con suerte, EPE ⇒ E[Y|x]) pero en §3 no vio de dónde salían $(\hat f-f)^2$ y $\mathrm{Var}(Y\mid x)$ tras tomar esperanza, ni a qué $p(x)$ se refería "integrando contra $p(x)$".
- Causa: concepto (falta el hilo) — sobre todo defecto de la notebook: el truco de sumar y restar y la integral del EPE estaban dichos en palabras, sin escribir. Se reescribieron §3–§6.
- Regla para reconocerlo: "sumar y restar un centro $b$" ⇒ $(a-c)^2=(a-b)^2+(b-c)^2+2(a-b)(b-c)$, y el cruzado muere si un factor es constante y el otro tiene esperanza 0. Con $b=f(x)=E[Y\mid x]$ sale el irreducible ($E[(Y-f)^2\mid x]$ ES la varianza); con $b=\bar f=E_\tau[\hat f]$ salen varianza + sesgo². "Integrar contra $p(x)$" = promediar en $x$ el resultado puntual (Paso 1 de la §2).
- Estado: pendiente (repasar: derivar en frío $Err(x_0)=\sigma^2+\text{sesgo}^2+\text{var}$ diciendo por qué muere cada cruzado)
