import os
# Set environment variables before importing torch
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import gc
import sys
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import warnings
warnings.filterwarnings('ignore')

# Custom ToTensor transform for numpy compatibility
class CustomToTensor:
    """Convert PIL image to tensor with numpy compatibility fix"""
    def __call__(self, pic):
        if isinstance(pic, Image.Image):
            # Convert PIL to numpy array manually with explicit dtype
            np_array = np.asarray(pic, dtype=np.float32)
            # Convert HWC to CHW format
            if len(np_array.shape) == 3:
                np_array = np_array.transpose((2, 0, 1))
            elif len(np_array.shape) == 2:
                np_array = np_array[np.newaxis, :, :]
            # Convert to tensor and normalize to [0,1]
            # Use contiguous array to avoid numpy compatibility issues
            tensor = torch.from_numpy(np.ascontiguousarray(np_array)) / 255.0
            return tensor
        else:
            raise TypeError(f'pic should be PIL Image. Got {type(pic)}')

# Inject custom function into torchvision
transforms.functional.to_tensor = CustomToTensor()

def main():
    # Check if image exists
    input_image_path = "/Users/vineetvijaykumar/rebelway/rebelwayAppliedML/hugging_face/bg_removal/wallhaven-n66r66_2560x1440.png"
    if not os.path.exists(input_image_path):
        print(f"Error: {input_image_path} not found")
        return
    
    print("Setting up PyTorch...")
    # Force PyTorch to use single thread and lower precision
    torch.set_num_threads(1)
    torch.set_float32_matmul_precision('medium')
    
    print("Loading image...")
    try:
        image = Image.open(input_image_path)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        print(f"Image loaded: {image.size}, mode: {image.mode}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    print("Loading model...")
    try:
        # Load model with memory optimizations
        model = AutoModelForImageSegmentation.from_pretrained(
            'briaai/RMBG-2.0', 
            trust_remote_code=True,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        
        # Move model to CPU
        model.to('cpu')
        
        model.eval()
        print("Model loaded successfully")
        
        # Force garbage collection
        gc.collect()
        
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("Processing image...")
    # Use smaller resolution to reduce memory usage
    image_size = (512, 512)
    
    try:
        # Manual preprocessing to avoid ToTensor issues
        resized_image = image.resize(image_size)
        
        # Convert to numpy array
        img_array = np.array(resized_image, dtype=np.float32) / 255.0
        
        # Convert HWC to CHW format
        img_array = img_array.transpose((2, 0, 1))
        
        # Convert to tensor manually
        tensor = torch.tensor(img_array, dtype=torch.float32)
        
        # Normalize
        mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        tensor = (tensor - mean) / std
        
        # Add batch dimension
        input_images = tensor.unsqueeze(0)
        print("Image preprocessed")
        
        print("Running inference...")
        with torch.no_grad():
            # Clear any cached memory
            gc.collect()
            
            # Run prediction
            preds = model(input_images)[-1].sigmoid()
            
        print("Post-processing...")
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)
        
        # Create output image
        result_image = image.copy()
        result_image.putalpha(mask)
        
        # Save result
        output_path = "test.png"
        result_image.save(output_path)
        print(f"Success! Background removed image saved as: {output_path}")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("Cleaning up memory...")
        try:
            if 'model' in locals():
                del model
            if 'preds' in locals():
                del preds
            if 'input_images' in locals():
                del input_images
            gc.collect()
        except:
            pass
        print("Done")

if __name__ == "__main__":
    main()
