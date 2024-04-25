import os
from typing import List
from PIL import Image
from huggingface_hub import hf_hub_download
from diffusers.utils import load_image

def resize_image(image, width, height) -> Image.Image:
    width0, height0 = image.size

    fit_width = width0 / height0 > width / height

    new_width = width if fit_width else int(width0 * height / height0)
    new_height = height if not fit_width else int(height0 * width / width0)

    resized = image.resize((new_width // 8 * 8, new_height // 8 * 8))
    return resized

    new_image = Image.new("RGB", (width, height), (0, 0, 0))
    new_image.paste(resized, ((width - new_width) // 2, (height - new_height) // 2))

    return new_image

def hf_download(fullname, offline=False):
    ns, project, filename = fullname.split('/', 2)
    return hf_hub_download(repo_id=f"{ns}/{project}", filename=filename, local_files_only=offline, resume_download=not offline)

def load_images(locations: List[str]) -> List[Image.Image]:
    if locations is None:
        return []
    files = [x for x in locations if os.path.isfile(x)]
    directories = [x for x in locations if os.path.isdir(x)]
    invalids = [x for x in locations if x not in files and x not in directories]
    assert len(invalids) == 0, f"Invalid path: {', '.join(invalids)}"
    for x in directories:
        files.extend(sorted([
            os.path.join(x, basename) for basename in os.listdir(x) if not basename.startswith('.')
        ]))
    return [load_image(x) for x in files]

def remove_none(input_dict):
    return {k: v for k, v in input_dict.items() if v is not None}

def to8(image: Image.Image) -> Image.Image:
    return image.resize((image.width - image.width % 8, image.height - image.height % 8), Image.LANCZOS)

def canny_from_pil(image, low_threshold=100, high_threshold=200):
    import cv2
    import numpy as np
    image = cv2.Canny(np.array(image), low_threshold, high_threshold)[:, :, None]
    return Image.fromarray(np.concatenate([image, image, image], axis=2))

class Object:
    def __init__(self, kvs):
        for key, value in kvs.items():
            setattr(self, key, value)

def obj(**kvs):
    return Object(kvs)
