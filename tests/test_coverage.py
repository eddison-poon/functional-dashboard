from reporting.coverage import *

def test_percentage():
    r=calculate_coverage(8,10)
    assert r.percentage==80.0

def test_zero_total():
    assert calculate_coverage(0,0).percentage==0.0

def test_manual():
    assert manual_coverage(20,15).percentage==75.0
