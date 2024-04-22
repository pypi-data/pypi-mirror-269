from typing import *
from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class CreateMappingTable(PyMySQLQuery):
    """결합연계정보인 일련번호 컬럼 간 매핑테이블 생성 클래스
    
       Parameters
       ----------
       pw, serverIP, port_num, user_name, kr_encoder : DB 접속 비밀번호, IP, 포트명, 유저명, 인코더 명
       database_name : 연결 대상 DB 스키마 이름

       Examples
       --------
       creater = CreateMappingTable(pw = "1234", serverIP = "localhost", port_num = 3306, 
                                    user_name = "root", database_name = "FINANCIALCONSUMER", kr_encoder = "utf8")
    """
    columns = []

    def __init__(self, pw: str, serverIP: str, port_num: int, 
                 user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
        self.keytable_dictionary = {} # {key(키 스키마) : value(키 테이블)}
        self.mapping_table = None

    def joinKeyTables(self, mapping_schema: str, mapping_tablename: str, 
                      key_schemas: List, key_tablenames: List, 
                      joinkey_column: str, serialnum_columns: List):
        """
        일련번호 컬럼을 암호화된 결합키 기준으로 결합하여 매핑테이블 만드는 실행 메서드

        Parameters
        ----------
        mapping_schema, mapping_tablename : 생성 예정인 매핑테이블 스키마, 테이블명 
        key_schemas, key_tablenames : 각 결합키 테이블의 스키마, 테이블명 리스트
        joinkey_column : 내부 조인에 사용할 컬럼 이름
        serialnum_columns : 일련번호 컬럼 이름들을 담은 리스트

        Examples
        --------
        creater.joinKeyTables(mapping_schema="FINANCIALCONSUMER", mapping_tablename="APPCARDMAP",
                              key_schemas=["FINANCIALCONSUMER", "FINANCIALCONSUMER"], 
                              key_tablenames=["APPKEY", "CARDKEY"],
                              joinkey_column="JOINKEY", serialnum_columns=["SERIALNUM_C", "SERIALNUM_A"])

        """
        schema, tablename = self.addMappingTable(mapping_schema, mapping_tablename)
        if self.checkKeyTableInfo(key_schemas, key_tablenames, joinkey_column, serialnum_columns):
            create_table_dql = f"CREATE TABLE {schema}.{tablename} AS "
            select_join_dql = self.createSelectJoinQuery(key_schemas, key_tablenames, joinkey_column, serialnum_columns)

            if len(key_tablenames) > 2:
                for i in range(2, len(key_tablenames)):
                    select_join_dql += f"{serialnum_columns[i]}, INNER JOIN {key_schemas[i]}.{key_tablenames[i]} ON {key_schemas[0]}.{key_tablenames[0]}.{joinkey_column} = {key_schemas[i]}.{key_tablenames[i]}.{joinkey_column} "
            else:
                pass
            data_query_language = create_table_dql + select_join_dql
        else:
            pass

        super().dataQueryLanguage(data_query_language + " ")
        super().executeQuery()
        super().commitTransaction()
    
    @classmethod
    def addMappingTable(cls, schema, tablename):
        """매핑테이블의 스키마와 테이블명 DBContainer의 메서드 활용하여 생성"""
        cls.mapping_table = DBContainer()
        cls.mapping_table.setSchemaTable(schema, tablename)
        schema = cls.mapping_table.getSchema()
        tablename = cls.mapping_table.getTable()

        return schema, tablename
    
    @classmethod
    def addColumns(cls, column: str):
        """컬럼명 추가 메서드"""
        cls.column = column

    def checkKeyTableInfo(self, key_schemas: List, key_tablenames: List, joinkey_column: str, serialnum_columns: List):
        """결합키 테이블에 내부 조인 키와 일련번호 컬럼이 있는지 검증하는 메서드"""
        for i in range(len(key_schemas)):
            check_query = f"SELECT 1 FROM {key_schemas[i]}.{key_tablenames[i]} WHERE {joinkey_column} IS NOT NULL AND {serialnum_columns[i]} IS NOT NULL"

            # 검증 쿼리 실행
            super().dataQueryLanguage(check_query)
            result = super().executeQuery()

            # 검증 결과 확인
            if result:
                print(f"{key_schemas[i]}.{key_tablenames[i]} 테이블은 필요한 내부 조인 키와 일련번호 컬럼을 가지고 있습니다.")
                return True
            else:
                print(f"{key_schemas[i]}.{key_tablenames[i]} 테이블은 필요한 내부 조인 키와 일련번호 컬럼을 가지고 있지 않습니다.")
                return False

    @classmethod
    def createSelectJoinQuery(self, key_schemas: List, key_tablenames: List, 
                              joinkey_column: str, serialnum_columns: List):
        """매핑테이블 조인 쿼리 만드는 메서드"""
        select_dql = f"SELECT {key_schemas[0]}.{key_tablenames[0]}.{joinkey_column}, {key_schemas[0]}.{key_tablenames[0]}.{serialnum_columns[0]}, {key_schemas[1]}.{key_tablenames[1]}.{serialnum_columns[1]} "
        
        from_dql = f"FROM {key_schemas[0]}.{key_tablenames[0]} "
        join_dql = f"INNER JOIN {key_schemas[1]}.{key_tablenames[1]} "
        on_dql = f"ON {key_schemas[0]}.{key_tablenames[0]}.{joinkey_column} = {key_schemas[1]}.{key_tablenames[1]}.{joinkey_column}"

        return select_dql + from_dql + join_dql + on_dql