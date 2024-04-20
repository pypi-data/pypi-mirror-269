import json, os

def utils_save_json(file_path, data, overwrite = True):
    def update_json():
        json_copy = utils_read_json(file_path)
        if json_copy is None:
            json_copy = {}
        json_copy.update(data)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(json_copy, file, indent=4, ensure_ascii=False)
        except:
            os.makedirs(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(json_copy, file, indent=4, ensure_ascii=False)
    json_file = utils_read_json(file_path)
    if json_file != None:
        if overwrite:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            except:
                os.makedirs(os.path.dirname(file_path))
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
        else:
            update_json()
    else:
        update_json() 

def utils_read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        if data == {}:
            return None
        else:
            return data
    else:
        return None