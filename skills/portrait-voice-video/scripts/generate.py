"""Generate an audio-driven full-frame portrait using the local audio.cpp Metal port."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from setup import MODEL_SHA256
import resource
import re
import subprocess
import tempfile
import time

ROOT = Path(os.environ.get('PORTRAIT_VOICE_RUNTIME', Path(__file__).resolve().parent / '.runtime')).resolve()


def run(image, audio, out, size, backend, steps):
    out.mkdir(parents=True, exist_ok=True)
    info = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-of', 'json', '-show_entries', 'format=duration', str(audio)
    ]))
    length = float(info['format']['duration'])
    with tempfile.TemporaryDirectory(prefix='.flashhead-',dir=out) as working:
        work = Path(working)
        mono = work / 'voice-16k.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(audio), '-ac', '1', '-ar', '16000', str(mono)], check=True)
        command = [str(ROOT / 'bin/audiocpp_cli'), '--family', 'soulx_flashhead', '--task', 'gen',
                   '--model', str(ROOT / 'flashhead-q8.gguf'), '--backend', backend, '--threads', '6',
                   '--audio', str(mono), '--request-option', 'reference_image_file=' + str(image.resolve()),
                   '--request-option', 'height=' + str(size), '--request-option', 'width=' + str(size),
                   '--request-option', 'seed=42', '--request-option', 'num_inference_steps=' + str(steps),
                   '--out-dir', str(work), '--metrics', '--log']
        stats = out / 'memory.txt'
        command = ['/usr/bin/time','-l','-o',str(stats),*command]
        start = time.monotonic()
        with (out / 'inference.log').open('w') as log:
            process = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        inference = time.monotonic() - start
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        result = {'sourceSeconds': length, 'size': size, 'backend':backend, 'steps':steps,
                  'inferenceSeconds':round(inference, 2), 'maxRSSBytes':usage.ru_maxrss, 'exitCode':process.returncode}
        result.update(modelSHA256=MODEL_SHA256, audioCppRelease='v0.9.6', seed=42,
                      referenceSHA256=hashlib.sha256(image.read_bytes()).hexdigest(),
                      audioSHA256=hashlib.sha256(audio.read_bytes()).hexdigest())
        measured = re.search(r'([0-9]+)\s+peak memory footprint',stats.read_text())
        if measured:
            result['peakMemoryFootprintBytes'] = int(measured.group(1))
        def report():
            (out / 'run.json').write_text(json.dumps(result, indent=2) + '\n')
        report()
        if process.returncode:
            raise SystemExit('Inference failed. See ' + str(out/'inference.log'))
        chunks = sorted(work.glob('soulx_flashhead_video_*.json'), key=lambda p:int(p.stem.rsplit('_',1)[1]))
        if not chunks:
            raise ValueError('No video chunks. See ' + str(out/'inference.log'))
        # Last audio block may contain silence padding. Limit the master to the input recording length.
        temp_movie = work / 'master.mp4'
        encoder = subprocess.Popen([
            'ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'rgb24',
            '-video_size',f'{size}x{size}', '-framerate', '25','-i','pipe:0','-i',str(audio),
            '-map','0:v:0','-map','1:a:0','-t',str(length),'-c:v','libx264','-crf','16','-pix_fmt','yuv420p',
            '-c:a','aac','-b:a','160k','-movflags','+faststart',str(temp_movie)], stdin=subprocess.PIPE)
        frames = 0
        with encoder.stdin:
            for chunk in chunks:
                entry = json.loads(chunk.read_text())
                meta = entry['meta']
                payload = bytes.fromhex(entry['payload_hex'])
                count = int(meta['frames'])
                if (meta['format'],int(meta['width']),int(meta['height']),int(meta['fps'])) != ('rgb24',size,size,25):
                    raise ValueError(f'Unexpected video format in {chunk.name}')
                if len(payload) != count * size * size * 3:
                    raise ValueError('Invalid video payload length')
                needed = min(count, max(0, round(length * 25) - frames))
                if needed:
                    encoder.stdin.write(payload[:needed*size*size*3])
                frames += count
        if encoder.wait() != 0:
            raise ValueError('FFmpeg failed')
        os.replace(temp_movie, out/'presenter.mp4')
        result.update(rawFrames=frames, chunks=len(chunks), totalSeconds=round(time.monotonic()-start,2))
        report()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('audio', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--size',type=int,default=320)
    parser.add_argument('--steps',type=int,default=4)
    parser.add_argument('--backend',default='metal',choices=['metal','cpu'])
    args=parser.parse_args()
    if args.size < 32 or args.size % 32:
        parser.error('Size must be a positive multiple of 32')
    run(args.image,args.audio,args.out,args.size,args.backend,args.steps)
