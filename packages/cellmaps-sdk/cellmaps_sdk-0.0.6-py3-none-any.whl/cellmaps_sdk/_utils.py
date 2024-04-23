from minio import Minio # type: ignore
import os
import requests
import re
from pathlib import Path
import uuid
from typing import Any, List, Dict
from ._config import Config as _Config #type: ignore
from ._raw_data import RAW #type: ignore


def _minio_healthcheck():
    # Ping the minio server, if it returns a status code of 200
    # the server is functioning correctly
    res = requests.get(f"http://{_Config._MINIO_HOST}:{_Config._MINIO_PORT}/minio/health/live")
    if res.status_code == 200:
        return True
    else:
        return False 
     
def get_minio_client():
    if _minio_healthcheck():
        client = Minio(
        endpoint=f"{_Config._MINIO_HOST}:{_Config._MINIO_PORT}",
        access_key=_Config._MINIO_ACCESS_KEY,
        secret_key=_Config._MINIO_SECRET_KEY,
        secure=False)
        return client   


# perhaps should also include an exclusion list form transformation functions (if the developer wants to do something more bespoke)
def read_raw_data(ExperimentClass: RAW, id: str = "", use_transformations: bool = True) -> List[Dict]:
    """
    Reads raw data based on the provided ExperimentClass.

    Args:
        ExperimentClass (Any): The class representing the experiment.
        id (str, optional): The experiment id. Defaults to "". This is the base prefix for the bucket (containing all experiment ids/names)
        use_transformations (bool, optional): Whether to use the transformation functions for the files which have them. Defaults to True.

    Returns:
        List[Dict]: A list of dictionaries containing the raw data for each experiment. Schema for the dictionary is as follows:
            {
                "experiment_name": str, (also the prefix)
                ** k:v (where k is the cdb_file_tag (from ExperimentClass) and v is the corresponding file name (or the transformed file if use_transformations is True and the file has a transformation function))
            }

    """
    client = get_minio_client()
    all_experiments = {}

    # Read prefixes only (these are the experiment ids)
    # prefixes cannot be tagged, so we need to read all prefixes and then filter out the ones that don't match the experiment tag
    for obj in client.list_objects(_Config._MINIO_EXPERIMENT_BUCKET,prefix=id):
        if obj.is_dir:
            # Remove slashed from prefix
            all_experiments[obj.object_name.replace("/","")] = {}
    
    # Recursively read all objects in the bucket 
    for obj in client.list_objects(_Config._MINIO_EXPERIMENT_BUCKET,recursive=True, include_user_meta=True):
        # exclude directories 
        if not obj.is_dir:
            # check if the experiment tag matches the experiment tag of the class
            if obj.tags['cdb_experiment_type'] == ExperimentClass.experiment_tag:
                # split the prefix and the file name (prefix is the experiment id)
                prefix, file = obj.object_name.split('/')
                # iterate over the files in the ExperimentClass (these are the files which should be present in the experiment prefix)
                for f in ExperimentClass.files:
                    # prevent files with same regex to be overwritten
                    if f.cdb_file_tag not in all_experiments[prefix].keys():
                        # check if the regex matches the file and the filetype matches the cdb_file_type
                        if re.match(f.file_regex, file) and obj.tags['cdb_file_type'] == f.cdb_file_type:
                            # add the file to the experiment dictionary for that prefix
                            if f.transformation_fn != None and use_transformations:
                                # apply the transformation function to the file (typically reading the file and transforming it to a different format, as opposed to simply retrieving the file name)
                                all_experiments[prefix][f.cdb_file_tag] = f.transformation_fn(obj)
                            else:
                                all_experiments[prefix][f.cdb_file_tag] = file
                            break

    # remove experiments that don't have all the required files
    valid_file_tags = [f.cdb_file_tag for f in ExperimentClass.files] # get all the cdb_file_tags for the experiment class

    # remove empty dictionaries (i.e. ones that have no file matches and also ones that don't have all the required files)
    # Shouldn't be required as the experiment tag should filter out the experiments that don't match the class / but just in case
    all_experiments = [{'experiment_name': k , **v} for k, v in all_experiments.items() if v and list(v.keys()) == valid_file_tags]
                            
    return all_experiments


def download_stacked_tiff_locally(url,dest="temp-files"):
    file_from_presigned_url = re.compile('/([^/]*)\?')
    matches = re.findall(file_from_presigned_url,url)
    assert len(matches) == 1, f'Regex found {len(matches)} in URL {url}'
     # Prepend UUID, so two workflows working on the same experimental data won't encounter race conditions
    local_filename = f"{str(uuid.uuid4())}_{matches[0]}"
    dest = Path(dest)
    try:
        os.mkdir(dest)
    except:
        pass
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest / local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment ifD
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
                
   
    return dest / local_filename

#  this also needs to be updated to use the new config
def get_experiment_data_urls(ExperimentClass: RAW, prefix_name: str) -> Dict:
    """
    Retrieves the URLs of experiment data files from a Minio bucket.

    Args:
        ExperimentClass (RAW): The experiment class containing the file information.
        prefix_name (str): The prefix name used to filter the objects in the Minio bucket.

    Returns:
        Dict: A dictionary containing the URLs of the experiment data files.

    Raises:
        Exception: If the experiment data is incomplete and some files are missing.

    """
    client = get_minio_client()
    urls = {}
    # iterate over the objects for a given experiment prefix
    for obj in client.list_objects(_Config._MINIO_EXPERIMENT_BUCKET,prefix_name,include_user_meta=True):
        # iterate over the files in the ExperimentClass
        for f in ExperimentClass.files:
            # check if the regex matches the file and the filetype matches the cdb_file_type
            if f.cdb_file_tag == obj.tags['cdb_file_type'] and re.match(f.file_regex, obj.object_name.split('/')[-1]):
                urls[f.cdb_file_tag] = client.get_presigned_url('GET', bucket_name=_Config._MINIO_EXPERIMENT_BUCKET,object_name=obj.object_name)
                break
    
    valid_file_tags = [f.cdb_file_tag for f in ExperimentClass.files] # get all the cdb_file_tags for the experiment class
    # check if all the required files are present (i.e. the experiment data is complete)
    if list(urls.keys()) == valid_file_tags:
        return urls
    # if not raise an error
    else:
        raise Exception('The experiment data is incomplete, some files are missing. Please check the experiment data and try again.\n Expected files: {valid_file_tags} \n Found files: {list(urls.keys())}')
