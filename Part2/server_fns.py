import base64
import shutil
import logging
import os

root = os.path.dirname(os.path.abspath(__file__))
s_path = os.path.join(root, "server_box")
c_path = os.path.join(root, "client_box")

format = "SERVER:%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


class FileServer:

    def list_directories(self):
        files_list = []
        for root, directories, files in os.walk(s_path, topdown=False):
            for name in files:
                file_locaton = os.path.join(root, name)
                logging.info("file_locaton="+file_locaton)
                base_path = file_locaton[file_locaton.rindex('server_box')+len("server_box/"):]
                files_list.append(base_path)
        return files_list


    def download(self, path):
        try:
            src_download_path = os.path.join(s_path, path)
            content = self._get_contents(src_download_path)
            return content
        except Exception as e:
            return "EXCEPTION CAUGHT AT DOWNLOAD"
    
    def rename(self, old_filename, new_filename):
        try:
            s_rename_o = os.path.join(s_path, old_filename)
            s_rename_n = os.path.join(s_path, new_filename)
            c_rename_o = os.path.join(c_path, old_filename)
            c_rename_n = os.path.join(c_path, new_filename)
            logging.info(f"RENAME REQUEST FROM {c_rename_o} to {c_rename_n}")
            os.rename(s_rename_o,s_rename_n)
            os.rename(c_rename_o,c_rename_n)
            logging.info("RENAME SUCCESS")
            return True
        except OSError as error:
            logging.info(error)
            return False

    def upload(self, f_o, path):
        try:
            target="client_box"
            if target in path:                
                path_to_be_uploaded = path.split("client_box/", 1)[1]
                full_path_to_be_uploaded = os.path.join(s_path, path_to_be_uploaded)                
            else:
                full_path_to_be_uploaded = os.path.join(s_path, path)
            if (f_o['Isdirectory']) and (not os.path.exists(full_path_to_be_uploaded)):
                os.makedirs(full_path_to_be_uploaded)
                return False
            elif f_o['Isdirectory']:
                return False
            self._createfile(f_o, full_path_to_be_uploaded)
            return True
        except Exception as e:
            logging.info("UPLOAD ERROR")
            return False

    def cleanup(self):        
        for filename in os.listdir(s_path):
            file_locaton = os.path.join(s_path, filename)
            try:
                if os.path.isfile(file_locaton) or os.path.islink(file_locaton):
                    os.unlink(file_locaton)
                elif os.path.isdir(file_locaton):
                    shutil.rmtree(file_locaton)
            except Exception as e:
                logging.info("ERROR: UNABLE TO DELETE")
                return False
        return True                

    def delete(self, path):
        try:
            substring="client_box"
            if(substring in path):
                path_to_be_deleted = path.split("client_box/", 1)[1]
            else:
                path_to_be_deleted = path
            full_path_to_be_deleted = os.path.join(s_path, path_to_be_deleted)   
            if os.path.isfile(full_path_to_be_deleted):
                os.remove(full_path_to_be_deleted)
            else:           
                shutil.rmtree(full_path_to_be_deleted)
            return True
        except OSError as e:
            logging.info("Error: UNABLE TO DELETE")
            return False

    def _createfile(self, f_o, full_path_to_be_uploaded):
        base_path = full_path_to_be_uploaded[:full_path_to_be_uploaded.rindex('/')]
        content = f_o['content']
        if (not os.path.exists(base_path)):
            os.makedirs(os.path.dirname(full_path_to_be_uploaded), exist_ok=True)

        with open(full_path_to_be_uploaded, 'wb') as temp_file:
            temp_file.write(base64.b64decode(content.data))
        return True

    def _get_contents(self, path):
        text_file = open(path, "rb")
        data = text_file.read()
        text_file.close()
        return base64.b64encode(data)