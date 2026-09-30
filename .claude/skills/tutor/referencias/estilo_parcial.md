# Cómo es un parcial de esta cátedra (1er parcial 2C 2026)

Fuente: `exams/1_P/explained/1_P.ipynb` (fotos en `exams/1_P/raw/`). Son **7 ejercicios**.
Cada uno toma una herramienta vista en clase y le pone un giro.

| Ej. | Formato | Herramienta | Giro |
|---|---|---|---|
| 1 | V/F de 8 identidades, con cálculo si es falso | SVD (clase 3) | `D` no conmuta; `D=diag(3,½)` por convención, no por el enunciado |
| 2 | Derivar y nombrar el estadístico (4 incisos) | EPE (clase 1) | Pérdida absoluta: no derivable en un punto ⇒ derivar por tramos ⇒ mediana |
| 3 | Elegir parámetros de un aumento de datos + una línea teórica | Ridge por datos aumentados (clase 4) | Se pierde el cuadrado: `a² = λ`, no `a = λ` |
| 4 | Opción múltiple, una sola correcta | Coordinate descent (clase 5) | Predictores idénticos + orden fijo ⇒ determinista; el primero absorbe todo |
| 5 | Opción múltiple con combinaciones ("2 y 3") | OLS + estandarización (clases 2 y 4) | Invertir un 2×2 con `ρ`; `β0` según `y` centrado o no |
| 6 | Completar identidades + respuestas de una palabra | Predictores ortogonales (clases 2–5) | `XᵀX = nI`; Ridge escala, Lasso recorta |
| 7 | Asignar afirmaciones a autores | Breiman / Donoho / Efron (sin clase) | Lectura de papers, no de las notebooks |

## Patrones que se repiten

1. **Una herramienta conocida + un giro.** Casi nunca es un ejercicio idéntico al de
   clase. El giro cambia una hipótesis (pérdida, orden, duplicados, normalización).
2. **El resultado de la clase no alcanza; hay que derivar un paso que la clase no
   derivó.** En el Ej. 2 la clase enuncia "mediana" sin deducir `P(Y≤c|x)=½`. En el
   Ej. 5 la clase no invierte el bloque 2×2.
3. **Hipótesis escondidas en el enunciado.** "Estandarizado", "centrado", "desvío
   dividiendo por n", "barrido cíclico en ese orden", "suponiendo peso no nulo". Cada una
   simplifica una cuenta. Hay que **leerlas como datos**, no como decoración.
4. **Distractores por analogía equivocada.** Ridge vs Lasso (repartir `c/3`),
   estandarizar ⇒ independientes, "la media" por inercia, "cualquiera" porque el mínimo
   no es único.
5. **Cálculos cortos.** Cada ejercicio se resuelve en 10–15 minutos si se reconoce la
   herramienta. Si la cuenta se vuelve larga, probablemente falta una hipótesis oculta.
6. **Sin gráficos ni código.** Todo a mano.
7. **Respuestas cortas pedidas de forma explícita** ("una sola palabra", "una línea").
   Se puntúa la idea correcta, no el desarrollo.
8. **Un ejercicio de cultura/lectura** (Ej. 7) fuera del material de clase.

## Cómo usar esto al generar un ejercicio

- Elegí una herramienta del tema y **cambiá una hipótesis**.
- Incluí al menos una **hipótesis oculta** que simplifique la cuenta y que el alumno
  tenga que nombrar.
- Incluí un **distractor por analogía equivocada** si el formato es opción múltiple.
- Que se resuelva a mano en 10–15 minutos.
- Escribí "Cómo reconocerlo" con las tres líneas: **La señal**, **Chequeo**, **Trampa**.
