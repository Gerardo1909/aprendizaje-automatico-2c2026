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
