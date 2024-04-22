from enum import Enum


class CPFCNS(Enum):
    CPF = "cpf"
    CNS = "cns"
    INVALIDO = "INVÁLIDO"


class CPFCNSCNPJ(Enum):
    CPF = "cpf"
    CNS = "cns"
    CNPJ = "cnpj"
    INVALIDO = "INVÁLIDO"
