# QuizzTN
# Controlled E-Commerce Product Image Generation (Stable Diffusion)
**CS 5542 - Quiz Challenge 1 | Author: Tina Nguyen**

## 1. Overview
This repository contains a data-driven image generation system built with **Stable Diffusion (DreamShaper 8)**. It takes structured e-commerce product metadata and converts it into high-fidelity, premium studio-quality images.

The project demonstrates how **Structured Prompt Templates** and **Negative Prompting** provides significantly more control over AI outputs compared to naive text prompts, ensuring consistency for commercial applications.

---

## 2. Quick Results Comparison
Below is a demonstration of how the **Controlled Generation** (Improved) outperforms the **Naive Baseline**.

| Baseline Prompt: "Women Summer Dress" | Improved: "Professional studio photography of red cotton casual dress..." |
|:---:|:---:|
| ![Product 1 Baseline](outputs/baseline/prod_1_baseline.png) | ![Product 1 Improved](outputs/improved/prod_1_improved.png) |
| *Generic style, inconsistent lighting* | *High texture fidelity, calibrated lighting, clean background* |

---

## 3. Technical Methodology
The pipeline follows a structured **Data-to-Prompt** approach evaluating **10 products across 3 seeds per prompt** (yielding 60 images).
1.  **Data Extraction**: Product attributes (Category, Color, Material, Style) are loaded from `data/products.csv`.
2.  **Prompt Engine**: A custom Python class (`src/generator.py`) maps these attributes into a detailed "Studio Photography" template.
3.  **Stable Diffusion Inference**: The system uses the high-performance `Lykon/dreamshaper-8` checkpoint via the Hugging Face `diffusers` library.
4.  **Quality Control**: Implements standard e-commerce negative prompts to remove watermarks, text, and artifacts.

---

## 4. Tools & Libraries Used
As required by the assignment, here is the list of technical tools:
- **Programming**: Python 3.x
- **Deep Learning**: PyTorch
- **Generative AI**: Hugging Face `diffusers`, `transformers`, `accelerate`
- **Data Science**: Pandas, NumPy
- **Evaluation**: `openai-clip` (Text-Image alignment), `scikit-image` (SSIM structure consistency)
- **Visualization**: Matplotlib, Pillow

---

## 5. 🤖 Use of AI Tools (Disclosure)
In accordance with the "Transparency" requirement of the challenge, AI was utilized as follows:
- **Coding Assistance**: Antigravity AI was used to draft the modular Python classes and the generation pipeline.
- **Documentation**: AI assisted in formatting the evaluation report and the dataset metadata descriptions.
- **Presentation**: The slide deck structure and video script were generated with AI assistance to ensure professional tone and clarity.

---

## 6. Repository Layout
- [**src/**](src/): Core Python logic for prompt engineering and generation.
- [**notebooks/**](notebooks/): Interactive Jupyter demo with visualizations.
- [**outputs/**](outputs/): Side-by-side comparison images.
- [**evaluation/**](evaluation/): Detailed [Results Report](evaluation/results.md) and failure analysis.
- [**slides/**](slides/): Submission-ready [Presentation PDF](slides/presentation.pdf) and HTML slides.
- [**demo/**](demo/): Narrated [Video Script](demo/video_script.md).
- [**data/**](data/): [Dataset & Metadata Description](data/dataset_description.md).

---

## 7. How to Reproduce
1. **Setup**: `pip install -r requirements.txt`
2. **Preview**: Open `notebooks/ecommerce_generation.ipynb` to see the results.
3. **Run Pipeline**: Execute `python src/generator.py` to see the prompt mapping logic.
4. **Evaluate**: Run `python src/evaluator.py` to regenerate the comparison report.
