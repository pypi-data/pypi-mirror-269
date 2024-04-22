from pseudonymizer.pseudonymizer import Pseudonymizer
from pseudonymizer.pseudonymizers.addressMaskingModule import AddressMaskingModule
from pseudonymizer.pseudonymizers.nameMasking import NameMaskingModule
from pseudonymizer.pseudonymizers.emailMasking import EmailMaskingModule
from pseudonymizer.pseudonymizers.residentNumMasking import ResidentNumberMaskingModule
from pseudonymizer.pseudonymizers.businessNumMasking import BusinessNumberMaskingModule
from pseudonymizer.pseudonymizers.phoneNumMasking import PhoneNumberMaskingModule

import re
from typing import *

    
class MaskingPseudonymizer(Pseudonymizer):
    """
    이름, 이메일, 주민등록번호, 사업자/법인등록번호, 연락처, 주소 데이터 마스킹 클래스
    
    Parameters
    ----------
    data_type : name, email, resident_number, business_number, phone_number, address
    masking_domain : data_type이 email인 경우, aaa@bbb.com 등 이메일 주소에서 도메인에 해당하는 bbb를 마스킹할지 여부를 True / False로 입력
    masking_part : data_type이 business_number 인 경우, 124-86-23875 형태에서 첫번째만 남기면 both, 두번째만 남기면 middle, 세번째만 남기면 rear 입력
    masking_loca : data_type이 address인 경우, 시군구 단위일 때 government_area, 읍면동 단위일 때 district 입력

    Examples
    --------
    name_pseudo = MaskingPseudonymizer(data_type="name")
    phone_pseudo = MaskingPseudonymizer(data_type="phone_number")
    address_masking = MaskingPseudonymizer(data_type="address", masking_loca="government_area")
    email_pseudo = MaskingPseudonymizer(data_type="email", masking_domain=True)
    """
    def __init__(self, data_type: str, 
                 masking_domain: bool = None, 
                 masking_part: str = None,
                 masking_loca: str = None):
        """data_type은 향후 pseudonymizer.py에서 Pseudonymn 실행 클래스의 
        self._dataframe[column] 개인식별정보의 유형으로 이름, 이메일, 주민등록번호, 사업자등록번호 중 하나로 선언"""
        self.data_type = data_type
        self.email_masker = EmailMaskingModule(masking_domain)
        self.name_masker = NameMaskingModule()
        self.resident_num_masker = ResidentNumberMaskingModule()
        self.business_num_masker = BusinessNumberMaskingModule(masking_part)
        self.phone_num_masker = PhoneNumberMaskingModule()
        self.address = AddressMaskingModule(masking_loca)

    def pseudonymizeData(self, data):
        if self.data_type == "name":
            return self.name_masker.pseudonymizeData(data)
        elif self.data_type == "email":
            return self.email_masker.pseudonymizeData(data)
        elif self.data_type == "resident_number":
            return self.resident_num_masker.pseudonymizeData(data)
        elif self.data_type == "business_number":
            return self.business_num_masker.pseudonymizeData(data)
        elif self.data_type == "phone_number":
            return self.phone_num_masker.pseudonymizeData(data)
        elif self.data_type == "address":
            return self.address.pseudonymizeData(data)
        else:
            raise ValueError("유효한 마스킹 대상 개인식별정보 데이터 타입이 아닙니다.")
            