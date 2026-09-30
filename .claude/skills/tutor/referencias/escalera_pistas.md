# Escalera de pistas

Objetivo: que el alumno llegue solo al paso que le faltaba. Cada escalón da **lo
mínimo** para avanzar. Si con un escalón responde bien, no subas más.

| Escalón | Qué das | Ejemplo (Ej. 2 del 1P: pérdida absoluta) |
|---|---|---|
| 0. Diagnóstico | Una pregunta: "¿qué planteaste y dónde se trabó?" | "¿Qué escribiste como EPE? ¿Qué pasó al derivar?" |
| 1. Concepto | Qué herramienta de la clase aplica y por qué | "Acordate de cómo se minimizó el EPE con pérdida cuadrática: punto a punto, con `c = f(x)` fijo." |
| 2. Primer paso | El planteo inicial, sin el cálculo | "Escribí `g(c) = E[\|Y-c\| \| x]` como integral y partila donde `y` cruza a `c`." |
| 3. Esqueleto | La derivación con huecos para completar | "`g'(c) = ∫_{-∞}^{c} ___ − ∫_{c}^{∞} ___ = 2F(c) − ___`" |
| 4. Resolución | Derivación completa, corta | Solo si la pide o tras dos intentos fallidos. |

## Reglas

- **Una pregunta por vez.** Nada de cuestionarios.
- **Reconocé lo que está bien antes de corregir.** El alumno suele tener el instinto
  correcto y falla en el último paso (derivar e igualar a 0 en el Ej. 5; "no derivable"
  en el Ej. 2). Decílo: es información sobre qué reforzar.
- **Si se traba en álgebra, no en concepto**, salteá al escalón 3 para esa parte:
  el concepto ya lo tiene.
- **Dos formas de ver lo mismo.** Cuando el camino formal es pesado, ofrecé la
  versión intuitiva (por ejemplo, el argumento de perturbación `δ` para la mediana) y
  después mostrá que coincide con la formal.
- **Hipótesis ocultas.** Las derivaciones del examen esconden supuestos ("están
  estandarizadas ⇒ `xᵀx/N = 1`", "columnas centradas ⇒ `Σx = 0`"). Hacé que el alumno los
  nombre **antes** de la cuenta.
- **Cierre fijo**, en tres líneas:
  - **La señal:** qué dato del enunciado dispara la herramienta.
  - **Chequeo de 30 segundos:** cómo verificar la respuesta sin rehacer todo.
  - **Trampa:** la analogía equivocada típica (Ridge vs Lasso, media vs mediana).
