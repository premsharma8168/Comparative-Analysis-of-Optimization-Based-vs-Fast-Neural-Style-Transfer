# Neural Style Transfer (NST) Benchmark - Comparative Analysis

## 🎯 About This Project
This project is an interactive web platform designed to compare two of the most popular Neural Style Transfer (NST) methodologies side-by-side. Neural Style Transfer is an artificial intelligence technique that takes two images—a **Content Image** (e.g., a photograph of your dog) and a **Style Image** (e.g., a painting by Van Gogh)—and blends them together so the output looks like the content image painted in the style of the style image.

The platform specifically compares the trade-offs between rendering **quality** and rendering **speed** by providing a visual A/B benchmark between:
1. **Optimization-Based NST** (The classic slow method)
2. **Fast NST** (The modern feed-forward method)

## ⚙️ How It Works (The Methodologies)

### 1. Optimization-Based NST (Gatys et al.)
- **How it works:** It uses an untrained white-noise image and slowly optimizes it step-by-step using a pre-trained VGG19 Convolutional Neural Network. It mathematically measures how much the current canvas differs from the Content Image (Content Loss) and the Style Image (Style Loss, calculated via Gram matrices) and iteratively repaints the image to minimize this difference.
- **Pros:** Completely flexible. You can upload *any* style image you want. High aesthetic quality.
- **Cons:** Extremely slow. It takes minutes on average hardware to generate a single image.

### 2. Fast NST (Johnson et al.)
- **How it works:** Instead of solving an optimization problem for every new image, an entire ResNet/Transformer neural network is pre-trained on a massive dataset of images specifically to apply **one single style**. 
- **Pros:** Lightning fast. Generates high-resolution stylized images in less than a second (real-time).
- **Cons:** Inflexible. You can only use the specific styles the network was trained on. You cannot upload a custom style image on the fly.

## 🛠️ How It Was Made (Technology Stack)
This project was constructed end-to-end to ensure optimal ML model performance and a premium user experience:
- **Backend (Python & FastAPI):** The server is built with lightweight and asynchronous FastAPI, capable of handling simultaneous heavy image processing endpoints. 
- **Machine Learning (PyTorch & OpenCV):** 
  - **PyTorch** handles the complex gradients and L-BFGS optimization loops for the Optimization-Based NST algorithm.
  - **OpenCV's DNN module** handles the compiled, lightning-fast inference for the Fast NST models.
- **Frontend (Vanilla HTML/CSS/JS):** A sleek, modern dashboard utilizing Dark Mode styling and Glassmorphism (dynamic blur effects) to create a premium application feel without requiring bloated frameworks like React.
- **Automated Tooling:** Custom download scripts to securely fetch and load `.t7` Torch models over the network natively.

## 🚀 How to Use the Project

### Prerequisites
Make sure you have **Python 3.8+** installed on your system.
It is highly recommended (but not strictly required) to run this in an environment with a dedicated GPU (CUDA).

### 1. Installation
Open your terminal inside the project root folder.
Install the required python dependencies:
```bash
pip install -r backend/requirements.txt
```

### 2. Model Setup
Download the pre-trained weights for the `Fast NST` side of the project. This script will automatically download the pre-compiled style modes (like Starry Night and Composition VII) into a `models/` folder.
```bash
python backend/download_models.py
```

### 3. Start the Server
Run the FastAPI backend server using uvicorn:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 4. Interactive Usage
Open your web browser and navigate directly to:
**[http://localhost:8000](http://localhost:8000)**

#### Left Panel: Optimization-Based NST
1. Under **Content Image**, upload the picture you want to style.
2. Under **Style Image**, upload **ANY** image that holds the artistic style you like.
3. Choose the number of **Iterations** (e.g., 50 for a quick test, 300 for maximum quality).
4. Click **Generate** and wait for the AI to repetitively calculate and paint.

#### Right Panel: Fast NST
1. Under **Content Image**, upload your picture.
2. Under **Select Style Model**, choose one of the pre-fetched `.t7` styles from the dropdown.
3. Click **Generate**.
4. The result will appear almost instantaneously.
