from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import math

router = APIRouter()

# === Shared model ===
class RootFindingInput(BaseModel):
    a: float = Field(default=None)
    b: float = Field(default=None)
    x0: float = Field(default=None)
    tol: float = Field(..., gt=0, description="Tolerance must be greater than 0.")

# === f(x) and derivative ===
def f(x): return x**2 - 2
def df(x): return 2 * x

# === Bisection ===
@router.post("/api/bisection")
def bisection_method(data: RootFindingInput):
    a, b, tol = data.a, data.b, data.tol
    if a is None or b is None:
        raise HTTPException(status_code=400, detail="Inputs 'a' and 'b' are required.")
    if a == b:
        raise HTTPException(status_code=400, detail="a and b must be different.")
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise HTTPException(status_code=400, detail="f(a) and f(b) must have opposite signs.")

    iterations = 0
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        fc = f(c)
        if fc == 0:
            break
        elif fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        iterations += 1

    return {"root": (a + b) / 2, "iterations": iterations, "error": abs(b - a) / 2}

# === Newton-Raphson ===
@router.post("/api/newton")
def newton_method(data: RootFindingInput):
    x = data.x0
    tol = data.tol
    if x is None:
        raise HTTPException(status_code=400, detail="Input 'x0' is required.")

    iterations = 0
    while True:
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise HTTPException(status_code=400, detail="Zero derivative encountered.")
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            break
        x = x_new
        iterations += 1

    return {"root": x_new, "iterations": iterations, "error": abs(f(x_new))}

# === Secant Method ===
@router.post("/api/secant")
def secant_method(data: RootFindingInput):
    x0, x1, tol = data.a, data.b, data.tol
    if x0 is None or x1 is None:
        raise HTTPException(status_code=400, detail="Inputs 'a' and 'b' are required for Secant method.")

    iterations = 0
    while abs(x1 - x0) > tol:
        f0, f1 = f(x0), f(x1)
        if f1 - f0 == 0:
            raise HTTPException(status_code=400, detail="Division by zero due to equal function values.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
        iterations += 1

    return {"root": x1, "iterations": iterations, "error": abs(f(x1))}

# === False Position ===
@router.post("/api/false-position")
def false_position_method(data: RootFindingInput):
    a, b, tol = data.a, data.b, data.tol
    if a is None or b is None:
        raise HTTPException(status_code=400, detail="Inputs 'a' and 'b' are required.")
    if a == b:
        raise HTTPException(status_code=400, detail="a and b must be different.")
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise HTTPException(status_code=400, detail="f(a) and f(b) must have opposite signs.")

    iterations = 0
    while abs(b - a) > tol:
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        if fc == 0:
            break
        elif fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        iterations += 1

    return {"root": c, "iterations": iterations, "error": abs(f(c))}

# === Fixed Point Iteration ===
@router.post("/api/fixed-point")
def fixed_point_method(data: RootFindingInput):
    x = data.x0
    tol = data.tol
    if x is None:
        raise HTTPException(status_code=400, detail="Input 'x0' is required.")

    def g(x): return (x + 2 / x) / 2  # Example g(x) for sqrt(2)

    iterations = 0
    while True:
        try:
            x_new = g(x)
        except ZeroDivisionError:
            raise HTTPException(status_code=400, detail="Division by zero during iteration.")
        if abs(x_new - x) < tol:
            break
        x = x_new
        iterations += 1

    return {"root": x_new, "iterations": iterations, "error": abs(f(x_new))}
