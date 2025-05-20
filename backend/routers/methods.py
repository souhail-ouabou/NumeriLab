from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError
import math

router = APIRouter()

class BisectionInput(BaseModel):
    a: float
    b: float
    tol: float

@router.post("/api/bisection")
def bisection_method(data: BisectionInput):
    def f(x):
        return x**2 - 2  # Exemple simple

    a, b, tol = data.a, data.b, data.tol

    # Validation: tol must be positive
    if tol <= 0:
        raise HTTPException(status_code=400, detail="Tolerance (tol) must be positive.")

    # Validation: a and b must be different
    if a == b:
        raise HTTPException(status_code=400, detail="a and b must be different.")

    # Validation: f(a) and f(b) must have opposite signs
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise HTTPException(
            status_code=400,
            detail="Function must have opposite signs at a and b (f(a) * f(b) < 0)."
        )

    iterations = 0

    while (b - a) / 2 > tol:
        c = (a + b) / 2
        fc = f(c)
        if fc == 0:
            break
        elif fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        iterations += 1

    return {
        "root": (a + b) / 2,
        "iterations": iterations,
        "error": abs(b - a) / 2
    }
