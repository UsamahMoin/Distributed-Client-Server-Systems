import base64
from genericpath import isfile
import os
import argparse
import logging
from xmlrpc.client import ServerProxy
from os.path import exists

# log setup
format = "CLIENT:%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

proxy = ServerProxy('http://localhost:3000', verbose=False)
root_directory = os.path.dirname(os.path.abspath(__file__))
client_folder_path = os.path.join(root_directory, "client_box")
polling_count = 0


def client_list_directory():
        clientFileList = []
        for root, directories, files in os.walk(client_folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                base_path = file_path[file_path.rindex('client_box')+len("client_box/"):]
                clientFileList.append(base_path)
        return clientFileList

def list(args):
    target = args.list[0]
    if target == "server":
        serverFileList = proxy.list_directories()
        logging.info(serverFileList)
    elif target == "client":
        clientFileList = client_list_directory()
        logging.info(clientFileList)
    else:
        logging.info("CHECK PATH")

def download(args):
    src = args.download[0]
    dst = args.download[1]
    content = proxy.download(src)
    if(content == 'DownloadException'):
        logging.info("FILE UNAVAILABLE")
    else:
        if(_createfile(content, dst)):
            logging.info("FILE DOWNLOADED")
    
def upload(args):
    src = args.upload[0]
    dst = args.upload[1]
    src_full_path = os.path.join(client_folder_path, src)
    print("src_full_path"+src_full_path)
    print("dest"+dst)
    if exists(src_full_path):
        file_src_obj = _buildMetaData(root_directory, src_full_path, False)
        file_src= _get_contents(src_full_path,file_src_obj)
        isUploadSuccessful = proxy.upload(file_src, dst)
        if isUploadSuccessful:
            print("UPLOADED")
        else:
            print("ERROR: PATH")
    else:
        logging.info(" FILE UNAVAILABLE ")

def rename(args):
    old_filename = args.rename[0]
    new_filename = args.rename[1]
    if proxy.rename(old_filename, new_filename):
        logging.info("FILE RENAMED")
    
def delete(args):
    target_path = args.delete[0]
    if proxy.delete(target_path):        
        logging.info("FILE DELETED")
    else:
        logging.info("FILE UNAVAILABLE")
    

def _buildMetaData(root, name, isDirectory):
    f_o = {
        'c_timestamp': os.path.getctime(os.path.join(root, name)),
        'timestamp': os.path.getmtime(os.path.join(root, name)),
        'Isdirectory': isDirectory,
        'file_path': os.path.join(root, name),
        'size': os.path.getsize(os.path.join(root, name))
    }
    return f_o


def _get_contents(path, f_o):
    if f_o['Isdirectory']:
        return f_o
    else:        
        text_file = open(path, "rb")
        data = text_file.read()
        text_file.close()
        f_o['content'] = base64.b64encode(data)
        return f_o


def _createfile(content, path):
    try:
        path = os.path.join(client_folder_path, path)    
        if (not os.path.exists(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as temp_file:
            temp_file.write(base64.b64decode(content.data))    
        return True
    except Exception as e:
        logging.info(f"Exception occured {e}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--list", type=str, nargs=1, metavar=('target'))
    parser.add_argument("-r", "--rename", type=str, nargs=2,metavar=('old_name', 'new_name'))
    parser.add_argument("-d", "--download", type=str, nargs=2,metavar=('src', 'dst'))
    parser.add_argument("-del", "--delete", type=str, nargs=1,metavar=('target'))
    parser.add_argument("-u", "--upload", type=str, nargs=2,metavar=('src', 'dst'))
    
    args = parser.parse_args()

    if args.download is not None:
        download(args)
    elif args.rename is not None:
        rename(args)
    elif args.delete is not None:
        delete(args)
    elif args.upload is not None:
        upload(args)
    elif args.list is not None:
        list(args)
