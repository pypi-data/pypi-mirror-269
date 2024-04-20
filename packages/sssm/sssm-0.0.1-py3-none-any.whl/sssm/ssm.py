import json
import scipy
import torch
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
import seaborn as sns
import pandas as pd
import mne
from utils import generate_results
from IPython.utils import io
from loguru import logger
import einops
from models.model import base_Model
from config_files import sleepEvent_Configs
from . import saved_models
from tqdm.autonotebook import tqdm
import joblib
from pandarallel import pandarallel
from glob import glob

class SSM:
    def __init__(self):
        self.model = self.__load_model()
        self.softmax = torch.nn.Softmax(dim=1)

    def predict(self):
        pass
    def plot_predictions(self):
        pass
    def to_json(self):
        pass
    def to_pandas(self):
        pass
    def __load_model(self):
        device = torch.device('cuda')
        model = base_Model(sleepEvent_Configs.Config()).to(device)
        from importlib import resources
        model_path = resources.path(saved_models,'ckp_last.pt')
        chkpoint = torch.load(model_path, map_location=device)
        pretrained_dict = chkpoint["model_state_dict"]
        model.load_state_dict(pretrained_dict)
        model.eval()
        return model

def get_data_epoch(EDF_PATH, epoch_id):
    edf_name = os.path.split(EDF_PATH)[1]
    dataset_id = str(int(edf_name.split('-')[1]))
    raw = mne.io.read_raw_edf(EDF_PATH, include=(
        ['EEG C3-CLE'] if np.isin('EEG C3-CLE', mne.io.read_raw_edf(EDF_PATH).ch_names) else ['EEG C3-LER']))
    epochs = mne.make_fixed_length_epochs(raw, duration=30)
    if epoch_id == 'all':
        return (epochs.load_data().resample(100).get_data() * 1e6).astype(np.float16)
    else:
        return (epochs[epoch_id].load_data().resample(100).get_data() * 1e6).astype(np.float16)


def prase_parameter(json_file):
    split = json_file.split('/')
    data_id = split[-2]
    dataset_id = data_id.split('-')[1][1]
    epoch_id = int(split[-1].split('.')[0])
    edf_path = f'/home/bkxcyu_arch/sdc/raw_dataset/MASS/MASS{dataset_id}/{data_id}.edf'
    return edf_path, epoch_id


def get_sample_from_json(json_file):
    edf_path, epoch_id = prase_parameter(json_file)
    with io.capture_output() as captured:
        return get_data_epoch(edf_path, epoch_id)


def predict(sample, filter_window=20):
    # sample = np.lib.stride_tricks.sliding_window_view(sample_.flatten(),(300)).reshape((-1,1,300))
    n_epoch = sample.shape[0]
    sliding_window_sample = np.lib.stride_tricks.sliding_window_view(sample, 300, axis=2)  # .reshape((-1,1,300)).shape
    sliding_window_sample = einops.rearrange(sliding_window_sample,
                                             'n_epoch n_ch n_window n_time -> (n_epoch n_window) n_ch n_time')
    with torch.no_grad():
        _sample = torch.from_numpy(sliding_window_sample).float().to(device)
        pre, fea = model(_sample)
        proba = softmax(pre).cpu().numpy()
        pre = einops.rearrange(pre, '(n_epoch n_window) n_class -> n_epoch n_window n_class', n_epoch=n_epoch)
        fea = einops.rearrange(fea, '(n_epoch n_window) n_hd n_step -> n_epoch n_window n_hd n_step', n_epoch=n_epoch)
    pred = np.argmax(proba, axis=1)
    proba = einops.rearrange(proba, '(n_epoch n_window) n_class -> n_epoch n_window n_class', n_epoch=n_epoch)
    pred = einops.rearrange(pred, '(n_epoch n_window) -> n_epoch n_window', n_epoch=n_epoch)
    pred_f = scipy.signal.medfilt(pred, [1, int(filter_window + 1)])
    return proba, pred, pred_f, pre, fea


def plot_predict(proba, pred, pred_f, ind=0, columns=None):
    proba = pd.DataFrame(proba[ind] * 100, columns=columns)
    sns.set_theme('notebook', style='ticks', palette='bright')
    ax = proba.plot(kind='area', figsize=(50, 4), alpha=0.9, stacked=True, lw=0)
    ax.set_xlim(0, proba.shape[0])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Probability")
    ax.set_xlabel("Time (0.01s)")
    # ax.plot(sample_[0,0,150:2850]/300+1.5,color='0')
    # confidence = proba.max(1)
    plt.legend(bbox_to_anchor=(0.04, 0.5))
    # plt.legend()
    plt.figure(figsize=(50, 4))
    plt.xlim(0, 2700)
    plt.plot(pred[ind] + 0.1)
    plt.yticks(range(len(labels)), labels, rotation=90)
    plt.ylabel("Label")
    plt.ylim(len(labels) - 0.5, -0.5)
    _ = plt.plot(pred_f[ind])


def plot_sample(sample, ind=0):
    plt.figure(figsize=(50, 4))
    plt.plot(sample[ind, 0, 150:2850], color='0', linewidth=0.8)
    plt.xlim(0, 2700)
    plt.ylim(-100, 100)
    plt.ylabel('Amp')


def del_pred_from_json_content(content, label='Sawtooth'):
    label_ind = []
    for i, each_pred in enumerate(content['predictions'][0]['result']):
        if each_pred['value']['timeserieslabels'][0] == label:
            label_ind.append(i)
    if len(label_ind) != 0:
        del content['predictions'][0]['result'][label_ind[0]:label_ind[-1] + 1]
    return content


def update_json(pred_f, proba, json_file, label, label_id):
    # pred_f = scipy.signal.medfilt(pred,[31])
    edf_path, epoch_id = prase_parameter(json_file)
    label_index = np.argwhere(pred_f == label_id)
    if label_index.shape[0] == 0:
        # logger.warning('there are no sawtooth')
        with open(json_file, 'r') as file:
            try:
                content = json.load(file)
                content = del_pred_from_json_content(content, label=label)
                content['predictions'][0]['score'] = 0.0
            except Exception as e:
                logger.warning(f'{e} \n in {json_file}')
                return
        with open(json_file, 'w') as file:
            json.dump(content, file, indent=2)
            return content

    last_ind = label_index[0]
    starts = [last_ind]
    ends = []
    for this_ind in label_index[1:]:
        if this_ind - last_ind == 1:
            last_ind = this_ind
        else:
            ends.append(last_ind)
            starts.append(this_ind)
            last_ind = this_ind
    ends.append(label_index[-1])
    starts = np.concatenate(starts) + 150
    ends = np.concatenate(ends) + 150

    df = pd.DataFrame({
        'Start': starts,
        'End': ends,
    })

    df['epoch_id'] = epoch_id
    df['label'] = label
    df['label_from'] = 'ssl_ft'
    df['Channel'] = 'C3'

    with open(json_file, 'r') as file:
        try:
            content = json.load(file)
        except Exception as e:
            logger.warning(f'{e} \n in {json_file}')
            return

    content = del_pred_from_json_content(content, label=label)

    for row in df.itertuples():
        res = generate_results(row.Start, row.End, row.label, row.label_from, row.Channel)
        content['predictions'][0]['result'].append(res)
    score = proba[label_index, 0].mean().item()
    content['predictions'][0]['score'] = score

    with open(json_file, 'w') as file:
        json.dump(content, file, indent=2)
    return content