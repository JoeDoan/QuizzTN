import os
import pandas as pd
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

class PromptEngine:
    """Engine to convert product metadata into baseline and improved prompts."""
    
    @staticmethod
    def generate_baseline_prompt(row):
        """Simplistic prompt based only on the title."""
        return f"{row['title']}"

    @staticmethod
    def generate_improved_prompt(row):
        """Structured prompt using metadata, style, and professional lighting."""
        color = row['color']
        material = row['material']
        title = row['title']
        style = row['style']
        category = row['category']
        
        # Structure: [Subject] [Attributes] [Style] [Environment] [Quality]
        prompt = (
            f"Professional studio photography of a {color} {material} {title}, "
            f"{style} aesthetic, centered composition, high-end {category} fashion, "
            f"soft cinematic lighting, white solid background, 8k resolution, photorealistic, sharp focus."
        )
        return prompt

    @staticmethod
    def get_negative_prompt():
        """Standard negative prompt to avoid common artifacts."""
        return "blurry, low quality, distorted, extra limbs, text, watermark, logo, messy background, low resolution, grain, shadows."

class ECommerceGenerator:
    def __init__(self, model_id="Lykon/dreamshaper-8", device="cuda"):
        self.device = device if torch.cuda.is_available() else "cpu"
        self.model_id = model_id
        self.pipe = None

    def load_model(self):
        print(f"Loading model {self.model_id} on {self.device}...")
        if self.device == "cuda":
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, torch_dtype=torch.float16
            ).to(self.device)
        else:
            self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id).to(self.device)
        print("Model loaded successfully.")

    def generate(self, prompt, neg_prompt=None, seed=42, output_path="output.png"):
        print(f"Generating: {prompt[:50]}... (Seed: {seed})")
        if self.pipe:
            generator = torch.Generator(device=self.device).manual_seed(seed)
            # Runway SD 1.5 defaults to 512x512
            image = self.pipe(prompt, negative_prompt=neg_prompt, generator=generator, num_inference_steps=25).images[0]
            image.save(output_path)
            return image
        else:
            print("Model not loaded. Skipping generation.")
            return None

def main():
    # Load data
    data_path = os.path.join("data", "products.csv")
    df = pd.read_csv(data_path)
    df = df.dropna(how='all') # Clean empty rows

    # Setup directories
    os.makedirs(os.path.join("outputs", "baseline"), exist_ok=True)
    os.makedirs(os.path.join("outputs", "improved"), exist_ok=True)

    # Initialize Engine
    engine = PromptEngine()
    
    # Initialize Generator
    generator = ECommerceGenerator(device="mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
    generator.load_model()
    
    seeds = [42, 123, 999]
    
    print("Generating images for current dataset...")
    for _, row in df.iterrows():
        p_id = int(row['product_id'])
        baseline = engine.generate_baseline_prompt(row)
        improved = engine.generate_improved_prompt(row)
        neg_prompt = engine.get_negative_prompt()
        
        print(f"\nProduct {p_id}: {row['title']}")
        
        for seed in seeds:
            base_out = os.path.join("outputs", "baseline", f"prod_{p_id}_baseline_seed{seed}.png")
            if not os.path.exists(base_out):
                generator.generate(prompt=baseline, seed=seed, output_path=base_out)
                
            impr_out = os.path.join("outputs", "improved", f"prod_{p_id}_improved_seed{seed}.png")
            if not os.path.exists(impr_out):
                generator.generate(prompt=improved, neg_prompt=neg_prompt, seed=seed, output_path=impr_out)

if __name__ == "__main__":
    main()
