from .howto100m_datamodule import Howto100mDataModule
from .yttemporal_datamodule import YTTemporalDataModule
from .vqa_datamodule import VQADataModule
from .mosei_datamodule import MOSEIDataModule
from .moseiemo_datamodule import MOSEIEMODataModule
from .msrvtt_datamodule import MsrvttDataModule
from .hdtf_datamodule import HDTFDataModule

_datamodules = {
    "howto100m": Howto100mDataModule,
    "yttemporal": YTTemporalDataModule,
    "vqa": VQADataModule,
    "mosei": MOSEIDataModule,
    "moseiemo": MOSEIEMODataModule,
    "msrvtt": MsrvttDataModule,
    "hdtf": HDTFDataModule,
}
