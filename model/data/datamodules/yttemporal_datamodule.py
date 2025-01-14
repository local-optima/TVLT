from TVLT.model.data.datasets import YTTemporalDataset
from .datamodule_base import BaseDataModule


class YTTemporalDataModule(BaseDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def dataset_cls(self):
        return YTTemporalDataset

    @property
    def dataset_cls_no_false(self):
        return YTTemporalDataset

    @property
    def dataset_name(self):
        return "yttemporal"
