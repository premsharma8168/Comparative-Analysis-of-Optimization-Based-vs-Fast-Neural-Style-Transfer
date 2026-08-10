# NeuroTransfer

A computer-vision application that compares **optimization-based Neural Style Transfer** with **fast feed-forward style transfer** through an interactive web interface.

## Overview

NeuroTransfer makes the quality-versus-speed trade-off between two Neural Style Transfer approaches directly observable. Users can provide content images, apply styles, and compare the behavior of optimization-based generation with fast inference models.

## Approaches

### Optimization-Based NST

Uses a pretrained VGG19 network and iterative optimization to minimize content and style losses. This approach supports arbitrary style images but requires significantly more computation per result.

### Fast NST

Uses pretrained feed-forward style-transfer models for rapid inference. It provides much faster generation while being limited to the styles represented by the available models.

## Features

- Side-by-side NST workflow
- Custom style image support for optimization-based NST
- Fast style-model inference
- Configurable optimization iterations
- Image upload and result visualization
- Web-based interface

## Tech Stack

- Python
- PyTorch
- OpenCV
- FastAPI
- Uvicorn
- HTML / CSS / JavaScript
- VGG19
- OpenCV DNN

## Run Locally

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Download the Fast NST model files:

```bash
python backend/download_models.py
```

Start the application:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000` in a browser.

## Project Goal

Study the practical trade-offs between iterative optimization and fast neural inference in Neural Style Transfer while packaging both approaches into a usable application.

## Author

**Prem Sharma**

GitHub: https://github.com/premsharma8168
