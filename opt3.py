import torch
from diffusers import StableDiffusion3Pipeline, AutoencoderKL
from pathlib import Path
import sys
from datetime import datetime

def generate_image(prompt, output_path, negative_prompt="", num_inference_steps=28, guidance_scale=7.0):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dimensions = [
        (1024, 576),  # 0.5K
        (896, 504),   # Between 0.5K and 720p
        (768, 432),   # 720p equivalent
        (640, 360),   # 360p
    ]
    try:
        vae = AutoencoderKL.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", subfolder="vae", torch_dtype=torch.float16)
        pipe = StableDiffusion3Pipeline.from_pretrained(
            "stabilityai/stable-diffusion-3-medium-diffusers",
            vae=vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16"
        )
        pipe.enable_attention_slicing()
        pipe.enable_sequential_cpu_offload()
        for width, height in dimensions:
            try:
                print(f"Attempting to generate image at {width}x{height}")
                with torch.inference_mode():
                    image = pipe(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        num_inference_steps=num_inference_steps,
                        guidance_scale=guidance_scale,
                        height=height,
                        width=width,
                    ).images[0]
                image.save(output_path, format="PNG", quality=95)
                print(f"Image successfully generated and saved to: {output_path}")
                print(f"Final dimensions: {width}x{height}")
                return
            except RuntimeError as e:
                print(f"Failed to generate at {width}x{height}: {e}")
                continue
        print("All attempted dimensions failed. Please try with smaller sizes or adjust your GPU memory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def read_prompts(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    if not torch.cuda.is_available():
        print("Warning: CUDA is not available. This script may run very slowly on CPU.")
        user_input = input("Do you want to continue? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting script.")
            sys.exit()

    prompts_file = "prompts.txt"
    prompts = read_prompts(prompts_file)

    if not prompts:
        print(f"No prompts found in {prompts_file}. Exiting.")
        sys.exit()

    negative_prompt = "blurry, low quality, distorted, square format, portrait orientation"

    for i, prompt in enumerate(prompts, 1):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_path = f"{i}_{timestamp}.png"
        print(f"\nGenerating image {i}/{len(prompts)}")
        print(f"Prompt: {prompt}")

        prompt += " realistic, 4k, detailed, landscape view"
        generate_image(prompt, output_path, negative_prompt)

if __name__ == "__main__":
    main()
