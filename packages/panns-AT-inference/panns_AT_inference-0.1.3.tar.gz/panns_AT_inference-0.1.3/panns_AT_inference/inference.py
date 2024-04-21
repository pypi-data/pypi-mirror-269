import os
import numpy as np
import argparse
import librosa
import matplotlib.pyplot as plt
import torch
from pathlib import Path

from .pytorch_utils import move_data_to_device
from .models import Cnn14, ResNet38, Wavegram_Logmel_Cnn14
from .config import labels, classes_num


def create_folder(fd):
    if not os.path.exists(fd):
        os.makedirs(fd)
        
        
def get_filename(path):
    path = os.path.realpath(path)
    na_ext = path.split('/')[-1]
    na = os.path.splitext(na_ext)[0]
    return na


class AudioTagging(object):
    def __init__(self, model_name=None, device='cuda'):
        """Audio tagging inference wrapper.
        """
        checkpoint_path = None
        
        if model_name in ['Cnn14', None]:
            checkpoint_path='{}/panns_data/Cnn14_mAP=0.431.pth'.format(str(Path.home()))
        elif model_name == 'ResNet38':
            checkpoint_path='{}/panns_data/ResNet38_mAP=0.434.pth'.format(str(Path.home()))
        elif model_name == 'Wavegram_Logmel_Cnn14':
            checkpoint_path='{}/panns_data/Wavegram_Logmel_Cnn14_mAP=0.439.pth'.format(str(Path.home()))
        print('Checkpoint path: {}'.format(checkpoint_path))      
    
        if not os.path.exists(checkpoint_path) or os.path.getsize(checkpoint_path) < 3e8:
            create_folder(os.path.dirname(checkpoint_path))
            if model_name in ['Cnn14', None]:            
                zenodo_path = 'https://zenodo.org/record/3987831/files/Cnn14_mAP%3D0.431.pth?download=1'
            elif model_name == 'ResNet38':
                zenodo_path = 'https://zenodo.org/records/3987831/files/ResNet38_mAP%3D0.434.pth?download=1'
            elif model_name == 'Wavegram_Logmel_Cnn14':
                zenodo_path = 'https://zenodo.org/records/3987831/files/Wavegram_Logmel_Cnn14_mAP%3D0.439.pth?download=1'
            os.system('wget -O "{}" "{}"'.format(checkpoint_path, zenodo_path))

        if device == 'cuda' and torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        
        self.labels = labels
        self.classes_num = classes_num

        # Model
        if model_name in ['Cnn14', None]:
            self.model = Cnn14(sample_rate=32000, window_size=1024, hop_size=320, 
                               mel_bins=64, fmin=50, fmax=14000, 
                               classes_num=self.classes_num)
        elif model_name == 'ResNet38':
            self.model = ResNet38(sample_rate=32000, window_size=1024, hop_size=320, 
                                  mel_bins=64, fmin=50, fmax=14000, 
                                  classes_num=self.classes_num)
        elif model_name == 'Wavegram_Logmel_Cnn14':
            self.model = Wavegram_logmel_Cnn14(sample_rate=32000, window_size=1024, hop_size=320, 
                                               mel_bins=64, fmin=50, fmax=14000, 
                                               classes_num=self.classes_num)
        
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model'])

        # Parallel
        if 'cuda' in str(self.device):
            self.model.to(self.device)
            print('GPU number: {}'.format(torch.cuda.device_count()))
            self.model = torch.nn.DataParallel(self.model)
        else:
            print('Using CPU.')

    def inference(self, audio):
        audio = move_data_to_device(audio, self.device)

        with torch.no_grad():
            self.model.eval()
            output_dict = self.model(audio, None)

        clipwise_output = output_dict['clipwise_output'].data.cpu().numpy()
        embedding = output_dict['embedding'].data.cpu().numpy()

        return clipwise_output, embedding
