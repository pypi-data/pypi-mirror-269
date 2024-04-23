import typing, time

from etiket_client.sync.backends.core_tools.core_tools_config_class import CoreToolsConfigData
from etiket_client.sync.backends.core_tools.data_getters.get_gates import get_gates_formatted
from etiket_client.sync.backends.core_tools.data_getters.get_pulses import get_AWG_pulses
from etiket_client.sync.backends.core_tools.real_time_sync.measurement_sync import live_measurement_synchronizer
from etiket_client.sync.base.sync_source_abstract import SyncSourceAbstract
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item, new_sync_item, FileType

try:
    import psycopg2
    from core_tools.data.ds.data_set import load_by_id
    from core_tools.data.ds.ds2xarray import ds2xarray
    from core_tools.data.SQL.connect import SQL_conn_info_local
except ImportError:
    print("Core-tools not installed, will not be able to use core tools sync")


class CoreToolsSync(SyncSourceAbstract):
    SyncAgentName = "core-tools"
    ConfigDataClass = CoreToolsConfigData
    MapToASingleScope = False
    LiveSyncImplemented = True

    @staticmethod
    def getNewDatasets(configData: CoreToolsConfigData, lastIdentifier: str) -> 'typing.List[new_sync_item] | None':
        SQL_conn_info_local(configData.host, configData.port, configData.user,
                        configData.password, configData.dbname, True)
        
        lastIdentifier = 0 if lastIdentifier is None else int(lastIdentifier)

        conn = psycopg2.connect(database=configData.dbname, user=configData.user, password=configData.password,
                                host=configData.host, port=configData.port)
        cur = conn.cursor()
        stmt = "SELECT id, project FROM global_measurement_overview WHERE id > %s ORDER BY id ASC"
        cur.execute(stmt, (lastIdentifier,))
        
        newSyncIdentifiers = [new_sync_item(dataIdentifier = str(row[0]), scopeIdentifier=row[1]) for row in cur.fetchall()]

        return newSyncIdentifiers
    
    @staticmethod
    def checkLiveDataset(configData: CoreToolsConfigData, syncIdentifier: sync_item):
        ds_ct = load_by_id(int(syncIdentifier.dataIdentifier))
        return not ds_ct.completed
    
    @staticmethod
    def syncDatasetNormal(configData: CoreToolsConfigData, syncIdentifier: sync_item):
        ds_ct = create_ds_from_core_tools(configData, syncIdentifier, False)
        if ds_ct.snapshot:
            f_info = file_info(name = 'snapshot', created = ds_ct.run_timestamp,
                               fileName = 'snapshot.json',
                               fileType= FileType.JSON,
                               file_generator = "core-tools")
            sync_utilities.upload_JSON(ds_ct.snapshot, syncIdentifier, f_info)
            
            pulses = get_AWG_pulses(ds_ct.snapshot)
            if pulses:
                f_info = file_info(name = 'AWG pulses', created = ds_ct.run_timestamp,
                                   fileName = 'pulses.hdf5',
                                   fileType= FileType.HDF5_NETCDF,
                                   file_generator = "core-tools")
                sync_utilities.upload_xarray(pulses, syncIdentifier, f_info)
                
            gates = get_gates_formatted(ds_ct.snapshot)
            if gates:
                f_info = file_info(name = 'gates', created = ds_ct.run_timestamp,
                                   fileName = 'gates.json',
                                   fileType= FileType.JSON,
                                   file_generator = "core-tools")
                sync_utilities.upload_JSON(gates, syncIdentifier, f_info)
        
        if ds_ct.metadata:
            f_info = file_info(name = 'metadata', 
                               fileName = 'metadata.json',
                               fileType= FileType.JSON,
                               created = ds_ct.run_timestamp, file_generator = "core-tools")
            sync_utilities.upload_JSON(ds_ct.metadata, syncIdentifier, f_info)
            
        ds_xarray = ds2xarray(ds_ct)
        f_info = file_info(name = "measurement",
                           fileName = 'measured_data.hdf5',
                           fileType= FileType.HDF5_NETCDF,
                           created = ds_ct.run_timestamp, file_generator = "core-tools")
        sync_utilities.upload_xarray(ds_xarray, syncIdentifier,f_info)
        
    @staticmethod
    def syncDatasetLive(configData: CoreToolsConfigData, syncIdentifier: sync_item):
        create_ds_from_core_tools(configData, syncIdentifier, True)
        lms = live_measurement_synchronizer(int(syncIdentifier.dataIdentifier), syncIdentifier.datasetUUID)
        try:
            while lms.is_complete() is not True:
                lms.sync()
                time.sleep(0.2)
        except Exception as e:
            raise e
        finally:
            lms.complete()

def create_ds_from_core_tools(configData: CoreToolsConfigData, syncIdentifier: sync_item, live : bool):
    ds_ct = load_by_id(int(syncIdentifier.dataIdentifier))
    
    description = f'database : {configData.dbname} | id : {ds_ct.id} | ct_uuid : {ds_ct.exp_uuid}'
    
    ds_info = dataset_info(name = ds_ct.name, datasetUUID = syncIdentifier.datasetUUID,
                alt_uid = str(ds_ct.exp_uuid), scopeUUID = syncIdentifier.scopeUUID,
                created = ds_ct.run_timestamp, keywords = ds_ct.keywords, description = description,
                attributes = {"sample" : ds_ct.sample_name, "set-up" : ds_ct.set_up})
    
    sync_utilities.create_ds(live, syncIdentifier, ds_info)
    return ds_ct