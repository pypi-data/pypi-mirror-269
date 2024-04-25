import os
from typing import Union, Optional

from dliswriter.file import DLISFile
from dliswriter.logical_record import eflr_types
from dliswriter.utils.enums import FrameIndexType

from tests.dlis_files_for_testing.common import make_df


def _add_channels(df: DLISFile, data_dict: dict, channel_kwargs: Optional[dict] = None) \
        -> tuple[eflr_types.ChannelItem, ...]:

    channel_kwargs = channel_kwargs or {}

    channels = []
    for key, value in data_dict.items():
        ch = df.add_channel(
            name=key,
            data=value,
            **channel_kwargs.get(key, {})
        )
        channels.append(ch)

    return tuple(channels)


def write_dlis_from_dict(fname: Union[str, os.PathLike[str]], data_dict: dict,
                         channel_kwargs: Optional[dict] = None) -> None:
    df = make_df()

    channels = _add_channels(df, data_dict=data_dict, channel_kwargs=channel_kwargs)
    df.add_frame("MAIN", index_type=FrameIndexType.VERTICAL_DEPTH, channels=channels)

    df.write(fname)
