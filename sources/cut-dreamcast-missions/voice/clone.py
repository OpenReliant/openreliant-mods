"""Clones a voice of the cut missions with Chatterbox and renders lines in it.

Each voice's speaker embedding is the mean of the embeddings of all its recorded lines, and its
acoustic prompt is ten seconds of its lines of two to six seconds. Both are kept in a cache folder.
"""

import os

import librosa
import numpy as np
import torch

from chatterbox.tts import ChatterboxTTS, Conditionals
from chatterbox.models.t3.modules.cond_enc import T3Cond
from chatterbox.models.s3tokenizer import S3_SR
from chatterbox.models.s3gen import S3GEN_SR

import voices


def load_model():
    return ChatterboxTTS.from_pretrained(device="mps" if torch.backends.mps.is_available() else "cpu")


def trimmed(path, rate):
    wav, _ = librosa.load(path, sr=rate)
    wav, _ = librosa.effects.trim(wav, top_db=35)
    return wav


def prepare(model, speech_dir, cache_dir, voice):
    """The voice's embedding and prompt, from the cache or made from its recorded lines."""
    os.makedirs(cache_dir, exist_ok=True)
    embed_path = os.path.join(cache_dir, f"{voice}.embed.npy")
    prompt_path = os.path.join(cache_dir, f"{voice}.prompt.npy")
    if not (os.path.exists(embed_path) and os.path.exists(prompt_path)):
        files = voices.files_of(speech_dir, voice)
        lines = [w for w in (trimmed(f, S3_SR) for f in files) if len(w) > S3_SR // 2]
        embeds = model.ve.embeds_from_wavs(lines, sample_rate=S3_SR)
        np.save(embed_path, embeds.mean(axis=0))
        prompt, total = [], 0
        by_length = sorted((trimmed(f, S3GEN_SR) for f in files), key=lambda w: abs(len(w) - 4 * S3GEN_SR))
        for wav in by_length:
            if total >= 10 * S3GEN_SR:
                break
            prompt += [wav, np.zeros(S3GEN_SR // 5, dtype=np.float32)]
            total += len(wav)
        np.save(prompt_path, np.concatenate(prompt))
    return np.load(embed_path), np.load(prompt_path)


def condition(model, embed, prompt_wav, exaggeration=0.5):
    """Makes the model speak in the voice of `embed` and `prompt_wav`."""
    ref_dict = model.s3gen.embed_ref(prompt_wav[: model.DEC_COND_LEN], S3GEN_SR, device=model.device)
    prompt_16k = librosa.resample(prompt_wav, orig_sr=S3GEN_SR, target_sr=S3_SR)
    tokens, _ = model.s3gen.tokenizer.forward([prompt_16k[: model.ENC_COND_LEN]], max_len=model.t3.hp.speech_cond_prompt_len)
    t3_cond = T3Cond(
        speaker_emb=torch.from_numpy(embed).float().unsqueeze(0).to(model.device),
        cond_prompt_speech_tokens=torch.atleast_2d(tokens).to(model.device),
        emotion_adv=exaggeration * torch.ones(1, 1, 1),
    ).to(device=model.device)
    model.conds = Conditionals(t3_cond, ref_dict)


def render(model, text, exaggeration=0.5, cfg_weight=0.5):
    """One line in the voice the model is conditioned on, at the model's rate."""
    wav = model.generate(text, exaggeration=exaggeration, cfg_weight=cfg_weight)
    return wav.squeeze(0).cpu().numpy()
