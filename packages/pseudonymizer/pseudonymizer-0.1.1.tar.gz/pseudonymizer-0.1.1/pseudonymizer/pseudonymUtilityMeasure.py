from pseudonymizer.pseudonym import Pseudonym
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from typing import *

class PseudonymUtilityMeasure(Pseudonym):
    """가명처리 기법이 적용된 개인정보(가명정보)의 유용성을 측정하는 지표"""
    def __init__(self, dataframe, attributes, pseudonymizeddata):
        super().__init__(dataframe)
        super().categorizeEquivalentClass(attributes)
        self.pseudonymizeddata = pseudonymizeddata
        
    def measureUtility(self, parameter, sensitive_attribute):
        """
        staticmethod에서는 부모클래스의 클래스속성 값을 가져오지만, classmethod에서는 cls인자를 활용하여 cls의 클래스속성을 가져오는 것을 알 수 있습니다.
        """
        if parameter == "cs":
            return self.cosineSimilarity(self._dataframe[sensitive_attribute], self.pseudonymizeddata[sensitive_attribute])
        elif parameter == "mc":
            return self.meanCorrelation(self._dataframe[sensitive_attribute], self.pseudonymizeddata[sensitive_attribute])
        elif parameter == "scd_sse":
            return self.standardizedEuclidianDistanceSSE(self._dataframe[sensitive_attribute], self.pseudonymizeddata[sensitive_attribute])
        elif parameter == "mgd":
            return self.meanGeneralizedDifference(self._dataframe[sensitive_attribute], self.pseudonymizeddata[sensitive_attribute])
        else:
            raise ValueError(f"{parameter}은 유효한 가명정보 유용성 평가지표가 아닙니다.")
            
    @classmethod
    def cosineSimilarity(cls, X_array, Y_array):
        """코사인 유사도로 원본과 비식별 동일 속성집합 간 벡터의 스칼라곱과 크기 계산 메서드
        벡터 간의 코사인 각도를 이용해 서로 간에 얼마나 유사한지 산정"""
        # metric 만드는 로직 구현 必
        X = X_array.copy()
        Y = Y_array.copy()

        dot_product = PseudonymUtilityMeasure.dotProduct(X, Y)
        # 벡터 정규화 수행
        norm_X = np.linalg.norm(X)
        norm_Y = np.linalg.norm(Y)
        if norm_X != 0 and norm_Y != 0:
            return dot_product / norm_X * norm_Y
        # np.dot(X, Y) / (norm(X)*norm(Y))
        else: 
            return 0
    
    @staticmethod
    def dotProduct(X_array, Y_array):
        """두 행렬곱(내적)을 수행하는 정적 메서드"""
        X = X_array.copy()
        Y = Y_array.copy()

        if isinstance(X, (int, float)) and isinstance(Y, (int, float)):
            # 스칼라 값인 경우 내적은 곱셈으로 계산
            return X * Y
        elif isinstance(X, pd.Series) and isinstance(Y, pd.Series):
            # 행렬인 경우 내적은 행렬의 곱셈 연산으로 계산
            if X.shape[0] != Y.shape[0]:
                raise ValueError("곱셈이 불가능한 행렬의 형태입니다.")

            result = 0
            for i in range(X.shape[0]):
                result += X.iloc[i] * Y.iloc[i]
            return result
        else:
            raise ValueError("내적 연산이 지원되지 않는 데이터 타입입니다.")


    @classmethod
    def meanCorrelation(cls, X_array, Y_array):
        """지정된 2개의 특정 속성쌍들에 대한 피어슨 상관계수에 대한 차이(평균절대오차) 계산 메서드"""
        X = X_array.copy()
        Y = Y_array.copy()

        X_mean = np.mean(X)
        Y_mean = np.mean(Y)

        correlation_coefficients: List = []
        # 상관계수 = 공분산 / 표준편차 계산하여 상관계수 1차원 배열에 추가
        for x, y in zip(X, Y):
            correlation = 0
            correlation = cls.dotProduct(x - X_mean, y - Y_mean) / (np.linalg.norm(x - X_mean) * np.linalg.norm(y - Y_mean))
            correlation_coefficients.append(abs(correlation))
        # 상관계수의 평균절대오차값 계산
        return np.mean(correlation_coefficients)
    
    @classmethod
    def standardizedEuclidianDistanceSSE(cls, X_array, Y_array):
        """표준화된 유클리디안 거리를 이용한 제곱합오차 계산 메서드"""
        X = X_array.copy()
        Y = Y_array.copy()

        standardized_X = (X - np.mean(X)) / np.std(X)
        standardized_Y = (Y - np.mean(Y)) / np.std(Y)
        # 표준화할 때 결측값(NA)에 대한 고려가 미비한 점이 남아있는 과제
        std_squared_error = np.sum( (standardized_X - standardized_Y)**2 )
        return std_squared_error

    @classmethod
    def meanGeneralizedDifference(cls, X_array, Y_array):
        """카테고리형 트리 구조를 갖는 문자 속성집합들 간의 평균 차이 계산 메서드
        원본과 비식별 동일 문자 속성집합 간 일반화된 차이(문자열 간의 유사도 측정)"""
        X = X_array.copy()
        Y = Y_array.copy()

        item_similarity, total_similarity, count = 0, 0, 0
        for x, y in zip(X, Y):
            item_similarity = cls.levenshteinDistance(x, y)
            total_similarity += item_similarity
            count += 1
        
        if count > 0:
            mean_similarity = total_similarity / count
        else:
            mean_similarity = 0
        return mean_similarity

    @staticmethod
    def levenshteinDistance(X, Y):
        """레벤슈타인 거리 유사도(편집 시 문자열 조작 최소횟수) 알고리즘을 계산하는 정적 메서드"""
        # 2차원 배열 생성 및 초기화
        m = len(X)
        n = len(Y)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # 첫 행, 첫 열 초기화
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # 동적 프로그래밍을 사용하여 레벤슈타인 거리 계산
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if X[i - 1] == Y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

        return dp[m][n]