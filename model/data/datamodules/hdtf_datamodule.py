from TVLT.model.data.datasets import HDTFDataset
from .datamodule_base import BaseDataModule


class HDTFDataModule(BaseDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def dataset_cls(self):
        return HDTFDataset

    @property
    def dataset_cls_no_false(self):
        return HDTFDataset

    @property
    def dataset_name(self):
        return "hdtf"
