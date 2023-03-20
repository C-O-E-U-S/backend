import torch
from PIL import Image
from lavis.models import load_model_and_preprocess

def classify(image):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # raw_image = Image.open("tennis.jpeg").convert("RGB")
    raw_image = Image.open(image).convert("RGB")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    return(model.generate({"image":image}))