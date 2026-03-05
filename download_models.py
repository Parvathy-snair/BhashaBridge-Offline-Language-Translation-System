import os
import zipfile
import requests
from tqdm import tqdm

# Paths
base_dir = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator"
models = {
    "opus-mt-en-hi": "https://huggingface.co/Helsinki-NLP/opus-mt-en-hi/resolve/main/pytorch_model.bin",
    "opus-mt-hi-en": "https://huggingface.co/Helsinki-NLP/opus-mt-hi-en/resolve/main/pytorch_model.bin",
}

# Each model also needs its config + tokenizer files
extra_files = [
    "config.json",
    "source.spm",
    "target.spm",
    "vocab.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
]

def download_file(url, dest):
    """Download a file with a progress bar."""
    r = requests.get(url, stream=True)
    total = int(r.headers.get('content-length', 0))
    with open(dest, 'wb') as f, tqdm(
        desc=os.path.basename(dest),
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

def download_model(model_name):
    model_dir = os.path.join(base_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)

    print(f"\n⬇️ Downloading {model_name} ...")

    # 1️⃣ Download pytorch model file
    model_url = models[model_name]
    model_path = os.path.join(model_dir, "pytorch_model.bin")
    if not os.path.exists(model_path):
        download_file(model_url, model_path)
    else:
        print("✅ pytorch_model.bin already exists.")

    # 2️⃣ Download other required files
    for file_name in extra_files:
        url = f"https://huggingface.co/Helsinki-NLP/{model_name}/resolve/main/{file_name}"
        dest = os.path.join(model_dir, file_name)
        if not os.path.exists(dest):
            try:
                download_file(url, dest)
            except Exception as e:
                print(f"⚠️ Could not download {file_name}: {e}")
        else:
            print(f"✅ {file_name} already exists.")

    print(f"🎉 {model_name} downloaded successfully.\n")


if __name__ == "__main__":
    for model in models:
        download_model(model)

    print("\n✅ All translation models downloaded to:")
    print(base_dir)
