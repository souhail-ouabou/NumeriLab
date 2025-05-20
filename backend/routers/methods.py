from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import math

router = APIRouter()

# === Shared model ===
class RootFindingInput(BaseModel):
    a: float = None
    b: float = None
    x0: float = None
    tol: float

# === f(x) and derivative (for some methods) ===
def f(x): return x**2 - 2
def df(x): return 2*x  # for Newton

# === Bisection ===
@router.post("/api/bisection")
def bisection_method(data: RootFindingInput):
    a, b, tol = data.a, data.b, data.tol
    fa, fb = f(a), f(b)
    if tol <= 0 or a == b or fa * fb > 0:
        raise HTTPException(status_code=400, detail="Invalid input for Bisection.")

    iterations = 0
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        fc = f(c)
        if fc == 0: break
        elif fa * fc < 0: b, fb = c, fc
        else: a, fa = c, fc
        iterations += 1

    return {"root": (a + b) / 2, "iterations": iterations, "error": abs(b - a) / 2}

# === Newton-Raphson ===
@router.post("/api/newton")
def newton_method(data: RootFindingInput):
    x = data.x0
    tol = data.tol
    if x is None or tol <= 0:
        raise HTTPException(status_code=400, detail="x0 and tol required.")

    iterations = 0
    while True:
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise HTTPException(status_code=400, detail="Derivative zero.")
        x_new = x - fx / dfx
        if abs(x_new - x) < tol: break
        x = x_new
        iterations += 1

    return {"root": x_new, "iterations": iterations, "error": abs(f(x_new))}

# === Secant Method ===
@router.post("/api/secant")
def secant_method(data: RootFindingInput):
    x0, x1, tol = data.a, data.b, data.tol
    if x0 is None or x1 is None or tol <= 0:
        raise HTTPException(status_code=400, detail="x0, x1, tol required.")

    iterations = 0
    while abs(x1 - x0) > tol:
        f0, f1 = f(x0), f(x1)
        if f1 - f0 == 0:
            raise HTTPException(status_code=400, detail="Division by zero.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
        iterations += 1

    return {"root": x1, "iterations": iterations, "error": abs(f(x1))}

# === False Position ===
@router.post("/api/false-position")
def false_position_method(data: RootFindingInput):
    a, b, tol = data.a, data.b, data.tol
    fa, fb = f(a), f(b)
    if tol <= 0 or a == b or fa * fb > 0:
        raise HTTPException(status_code=400, detail="Invalid input for False Position.")

    iterations = 0
    while abs(b - a) > tol:
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        if fc == 0: break
        elif fa * fc < 0: b, fb = c, fc
        else: a, fa = c, fc
        iterations += 1

    return {"root": c, "iterations": iterations, "error": abs(f(c))}

# === Fixed Point Iteration ===
@router.post("/api/fixed-point")
def fixed_point_method(data: RootFindingInput):
    x = data.x0
    tol = data.tol
    if x is None or tol <= 0:
        raise HTTPException(status_code=400, detail="x0 and tol required.")

    def g(x): return (x + 2 / x) / 2  # Example: sqrt(2) => g(x) = 0.5(x + 2/x)

    iterations = 0
    while True:
        x_new = g(x)
        if abs(x_new - x) < tol: break
        x = x_new
        iterations += 1

    return {"root": x_new, "iterations": iterations, "error": abs(f(x_new))}
