from huggingface_hub.repocard import hf_hub_download
import torch
import json
import struct
from argparse import ArgumentParser
from safetensors.torch import save_file
import operator as op
from functools import reduce

def pt2st():

    parser = ArgumentParser('pt to safetensors')
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--output', '-o', type=str)
    args = parser.parse_args()

    save_file(torch.load(args.input), args.output)

def st_inspect():

    parser = ArgumentParser('safetensor inspect')
    parser.add_argument('--file', type=str)
    parser.add_argument('--hf', type=str)
    args = parser.parse_args()

    path = args.file
    if args.hf:
        ns, project, filename = args.hf.split('/', 2)
        path = hf_hub_download(repo_id=f"{ns}/{project}", filename=filename, local_files_only=True)

    with open(path, 'rb') as f:
        files = json.loads(f.read(struct.unpack('<Q', f.read(8))[0]).decode())
        for k, v in files.items():
            if not v.get('shape'): continue
            print(k, reduce(op.mul, v['shape'], 1), 'x'.join(map(str, v['shape'])))

def to_fp16():

    parser = ArgumentParser('save model as fp16')
    parser.add_argument('model', type=str)
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    from diffusers import AutoPipelineForText2Image
    pipe = AutoPipelineForText2Image.from_pretrained(args.model, torch_dtype=torch.float16)

    pipe.save_pretrained(args.output, variant='fp16')

def hf_path():

    parser = ArgumentParser('get hf cache path')
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    ns, project, filename = args.file.split('/', 2)
    print(hf_hub_download(repo_id=f"{ns}/{project}", filename=filename, local_files_only=True))
