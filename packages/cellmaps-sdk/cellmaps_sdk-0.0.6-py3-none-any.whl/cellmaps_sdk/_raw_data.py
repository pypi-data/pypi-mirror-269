from abc import ABC as _ABC
from typing import List as _List, Any as _Any
from ._utils import get_minio_client as _get_minio_client
from ._config import Config as _Config

# These files denote the raw data files that are associated with the experiment (that the user will upload to cdb)

# File Transformation fn's
def retrieve_txt_as_list(obj: _Any) -> _List[str]:
    """
    Retrieve text data from a MinIO object and return it as a list of strings. Done for the ChannelMarkers files, but can be used for any text file with a similar format.

    Args:
        obj (Any): The object to retrieve the text data from.

    Returns:
        List[str]: A list of strings containing the text data.

    Raises:
        Any exceptions raised by the underlying operations.

    """
    client = _get_minio_client()
    try:
        response = client.get_object(_Config._MINIO_EXPERIMENT_BUCKET, object_name=obj.object_name)
        
        data = [l.rstrip() for l in response.data.decode().split('\n') if l.rstrip() != '']
        # Read data from response.
    finally:
        response.close()
        response.release_conn()

    return data

# this on the object level
class _File:
    """
    Represents a file with its regular expression and CDB file tag.

    Attributes:
        file_regex (str): The regular expression used to match the file.
        cdb_file_tag (str): The CDB file tag associated with the file.
    """

    def __init__(self, file_regex, cdb_file_tag,transformation_fn=None):
        self.file_regex: str = file_regex
        self.cdb_file_tag: str = cdb_file_tag
        self.transformation_fn = transformation_fn

class _RAW(_ABC):
    """
    Represents a base class for RAW data.

    Attributes:
        experiment_tag (str): The experiment tag associated with the RAW data.
        files (List[File]): A list of File objects representing the RAW data files.
    """

    experiment_tag: str
    files: _List[_File]

    def __init__(self):
        self.check_variables()

    @classmethod
    def check_variables(cls):
        """
        Check if all required variables are present in the child class.

        Raises:
            Exception: If any required variables are missing.
        """
        super_set = set(_RAW.__dict__['__annotations__'].keys())
        sub_set = set({k:v for k,v in cls.__dict__.items() if not k.startswith('__') and not k.startswith('_')}.keys())
        
        diff = super_set.difference(sub_set)

        if diff:
            raise Exception(f"Missing required variables: {', '.join(diff)}")
        
class RAW_TMA(_RAW):
    """
    A class representing RAW data for TMA experiments.
    
    Attributes:
        experiment_tag (str): The experiment tag for TMA.
        files (list): A list of File objects representing the files associated with TMA experiments.
    """
    experiment_tag = 'TMA'
    files = [_File(file_regex = r'^[\w,\s-]+(?:\.tiff|\.tif|\.ome.tiff|\.qptiff)', cdb_file_tag = 'tiff_name'),
            _File(file_regex = r"\S*.txt", cdb_file_tag= 'channel_markers',transformation_fn=retrieve_txt_as_list)]


class RAW_WSI(_RAW):
    """
    Represents a Whole Slide Image (WSI) in the RAW format.

    Attributes:
        experiment_tag (str): The experiment tag for the WSI.
        files (list): A list of File objects representing the files associated with the WSI.
    """
    experiment_tag = 'WSI'
    files = [_File(file_regex = r'^[\w,\s-]+(?:\.tiff|\.tif|\.ome.tiff|\.qptiff)', cdb_file_tag = 'tiff_name'),
            _File(file_regex = r"\S*.txt", cdb_file_tag= 'channel_markers',transformation_fn=retrieve_txt_as_list)]
    

