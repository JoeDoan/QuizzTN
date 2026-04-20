import os
import json
import pandas as pd
import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from skimage.metrics import structural_similarity as ssim

def load_clip_model():
    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading CLIP model on {device}...")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor, device

def compute_clip_score(image_path, text, model, processor, device):
    if not os.path.exists(image_path):
        return 0.0
    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    return logits_per_image.item() / 100.0

def compute_ssim_score(image_paths):
    valid_paths = [p for p in image_paths if os.path.exists(p)]
    if len(valid_paths) < 2:
        return 0.0
        
    images = [np.array(Image.open(p).convert("L").resize((256, 256))) for p in valid_paths]
    score = 0.0
    count = 0
    for i in range(len(images)):
        for j in range(i+1, len(images)):
            score += ssim(images[i], images[j], data_range=255)
            count += 1
    return float(score / count) if count > 0 else 0.0

def evaluate_pipeline():
    """Generates a quantitative evaluation using CLIP and SSIM."""
    data_path = os.path.join("data", "products.csv")
    df = pd.read_csv(data_path).dropna(how='all')
    
    # Load evaluator models
    try:
        clip_model, clip_processor, device = load_clip_model()
    except Exception as e:
        print(f"Failed to load CLIP. Did you run pip install transformers? Error: {e}")
        return

    seeds = [42, 123, 999]
    results = []

    print("Evaluating generated images...")
    for _, row in df.iterrows():
        p_id = int(row['product_id'])
        title = row['title']
        
        base_paths = [os.path.join("outputs", "baseline", f"prod_{p_id}_baseline_seed{s}.png") for s in seeds]
        impr_paths = [os.path.join("outputs", "improved", f"prod_{p_id}_improved_seed{s}.png") for s in seeds]
        
        # Calculate CLIP on first seed for simplicity
        base_clip = compute_clip_score(base_paths[0], title, clip_model, clip_processor, device)
        impr_clip = compute_clip_score(impr_paths[0], title, clip_model, clip_processor, device)
        
        # Calculate SSIM across seeds
        base_ssim = compute_ssim_score(base_paths)
        impr_ssim = compute_ssim_score(impr_paths)
        
        results.append({
            "product_id": p_id,
            "title": title,
            "baseline_clip": base_clip,
            "improved_clip": impr_clip,
            "baseline_ssim": base_ssim,
            "improved_ssim": impr_ssim
        })
        print(f"[{p_id}] {title} | CLIP Baseline: {base_clip:.3f} | CLIP Improved: {impr_clip:.3f}")

    # Output JSON
    os.makedirs("evaluation", exist_ok=True)
    with open(os.path.join("evaluation", "quantitative_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Output Markdown Report
    report = "# Quantitative Evaluation Report\n\n"
    report += "This report evaluates 'Naive' baseline prompts against 'Structured' controlled prompts using mathematical metrics (CLIP for alignment, SSIM for seed consistency).\n\n"
    report += "| Product ID | Title | Baseline CLIP | Improved CLIP | Baseline SSIM | Improved SSIM |\n"
    report += "|---|---|---|---|---|---|\n"
    
    for r in results:
        report += f"| {r['product_id']} | {r['title']} | {r['baseline_clip']:.3f} | {r['improved_clip']:.3f} | {r['baseline_ssim']:.3f} | {r['improved_ssim']:.3f} |\n"
        
    with open(os.path.join("evaluation", "results.md"), "w") as f:
        f.write(report)
        
    print("\nEvaluation successfully completed. See evaluation/results.md")

if __name__ == "__main__":
    evaluate_pipeline()
