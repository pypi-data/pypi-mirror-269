from cached_path import cached_path


import torch

torch.manual_seed(0)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

import random

random.seed(0)

import numpy as np

np.random.seed(0)


# load packages
import time
import random
import yaml
from munch import Munch
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import torchaudio
import librosa


from mfs_styletts2.models import *
from mfs_styletts2.utils import *
from mfs_styletts2.text_utils import TextCleaner

textclenaer = TextCleaner()


device = "cuda" if torch.cuda.is_available() else "cpu"

to_mel = torchaudio.transforms.MelSpectrogram(
    n_mels=80, n_fft=2048, win_length=1200, hop_length=300
)
mean, std = -4, 4


def length_to_mask(lengths):
    mask = (
        torch.arange(lengths.max())
        .unsqueeze(0)
        .expand(lengths.shape[0], -1)
        .type_as(lengths)
    )
    mask = torch.gt(mask + 1, lengths.unsqueeze(1))
    return mask


def preprocess(wave):
    wave_tensor = torch.from_numpy(wave).float()
    mel_tensor = to_mel(wave_tensor)
    mel_tensor = (torch.log(1e-5 + mel_tensor.unsqueeze(0)) - mean) / std
    return mel_tensor


def compute_style(ref_dicts):
    reference_embeddings = {}
    for key, path in ref_dicts.items():
        wave, sr = librosa.load(path, sr=24000)
        audio, index = librosa.effects.trim(wave, top_db=30)
        if sr != 24000:
            audio = librosa.resample(audio, sr, 24000)
        mel_tensor = preprocess(audio).to(device)

        with torch.no_grad():
            ref = model.style_encoder(mel_tensor.unsqueeze(1))
        reference_embeddings[key] = (ref.squeeze(1), audio)

    return reference_embeddings


# load phonemizer
from openphonemizer import OpenPhonemizer

phonemizer = OpenPhonemizer()


config = yaml.safe_load(open(str(cached_path('hf://yl4579/StyleTTS2-LJSpeech/Models/LJSpeech/config.yml'))))

# load pretrained ASR model
ASR_config = str(cached_path('https://raw.githubusercontent.com/yl4579/StyleTTS2/main/Utils/ASR/config.yml'))
ASR_path = str(cached_path('https://github.com/yl4579/StyleTTS2/raw/main/Utils/ASR/epoch_00080.pth'))
text_aligner = load_ASR_models(ASR_path, ASR_config)

# load pretrained F0 model
F0_path = str(cached_path('https://github.com/yl4579/StyleTTS2/raw/main/Utils/JDC/bst.t7'))
pitch_extractor = load_F0_models(F0_path)

# load BERT model
from .Utils.PLBERT.util import load_plbert

plbert = load_plbert()

model = build_model(
    recursive_munch(config["model_params"]), text_aligner, pitch_extractor, plbert
)
_ = [model[key].eval() for key in model]
_ = [model[key].to(device) for key in model]

# params_whole = torch.load("Models/LJSpeech/epoch_2nd_00100.pth", map_location='cpu')
params_whole = torch.load(
    str(
        cached_path(
            "hf://yl4579/StyleTTS2-LJSpeech/Models/LJSpeech/epoch_2nd_00100.pth"
        )
    ),
    map_location="cpu",
)
params = params_whole["net"]

for key in model:
    if key in params:
        try:
            model[key].load_state_dict(params[key])
        except:
            from collections import OrderedDict

            state_dict = params[key]
            new_state_dict = OrderedDict()
            for k, v in state_dict.items():
                name = k[7:]  # remove `module.`
                new_state_dict[name] = v
            # load params
            model[key].load_state_dict(new_state_dict, strict=False)
#             except:
#                 _load(params[key], model[key])
_ = [model[key].eval() for key in model]

from .Modules.diffusion.sampler import DiffusionSampler, ADPM2Sampler, KarrasSchedule

sampler = DiffusionSampler(
    model.diffusion.diffusion,
    sampler=ADPM2Sampler(),
    sigma_schedule=KarrasSchedule(
        sigma_min=0.0001, sigma_max=3.0, rho=9.0
    ),  # empirical parameters
    clamp=False,
)


def inference(text, noise, diffusion_steps=5, embedding_scale=1):
    text = text.strip()
    text = text.replace('"', "")
    ps = phonemizer(text)

    tokens = textclenaer(ps)
    tokens.insert(0, 0)
    tokens = torch.LongTensor(tokens).to(device).unsqueeze(0)

    with torch.no_grad():
        input_lengths = torch.LongTensor([tokens.shape[-1]]).to(tokens.device)
        text_mask = length_to_mask(input_lengths).to(tokens.device)

        t_en = model.text_encoder(tokens, input_lengths, text_mask)
        bert_dur = model.bert(tokens, attention_mask=(~text_mask).int())
        d_en = model.bert_encoder(bert_dur).transpose(-1, -2)

        s_pred = sampler(
            noise,
            embedding=bert_dur[0].unsqueeze(0),
            num_steps=diffusion_steps,
            embedding_scale=embedding_scale,
        ).squeeze(0)

        s = s_pred[:, 128:]
        ref = s_pred[:, :128]

        d = model.predictor.text_encoder(d_en, s, input_lengths, text_mask)

        x, _ = model.predictor.lstm(d)
        duration = model.predictor.duration_proj(x)
        duration = torch.sigmoid(duration).sum(axis=-1)
        pred_dur = torch.round(duration.squeeze()).clamp(min=1)

        pred_dur[-1] += 5

        pred_aln_trg = torch.zeros(input_lengths, int(pred_dur.sum().data))
        c_frame = 0
        for i in range(pred_aln_trg.size(0)):
            pred_aln_trg[i, c_frame : c_frame + int(pred_dur[i].data)] = 1
            c_frame += int(pred_dur[i].data)

        # encode prosody
        en = d.transpose(-1, -2) @ pred_aln_trg.unsqueeze(0).to(device)
        F0_pred, N_pred = model.predictor.F0Ntrain(en, s)
        out = model.decoder(
            (t_en @ pred_aln_trg.unsqueeze(0).to(device)),
            F0_pred,
            N_pred,
            ref.squeeze().unsqueeze(0),
        )

    return out.squeeze().cpu().numpy()


def LFinference(
    text, s_prev, noise, alpha=0.7, diffusion_steps=5, embedding_scale=1, phonemize=True
):
    text = text.strip()
    text = text.replace('"', "")
    text = text.replace("``", '"')
    text = text.replace("''", '"')
    if phonemize:
        ps = phonemizer(text)
    else:
        ps = text

    tokens = textclenaer(ps)
    tokens.insert(0, 0)
    tokens = torch.LongTensor(tokens).to(device).unsqueeze(0)

    with torch.no_grad():
        input_lengths = torch.LongTensor([tokens.shape[-1]]).to(tokens.device)
        text_mask = length_to_mask(input_lengths).to(tokens.device)

        t_en = model.text_encoder(tokens, input_lengths, text_mask)
        bert_dur = model.bert(tokens, attention_mask=(~text_mask).int())
        d_en = model.bert_encoder(bert_dur).transpose(-1, -2)

        s_pred = sampler(
            noise,
            embedding=bert_dur[0].unsqueeze(0),
            num_steps=diffusion_steps,
            embedding_scale=embedding_scale,
        ).squeeze(0)

        if s_prev is not None:
            # convex combination of previous and current style
            s_pred = alpha * s_prev + (1 - alpha) * s_pred

        s = s_pred[:, 128:]
        ref = s_pred[:, :128]

        d = model.predictor.text_encoder(d_en, s, input_lengths, text_mask)

        x, _ = model.predictor.lstm(d)
        duration = model.predictor.duration_proj(x)
        duration = torch.sigmoid(duration).sum(axis=-1)
        pred_dur = torch.round(duration.squeeze()).clamp(min=1)

        pred_aln_trg = torch.zeros(input_lengths, int(pred_dur.sum().data))
        c_frame = 0
        for i in range(pred_aln_trg.size(0)):
            pred_aln_trg[i, c_frame : c_frame + int(pred_dur[i].data)] = 1
            c_frame += int(pred_dur[i].data)

        # encode prosody
        en = d.transpose(-1, -2) @ pred_aln_trg.unsqueeze(0).to(device)
        F0_pred, N_pred = model.predictor.F0Ntrain(en, s)
        out = model.decoder(
            (t_en @ pred_aln_trg.unsqueeze(0).to(device)),
            F0_pred,
            N_pred,
            ref.squeeze().unsqueeze(0),
        )

    return out.squeeze().cpu().numpy(), s_pred
