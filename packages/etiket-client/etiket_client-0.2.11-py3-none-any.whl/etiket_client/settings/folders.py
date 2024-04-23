import platformdirs as pd
import os, sys, hashlib

# TODO :: general question, should data and sql by linked to a folder on the system rather than a user folder?

def get_sql_url():
    path  = f"{pd.user_data_dir()}/qdrive/sql/" 
    if not os.path.exists(path):
        os.makedirs(path)
    return f"sqlite+pysqlite:///{path}etiket_db.sql"

def get_data_dir():
    path  = f"{pd.user_data_dir()}/qdrive/data/" 
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_file_dir(scope_uuid, dataset_uuid, file_uuid, version_id):
    fpath = f'{get_data_dir()}{scope_uuid}/{dataset_uuid}/{file_uuid}/{version_id}/'            
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    return fpath

def get_user_data_dir():
    python_env = hashlib.md5(sys.prefix.encode('utf-8')).hexdigest()
    path  = f"{pd.user_data_dir()}/qdrive/user_data/{python_env}/" 
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_log_dir():
    path  = f"{pd.user_data_dir()}/qdrive/logs/" 
    if not os.path.exists(path):
        os.makedirs(path)
    return path