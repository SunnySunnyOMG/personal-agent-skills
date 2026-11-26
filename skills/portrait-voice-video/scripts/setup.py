"""Install the pinned arm64 Metal release and a single Q8 checkpoint locally."""
import hashlib
import os
from pathlib import Path
import subprocess

ROOT = Path(os.environ.get('PORTRAIT_VOICE_RUNTIME', Path(__file__).resolve().parent / '.runtime')).resolve()
WEIGHTS = 'https://huggingface.co/audio-cpp/SoulX-FlashHead-GGUF/resolve/cc83157045008de647a4ba11ca5ed19e66caa575/SoulX-FlashHead-Lite-Q8_0.gguf?download=true'
BINARY = 'https://github.com/0xShug0/audio.cpp/releases/download/v0.9.6/audio-v0.9.6-bin-macos-arm64-metal.tar.gz'
MODEL_SHA256 = '29f186f666a4b1ee8af257a2163d521545d94c600c46d97998c57d6fefc95751'
BINARY_SHA256 = '11848bf10d1142f18ec852051ff8dcd90c12b65b95e6f902b487bae565e3dfe0'


def verified_download(url, name, size, expected):
    path = ROOT / name
    if not path.is_file() or path.stat().st_size < size:
        subprocess.run(['curl', '--fail', '--location', '--retry', '3', '-C', '-', url, '-o', str(path)], check=True)
    sha = hashlib.sha256()
    with path.open('rb') as asset:
        for block in iter(lambda: asset.read(4 * 1024 * 1024), b''):
            sha.update(block)
    if sha.hexdigest() != expected:
        raise ValueError(f'Integrity check failed for {path}')
    return path


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=True)
    runtime = verified_download(BINARY, 'audio.tar.gz', 40423741, BINARY_SHA256)
    (ROOT / 'bin').mkdir(exist_ok=True)
    subprocess.run(['tar', '-xzf', str(runtime), '-C', str(ROOT / 'bin')], check=True)
    verified_download(WEIGHTS, 'flashhead-q8.gguf', 2850631296, MODEL_SHA256)
