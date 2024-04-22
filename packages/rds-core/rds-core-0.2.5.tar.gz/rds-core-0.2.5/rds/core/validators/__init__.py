from typing import Union
import re
from rds.core.types import CPFCNS, CPFCNSCNPJ

RE_CNS = re.compile("^\d{15}$")
RE_CPF = re.compile("^\d{11}$")
RE_CNPJ = re.compile("^\d{14}$")


def validate_cpf(value: str) -> bool:
    return RE_CPF.match(value)


def validate_cns(value: str) -> bool:
    return RE_CNS.match(value)


def validate_cnpj(value: str) -> bool:
    return RE_CNPJ.match(value)


def validate_cns_cpf(value: str) -> Union[CPFCNS, None]:
    if validate_cpf(value):
        return CPFCNS.CPF

    if validate_cns(value):
        return CPFCNS.CNS

    return CPFCNS.INVALIDO


def validate_cns_cpf_cnpj(value: str) -> Union[CPFCNS, None]:
    if validate_cpf(value):
        return CPFCNSCNPJ.CPF

    if validate_cns(value):
        return CPFCNSCNPJ.CNS

    if validate_cnpj(value):
        return CPFCNSCNPJ.CNS

    return CPFCNSCNPJ.INVALIDO
