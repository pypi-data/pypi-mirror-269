# sd-tools

generating images from the command line and web UI

![web](https://github.com/zweifisch/sd-tools/assets/447862/3855dbd1-65ba-4721-ad44-0af6d79eb0c0)

https://github.com/zweifisch/sd-tools/assets/447862/e39bee8d-f7b4-41d9-b1ec-640f341835b5

```shell
pip install sd-tools
```

## Basics

```shell
sdxl 'locomotive'
```

If the model can't be downloaded, try using a huggingface mirror:

```shell
export HF_MIRROR=https://hf-mirror.com
```

To get better result, use more steps and higher resolutions:

```shell
sdxl 'locomotive' --size 720 --steps 4
```

Generate more with `--count`:

```shell
sdxl 'locomotive' --size 1024x576 --steps 4 --count 3
```

By default, images are save to `output/{seed}-{time}.webp`, which can be customized via `-o`:

```shell
sdxl 'locomotive' -o 'output/{seed}-{size}-{cfg}-{time}.webp'
```

### Interactive Mode

The loading of the model can task some time, use `-i` to enter interactive mode, keeping the model loaded:

```shell
sdxl 'locomotive' --size 1024x576 --steps 4 -i
```

Edited prompt and press enter:

```
> locomotive
```

`size`, `count`, `steps` and `cfg` can also be set on the fly:

```
> locomotive size=1024 cfg=1.9
```

### Web UI

```shell
sdxl 'A green frog' \
 --model 'Lykon/dreamshaper-xl-lightning' \
 --scheduler 'DPM++ SDE Karras' \
 --listen 8888
```

### Custom Models

To use a specific model:

```shell
sdxl 'locomotive' \
 --model Lykon/dreamshaper-xl-lightning \
 --steps 6 \
 --size 1024x576 \
 --scheduler 'DPM++ SDE Karras' \
 --cfg 2 \
```

More models can be found on [huggingface](https://huggingface.co/models?pipeline_tag=text-to-image&sort=trending) and [civitai](https://civitai.com/models), models with Lightning or Turbo can generate image in less than 8 steps.

For models without fp16 variant or safetensor format, add `--no-fp16` or `--no-safetensor`

```shell
sdxl 'locomotive' \
 --model RunDiffusion/Juggernaut-XL-Lightning \
 --cfg 1.5 \
 --steps 6 \
 --size 832x1216 \
 --scheduler 'DPM++ SDE' \
 --no-fp16 --no-safetensor
```

To use models downloaded from civitai:

```shell
sdxl 'locomotive' --model ./model.safetensors
```

### Loras

Loras are like plugins for the base model, multiple loras can be used:

```shell
sdxl 'locomotive' \
 --model SG161222/RealVisXL_V4.0_Lightning \
 --steps 8 \
 --size 1024x576 \
 --loras ./lora1.safetensors ./lora2.safetensors:0.8 \
```

### Speed Up Generation

Using `--lcm`, `--tcd`, `--hyper` or `--lightning` to speed up generation, not necessary for turbo/lightning models:

```shell
sdxl 'locomotive' \
 --model SG161222/RealVisXL_V4.0 \
 --steps 4 \
 --size 1024x576 \
 --tcd 1 \
```

## More Controlling

### Canny

```shell
sdxl 'protrait of a man' --canny photo.jpg --canny-low 100 --canny-high 200
```

### Depth

```shell
sdxl 'protrait of a man' --depth photo.jpg
```

### Pose

```shell
sdxl 'protrait of a man' --pose photo.jpg
```

### Inpainting

```shell
sdxl 'helmet' \
 --inpaint test/tesla.webp \
 --inpaint-mask mask.png \
 --steps 40 \
 -i \
 -o output/preview.png
```

Open mask.png, paint the area to be modified, close image editor, then press Enter to start inpainting.

## Style and Face

### Photo Maker

```shell
pip install 'sd-tools[photomaker]'
```

use `img` to indicate the reference target

```shell
sdxl 'man img holding a toy car' \
 --model Lykon/dreamshaper-xl-lightning \
 --steps 6 \
 --cfg 2 \
 --photo-maker test/tesla.webp \
 --scheduler 'DPM++ SDE Karras'
```

multiple reference images can be provided:

`--photo-maker 1.png 2.png`

### IP-Adapter Plus

style reference, multiple images can be used:

```shell
sdxl 'portrait of a man' \
 --model Lykon/dreamshaper-xl-lightning \
 --scheduler 'DPM++ SDE Karras' \
 --steps 8 --size 1024x576 \
 --ipa-plus test/ghibli \
 --ipa-plus-scale 0.7 \
 --seed 0
```

face reference, multiple images can be used:

```shell
sdxl 'portrait of a man' \
 --model Lykon/dreamshaper-xl-lightning \
 --scheduler 'DPM++ SDE Karras' \
 --steps 8 --size 1024x576 \
 --ipa-plus-face test/tesla-s.webp \
 --ipa-plus-scale 0.4 \
 --seed 0
```

combined

```shell
sdxl 'portrait of a man' \
 --model Lykon/dreamshaper-xl-lightning \
 --scheduler 'DPM++ SDE Karras' \
 --steps 8 --size 1024x576 \
 --ipa-plus test/ghibli \
 --ipa-plus-face test/tesla-s.webp \
 --ipa-plus-scale 0.7 0.4 \
 --cfg 2 \
 --seed 0
```

### IP-Adapter FaceID Plus

```shell
pip install 'sd-tools[faceid]'
```

```shell
sdxl 'man walking on the moon' \
 --model Lykon/dreamshaper-xl-lightning \
 --scheduler 'DPM++ SDE Karras' \
 --steps 6 \
 --cfg 2 \
 --ipa-faceid-plus test/tesla.webp
```

### InstantID

```shell
pip install 'sd-tools[faceid]'
```

```shell
sdxl 'man walking on the moon' \
 --model Lykon/dreamshaper-xl-lightning \
 --scheduler 'DPM++ SDE Karras' \
 --steps 6 \
 --cfg 2 \
 --instantid test/tesla.webp
```

### IP Composition Adapeter

```shell
sdxl 'Arnold Schwarzenegger' \
 --model Lykon/dreamshaper-xl-lightning \
 --scheduler 'DPM++ SDE Karras' \
 --steps 6 \
 --cfg 1.2 \
 --ip-composition test/tesla.webp
```

## HTTP Server

```shell
sdxl 'man walking on the moon' --listen 127.0.0.1:8800
```

Invoking using curl:

```shell
curl '127.0.0.1:8800?prompt=shell&seed=1' > image.webp
```

## Live Preview

```shell
sdxl 'locomotive' --size 512 -i -o output/preview.png
```

Open output folder in Finder, switch to gallery mode, once generated, image preview will be updated.

You can even set a count to generate more images:

```shell
> locomotive count=3
```

To keep the generated images, pass an additional ouput path:

```shell
sdxl 'locomotive' --size 512 -i -o output/preview.png 'output/{seed}.webp'
```

## More Examples

### Realvis

```shell
sdxl 'portrait of a woman img, chinese paint style' \
 --model SG161222/RealVisXL_V4.0_Lightning \
 --steps 6 --size 768x1024 \
 --scheduler 'DPM++ SDE Karras' \
 --cfg 2
```

### DreamShaper

```shell
sdxl 'locomotive comming' \
 --model Lykon/dreamshaper-xl-lightning \
 --steps 6 --size 1024x576 \
 --scheduler 'DPM++ SDE Karras' \
 --cfg 2
```

### Juggernaut

```shell
sdxl 'portrait of a woman, chinese painting style, Full Body Shot' \
 --model RunDiffusion/Juggernaut-XL-Lightning \
 --cfg 1.9 \
 --steps 6 \
 --size 832x1216 \
 --scheduler 'DPM++ SDE' \
 --no-fp16 --no-safetensor
```

## SD 1.5

```shell
sd -h
```

### IP-Adapeter FaceID Portrait

```shell
sd 'portrait of man, masterpiece' \
 --model Lykon/dreamshaper-8 \
 --steps 8 \
 --lcm 1 \
 --ipa-portrait photo1.png photo2.png \
 -i
```

### IP-Adapter Plus

```shell
sd 'man walking down the street' \
 --model Lykon/dreamshaper-8 \
 --steps 10 \
 --size 760 \
 --ipa-plus-scale 0.8 \
 --ipa-plus-face test/tesla-s.webp \
 --lcm 1
```

### IP-Adapter Plus Face

```shell
sd 'man in nature' \
 --model Lykon/dreamshaper-8 \
 --steps 10 \
 --size 760 \
 --ipa-plus-scale 0.8 \
 --ipa-plus test/ghibli \
 --lcm 1
```

### IP Composition Adapeter

```shell
sd 'Arnold Schwarzenegger' \
 --model Lykon/dreamshaper-8 \
 --steps 10 \
 --lcm 1 \
 --seed 4 \
 --ip-composition test/tesla.webp
```

### Sketch to Image

[image2image-turbo](https://github.com/GaParmar/img2img-turbo?tab=readme-ov-file)

```shell
sd 'ethereal fantasy concept art of cat, magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy' \
  --sketch sketch.png -i -o output/preview.webp
```

### SDXS

[SDXS: Real-Time One-Step Latent Diffusion Models with Image Conditions](https://arxiv.org/abs/2403.16627)

```shell
sd --model zweifisch/sdxs-512-0.9-fp16 'chihuahua' --steps 1 --count 10
```

### YOSO

[You Only Sample Once](https://www.arxiv.org/abs/2403.12931)

```shell
sd --model 'SG161222/Realistic_Vision_V6.0_B1_noVAE' 'chihuahua' --steps 2 --no-fp16 --no-safetensor --yoso 1 --count 10 --cfg 1
```
