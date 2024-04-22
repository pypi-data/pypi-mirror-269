from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.encryptionPseudonyms.encrypttoKeyColumn import EncryptoKeyColumn
from pseudonymizer.encryptionPseudonyms.insertKeyintoMainTable import InsertKeyintoMainTable
from pseudonymizer.encryptionPseudonyms.insertTargetintoMainTable import InsertTargetintoMainTable
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery
from pseudonymizer.encryptionPseudonyms.updateSerialNumColumn import UpdateSerialNumColumn


class UpdateEncryptedKeyIntoDB(PyMySQLQuery):
    """결합키 암호화 및 결합대상정보 테이블 생성 클래스
       
       Parameters
       ----------
       pw, serverIP, port_num, user_name, kr_encoder : DB 접속 비밀번호, IP, 포트명, 유저명, 인코더 명
       database_name : 연결 대상 DB 스키마 이름
       main_tablename : 원본 테이블 이름
       key_schema, key_tablename : 결합키 생성항목 저장 스키마 & 테이블 이름
       target_schema, target_tablename : 결합대상정보 저장 스키마 & 테이블 이름 

       Examples
       --------
       retail_update = UpdateEncryptedKeyIntoDB(pw="1234", serverIP = "localhost", 
                                                port_num = 3306, 
                                                user_name = "root", 
                                                database_name = "FINANCIALCONSUMER", 
                                                kr_encoder = "utf8",
                                                main_tablename="DATA_RETAIL_PSEUDO",
                                                key_schema="FINANCIALCONSUMER", key_tablename="RETAIL_KEY",
                                                target_schema="FINANCIALCONSUMER", target_tablename="RETAIL_TARGET")
    """
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str, 
                 main_tablename: str, key_schema: str, key_tablename: str,
                 target_schema: str, target_tablename: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
        DQL = f"SELECT * FROM {main_tablename}"
        super().dataQueryLanguage(DQL)
        self.table = super().executeQueryAsDataFrame()
        super().commitTransaction()

        self.main_table = DBContainer()
        self.main_table.setSchemaTable(schema=database_name, table=main_tablename)

        self.key_table = DBContainer()
        self.key_table.setSchemaTable(schema=key_schema, table=key_tablename)

        self.target_table = DBContainer()
        self.target_table.setSchemaTable(schema=target_schema, table=target_tablename)

        self.updateSerialNumColumn = UpdateSerialNumColumn(pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.insertKeyintoMainTable = InsertKeyintoMainTable(pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.insertTargetintoMainTable = InsertTargetintoMainTable(pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.encryptoKeyColumn = EncryptoKeyColumn(pw, serverIP, port_num, user_name, database_name, kr_encoder)
    
    def __str__(self):
        return self.table.info()

    def UpdateintoDBTables(self, key_table: list, key_column: str, serial_column: str, serial_text: str, 
                           identifier_column, salt_value: str, salt_column: str, key_schema: str, hash_byte_type: str):
        """일련번호 컬럼 생성, 결합키 생성항목 및 결합 대상정보 테이블 입력, 결합키 암호화 실행 메서드
        
           Parameters
           ----------
           key_table : 결합키 생성항목으로 쓰일 컬럼명 리스트
           key_column : 결합키가 저장될 컬럼명
           serial_column : 일련번호가 저장될 컬럼명
           serial_text : 일련번호를 만들 때 테이블명을 구별하는 문자 (예: A1, B1, C1의 A, B, C)
           identifier_column : 이미 일련번호가 저장된 컬럼명. 없으면 None 입력
           salt_value : 암호화를 위한 Salt값
           salt_column : Salt값이 저장될 컬럼명
           key_schema : 결합키 테이블이 저장될 스키마명
           hash_byte_type : 결합키의 바이트 값 (예: 256, 512)
        
           Examples
           --------
           retail_update.UpdateintoDBTables(key_table=["NAME", "GENDER", "AGE", "PHONE_NUMBER"],
                                            key_column="JOINKEY", serial_column="SERIALNUM_RETAIL",
                                            serial_text="R", identifier_column=None,
                                            key_schema="FINANCIALCONSUMER",
                                            salt_value="ad17f60470baf557fb0b2618c8c64c7c", salt_column="SALT",
                                            hash_byte_type=256)
        """
        self.updateSerialNumColumn.addSerialNumColumn(tables = self.main_table, serial_column = serial_column, 
                                serial_text = serial_text, 
                                identifier_column = identifier_column)
        
        self.insertKeyintoMainTable.insertKeyIntoDB(tables = self.main_table,
                                                    key_table_info = self.key_table, 
                                                    key_table = key_table, 
                                                    join_key = key_column,
                                                    salt_value = salt_value, 
                                                    salt_column = salt_column,
                                                    serial_column = serial_column, 
                                                    serial_text = serial_text)
        
        self.insertTargetintoMainTable.insertTargetIntoDB(tables = self.main_table,
                                                          target_table = self.target_table, 
                                                          key_table = key_table)
        
        self.encryptoKeyColumn.encryptoKeytoHashvalue(hash_byte_type = hash_byte_type, 
                                                     key_schema = key_schema, 
                                                     key_table = self.key_table.getTable(), 
                                                     key_column = key_column, 
                                                     salt_column = salt_column)
        
    def printKeyTablesInfo(cls, schema_tablename: dict):
        """테이블 컬럼명 확인절차 실행 메서드

           Parameters
           ----------
           schema_tablename: 키테이블명 저장된 딕셔너리 ({key(키 스키마) : value(키 테이블)} 형태)
        """
        # 키테이블명 딕셔너리 = {key(키 스키마) : value(키 테이블)}
        schema = schema_tablename.keys()
        tablename = schema_tablename.values()

        # 키테이블의 컬럼명(결합키, 일련번호, 솔트) 반환
        sql = f"SHOW COLUMNS FROM {schema}.{tablename}"
        super().dataQueryLanguage(sql)
        key_schema_tablenames = super().executeQueryAsDataFrame()["Field"].tolist()
        
        return key_schema_tablenames