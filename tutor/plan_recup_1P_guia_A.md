# Plan para el recuperatorio del 1P: Guía A (dom 8/11 → vie 13/11)

Mismo método que la Guía B: cada esquema te da **la movida y la estructura con huecos**,
no la resolución. Lo completás en hoja en blanco y lo contrastás **solo** con *Resultados*.
Si te trabás: `tutor/movidas.md` → `/tutor duda` → notebook (una línea y la cerrás).

## La idea: el recuperatorio va a tener los mismos 7 casilleros que el 1P

La guía está armada en espejo del 1P. Cada ejercicio del parcial tiene su "remedio":

| 1P | Tema | Remedio en la guía | ¿Falló? (diario) | Giro probable en el recuperatorio |
|---|---|---|---|---|
| Ej. 1 | SVD, V/F | **2** (+1 d) | no | otra X, signos de U cambiados, `X⁻¹ = VD⁻¹Uᵀ` |
| Ej. 2 | pérdida absoluta ⇒ mediana | **4** a–c, **3** | **sí** | pinball `τ` (4 d), Y discreta con empate en ½ |
| Ej. 3 | Ridge por datos aumentados | **15** a, b | no | `λⱼ` distinto por coordenada ⇒ `aⱼ = √λⱼ` |
| Ej. 4 | coordinate descent con clones | **17** a → **18** b, f (+14 a) | **sí** | otro orden/inicio, Elastic Net con clones, `xᵀx/N ≠ 1` |
| Ej. 5 | 2×2 con ρ | **9** a–c, e (+13) | **sí** | otro par correlacionado, `Var(β̂₁+β̂₂)`, divisor `N−1` |
| Ej. 6 | ortogonales | **19** a, b, e, f, g | no | normalización `xᵀx = 1` en vez de `N` |
| Ej. 7 | papers | **21** | no | afirmaciones que mezclan dos autores |

Los 2,5 puntos que te faltan están en las tres filas marcadas **sí**: salen de M1, M6 y M7.
Las otras cuatro hay que **asegurarlas**, no aprenderlas.

**Se saltea:** 5, 6, 7 c/e, 8, 10, 11 c, 12 b, 16, 20 y toda la Parte II (el parcial es a
mano, sin código). Son buenos ejercicios, pero no entran en ningún casillero del 1P. El 7 (a, b, d)
y el 16 (a, b) quedan como extra si te sobra tiempo: son M1/M5 y M2.

## Notas sobre la guía (verificada con numpy, ej. por ej.)

Ningún resultado numérico está mal. Ojo con tres redacciones:

- **Ej. 2, nota final:** dice "no necesariamente en orden decreciente". La convención es
  **decreciente**. En el 1P el enunciado listaba "½ y 3" en un orden que no cerraba, y lo
  que manda es que `UDVᵀ = X` con las U y V dadas.
- **Ej. 15 b:** el "β₀" es un **vector objetivo** de p componentes, no el intercepto:
  `ỹ = (y; √λ·β₀)`.
- **Ej. 21:** no hay papers en el repo; la clave del 1P también salió de memoria. Las
  afirmaciones dudosas son la **3** (Efron por "superficie más ruido", pero suena a Breiman),
  la 2 y la 7. Si podés, leé un resumen de una carilla de cada paper.

---

## Domingo 8: la mediana (diario: 1P Ej. 2) — M3, M7

### Ej. 4 a–c 🧮 (en frío, 25 min)
- **a)** `EPE = E_X[ ____ ]`. ¿Por qué alcanza con minimizar adentro para cada `x`? (M3, una línea).
- **b)** `E[|Y−c| | x] = ∫_{y<c} (____) p(y|x) dy + ∫_{y>c} (____) p(y|x) dy`.
  Derivá cada tramo respecto de `c` (el integrando ya no tiene módulo).
  Queda `P(Y<c|x) − P(Y>c|x) = 0` ⇒ `F(c) = ____`.
- **Sin integrales:** corré `c` un `δ`. ¿Cuánto paga cada punto de la izquierda? ¿Y de la derecha?
- **d) (el giro probable):** lo mismo con pesos `τ` y `1−τ` ⇒ `F(c) = ____`.

### Ej. 3 a–c (20 min)
- Es el 4 con números. Para la mediana discreta: el primer valor donde la acumulada **llega a ½**.
- Cada EPE, **con su propia pérdida**. Promediá las dos celdas con `P(X) = ½`.

## Lunes 9: los clones (diario: 1P Ej. 4) — M7, M6

### Ej. 17 a 🧮 (12 min)
- Tres tramos: `β > 0` (derivás: `β = a − ____`, vale si `a > ____`), `β < 0` (simétrico), y si ninguno vale ⇒ `β = 0`.
- Juntalo en `S(a, λ) = sign(a)(|a| − λ)₊`. Dibujalo junto a `a/(1+λ)` (17 c): Lasso **recorta**, Ridge **escala**.

### Ej. 14 a (8 min) — antes del 18, para el contraste
- Por simetría `β₁ = β₂ = b`. Costo: `‖y − ____ b x‖² + ____ λ b²` (son **dos** penalidades). Derivá.
- Ridge **reparte**. ¿Cuánto vale la suma? Compará con el 13.

### Ej. 18 b, f 🧮 (25 min) — es exactamente donde te rompiste
- Hipótesis oculta (M6): `x` estandarizado ⇒ `xᵀx/N = ____`. Por eso la actualización es solo `S(a, λ)`.
- **β₁:** con `β = 0`, el residuo parcial es `r⁽¹⁾ = y`, así que `a₁ = ____` ⇒ `β₁ = S(____, λ) = ____`.
- **β₂:** el residuo parcial ahora descuenta lo que ya explicó `β₁`: `r⁽²⁾ = y − x β₁`.
  `a₂ = (1/N)xᵀy − β₁ · ____ = ____`. ¿Qué devuelve `S(a₂, λ)`?
- **β₃:** idéntico. **Segundo barrido:** ¿cambia algo?
- **f)** En una frase: "el primero que se actualiza se lleva todo porque ____".
- **Repetí al toque con otro orden (18 c).**

## Martes 10: el 2×2 con ρ (diario: 1P Ej. 5) — M1, M6

### Ej. 9 a, b, e 🧮 (20 min)
- **Antes de mirar el `XᵀX` del enunciado:** escribí el RSS, derivá respecto de `β₀, β₁, β₂`
  e igualá a 0 (M1). Esas tres ecuaciones **son** `XᵀXβ = Xᵀy`. Este paso es el que el
  ejercicio te da armado, y es el que te faltó en el parcial.
- Usá `Σxᵢⱼ = ____` y `Σxᵢⱼ² = ____` (M6): la ecuación de `β₀` se despega sola ⇒ `β₀ = ____`.
- Lo que queda: `N[[1, ρ],[ρ, 1]] (β₁, β₂)ᵀ = (Σx₁y, Σx₂y)ᵀ`. Inversa del 2×2: `1/det · [[d, −b],[−c, a]]`, con `det = ____`.
- **e)** La primera fila del 2×2 dividida por N: `β₁ + ρβ₂ = ____`. ¿Qué es el lado derecho? (Sin cuentas nuevas).
- **c)** M4: `Var = σ² · [(XᵀX)⁻¹]₁₁ = ____`.

### Ej. 13 a (5 min) — Ridge 1D 🧮
- Derivá e igualá a 0. Después reemplazá `xᵀx` por `N`: aparece `N/(N+λ)`, el factor del 19 e.

### Ej. 19 a, b, e, f (20 min) — el 1P Ej. 6, asegurarlo
- `XᵀX = ____ · I` ⇒ todo es dividir por eso. La trampa es poner 1 en vez de `N`.
- **e)** Ridge (sin `1/2N`) vs **f)** Lasso (con `1/2N`): escribí los dos costos lado a lado antes de derivar.
- **g)** como chequeo numérico (5 min).

## Miércoles 11: simulacro + los casilleros "seguros"

- **Mañana (45 min):** Ej. 2 (SVD, V/F) y Ej. 15 a, b (aumentados: `a² = λ`, `b = 0` para que muera el cruzado). Sin mirar.
- **Tarde: simulacro cronometrado, 7 ejercicios, 1 por casillero, con giro.** Pedilo con
  `/tutor practica simulacro_recup`: te armo ejercicios **nuevos**, no los de la guía.
  Corregí con `/tutor corregir` y lo que falle va al diario.

## Jueves 12: repaso en frío, liviano

- Rederivá **sin mirar** el 4 b (del domingo), el 18 b (del lunes) y el 9 b (del martes).
  Con 3–4 días de distancia es la prueba 3 del criterio de "estudiado": si salen, las
  entradas del diario pasan de estado.
- Ej. 21 (15 min): tres palabras clave por autor. Breiman: Rashomon, dos culturas, 98 %/2 %.
  Donoho: Tukey 1962, Common Task Framework, "ciencia de la ciencia de datos".
  Efron: superficie + ruido, predicción vs. estimación vs. atribución, concept drift.
- **Nada nuevo después de las 20 h. Dormir.**

---

**Si te atrasás, este es el orden de prioridad:** 4 → 18 → 9 → 19 → 2 → 15 → 3 → 21.
