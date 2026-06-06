"""Fixture with intentional architectural debt.

Docs: complex.doc.md
"""


def simple_ok():
    """Clean, short, used."""
    return 42


def complex_nested(x: int) -> int:
    """High cyclomatic complexity."""
    if x > 0:
        if x > 10:
            if x > 20:
                return 30
            elif x > 15:
                for i in range(5):
                    if i % 2 == 0:
                        while i < 10:
                            i += 1
                        return i
    return 0


def long_function():
    """Way too many lines."""
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26
    aa = 27
    ab = 28
    ac = 29
    ad = 30
    ae = 31
    af = 32
    ag = 33
    ah = 34
    ai = 35
    aj = 36
    ak = 37
    al = 38
    am = 39
    an = 40
    ao = 41
    ap = 42
    aq = 43
    ar = 44
    as_ = 45
    at = 46
    au = 47
    av = 48
    aw = 49
    ax = 50
    ay = 51
    az = 52
    ba = 53
    bb = 54
    bc = 55
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t + u + v + w + x + y + z + aa + ab + ac + ad + ae + af + ag + ah + ai + aj + ak + al + am + an + ao + ap + aq + ar + as_ + at + au + av + aw + ax + ay + az + ba + bb + bc


def unused_function():
    """Never called anywhere."""
    return "dead"


class UnusedClass:
    """Never instantiated."""
    pass
