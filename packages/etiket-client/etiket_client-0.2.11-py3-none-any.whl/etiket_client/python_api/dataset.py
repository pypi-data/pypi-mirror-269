from etiket_client.local.dao.dataset import dao_dataset, DatasetCreate, DatasetUpdate
from etiket_client.local.database import Session

from etiket_client.remote.endpoints.dataset import dataset_read as dataset_read_remote

from etiket_client.python_api.dataset_model.dataset import dataset_model
from etiket_client.local.exceptions import DatasetNotFoundException

import uuid

def dataset_create(datasetCreate:DatasetCreate):
    with Session() as session:
        ds = dao_dataset.create(datasetCreate, session)
    return dataset_model(ds, None)

def dataset_read(dataset_uuid:'uuid.UUID | str'):
    local_ds = None
    with Session() as session:
        try :
            local_ds = dao_dataset.read(dataset_uuid, session)
        except DatasetNotFoundException as e:
            pass
        except Exception as e:
            raise e
    
    try:
        remote_ds = dataset_read_remote(dataset_uuid)
    except Exception as e:
        remote_ds = None
    
    if local_ds is None and remote_ds is None:
        raise DatasetNotFoundException(f"Dataset with uuid {dataset_uuid} not found")
    
    return dataset_model(local_ds, remote_ds)