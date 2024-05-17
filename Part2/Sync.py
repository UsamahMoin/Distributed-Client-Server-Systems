import filecmp
import threading
import time
import os
from xmlrpc.client import ServerProxy
import base64
import os
from xmlrpc.client import ServerProxy
from os.path import exists

proxy = ServerProxy('http://localhost:3000', verbose=False)

root = os.path.dirname(os.path.abspath(__file__))
s_path = os.path.join(root, "server_box\\files")
c_path = os.path.join(root, "client_box\\files")

def DirComparisionToUpload(server_path, client_path):    
    src = filecmp.dircmp(server_path,client_path)
    for src in src.right_only:
        dst = "files/"+src
        src_full_path = os.path.join(c_path, src)
        if exists(src_full_path):
            file_src_obj = _buildMetaData(root, src_full_path, False)
            file_src= _get_contents(src_full_path,file_src_obj)
            isUploadSuccessful = proxy.upload(file_src, dst)
            if isUploadSuccessful:
                print("NEW FILE UPLOADED")
            else:
                print("ERROR: PATH")

def checkModified(server_path,client_path):
    src = filecmp.dircmp(server_path,client_path)
    for src in src.common_files:
        dst = "files/" +src
        src_full_path = os.path.join(c_path, src)
        dest_full_path = os.path.join(s_path, src)
        if exists(src_full_path and dest_full_path):
            file_src_obj = _buildMetaData(root, src_full_path, False)
            file_dest_obj = _buildMetaData(root, dest_full_path, False)
            file_src= _get_contents(src_full_path,file_src_obj)
            file_dest= _get_contents(dest_full_path,file_dest_obj)
            if((round(_get_timestamp(file_src)),1) != (round(_get_timestamp(file_dest)),1)):
                # print(src_full_path)
                # print(round(_get_timestamp(file_src)),1)
                # print(dest_full_path)
                # print(round(_get_timestamp(file_dest)),1)
                isUploadSuccessful = proxy.upload(file_src, dst)
                if isUploadSuccessful:
                    print("MODIFIED FILE UPDATED")
                else:
                    print("ERROR: PATH")


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
        txt_doc = open(path, "rb")
        data = txt_doc.read()
        txt_doc.close()
        f_o['content'] = base64.b64encode(data)
        return f_o

def _get_timestamp(f_o):
    return f_o['timestamp']
    

def DirComparisionToDelete(client_path, server_path):
    
    result = filecmp.dircmp(client_path,server_path)
    for x in result.left_only:
        dst = "files/" + x
        if result =='SYNC':
            continue
        else:
            proxy.delete(dst)
            print("FILE DELETED")

def main():
    while True:
        th2 = threading.Thread(target=DirComparisionToDelete, args=(s_path, c_path))
        th2.start()
        th2.join()
        th1 = threading.Thread(target=DirComparisionToUpload, args=(s_path, c_path))
        th1.start()
        th1.join()
        th3 = threading.Thread(target=checkModified, args=(s_path, c_path))
        th3.start()
        th3.join()
        for i in range(5):
            time.sleep(2)

    
    
    

if __name__ == '__main__':
   main()
   