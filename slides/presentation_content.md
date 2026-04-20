# Presentation: Controlled E-Commerce Product Image Generation
## CS 5542 Quiz Challenge 1 | Stable Diffusion XL | Tina Nguyen

---

## Slide 1: Title
**Controlled E-Commerce Product Image Generation**
Using Stable Diffusion XL for Structured Prompt Engineering

**Student**: Tina Nguyen
**Course**: CS 5542 — Big Data Analytics
**Scenario**: Option 1 — E-Commerce Product Image Generation
**Submission Date**: April 20, 2026

> *"From raw metadata to professional studio photography — automated, reproducible, and quantitatively evaluated."*

---

## Slide 2: Scenario Description

### The Problem
E-commerce platforms like Amazon and Shopify need **thousands of consistent, professional product images**. Manual photography is expensive and slow. Generic AI prompts produce unpredictable results:
- Random backgrounds
- Inconsistent lighting
- Varied styles between shots of the same product

### The Goal
Build an AI pipeline that takes **structured product metadata** and automatically generates **professional, catalog-ready images** — controllably and at scale.

### Why It Matters
Product image quality directly impacts conversion rates. Studies show consistent white-background images increase purchase intent by **20-30%** over amateur photography.

---

## Slide 3: Dataset

### Source
Custom structured CSV: `data/products.csv`

### 10 Products Across 5 Categories

| Category | Products |
|---|---|
| Apparel | Women Summer Dress, Hoodie |
| Footwear | Running Shoes, Sneakers |
| Accessories | Leather Backpack, Wrist Watch, Handbag |
| Kitchenware | Coffee Mug |
| Electronics | Smart Speaker, Wireless Earbuds |

### Attributes per Product
`product_id` · `title` · `category` · `color` · `material` · `style`

**Example row**: `3, Coffee Mug, mug, white, ceramic, minimalist`

### Scale
- 10 products × 3 seeds × 2 prompt strategies = **60 total images generated**

---

## Slide 4: Methodology — Pipeline Architecture

```
CSV Metadata
    ↓
PromptEngine (src/generator.py)
    ↓                    ↓
Baseline Prompt    Structured Prompt
(title only)       (color + material + style + lighting + background)
    ↓                    ↓
Stable Diffusion XL 1.0 (A100 GPU, fp16)
    ↓                    ↓
30 Baseline Images  30 Improved Images
         ↓
CLIP + SSIM Evaluation (src/evaluator.py)
         ↓
Quantitative Report (evaluation/results.md)
```

### Key Design Decisions
1. **Seed-controlled generation** (seeds 42, 123, 999) — ensures reproducibility
2. **Skip-if-exists logic** — idempotent pipeline, safe to re-run
3. **fp16 precision** on A100 — 2× throughput with identical output quality

---

## Slide 5: Prompt Engineering Strategy

### Strategy A — Naive Baseline
> Uses **only the product title**. No style, no control, no constraints.

**Example**: `"Coffee Mug"`

**Problems**: Random background, arbitrary lighting, unpredictable style (sometimes cartoon, sometimes realistic)

---

### Strategy B — Structured (Improved)
> Full attribute-to-prompt mapping with 5 controlled dimensions.

**Template**:
```
Professional studio photography of a [color] [material] [title],
[style] aesthetic, centered composition, high-end [category],
soft cinematic lighting, white solid background, 8k resolution,
photorealistic, sharp focus.
```

**Example**: `"Professional studio photography of a white ceramic Coffee Mug, minimalist aesthetic, centered composition, soft cinematic lighting, white solid background, 8k resolution, photorealistic, sharp focus."`

### Negative Prompt (Applied to All Structured Images)
`"blurry, low quality, distorted, extra limbs, text, watermark, logo, messy background, low resolution, grain, shadows."`

### 5 Controlled Attributes
| Attribute | Value from CSV | Effect |
|---|---|---|
| Color | `white` | Forces monochromatic palette |
| Material | `ceramic` | Controls surface texture rendering |
| Style | `minimalist` | Constrains aesthetic direction |
| Lighting | `soft cinematic` | Standardizes illumination |
| Background | `white solid` | Eliminates random scenes |

---

## Slide 6: Tools & Technical Stack

| Component | Tool | Purpose |
|---|---|---|
| **Language** | Python 3.10 | Pipeline scripting |
| **Generative AI** | Stable Diffusion XL 1.0 | Image generation |
| **Framework** | Hugging Face `diffusers` | SD pipeline management |
| **GPU** | NVIDIA A100 (via Colab) | Inference acceleration |
| **Precision** | fp16 | Memory optimization |
| **Evaluation** | `openai/clip-vit-base-patch32` | Text-image alignment |
| **Evaluation** | `scikit-image` SSIM | Cross-seed consistency |
| **Data** | `pandas` | CSV metadata loading |
| **Visualization** | `matplotlib`, `PIL` | Image display & charts |

**Execution**: Google Colab notebook (`notebooks/ecommerce_generation.ipynb`) 
— one-click Run All, pulls code directly from GitHub via `git clone`.

---

## Slide 7: Results — Visual Showcase

### Baseline vs. Structured Prompt Comparison

| Product | Baseline (title only) | Structured (full template) |
|---|---|---|
| ☕ Coffee Mug | Cluttered, shadowy, varied | Clean white ceramic, consistent |
| 👟 Sneakers | Random background, flat | Studio-lit, white bg, sharp |
| 👜 Handbag | Inconsistent lighting | Elegant, luxury aesthetic |

**Key Visual Observations**:
- ✅ Structured prompts produce **uniformly white backgrounds** across all 10 products
- ✅ Material tokens (`ceramic`, `leather`, `mesh`) produce **noticeably different surface textures**
- ✅ `Soft cinematic lighting` creates professional **shadow gradients** below objects
- ⚠️ Footwear (shoes, sneakers) shows highest variance across seeds due to geometric complexity

*See `outputs/baseline/` and `outputs/improved/` for all 60 generated images.*

---

## Slide 8: Evaluation — Quantitative Results

### CLIP Score (Text-Image Alignment)

| | Baseline Average | Improved Average | Δ |
|---|---|---|---|
| CLIP Score | 0.288 | 0.279 | -0.009 |

→ Statistically equivalent. **Adding 20+ control tokens does NOT degrade object recognition.**

---

### SSIM (Cross-Seed Consistency) — Key Finding

| | Baseline Average | Improved Average | Δ |
|---|---|---|---|
| SSIM | 0.360 | 0.442 | **+22.8%** |

→ Structured prompts produce **significantly more consistent images** across random seeds.

**Top Performers (SSIM improvement)**:
- Coffee Mug: 0.460 → **0.732** (+59%)
- Smart Speaker: 0.498 → **0.716** (+44%)
- Sneakers: 0.170 → **0.349** (+105%)

---

## Slide 9: Failure Analysis & Limitations

### Failure Case 1: Leather Backpack (SSIM Regression)
- **Result**: SSIM dropped from 0.614 → 0.258
- **Why**: Complex sub-components (straps, buckles, zippers) varied placement across seeds
- **Lesson**: Multi-component products need positional tokens (e.g., *"single front pocket"*)

### Failure Case 2: Running Shoes (Persistently Low SSIM)
- **Result**: Baseline 0.100 → Improved 0.177 (still low)
- **Why**: Complex footwear geometry (laces, mesh, sole) creates high inter-seed variance
- **Lesson**: Text-to-image alone insufficient; **ControlNet** or **img2img** needed for geometric precision

### Failure Case 3: Watch Dials
- **Result**: Fine detail (numbers, hands) inconsistent and sometimes blurry
- **Why**: SDXL's 1024×1024 resolution is insufficient for sub-millimeter detail rendering
- **Lesson**: Super-resolution post-processing (e.g., ESRGAN) would help

### Key Trade-off Identified
> Higher SSIM (consistency) reduces image variety.
> For **e-commerce** → consistency is desirable ✅
> For **creative/art generation** → baseline provides more diversity ✅

---

## Slide 10: Findings, Conclusions & AI Disclosure

### Core Findings
1. ✅ **Structured prompt engineering measurably improves consistency** (+22.8% SSIM)
2. ✅ **CLIP alignment is preserved** — structured prompts do not confuse the model
3. ✅ **The pipeline is fully automated** — CSV in, studio images out
4. ✅ **60 images generated** across 10 products and 3 seeds on NVIDIA A100 GPU

### Limitations & Future Work
- **ControlNet integration** would allow precise pose/angle control (e.g., always 3/4 view)
- **Larger product catalog** (100+ items) with real Amazon metadata would stress-test scalability
- **Multimodal extension**: Generate product description text alongside images using a VLM

### AI Tools Disclosure (Required)
| Tool | Usage |
|---|---|
| **Antigravity AI** | Pipeline architecture, evaluator code, slide/report writing |
| **Hugging Face SDXL** | Image generation model |
| **Google Colab** | GPU execution environment |

*All design decisions, experimental setup, and analytical conclusions were reviewed and validated by the student.*

---

### GitHub Repository
🔗 https://github.com/JoeDoan/QuizzTN
