# -*- coding: utf-8 -*-
import bson

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


    #Private Function