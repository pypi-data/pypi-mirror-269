#submodule1/module2.py
# -*- coding: utf-8 -*-
from robot.api.deco import keyword
import ast
import pymongo
import logging
import bson



class XDrint:

    def __init__(self):
        self._dbconnection = None


    def CDCDCD(self):
        print("Hello, world! เทสภาษาไทย222")


    @keyword("XConnect Mongodb With URL")
    def connect_to_mongodb_with_uri(self, dbURI, timeout=10):
        """
        ***|    Description     |***
        | *`Connect Mongodb With URL`* | เป็น Keyword ไว้เชื่อมต่อกับ MongoDB โดยใช้ URI โดยเฉพาะ |

        
        ***|    Example     |***
        | *`Connect Mongodb With URL`* | *`mongodb+srv://username:password@host`* | *`timeout=10`* |
        

        ***|    Parameters     |***
            - **`dbURI`**  URL สำหรับการเชื่อมต่อไปยัง MongoDB.
            - **`timeout`**  ตั้งเวลา TimeOut ในการเชื่อมต่อไปยัง MongoDB.

            
       *`Create By Tassana Khrueawan`*
        """
        try:
            self._dbconnection = pymongo.MongoClient(dbURI, serverSelectionTimeoutMS=timeout*1000)
            self._dbconnection.server_info()
            logging.debug("| Succeed: เชื่อมต่อกับ MongoDB โดยใช้ URI | %s |" % dbURI)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            logging.error("| Fail: การเชื่อมต่อ MongoDB ล้มเหลว เนื่องจาก TimeOut | %s |" % str(e))
            raise Exception("การเชื่อมต่อ MongoDB ล้มเหลว เนื่องจาก TimeOut")
        except Exception as e:
            logging.error("| Fail: การเชื่อมต่อ MongoDB ล้มเหลว | %s |" % str(e))
            raise Exception("การเชื่อมต่อ MongoDB ล้มเหลว: " + str(e))
        

    @keyword("XQuery MongoDB")
    def query_mongodb(self, database_name, collection_name, query, limit=None, sort=None):
        """
        ***|    Description     |***
        |   *`Query MongoDB`*   |   เป็น Keyword สำหรับ Query ข้อมูลใน Collection พร้อมกับการกำหนดจำนวนข้อมูลสูงสุดและการเรียงลำดับข้อมูล |

        
        ***|    Example     |***
        | *`${result}`* | *`Query MongoDB`* | *`database_name`* | *`collection_name`* | *`Command Query`* | *`limit=5`* | *`sort=[("date", -1)]`* |
        | *`Log`* | *`${result}`* |

        
        ***|    Parameters     |***
            - **`database_name`**  ชื่อของฐานข้อมูล.
            - **`collection_name`**  ชื่อของ collection.
            - **`query`**  คำสั่ง Query.
            - **`limit`**  (Optional) จำนวนข้อมูลสูงสุดที่ต้องการส่งกลับ.
            - **`sort`**  (Optional) ลำดับข้อมูล ตัวอย่างเช่น [("field", -1 มากไปน้อย ,  1 น้อยไปมาก)].

        *`Create By Tassana Khrueawan`*
        """
        collection = self._dbconnection[database_name][collection_name]
        query_dict = ast.literal_eval(query)
        cursor = collection.find(query_dict)
        
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)

        results = list(cursor)
        return results
      
    
    @keyword("XQuery Dynamic Value")
    def query_dynamic_value(self, result, field='None', value='None', expect=None):
        """
        ***|    Description     |***
        |   *`XQuery Dynamic Value`*   |   เป็น Keyword สำหรับ Query ข้อมูลใน Collection แบบเจาะลงไป |

        
        ***|    Example     |***
        | *`${arpu_value}`* | *`XQuery Dynamic Value`* | *`result`* | *`productCharacteristic`* | *`name`* | *`arpu`* |
        | *`Log`* | *`${arpu_value}`* |

        
        ***|    Parameters     |***
        - **`result`**  ผลลัพธ์ของการ Query ที่เป็นรายการข้อมูลจาก MongoDB.
        - **`field`**   ชื่อฟิลด์ในข้อมูลที่ต้องการเจาะลงไป.
        - **`value`**   ชื่อคีย์ภายในฟิลด์ที่ต้องการเข้าถึง.
        - **`expect`**  ค่าที่ต้องการเทียบเพื่อหาข้อมูลที่ตรงกับเงื่อนไข.


        *`Create By Tassana Khrueawan`*
        """
        for item in result:
            if field in item and isinstance(item[field], list):
                if expect:
                    for char in item[field]:
                        if char.get(value) == expect:
                            return char.get('value')
                else:
                    return item[field]
        return None


    @keyword("XQuery Specific Value")
    def query_specific_value(self, result, field_name=None):
        """
        ***|    Description     |***
        |   XQuery Specific Value   |   Keyword สำหรับ Query ข้อมูลใน Collection แบบไม่เจาะลงไป |

        
        ***|    Example     |***
        | *`${name}`* | *`XQuery Specific Value`* | *`result`* | *`name`* |
        | *`Log`* | *`${name}`* |


        ***|    Parameters     |***
        - **`result`**  ผลลัพธ์ของการ Query ที่เป็นรายการข้อมูลจาก MongoDB.
        - **`field_name`**   ชื่อฟิลด์ที่ต้องการเข้าถึงเพื่อค้นหาค่าภายใน.


        *`Create By Tassana Khrueawan`*
        """
        if not field_name:
            return result

        results = []
        if isinstance(result, list):
            for doc in result:
                if isinstance(doc, dict) and field_name in doc:
                    results.append(doc[field_name])
        else:
            results = result.get(field_name, None)

        return results


    @keyword("XConvert BSON Document to JSON Object")
    def bson_to_json_object(self, bson_data):
        """
        แปลงข้อมูล BSON เป็นอ็อบเจกต์ Python (dictionary หรือ list) โดยไม่ต้องแปลงเป็นสตริง JSON

        พารามิเตอร์:
        - bson_data: ข้อมูล BSON ในรูปแบบไบต์สตริงหรือดิกชันนารี

        ผลลัพธ์ที่ได้:
        - อ็อบเจกต์ Python ซึ่งอาจเป็นดิกชันนารีหรือลิสต์ของดิกชันนารีที่แสดงถึงข้อมูล BSON

        ตัวอย่างการใช้งาน:
        | ${json_object} = | Convert BSON Document to JSON Object | ${bson_data} |
        """
        try:
            if isinstance(bson_data, bytes):
                bson_data = bson.loads(bson_data)
            # Convert BSON directly to a Python object without converting to a JSON string
            return bson_data  # This returns a Python dictionary or list of dictionaries
        except Exception as e:
            return f"Failed to convert BSON to JSON object: {str(e)}"