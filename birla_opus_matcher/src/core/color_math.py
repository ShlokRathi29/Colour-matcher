from __future__ import annotations

import numpy as np


# ---------- RGB -> XYZ -> LAB (D65) ----------

def _srgb_to_linear(c: float) -> float:
    c = c / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def rgb_to_lab(r: int, g: int, b: int) -> tuple[float, float, float]:
    """
    Convert sRGB (0-255) to CIE Lab (D65/2°).
    Deterministic, no external dependencies.
    """
    rl = _srgb_to_linear(r)
    gl = _srgb_to_linear(g)
    bl = _srgb_to_linear(b)

    # linear RGB -> XYZ (sRGB D65)
    x = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    # normalize with D65 reference white
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    x, y, z = x / xn, y / yn, z / zn

    def f(t: float) -> float:
        if t > 0.008856:
            return t ** (1 / 3)
        return (7.787 * t) + (16 / 116)

    fx, fy, fz = f(x), f(y), f(z)

    L = (116 * fy) - 16
    a = 500 * (fx - fy)
    b2 = 200 * (fy - fz)
    return (float(L), float(a), float(b2))


# ---------- CIEDE2000 ----------

def ciede2000(lab1: np.ndarray, lab2: np.ndarray) -> float:
    """
    CIEDE2000 color difference ΔE00 between two Lab colors.
    Inputs: np.array([L,a,b])
    Returns: float
    """
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    # Mean L*
    L_bar = 0.5 * (L1 + L2)

    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)
    C_bar = 0.5 * (C1 + C2)

    G = 0.5 * (1 - np.sqrt((C_bar**7) / (C_bar**7 + 25**7)))

    a1p = (1 + G) * a1
    a2p = (1 + G) * a2

    C1p = np.sqrt(a1p**2 + b1**2)
    C2p = np.sqrt(a2p**2 + b2**2)
    C_bar_p = 0.5 * (C1p + C2p)

    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360

    dLp = L2 - L1
    dCp = C2p - C1p

    dhp = h2p - h1p
    if C1p * C2p == 0:
        dhp = 0
    elif dhp > 180:
        dhp -= 360
    elif dhp < -180:
        dhp += 360

    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))

    # Calculate mean values
    L_bar_p = 0.5 * (L1 + L2)
    C_bar_p = 0.5 * (C1p + C2p)

    if C1p * C2p == 0:
        h_bar_p = h1p + h2p
    else:
        if abs(h1p - h2p) > 180:
            h_bar_p = (h1p + h2p + 360) / 2 if (h1p + h2p) < 360 else (h1p + h2p - 360) / 2
        else:
            h_bar_p = (h1p + h2p) / 2

    T = (
        1
        - 0.17 * np.cos(np.radians(h_bar_p - 30))
        + 0.24 * np.cos(np.radians(2 * h_bar_p))
        + 0.32 * np.cos(np.radians(3 * h_bar_p + 6))
        - 0.20 * np.cos(np.radians(4 * h_bar_p - 63))
    )

    dTheta = 30 * np.exp(-(((h_bar_p - 275) / 25) ** 2))
    Rc = 2 * np.sqrt((C_bar_p**7) / (C_bar_p**7 + 25**7))

    Sl = 1 + (0.015 * ((L_bar_p - 50) ** 2)) / np.sqrt(20 + ((L_bar_p - 50) ** 2))
    Sc = 1 + 0.045 * C_bar_p
    Sh = 1 + 0.015 * C_bar_p * T

    Rt = -np.sin(np.radians(2 * dTheta)) * Rc

    # Weighting factors
    Kl = Kc = Kh = 1.0

    dE = np.sqrt(
        (dLp / (Kl * Sl)) ** 2
        + (dCp / (Kc * Sc)) ** 2
        + (dHp / (Kh * Sh)) ** 2
        + Rt * (dCp / (Kc * Sc)) * (dHp / (Kh * Sh))
    )
    return float(dE)
