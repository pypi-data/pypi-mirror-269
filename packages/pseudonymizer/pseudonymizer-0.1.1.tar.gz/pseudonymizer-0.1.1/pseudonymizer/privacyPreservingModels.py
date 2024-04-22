from pseudonymizer.deidentificationTechnique.equivalentClass import EquivalentClass
from pseudonymizer.deidentificationTechnique.kAnonymity import K_Anonymity
from pseudonymizer.deidentificationTechnique.lDiversity import L_Diversity
from pseudonymizer.deidentificationTechnique.tClosenessFactor import T_Closeness_F
from pseudonymizer.deidentificationTechnique.tClosenessNumeric import T_Closeness_N
from pseudonymizer.deidentificationTechnique.differentialPrivacy import DifferentialPrivacy
from pseudonymizer.deidentificationTechnique.gaussiandifferentialPrivacy import GaussianDifferentialPrivacy
from typing import *


class PrivacyPreservingModel:
    """
    개인식별가능정보 속성을 기준으로 그룹화된 데이터로 프라이버시 보호 모델을 적용하여 정량적인 위험성을 규정하는 실행 클래스
    
    Parameters
    ----------
    self._dataframe: 가명처리 기법 적용 전후 데이터 입력
    self.equivalnt_class: 준식별자를 이용한 그룹화 기법, 동질집합을 정의
    K_Anonymity(): 개별 레코드가 최소한 K개 이상 동일한 속성값을 가지도록 하는 K-익명성 기법
    L_Diversity(): 각 동질집합 내 특정 민감 속성의 빈도가 L값 이상의 다양성을 가지도록 하는 L-다양성 기법
    T_Closeness_N(): 연속형 민감정보(SA)의 분포를 전체 데이터 셋의 분포와 유사하도록 하는 T-근접성 기법
    T_Closeness_F(): 범주형 민감정보(SA)의 분포를 전체 데이터 셋의 분포와 유사하도록 하는 T-근접성 기법
    DifferentialPrivacy(): 라플라스 메커니즘 적용 차분 프라이버시 기법으로, 차등적 정보보호 기능을 수행
    GaussianDifferentialPrivacy(): 가우시안 메커니즘 적용 차분 프라이버시 기법
    """
    def __init__(self, dataframe, epsilon):
        self._dataframe = dataframe
        self.equivalnt_class = EquivalentClass(self._dataframe)
        self.Kanonymity = K_Anonymity(self._dataframe)
        self.Ldiversity = L_Diversity(self._dataframe)
        self.TclosenessNum = T_Closeness_N(self._dataframe)
        self.TclosenessFac = T_Closeness_F(self._dataframe)
        self.LaplaceLDP = DifferentialPrivacy(self._dataframe, epsilon)
        self.GaussianLDP = GaussianDifferentialPrivacy(self._dataframe, epsilon)

    def applyKAnonymityOrLDiversity(self, method: str, K: int, L: int, attributes: List[str], sensitive_attribute):
        """
        K-익명성과 L-다양성 모델을 선택적으로 적용하는 실행 메서드
        
        Parameters
        ----------
        method(K or L): 프라이버시 보호 모델 메서드 입력
        K, L, attributes, sensitive_attribute(keyword arguments): 각 기법에 필요한 파라미터를 받아옴
        K: K-익명성의 각 동질집합별 레코드의 최소한도 K 규정
        L: L-다양성의 각 동질집합별 민감속성 값의 최소한도 L 규정
        attributes: 동질집합을 생성할 각 개인식별정보 컬럼의 둘 이상의 조합을 설정
        sensitive_attribute: 민감정보에 해당하는 속성 정의

        Examples
        --------
        books_pseudo = PrivacyPreservingModel(
            dataframe = DATA_RETAIL_TABLE, epsilon = 3)
        K_data = books_pseudo.applyKAnonymityOrLDiversity(
            method="K", K = 3, L = None, attributes = ["AGE", "GENDER"], sensitive_attribute = None)
        L_data = books_pseudo.applyKAnonymityOrLDiversity(
            method="L", K = 3, L = 3, attributes = ["AGE", "GENDER"], sensitive_attribute = "NUM_PURCHASES_BOOKS")
        """
        if method == "K":
            self.Kanonymity.applyKAnonymity(K, attributes)
                # Kanonymity Input | K: int, attributes: List[str]
            print(self.Kanonymity.sensitive_data)
            return self.Kanonymity.K_data
        elif method == "L":
            self.Ldiversity.applyLDiversity(K, L, attributes, sensitive_attribute)
                # Ldiversity Input | K: int, L: int, attribute: List[str], sensitive_attribute
            print(self.Ldiversity.sensitive_data)
            return self.Ldiversity.L_data
        else:
            raise ValueError(f"입력받은 {method}는 유효한 개인정보 보호 기법이 아닙니다.")
        
    def applyLocalLDiversity(self, K: int, L: int, attributes: List[str], sensitive_attribute: str, LocalL: int):
        """
        지역 L-다양성 모델을 적용하는 실행 메서드

        Parameters
        ----------
        K: K-익명성의 각 동질집합별 레코드의 최소한도 K 규정
        L: L-다양성의 각 동질집합별 민감속성 값의 최소한도 L 규정
        LocalL: 지역 L-다양성의 각 동질집합별 민감속성 값의 유형별 최소한도 L 규정
        attributes: 동질집합을 생성할 각 개인식별정보 컬럼의 둘 이상의 조합을 설정
        sensitive_attribute: 민감정보에 해당하는 속성 정의

        Examples
        --------
        books_pseudo = PrivacyPreservingModel(
            dataframe = DATA_RETAIL_TABLE, epsilon = 3)
        LL_data = books_pseudo.applyLocalLDiversity(
            K = 3, L = 3, LocalL = 2, attributes = ["AGE", "GENDER"], sensitive_attribute = "NUM_PURCHASES_BOOKS")
        """
        self.Ldiversity.applyLDiversity(K, L, attributes, sensitive_attribute)
            # Ldiversity Input | K: int, L: int, attribute: List[str], sensitive_attribute
        self.Ldiversity.applyLocalLDiversity(LocalL)
            # LocalLdiversity | local_L: int
        print(self.Ldiversity.local_sensitive_data)
        return self.Ldiversity.LocalL_data

    def applyTCloseness(self, method: str, quasi_identifiers, sensitive_attribute: str, tolerance: float):
        """
        T-근접성 모델을 적용하는 실행 메서드

        Parameters
        ----------
        method: 프라이버시 보호 기법을 적용(Numeric or Factor)
        quasi_identifiers -> any: 각 동질집합 중 특정 준식별자(개인식별정보) 조합
        sensitive_attribute: 민감정보에 해당하는 속성 정의
        tolerance: 이상치에 대한 경계값 설정(0.0 ~ 1.0)

        Examples
        --------
        books_pseudo = PrivacyPreservingModel(
            dataframe = DATA_RETAIL_TABLE, epsilon = 3)      
        books_pseudo.applyTCloseness(
            method = "Numeric", tolerance = 0.1, quasi_identifiers = ["AGE", "GENDER"], sensitive_attribute = "NUM_PURCHASES_BOOKS")
        books_pseudo.applyTCloseness(
            method = "Factor", tolerance = 0.1, quasi_identifiers = ["AGE", "GENDER"], sensitive_attribute = "SHIPPING_ADDRESS")
        """
        if method == "Numeric":
            self.TclosenessNum.applyTCloseness(quasi_identifiers, tolerance, sensitive_attribute)
            print(self.TclosenessNum.sensitive_data)
            return self.TclosenessNum.T_data
        
        elif method == "Factor":
            self.TclosenessFac.applyTCloseness(quasi_identifiers, tolerance, sensitive_attribute)
            print(self.TclosenessFac.sensitive_data)
            return self.TclosenessFac.T_data
        
        else:
            raise ValueError(f"입력받은 {method}는 유효한 t-근접성 기법 적용 자료형이 아닙니다.")
            
    def applyDPrivacy(self, method, boundary, attributes, sensitive_attribute, outlier):
        """
        차분 프라이버시 기법(차등적 정보보호 기능)을 적용하는 메서드

        Parameters
        ----------
        method: 프라이버시 보호 기법을 적용(Numeric or Factor)
        boundary(N): 평균치의 상하에 표준 편차의 N배의 폭을 이상치 분류 기준 설정
        quasi_identifiers -> any: 각 동질집합 중 특정 준식별자(개인식별정보) 조합
        sensitive_attribute: 민감정보에 해당하는 속성 정의
        outlier: 이상치의 기준 설정(upper or lower)

        Examples
        --------
        books_pseudo = PrivacyPreservingModel(
            dataframe = DATA_RETAIL_TABLE, epsilon = 3) 
        books_pseudo.applyDPrivacy(
            method="Laplace", boundary = 3, outlier="upper", 
            attributes = ["AGE", "GENDER"], sensitive_attribute = "NUM_PURCHASES_BOOKS")
        books_pseudo.applyDPrivacy(
            method="Gaussian", boundary = 3, outlier="upper", 
            attributes = ["AGE", "GENDER"], sensitive_attribute = "NUM_PURCHASES_EDU")
        """
        if method == "Laplace":
            self.LaplaceLDP.dataDeviatingfromCI(boundary, attributes, sensitive_attribute)
            self.LaplaceLDP.dataGlobalSensitivity(outlier)
            return self.LaplaceLDP._dataframe
        
        elif method == "Gaussian":
            self.GaussianLDP.dataDeviatingfromCI(boundary, attributes, sensitive_attribute)
            self.GaussianLDP.dataGlobalSensitivity(outlier)
            return self.GaussianLDP._dataframe
        
        else:
            raise ValueError(f"입력받은 {method}는 유효한 차분 프라이버시 보호 기법 적용 확률분포가 아닙니다.")
                
    def __str__(self):
        """
        동질집합에 대한 정보를 문자열로 반환하는 메서드
        
        Examples
        --------
        books_pseudo = PrivacyPreservingModel(
            dataframe = DATA_RETAIL_TABLE, epsilon = 3)
        print(books_pseudo)
        """
        return str(self.equivalent_class)