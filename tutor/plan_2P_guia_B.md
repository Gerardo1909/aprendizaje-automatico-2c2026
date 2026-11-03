# Plan para el 2do parcial: Guía B (mar 3/11 → vie 6/11)

Las derivaciones que importan quedan todas; lo que se corta son las cuentas largas.
Cada esquema da **la movida y la estructura con huecos**, no la resolución:
completala en hoja en blanco y contrastá **solo** con la sección *Resultados* de la guía.
Si te trabás: `tutor/movidas.md` → `/tutor duda` → notebook (una línea y la cerrás).

> Ensambles salió del temario. No supervisado entra pero no está en la guía: se lee
> por encima en `src/notebooks/explained/8_aprendizaje_no_supervisado.ipynb`
> (mapa, 🧰, "La idea en criollo" y 🧮).

---

## Martes: logística y Newton

### Ej. 9 a): solo la derivada de σ (M1)
- `1 − σ(z)` = poné todo sobre `1 + e^z` y multiplicá arriba y abajo por `e^{−z}`.
- `σ'(z)`: regla del cociente → separá en `σ · (algo)` y reconocé que el algo es `1 − σ`.
- La vas a usar en el 11 b).

### Ej. 11: log-verosimilitud, gradiente, Hessiano (M10, M1) 🧮
- **a)** `log P(yᵢ|xᵢ) = yᵢ log pᵢ + (1−yᵢ) log(1−pᵢ)`. Reagrupá como `yᵢ log(pᵢ/(1−pᵢ)) + log(1−pᵢ)`.
  El primer log es `____` (9 a), el segundo es `−log(1 + ____)`. Sumá en `i` (M10: el log convierte el producto en suma).
- **b)** Derivá término a término respecto de `β`:
  `∂/∂β log(1 + e^{βᵀx}) = ____ · x`. Para el Hessiano: `∂pᵢ/∂β = ____ · xᵢ` (regla de la cadena + 9 a).
  Dimensiones: el gradiente es un vector `(p+1)×1` y el Hessiano una matriz `(p+1)×(p+1)`; `xᵢxᵢᵀ` es un producto exterior.
- **c)** `vᵀ xᵢ xᵢᵀ v = (____)²`. ¿Qué signo tiene `pᵢ(1−pᵢ)`? ⇒ la función es cóncava ⇒ ¿cuántos máximos?
- **d)** La primera coordenada de `xᵢ` es 1 ⇒ la primera ecuación es `Σ(yᵢ − pᵢ) = 0`. ¿Qué dice en palabras?
  Solo intercepto ⇒ todos los `pᵢ` son iguales ⇒ `p = ____` ⇒ `β̂₀ = logit(____)`.
- **e)** Escribí `−ℓ` usando la forma de a) *antes* de reagrupar.

### Ej. 13 b) (y c)): Newton sobre `g'` (M9). Es tu error del diario.
- Optimizar = buscar la raíz de `g'`. Escribí `g'` y `g''`.
- Paso: `x_{n+1} = x_n − g'(x_n)/g''(x_n)` → simplificá hasta `2x_n − x_n²`.
- Restale 1 a los dos lados y factorizá: aparece un cuadrado ⇒ el error se ____ en cada paso (convergencia cuadrática).
- c) Desde `x₀ = 2`, ¿dónde cae `x₁`? ¿Está en el dominio?

### Ej. 14 a, b, d): un paso de Newton = IRLS (M9, M1) 🧮
- **a)** Es el 11 b) en 1D y sin intercepto: `ℓ' = Σ xᵢ(yᵢ − pᵢ)`, `ℓ'' = −Σ ____`.
- **b)** En `β = 0`, todos los `pᵢ = ____`. Calculá `ℓ'(0)` y `ℓ''(0)` y después `β¹ = 0 − ℓ'/ℓ''`.
- **d)** `wᵢ = pᵢ(1−pᵢ)`, `zᵢ = 0 + (yᵢ − pᵢ)/wᵢ`. Mínimos cuadrados ponderados en 1D sin intercepto:
  derivá `Σ wᵢ(zᵢ − βxᵢ)²` e igualá a 0 (M1) ⇒ `β = Σwᵢxᵢzᵢ / Σwᵢxᵢ²`. Tiene que darte lo mismo que en b).
- Saltá c).

### Ej. 15 a, c, d): separabilidad y regularización
- **a)** Con `y = (0,0,1,1)` el signo de `xᵢ` predice `yᵢ`. Cuando `β → ∞`, ¿a qué tiende cada `pᵢ`? ¿Y cada término de `ℓ`?
  Ojo: `ℓ < 0` siempre ⇒ el supremo es 0, pero no se alcanza ⇒ ¿existe el estimador de MV?
- **c)** Agregale `−2λβ` al gradiente y `−2λ` al Hessiano. Argumento: ahora `ℓ − λβ² → ____` cuando `|β| → ∞`
  y es estrictamente cóncava ⇒ hay un único máximo.
- **d)** `|β|` en 0 → M7. ¿Qué le falta a Newton?

---

## Miércoles: Bayes y LDA

### Ej. 3 a, b, c): frontera de Bayes en 1D (M3, M1)
- **a)** Bayes ⇒ `argmax_k πₖ fₖ(x)` (M3: se decide punto por punto). Tomá log y **tachá lo que es igual en las dos clases**
  (la constante de la gaussiana y el término `____`, porque `σ²` es común). Lo que queda es `δₖ`.
- **b)** `δ₁ = δ₂` es lineal en `x` → despejá. Separá `(μ₁²−μ₂²) = (μ₁−μ₂)(μ₁+μ₂)`.
- **c)** Reemplazá. ¿El término del log empuja hacia `μ₁` o hacia `μ₂`? Pensalo como "la clase más probable gana terreno".
- (d) sale mirando b): `σ²` multiplica al log.

### Ej. 5 a, b, d, e): LDA en `p` dimensiones (M3) 🧮
- **a)** `log P(k|x)/P(l|x) = log fₖ/f_l + log πₖ/π_l`. ¿Por qué no aparece `p(x)`?
  Al expandir las gaussianas, se cancelan dos cosas **solo porque `Σₖ = Σ`**: `____` y `____`.
- **b)** Expandí `(x−μₖ)ᵀΣ⁻¹(x−μₖ) = xᵀΣ⁻¹x − 2____ + ____` (usá que `Σ⁻¹` es simétrica). Tachá `xᵀΣ⁻¹x` → queda lineal → `δₖ`.
- **c)** Lo que en a) se cancelaba por `Σ` común ahora queda: `−½ log|Σₖ|` y la forma cuadrática completa.
- **d)** Contá: priors `K−1`, medias `K·p`, una matriz simétrica `p×p` tiene `p(p+1)/2` parámetros (LDA tiene una, QDA tiene `K`).
  Logística: `K−1` vectores de `p+1`.
- **e)** Generativo = modela `p(x, g)`. Para generar datos sintéticos: primero `g ~ ____`, después `x | g ~ ____`. ¿La logística modela `p(x)`?

### (Si sobra) Ej. 7 c): Mahalanobis = euclídea esferizada (M5)
- `x* = D^{−1/2}Uᵀx` ⇒ `‖x* − μ*‖² = (x−μ)ᵀ U D^{−1} Uᵀ (x−μ) = (x−μ)ᵀ ____ (x−μ)`.

---

## Jueves: evaluación y papers

### Ej. 18: estimador encogido (M4, M2, M1)
- **a)** `μ̂_λ = aᵀY` con `a = 1/(N+λ) · 𝟏` (lineal en `Y` ⇒ M4).
  `E[μ̂_λ] = ____ μ` ⇒ sesgo `= E[μ̂] − μ`. `Var = σ²‖a‖² = ____`.
- **b)** ECM = sesgo² + var (es M2 con centro `b = E[μ̂]`: ¿por qué muere el cruzado?).
- **c)** Mirá los límites de cada término.
- **d)** Derivá el ECM respecto de `λ` e igualá a 0 (M1). Ayuda: el denominador `(N+λ)²` es común, así que trabajá el numerador.
  ¿Depende de algo que no conocés?

### Ej. 19 a, b, d): sesgo-varianza y df (M2, M3, M4, M5) 🧮
- **a)** Dos veces M2 (con `x₀` fijo, M3):
  1. `Y − f̂ = (Y − f(x₀)) + (f(x₀) − f̂)`. El cruzado muere porque `ε` es ____ del conjunto de entrenamiento y tiene media 0 ⇒ `σ²_ε + E(f(x₀) − f̂)²`.
  2. `f(x₀) − f̂ = (f(x₀) − Ef̂) + (Ef̂ − f̂)`. El primer paréntesis es ____ y el segundo tiene esperanza ____ ⇒ sesgo² + varianza.
  **Escribí la justificación de cada cruzado: es lo que se evalúa.**
- **b)** M4: `Var(hᵀy) = hᵀ Cov(y) h`. Supuestos: `X` fija, `Cov(y) = ____`.
- **d)** Reemplazá en `Σ d_j²/(d_j² + α)`. ¿Qué factor se va a 0 primero cuando `α` crece: el de `d_j` grande o el de `d_j` chico?

### Ej. 22 + 23: qué está mal + papers (sin cuentas, unos 20 min)
Plantilla para cada escenario del 22: **problema** (fuga / double dipping / sesgo por elegir el máximo / record-wise / p-hacking) →
**optimista o pesimista** → **arreglo** (selección dentro del fold, CV anidada / test intocado, GroupKFold, preregistro, preprocesar solo con train).
Los papers no están en ninguna notebook: la fuente es *Resultados* 22–23. Para asignar autores alcanza con
**Saeb** = record-wise vs subject-wise · **Ball** = double dipping / random data test · **Simmons** = grados de libertad del investigador.

### Jueves a la noche
Sin mirar nada, rehacé **11 b)** y **5 b)**.

---

## Prioridad 2 (solo si sobra tiempo)
- **2 b, c**: masking; `Σₖ f̂ₖ = 1` sale de `Σₖ Yₖ = 𝟏` y de que la proyección es lineal y deja fijo a `𝟏` (por el intercepto). Repasa la entrada del diario de ESL 4.2.
- **21 c, d**: `ȳ₍₋ᵢ₎ = (Nȳ − yᵢ)/(N−1)` → restáselo a `yᵢ` y simplificá.
- **12 b, c**: log-odds del softmax = diferencia de los coeficientes ⇒ solo la diferencia es identificable.
- **20**: ¿qué está fijo (τ, los xᵢ) y qué es aleatorio en cada caso?

## Lo que salteás
1, 4, 6, 8, 10, 16, 17 y toda la Parte II. Leé solo las conclusiones de *Resultados* 1 c), 8 d) y 10 c).

## Para corregir
Pegá **11, 5 y 19** en `/tutor corregir`.
