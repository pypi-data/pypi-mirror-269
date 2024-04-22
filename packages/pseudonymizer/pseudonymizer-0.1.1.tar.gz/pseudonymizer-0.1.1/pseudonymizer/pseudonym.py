from typing import List
import pandas as pd
from pseudonymizer.pseudonymizer import Pseudonymizer
from pseudonymizer.pseudonymizers.columncategorization import CategorizationOfColumn
from pseudonymizer.pseudonymizers.microAggregation import MicroAggregation
from pseudonymizer.pseudonymizers.topandBottomCoding import TopandBottomCoding


class Pseudonym:
    def __init__(self, dataframe):
        """원본정보(재현데이터)와 가명처리 구체 클래스를 인스턴스 변수로 선언하는(초기화) 생성자"""
        self._dataframe = dataframe.copy()
        self.equivalent_class = {}
        self._pseudonymizers = []
        self._pseudonymDictionary = {}
        
    def __str__(self):
        # __repr__
        """캡슐화된 데이터셋의 속성(컬럼)정보를 반환하는 메서드"""
        return self._dataframe.info()
    
    def categorizeEquivalentClass(self, attributes: List[str]):
        """각 행(레코드)에 대한 개인식별가능정보 속성(컬럼)들 사이에 동질 집합을 확인하는 메서드
        Pseudonym(dataframe).equivalent_class.keys()를 통해 동질집합 확인
        
        Parameters
        ----------
        attributes : 동질집합을 생성할 각 개인식별정보 컬럼의 둘 이상의 조합을 설정

        Examples
        --------
        일반적으로 나이 + 주소 + 성별 조합(동질 집합)이 재식별 가능성 있음
        (예: 주소의 경우, 시군구만 남기고 읍면동 단위 삭제)
        """
        groupby_data = self._dataframe.groupby(attributes)
        for group, data in groupby_data:
            if len(group) > 1:
                # key = tuple(group)
                key = group if len(group) > 1 else group[0]
                # 딕셔너리에서 키 값으로 리스트(동적 타입)는 사용할 수 없으므로 튜플로 변환
                # 단일 값인 경우 그룹을 튜플이 아닌 값으로 설정
                self.equivalent_class[key] = data.index.tolist()
                # 동질 집합에 해당하는 행(레코드)의 인덱스 번호를 키 값으로 조회되도록 저장
                
    def countEquivalentClass(self):
        """동질집합별 식별자의 레코드 수 출력 메서드"""
        for group_key, index_value in self.equivalent_class.items():
            print(group_key, len(index_value))
            
    def addPseudonymizer(self, pseudonymizer):
        """입력된 pseudonymizer 클래스가 가명처리 적용 객체 타입이 맞는지 검증하는 메서드

           Parameters
           ----------
           pseudonymizer : 가명처리 기법 적용 객체 입력
        
           가명처리 적용 객체 타입
           ------------------
           CategorizationOfNumeric, TopandBottomCoding, CategorizationOfColumn,
           MicroAggregation, MaskingPseudonymizer, CategorizationOfCharacter, RandomRoundingPseudonymizer
        """
        if isinstance(pseudonymizer, Pseudonymizer):
            self._pseudonymizers.append(pseudonymizer)
        else:
            print("입력받은 {} 기술은 가명처리 기법에 추가할 수 없습니다.".format(pseudonymizer))
    
    def addDictionary(self, column, pseudonymizers: List):
        """가명처리를 수행할 데이터 컬럼명과 해당 열에 적용할 여러 가명처리 기법 리스트를 입력받아 다양한 비식별 조치를 수행할 수 있도록 지정하는 메서드
        
           Parameters
           ----------
           column : 가명처리 기법 적용 대상 컬럼 입력
           pseudonymizers : 가명처리 기법 적용 객체 리스트 형태로 입력

           가명처리 적용 객체 타입
           ------------------
           CategorizationOfNumeric, TopandBottomCoding, CategorizationOfColumn,
           MicroAggregation, MaskingPseudonymizer, CategorizationOfCharacter, RandomRoundingPseudonymizer

           Examples
           --------
           pseudonymizer.addDictionary(column="NAME", pseudonymizers=[name_pseudo])
           pseudonymizer.addDictionary(column="HOME_ADDRESS", pseudonymizers=[address_masking])
        """
        self._pseudonymDictionary[column] = pseudonymizers
        
    def pseudonymizeData(self):
        """가명처리 기법을 해당 컬럼에 적용하는 메서드(apply함수를 활용하여 데이터프레임 모든 행, 특정 열에 비식별조치를 취하는 접근방식) """
        for column, pseudonymizers in self._pseudonymDictionary.items():
            for pseudonymizer in pseudonymizers:
                if isinstance(pseudonymizer, CategorizationOfColumn) or isinstance(pseudonymizer, TopandBottomCoding): 
                    self._dataframe[column] = pseudonymizer.pseudonymizeData(self._dataframe[column])
                elif isinstance(pseudonymizer, MicroAggregation):
                    self._dataframe[column] = pseudonymizer.pseudonymizeData(self._dataframe, column, self.equivalent_class)
                else:
                    self._dataframe[column] = self._dataframe[column].apply(pseudonymizer.pseudonymizeData)

    def getPseudonymizedDataframe(self):
        """가명처리 데이터 반환"""
        return self._dataframe