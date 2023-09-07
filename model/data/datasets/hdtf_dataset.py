from .base_video_dataset import BaseVideoDataset
import os
import tqdm
import json
import random

class HDTFDataset(BaseVideoDataset):
    def __init__(self, *args, split="", **kwargs):
        self.split = split
        self.keys = None
        super().__init__(*args, **kwargs)  
        
    def __len__(self):
        return len(self.keys)
    
    def _load_metadata(self):
        print("loading metadata for hdtf")
        
        if not os.path.exists(os.path.join(self.metadata_dir, 'hdtf_train.json')):
            # captions = json.load(open(os.path.join(self.metadata_dir, 'caption.json')))           
            # new_caption = {}

            video_keys = []
            exist_videos = list(os.listdir(os.path.join(self.metadata_dir, 'hdtf/')))
            exist_videos = exist_videos * 100  # 将 exist_videos 重复 n 次构造更大的列表
            for video in exist_videos:
                video_keys += [video.split('.')[0]]
            # all_keys = video_keys
            # for key in tqdm(all_keys):
                # new_caption[key] = captions[key]

            all_samples = video_keys # list(new_caption.items())
            random.shuffle(all_samples)
            video_train = all_samples[:-10]
            video_val = all_samples[-10:]
            
            train_meta = [(key, key) for key in video_train]
            train_meta = dict(train_meta)
            
            val_meta = [(key, key) for key in video_val]
            val_meta = dict(val_meta)
            
            json.dump(train_meta, open(os.path.join(self.metadata_dir, 'hdtf_train.json'), 'w'))
            json.dump(val_meta, open(os.path.join(self.metadata_dir, 'hdtf_val.json'), 'w'))

        if self.split=='train':
            self.metadata = json.load(open(os.path.join(self.metadata_dir, 'hdtf_train.json')))
        else:
            self.metadata = json.load(open(os.path.join(self.metadata_dir, 'hdtf_val.json')))
    
    def get_suite(self, index):
        sample = self.metadata[self.keys[index]]
        # print(f'sample: {sample}')
        sample_idx = random.choice(range(len(sample['start'])))
        video_path = os.path.join(self.metadata_dir, 'hdtf/', self.keys[index]+'.mp4')
        timestamp = [sample['start'][max(sample_idx-1, 0)], sample['end'][min(sample_idx+1, len(sample['start'])-1)]] 
        
        ret = dict()     
        ret.update(self._get_video_audio(index, video_path, timestamp))
        
        for i in range(self.draw_false_video):
            random_index = random.randint(0, len(self.keys) - 1)
            sample_f = self.metadata[self.keys[random_index]]
            sample_idx_f = random.choice(range(len(sample_f['start'])))
            timestamp_f = [sample_f['start'][max(sample_idx_f-1, 0)], sample_f['end'][min(sample_idx_f+1, len(sample_f['start'])-1)]] 
            video_path_f = os.path.join(self.metadata_dir, 'hdtf/', self.keys[random_index]+'.mp4')
            ret.update(self._get_false_video(i, video_path_f, timestamp_f))
            
        return ret