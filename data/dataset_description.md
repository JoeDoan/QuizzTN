# Dataset Description

## 1. Overview
This dataset contains structured product metadata used for generating product images using Stable Diffusion. The dataset is designed to simulate real-world e-commerce product information.

Each row represents a single product and includes descriptive attributes that can be converted into text prompts for image generation.

---

## 2. Dataset Type
- Format: CSV (Comma-Separated Values)
- Size: Small (for demonstration and experimentation)
- Purpose: Prompt generation for controlled image synthesis

---

## 3. Columns Description

### product_id
- **Type:** Integer
- **Description:** Unique identifier for each product

---

### title
- **Type:** Text
- **Description:** Name of the product (e.g., "Women Summer Dress", "Running Shoes")

---

### category
- **Type:** Text (Categorical)
- **Description:** General category of the product
- **Examples:** dress, shoes, mug, bag, watch

---

### color
- **Type:** Text
- **Description:** Primary color of the product
- **Examples:** red, black, white, brown, silver

---

### material
- **Type:** Text
- **Description:** Material used in the product
- **Examples:** cotton, leather, ceramic, metal, mesh

---

### style
- **Type:** Text
- **Description:** Design or aesthetic style of the product
- **Examples:** casual, sporty, minimalist, elegant, luxury

---

## 4. Purpose of the Dataset
The dataset is used to:
- Convert structured product data into text prompts
- Generate product images using Stable Diffusion
- Compare baseline vs structured prompt strategies
- Evaluate image quality, alignment, and consistency

---

## 5. Data-to-Prompt Mapping

Each row in the dataset is transformed into a text prompt.

### Example:

**Input (CSV row):**
`1, Women Summer Dress, dress, red, cotton, casual`

**Baseline Prompt:**
*"Women Summer Dress"*

**Improved Prompt:**
*"Professional studio photography of a red cotton Women Summer Dress, casual aesthetic, centered composition, high-end dress fashion, soft cinematic lighting, white solid background, 8k resolution, photorealistic, sharp focus."*

---

## 6. Access and Usage
This dataset is stored in `data/products.csv`. It can be loaded using standard data libraries like Pandas for automated prompt generation in Python.
