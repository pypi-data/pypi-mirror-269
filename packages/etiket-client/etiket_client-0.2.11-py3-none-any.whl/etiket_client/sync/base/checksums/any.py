import hashlib

def md5(file_path, blocksize=65536):
    m = hashlib.md5()
    with open(file_path , "rb" ) as f:
        while chunk := f.read(blocksize):
            m.update(chunk)
    return m.hexdigest()