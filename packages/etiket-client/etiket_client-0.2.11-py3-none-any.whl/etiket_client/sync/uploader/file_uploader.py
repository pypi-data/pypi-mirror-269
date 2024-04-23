from etiket_client.remote.endpoints.file import file_validate_upload
from etiket_client.remote.endpoints.models.file import FileValidate, FileSignedUploadLinks
from etiket_client.exceptions import RequestFailedException

import requests, logging

logger = logging.getLogger(__name__)

# TODO on the server side, make sure only one client can upload.
def upload_new_file(file_raw_name, upload_info  : FileSignedUploadLinks, md5_checksum, ntries = 0):
    try:
        n_parts = len(upload_info.presigned_urls)
        chunck_size = upload_info.part_size
        etags = []
        
        with open(file_raw_name, 'rb') as file:
            for i in range(n_parts):
                file.seek(i * chunck_size)
                data = file.read(chunck_size)

                for n_tries in range(3):
                    success, response = upload_chunck(upload_info.presigned_urls[i], data)
                    if n_tries == 2 and success == False:
                        raise RequestFailedException('Failed to upload file.')
                    if success == True:
                        break

                etags.append(str(response.headers['ETag']))

        fv = FileValidate(uuid=upload_info.uuid, version_id=upload_info.version_id,
                            upload_id=upload_info.upload_id, md5_checksum=md5_checksum,
                            etags=etags)
        file_validate_upload(fv)
    
    except Exception as e:
        if ntries < 3:
            logger.warning(f'Failed to upload file with name {file_raw_name}.\n Error message :: {e}, try {ntries} (and trying again).\n)')
            upload_new_file(file_raw_name, upload_info, ntries+1)
        else :
            logger.exception(f'Failed to upload file with name {file_raw_name}.\n')
            raise e
    
def upload_chunck(url, data):
    response = requests.put(url, data=data)

    if response.status_code >=400:
        response_json = None
        if response:
            response_json = response.json()
        logging.warning(f'Failed to upload a chunk to url with hash ({hash(url)}).\nRAW JSON resonse :: {response_json}')
        return False, response
    return True, response