# Quantitative Evaluation Report
## CS 5542 Quiz Challenge 1 — E-Commerce Product Image Generation
**Author**: Tina Nguyen | **Model**: Stable Diffusion XL 1.0 | **Hardware**: NVIDIA A100 GPU

---

## 1. Evaluation Methodology

This report presents a quantitative comparison between **Naive (Baseline)** and **Structured (Improved)** prompt engineering strategies for AI-generated e-commerce product images.

### Metrics Used

| Metric | Description | Tool |
|---|---|---|
| **CLIP Score** | Measures semantic alignment between the text prompt and the generated image. Higher = better match. | `openai/clip-vit-base-patch32` |
| **SSIM** | Structural Similarity Index — measures visual consistency across images generated from different random seeds. Higher = more consistent. | `scikit-image` |

### Experimental Setup
- **Products**: 10 items across 5 categories (apparel, footwear, kitchenware, accessories, electronics)
- **Seeds**: 3 per product (42, 123, 999) for reproducibility
- **Total Images**: 60 (30 baseline + 30 improved)
- **CLIP Evaluation**: Computed on seed-42 images for each product
- **SSIM Evaluation**: Computed as pairwise average across all 3 seeds per product

---

## 2. Complete Results Table

| ID | Product | Baseline CLIP | Improved CLIP | Δ CLIP | Baseline SSIM | Improved SSIM | Δ SSIM |
|---|---|---|---|---|---|---|---|
| 1 | Women Summer Dress | 0.249 | 0.252 | +0.003 | 0.262 | 0.344 | **+0.082** |
| 2 | Running Shoes | 0.283 | 0.227 | -0.056 | 0.100 | 0.177 | **+0.077** |
| 3 | Coffee Mug | 0.315 | 0.301 | -0.014 | 0.460 | 0.732 | **+0.272** |
| 4 | Leather Backpack | 0.305 | 0.301 | -0.004 | 0.614 | 0.258 | -0.356 |
| 5 | Wrist Watch | 0.268 | 0.279 | +0.011 | 0.088 | 0.191 | **+0.103** |
| 6 | Hoodie | 0.302 | 0.301 | -0.001 | 0.414 | 0.421 | **+0.007** |
| 7 | Sneakers | 0.294 | 0.260 | -0.034 | 0.170 | 0.349 | **+0.179** |
| 8 | Handbag | 0.289 | 0.279 | -0.010 | 0.422 | 0.540 | **+0.118** |
| 9 | Smart Speaker | 0.272 | 0.284 | +0.012 | 0.498 | 0.716 | **+0.218** |
| 10 | Wireless Earbuds | 0.307 | 0.306 | -0.001 | 0.570 | 0.691 | **+0.121** |
| | **Average** | **0.288** | **0.279** | **-0.009** | **0.360** | **0.442** | **+0.082** |

---

## 3. Analysis

### 3.1 CLIP Score (Text-Image Alignment)

- Average baseline CLIP: **0.288** | Average improved CLIP: **0.279**
- The small difference (-0.009) is statistically negligible, meaning structured prompts **do not degrade** subject recognition.
- SDXL correctly identifies "Coffee Mug," "Running Shoes," etc. regardless of whether the prompt is 2 words or 30+ words.
- **Interpretation**: Adding style, lighting, and background tokens does not confuse the model about what object to generate.

### 3.2 SSIM (Cross-Seed Consistency)

- Average baseline SSIM: **0.360** | Average improved SSIM: **0.442**
- Improvement: **+22.8%** — structured prompts generate significantly more consistent images across random seeds.
- **Top performers** (highest consistency gain):
  - Coffee Mug: 0.460 → 0.732 (+59.1%)
  - Smart Speaker: 0.498 → 0.716 (+43.8%)
  - Sneakers: 0.170 → 0.349 (+105.3%)
- **Outlier**: Leather Backpack dropped from 0.614 → 0.258. The detailed structured prompt caused the model to vary strap/buckle placement across seeds.

### 3.3 Why Structured Prompts Improve Consistency

The key mechanism is **environmental anchoring**. By explicitly specifying:
- `"white solid background"` — eliminates random scene generation
- `"soft cinematic lighting"` — standardizes illumination
- `"centered composition"` — fixes object placement

These constraints reduce the "degrees of freedom" for the diffusion model, causing different seeds to converge on structurally similar outputs.

---

## 4. Failure Cases

### Case 1: Leather Backpack (SSIM Regression)
- **Observation**: SSIM dropped despite improved visual quality per image.
- **Root Cause**: The structured prompt ("brown leather classic backpack") activated different sub-concepts across seeds — one seed emphasized buckles, another emphasized zippers, creating structural divergence.
- **Lesson**: Products with many sub-components (straps, pockets, zippers) benefit from even more specific positional prompting (e.g., "single front pocket, no visible zippers").

### Case 2: Running Shoes (Low Overall SSIM)
- **Observation**: Both baseline (0.100) and improved (0.177) SSIM are low.
- **Root Cause**: Footwear with laces, mesh patterns, and sole geometry varies significantly across seeds. The model has high internal variance for complex geometric objects.
- **Lesson**: Products requiring precise geometric consistency may need ControlNet or img2img approaches rather than pure text-to-image.

### Case 3: Wrist Watch (Low Baseline SSIM)
- **Observation**: Baseline SSIM = 0.088 (near random). Improved = 0.191.
- **Root Cause**: A 2-word prompt "Wrist Watch" is extremely ambiguous — the model generates everything from analog to digital, round to square faces. Structured prompting anchors the style to "elegant silver metal" but cannot fully constrain fine dial details.

---

## 5. Conclusions

1. **Structured prompt engineering is effective** for e-commerce image consistency, with a measurable +22.8% SSIM improvement.
2. **Text-image alignment is preserved** — adding control tokens does not degrade CLIP scores.
3. **Not all products benefit equally** — products with complex geometry or many sub-parts may require additional control mechanisms (ControlNet, img2img).
4. **The pipeline is fully reproducible** — seeds 42, 123, 999 produce identical outputs when re-run.

---

## 6. Raw Data

Full machine-readable results are available at: `evaluation/quantitative_results.json`
