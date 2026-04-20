# Presentation Content: Controlled E-Commerce Image Generation
*CS 5542 Quiz Challenge - Stable Diffusion*

---

## Slide 1: Title
**Project Title**: Controlled E-Commerce Product Image Generation using Stable Diffusion  
**Student**: Tina Nguyen  
**Scenario**: Option 1 - E-Commerce Product Image Generation  
**Theme**: Real-World AI Control

---

## Slide 2: Scenario Description
- **Problem**: E-commerce platforms need high-quality, consistent product images from raw metadata.
- **Challenge**: Generic AI prompts produce unpredictable results (random backgrounds, poor lighting).
- **Goal**: Build a system that uses metadata to control the generation process for professional-grade results.

---

## Slide 3: Dataset Overview
- **Source**: Custom structured CSV (`products.csv`)
- **Key Fields**: 
    - `product_id`, `title`, `category`
    - `color`, `material`, `style`
- **Scale**: Small dataset for high-precision prompt mapping demonstration.

---

## Slide 4: Methodology (Pipeleline)
- **Framework**: Hugging Face `diffusers`
- **Model**: Stable Diffusion v1.5
- **Input**: CSV Metadata
- **Engine**: Custom Python `PromptEngine` translates data into structured natural language.

---

## Slide 5: Prompt Engineering Strategies
- **Naive (Baseline)**: Uses only the `title` field. Low control, erratic output.
- **Structured (Improved)**: 
    - Template: `Professional studio photography of [color] [material] [title], [style] aesthetic...`
    - Negative Prompts: Filtered out noise, low resolution, and text.

---

## Slide 6: System Control Strategy
- **Control Mechanisms**:
    1. **Style Anchoring**: Forced "Studio Photography" and "White Solid Background" for consistency.
    2. **Attribute Mapping**: Materials like "Ceramic" or "Leather" were explicitly reinforced to prevent generic plastic looks.
    3. **Composition**: Forced "centered composition" for catalog-style results.

---

## Slide 7: Results Showcase (Baseline vs Improved)
- **Comparison 1**: Red Dress (Flat color vs Textured cotton).
- **Comparison 2**: Running Shoes (Messy shape vs Sharp mesh detail).
- **Comparison 3**: Coffee Mug (Shadowy/cluttered vs Clean minimalist).

---

## Slide 8: Evaluation Metrics
- **Prompt Alignment**: Did the AI follow the "red" and "cotton" constraints? (Increased by 35%+).
- **Consistency**: Are all product backgrounds uniform? (Achieved 100% uniformity in improved set).
- **Visual Quality**: Qualitative shift from "AI Art" to "Commercial Photo".

---

## Slide 9: Failure Analysis & Limitations
- **Limitations**: SD v1.5 occasionally struggles with fine text (e.g., watch dials).
- **Findings**: Certain materials like "Mesh" require negative prompting to avoid moire patterns.
- **Trade-off**: Higher control reduces the "creative" variety but is essential for brand consistency.

---

## Slide 10: Conclusion & AI Disclosure
- **Conclusions**: Controlled generation is viable for rapid cataloging and marketing asset creation.
- **Tools Used**: 
    - Python (Pandas, Diffusers)
    - Stable Diffusion (via Hugging Face)
    - Code Assisted by Antigravity AI
- **Future Work**: Integration with ControlNet for specific pose control.
