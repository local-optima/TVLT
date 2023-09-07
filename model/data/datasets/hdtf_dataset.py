from .base_video_dataset import BaseVideoDataset
import os
import re
import random
import cv2
import json


class HDTFDataset(BaseVideoDataset):
    def __init__(self, *args, split="", **kwargs):
        self.split = split
        self.keys = None
        self.videos = []
        self.person_videos = {}
        super().__init__(*args, **kwargs)  

    def _load_metadata(self):
        print("loading metadata for hdtf")
        self.root_dir = os.path.join(self.metadata_dir, 'hdtf/')
        self.load_videos(self.root_dir)
        
        # 构建包含视频元数据的字典
        self.metadata = {}

        if self.split == 'train':
            metadata_file = os.path.join(self.metadata_dir, 'hdtf_train.json')
        else:
            metadata_file = os.path.join(self.metadata_dir, 'hdtf_val.json')

        if os.path.exists(metadata_file):
            # 从文件中读取 self.metadata
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            for video_name in self.videos:
                video_path = os.path.join(self.root_dir, video_name + ".mp4")
                person_name, video_id = self.parse_video_name(video_name)
                total_duration = self.get_video_duration(video_path)
                self.metadata[video_name] = {
                    'person_name': person_name,
                    'video_id': video_id,
                    'total_duration': total_duration
                }

            # 将 self.metadata 保存到对应的 json 文件
            with open(metadata_file, 'w') as f:
                json.dump(self.metadata, f)
            
    def load_videos(self, root_dir):
        video_files = os.listdir(root_dir)
        if self.split == 'train':
            video_files = video_files[:int(len(video_files) * 0.9)]
        else:
            video_files = video_files[-int(len(video_files) * 0.1):]
                    
        for video_file in video_files:
            if video_file.endswith(".mp4"):
                video_name = os.path.splitext(video_file)[0]
                self.videos.append(video_name)
                person_name, video_id = self.parse_video_name(video_name)
                if person_name in self.person_videos:
                    self.person_videos[person_name].append(video_id)
                else:
                    self.person_videos[person_name] = [video_id]

    def parse_video_name(self, video_name):
        # 解析视频名称，提取人物和视频编号
        match = re.match(r"(\w+)_(.+?)_(\d+)", video_name)
        person_name = match.group(1) + "_" + match.group(2)
        video_id = match.group(3)
        return person_name, video_id


    def get_video_duration(self, video_path):
        # 使用OpenCV获取视频的总帧数和帧率
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        # 计算视频的总时长
        total_duration = total_frames / fps

        return total_duration

    def __len__(self):
        return len(self.keys) * 100

    def __getitem__(self, index):
        # 构建result字典，包含正样本和负样本的表示
        result = {}
        
        video_name = self.keys[index % len(self.keys)]
        video_path = os.path.join(self.root_dir, video_name + ".mp4")

        # 构建正样本时间戳
        positive_timestamp = self.get_random_time_stamp(video_name)

        # 调用self._get_video_audio方法获取正样本视频和音频的表示
        positive_result = self._get_video_audio(index, video_path, positive_timestamp)
        
        # 将正样本的表示添加到result中
        result.update(positive_result)
        
        for i in range(self.draw_false_video):
            # 随机选择一个不是当前人物的视频
            person_name = self.parse_video_name(video_name)[0]
            negative_video_name = self.get_random_negative_video_name(person_name)
            negative_video_path = os.path.join(self.root_dir, negative_video_name + ".mp4")
            
            # 构建负样本时间戳
            negative_timestamp = self.get_random_time_stamp(negative_video_name)

            # 获取负样本视频的表示
            negative_result = self._get_false_video(i, negative_video_path, negative_timestamp)
            
            # 将负样本的表示添加到result中
            result.update(negative_result)

        return result

    def get_random_time_stamp(self, video_name):
        # 获取视频的总时长
        total_duration = self.metadata[video_name]['total_duration']
        
        # 随机选择正样本片段的开始和结束时间
        start = random.uniform(0, total_duration - 1)  # 片段开始时间
        end = random.uniform(start + 1, total_duration - 1)  # 片段结束时间

        if not 0 <= start < end < total_duration:
            print(f"start: {start}, end: {end}")
        
        # 构建正样本时间戳
        return [start, end]

    def get_random_negative_video_name(self, current_person):
        # 随机选择一个不是当前人物的视频
        person_names = list(self.person_videos.keys())
        person_names.remove(current_person)
        random_person = random.choice(person_names)
        random_videos = self.person_videos[random_person]
        random_video = random.choice(random_videos)
        return f"{random_person}_{random_video}"
