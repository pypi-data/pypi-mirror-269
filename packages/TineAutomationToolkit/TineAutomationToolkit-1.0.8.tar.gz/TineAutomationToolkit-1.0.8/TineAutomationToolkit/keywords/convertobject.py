# -*- coding: utf-8 -*-
import bson
import logging

class ConvertObject:

    def __init__(self):
        #เนื่องจากปัญหาเรื่องโครงสร้าง structure เลยยังไม่สามารถใช้ได้
        # self._bi = BuiltIn()
        pass

    #KeyWord

    def convert_bson_to_json(self, bson_data):
        """ Owner : tassana.k@epic-consulting.net
        Convert BSON data to a Python object (dictionary or list) 
        without converting it to a JSON string.

        ==========================================================

        แปลงข้อมูล BSON เป็นอ็อบเจกต์ Python (dictionary หรือ list) 
        โดยไม่ต้องแปลงเป็นสตริง JSON
        """
        try:
            if isinstance(bson_data, bytes):
                bson_data = bson.loads(bson_data)
            # Convert BSON directly to a Python object without converting to a JSON string
            return bson_data  # This returns a Python dictionary or list of dictionaries
        except Exception as e:
            return f"Failed to convert BSON to JSON object: {str(e)}"

    def log_tree_structure_data(self, data):
        """ Owner : tassana.k@epic-consulting.net
        ***|    Description     |***
        |   *`Log Tree Data`*   |   เป็น Keyword สำหรับ Log Data ให้ออกมาเป็น Tree Data |

        ***|    Example     |***
        | *`Log Tree Data`* | *`${value}`* |
        
        ***|    Parameters     |***
            - **`data`**  ข้อมูล Json.
        """
        self._tree_structure(data)

    #Private Function

    def _tree_structure(self, data, level=0, prefix=''):
        indent = "│   " * level
        branch = "├── " if level > 0 else ""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    logging.info(f"{indent}{branch}{key}")
                    self._tree_structure(value, level + 1)
                else:
                    logging.info(f"{indent}{branch}{key}: {value}")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                logging.info(f"{indent}├── [{i}]")
                self._tree_structure(item, level + 1)
        else:
            logging.info(f"{indent}{branch}{prefix}{data}")