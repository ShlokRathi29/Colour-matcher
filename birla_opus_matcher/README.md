# Birla Opus Paint Shade Matcher (ΔE2000)

A local Flask API that matches an uploaded paint shade image to the closest Birla Opus shade using:
- OpenCV color extraction
- RGB → CIELAB conversion
- CIEDE2000 ΔE comparison

## Features
- Single-brand matching: Birla Opus only
- Top-K closest matches
- Confidence scoring
- Deterministic & testable backend

## Setup

### 1. Create venv
```bash
python -m venv .venv
.venv\Scripts\activate
