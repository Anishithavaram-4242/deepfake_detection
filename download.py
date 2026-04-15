import argparse
import os
import urllib.request
import json
from tqdm import tqdm
import random   # ✅ ADDED

BASE_URL = "http://kaldir.vc.in.tum.de/faceforensics/v3/"

DATASETS = {
    "original": "original_sequences/youtube",
    "Deepfakes": "manipulated_sequences/Deepfakes",
    "FaceSwap": "manipulated_sequences/FaceSwap",
    "Face2Face": "manipulated_sequences/Face2Face"
}

def download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--compression", default="c23")
    parser.add_argument("--num_videos", type=int, default=50)
    args = parser.parse_args()

    dataset_path = DATASETS[args.dataset]

    print("Downloading:", args.dataset)

    filelist_url = BASE_URL + "misc/filelist.json"
    file_pairs = json.loads(urllib.request.urlopen(filelist_url).read().decode())

    filelist = []
    for pair in file_pairs:
        if args.dataset == "original":
            filelist += pair
        else:
            filelist.append("_".join(pair))

    # ✅ FIX (RANDOM SELECTION)
    random.shuffle(filelist)
    filelist = filelist[:args.num_videos]

    for fname in tqdm(filelist):
        video_url = "{}/{}/{}/videos/{}.mp4".format(
            BASE_URL.rstrip("/"),
            dataset_path,
            args.compression,
            fname
        )

        save_path = os.path.join(
            args.output_path,
            dataset_path,
            args.compression,
            "videos",
            fname + ".mp4"
        )

        download_file(video_url, save_path)

    print("Done:", args.dataset)

if __name__ == "__main__":
    main()
