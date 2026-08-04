# Phase 4.1.6 – Stabilization

## Purpose

This package improves repository portability by ensuring pytest can
discover the repository root consistently.

## Changes

- Added `conftest.py` to place the repository root on `sys.path`.
- Added `pytest.ini` to standardize pytest configuration.
- No production code changes.
- No canonical model changes.
- No dashboard behavior changes.

## Expected Result

Running `pytest` from the repository root should consistently resolve
imports such as `python.dashboard_engine.*`.
