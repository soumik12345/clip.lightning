import os
import wandb
import pandas as pd

from .base import ImageRetrievalDataset


class Flickr8kDataset(ImageRetrievalDataset):
    def __init__(self, artifact_id: str, tokenizer=None, max_length: int = 100) -> None:
        super().__init__(artifact_id, tokenizer, max_length)

    def fetch_dataset(self):
        if wandb.run is None:
            api = wandb.Api()
            artifact = api.artifact(self.artifact_id, type="dataset")
        else:
            artifact = wandb.use_artifact(self.artifact_id, type="dataset")
        artifact_dir = artifact.download()
        annotations = pd.read_csv(os.path.join(artifact_dir, "captions.txt"))
        image_files = [
            os.path.join(artifact_dir, "Images", image_file)
            for image_file in annotations["image"].to_list()
        ]
        for image_file in image_files:
            assert os.path.isfile(image_file)
        captions = annotations["caption"].to_list()
        return image_files, captions
