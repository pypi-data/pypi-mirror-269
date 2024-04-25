import operator as _operator
from collections.abc import Callable as _Callable
from enum import Enum as _Enum

from django.db import models as _models
from django.db.models import enums as _enums

__all__ = [
    "States",
    "Colors",
    "Operator",
    "OrderedTextChoices",
    "Qualification",
    "LegalNatureQualification",
]


class Operator(_Enum):
    LT = _operator.lt
    GT = _operator.gt
    LTE = _operator.le
    GTE = _operator.ge


class OrderedTextChoices(_models.TextChoices):
    """Class for creating enumerated string choices, establishing hierarchy between the
    values. Lowest members has higher values than the highest, then, you can compare
    the two using compare method::

        from b2_utils.enums import Operator, OrderedTextChoices

        class Role(OrderedTextChoices):
            SUPPORT = "SUPPORT", "Support"
            MANAGER = "MANAGER", "Manager"
            ADMIN = "ADMIN", "Admin"

        Role.compare(Role.ADMIN, Operator.GT, Role.SUPPORT) # True
    """

    @classmethod
    def _get_value(cls, choice) -> int | None:
        for index, option in enumerate(cls.choices):
            if choice == option[0]:
                return index
        return None

    @classmethod
    def compare(cls, first, operator: Operator | _Callable, second) -> bool:
        """Compares two values from the same Enum.

        Parameters
        ---------
        first : any
            The first operand
        operator : Operator | Callable
            The operator used to make the comparison. It also can be a function, in
            that case, your function may accept receive two integers, and return a
            boolean. Eg::

            def custom_compare(a: int, b: int) -> bool:
                return b - a == 3

        second : any
            The second operand

        Returns
        -------
        bool
            A boolean which represents the result of operation between the two operands
        """
        if callable(operator):
            return operator(cls._get_value(first), cls._get_value(second))

        return operator.value(cls._get_value(first), cls._get_value(second))


class States(_enums.TextChoices):
    AC = "AC", "Acre"
    AL = "AL", "Alagoas"
    AM = "AM", "Amazonas"
    AP = "AP", "Amapá"
    BA = "BA", "Bahia"
    CE = "CE", "Ceará"
    ES = "ES", "Espírito Santo"
    GO = "GO", "Goiás"
    MA = "MA", "Maranhão"
    MG = "MG", "Minas Gerais"
    MS = "MS", "Mato Grosso do Sul"
    MT = "MT", "Mato Grosso"
    PA = "PA", "Pará"
    PB = "PB", "Paraíba"
    PE = "PE", "Pernambuco"
    PI = "PI", "Piauí"
    PR = "PR", "Paraná"
    RJ = "RJ", "Rio de Janeiro"
    RN = "RN", "Rio Grande do Norte"
    RO = "RO", "Rondônia"
    RR = "RR", "Roraima"
    RS = "RS", "Rio Grande do Sul"
    SC = "SC", "Santa Catarina"
    SE = "SE", "Sergipe"
    SP = "SP", "São Paulo"
    TO = "TO", "Tocantins"
    DF = "DF", "Distrito Federal"


class Colors(_enums.IntegerChoices):
    PINK = 0xFFC0CB, "Pink"
    HOTPINK = 0xFF69B4, "Hot Pink"
    LIGHTPINK = 0xFFB6C1, "Light Pink"
    DEEPPINK = 0xFF1493, "Deep Pink"
    PALEVIOLETRED = 0xDB7093, "Pale Violet Red"
    MEDIUMVIOLETRED = 0xC71585, "Medium Violet Red"
    LAVENDER = 0xE6E6FA, "Lavender"
    THISTLE = 0xD8BFD8, "Thistle"
    PLUM = 0xDDA0DD, "Plum"
    ORCHID = 0xDA70D6, "Orchid"
    VIOLET = 0xEE82EE, "Violet"
    MAGENTA = 0xFF00FF, "Magenta"
    MEDIUMORCHID = 0xBA55D3, "Medium Orchid"
    DARKORCHID = 0x9932CC, "Dark Orchid"
    DARKVIOLET = 0x9400D3, "Dark Violet"
    BLUEVIOLET = 0x8A2BE2, "Blue Violet"
    DARKMAGENTA = 0x8B008B, "Dark Magenta"
    PURPLE = 0x800080, "Purple"
    MEDIUMPURPLE = 0x9370DB, "Medium Purple"
    MEDIUMSLATEBLUE = 0x7B68EE, "Medium Slate Blue"
    SLATEBLUE = 0x6A5ACD, "Slate Blue"
    DARKSLATEBLUE = 0x483D8B, "Dark Slate Blue"
    REBECCAPURPLE = 0x663399, "Rebecca Purple"
    INDIGO = 0x4B0082, "Indigo"
    LIGHTSALMON = 0xFFA07A, "Light Salmon"
    SALMON = 0xFA8072, "Salmon"
    DARKSALMON = 0xE9967A, "Dark Salmon"
    LIGHTCORAL = 0xF08080, "Light Coral"
    INDIANRED = 0xCD5C5C, "Indian Red"
    CRIMSON = 0xDC143C, "Crimson"
    RED = 0xFF0000, "Red"
    FIREBRICK = 0xB22222, "Fire Brick"
    DARKRED = 0x8B0000, "DarkRed"
    ORANGE = 0xFFA500, "Orange"
    DARKORANGE = 0xFF8C00, "Dark Orange"
    CORAL = 0xFF7F50, "Coral"
    TOMATO = 0xFF6347, "Tomato"
    ORANGERED = 0xFF4500, "Orange Red"
    GOLD = 0xFFD700, "Gold"
    YELLOW = 0xFFFF00, "Yellow"
    LIGHTYELLOW = 0xFFFFE0, "Light Yellow"
    LEMONCHIFFON = 0xFFFACD, "Lemon Chiffon"
    LIGHTGOLDENRODYELLOW = 0xFAFAD2, "Light Goldenrod Yellow"
    PAPAYAWHIP = 0xFFEFD5, "Papaya Whip"
    MOCCASIN = 0xFFE4B5, "Moccasin"
    PEACHPUFF = 0xFFDAB9, "Peach Puff"
    PALEGOLDENROD = 0xEEE8AA, "Pale Goldenrod"
    KHAKI = 0xF0E68C, "Khaki"
    DARKKHAKI = 0xBD536B, "Dark Khaki"
    GREENYELLOW = 0xADFF2F, "Green Yellow"
    CHARTREUSE = 0x7FFF00, "Chartreuse"
    LAWNGREEN = 0x7CFC00, "Lawn Green"
    LIME = 0x00FF00, "Lime"
    LIMEGREEN = 0x32CD32, "Lime Green"
    PALEGREEN = 0x98FB98, "Pale Green"
    LIGHTGREEN = 0x90EE90, "Light Green"
    MEDIUMSPRINGGREEN = 0x00FA9A, "Medium Spring Green"
    SPRINGGREEN = 0x00FF7F, "Spring Green"
    MEDIUMSEAGREEN = 0x3CB371, "Medium Sea Green"
    SEAGREEN = 0x2E8B57, "Sea Green"
    FORESTGREEN = 0x228B22, "Forest Green"
    GREEN = 0x008000, "Green"
    DARKGREEN = 0x006400, "Dark Green"
    YELLOWGREEN = 0x9ACD32, "Yellow Green"
    OLIVEDRAB = 0x6B8E23, "Olive Drab"
    DARKOLIVEGREEN = 0x556B2F, "Dark Olive Green"
    MEDIUMAQUAMARINE = 0x66CDAA, "Medium Aquamarine"
    DARKSEAGREEN = 0x8FBC8F, "Dark Sea Green"
    LIGHTSEAGREEN = 0x20B2AA, "Light Sea Green"
    DARKCYAN = 0x008B8B, "Dark Cyan"
    TEAL = 0x008080, "Teal"
    CYAN = 0x00FFFF, "Cyan"
    LIGHTCYAN = 0xE0FFFF, "Light Cyan"
    PALETURQUOISE = 0xAFEEEE, "Pale Turquoise"
    AQUAMARINE = 0x7FFFD4, "Aquamarine"
    TURQUOISE = 0x40E0D0, "Turquoise"
    MEDIUMTURQUOISE = 0x48D1CC, "Medium Turquoise"
    DARKTURQUOISE = 0x00CED1, "Dark Turquoise"
    CADETBLUE = 0x5F9EA0, "Cadet Blue"
    STEELBLUE = 0x4682B4, "Steel Blue"
    LIGHTSTEELBLUE = 0xB0C4DE, "Light Steel Blue"
    LIGHTBLUE = 0xADD8E6, "Light Blue"
    POWDERBLUE = 0xB0E0E6, "Powder Blue"
    LIGHTSKYBLUE = 0x87CEFA, "Light Sky Blue"
    SKYBLUE = 0x87CEEB, "Sky Blue"
    CORNFLOWERBLUE = 0x6495ED, "Cornflower Blue"
    DEEPSKYBLUE = 0x00BFFF, "Deep Sky Blue"
    DODGERBLUE = 0x1E90FF, "Dodger Blue"
    ROYALBLUE = 0x4169E1, "Royal Blue"
    BLUE = 0x0000FF, "Blue"
    MEDIUMBLUE = 0x0000CD, "Medium Blue"
    DARKBLUE = 0x00008B, "Dark Blue"
    NAVY = 0x000080, "Navy"
    MIDNIGHTBLUE = 0x191970, "Midnight Blue"
    CORNSILK = 0xFFF8DC, "Cornsilk"
    BLANCHEDALMOND = 0xFFEBCD, "Blanched Almond"
    BISQUE = 0xFFE4C4, "Bisque"
    NAVAJOWHITE = 0xFFDEAD, "Navajo White"
    WHEAT = 0xF5DEB3, "Wheat"
    BURLYWOOD = 0xDEB887, "Burly Wood"
    TAN = 0xD2B48C, "Tan"
    ROSYBROWN = 0xBC8F8F, "Rosy Brown"
    SANDYBROWN = 0xF4A460, "Sandy Brown"
    GOLDENROD = 0xDAA520, "Goldenrod"
    DARKGOLDENROD = 0xB8860B, "Dark Goldenrod"
    PERU = 0xCD853F, "Peru"
    CHOCOLATE = 0xD2691E, "Chocolate"
    OLIVE = 0x808000, "Olive"
    SADDLEBROWN = 0x8B4513, "Saddle Brown"
    SIENNA = 0xA0522D, "Sienna"
    BROWN = 0xA52A2A, "Brown"
    MAROON = 0x800000, "Maroon"
    WHITE = 0xFFFFFF, "White"
    SNOW = 0xFFFAFA, "Snow"
    HONEYDEW = 0xF0FFF0, "Honeydew"
    MINTCREAM = 0xF5FFFA, "Mint Cream"
    AZURE = 0xF0FFFF, "Azure"
    ALICEBLUE = 0xF0F8FF, "Alice Blue"
    GHOSTWHITE = 0xF8F8FF, "Ghost White"
    WHITESMOKE = 0xF5F5F5, "White Smoke"
    SEASHELL = 0xFFF5EE, "Seashell"
    BEIGE = 0xF5F5DC, "Beige"
    OLDLACE = 0xFDF5E6, "Old Lace"
    FLORALWHITE = 0xFFFAF0, "Floral White"
    IVORY = 0xFFFFF0, "Ivory"
    ANTIQUEWHITE = 0xFAEBD7, "Antique White"
    LINEN = 0xFAF0E6, "Linen"
    LAVENDERBLUSH = 0xFFF0F5, "Lavender Blush"
    MISTYROSE = 0xFFE4E1, "Misty Rose"
    GAINSBORO = 0xDCDCDC, "Gainsboro"
    LIGHTGRAY = 0xD3D3D3, "Light Gray"
    SILVER = 0xC0C0C0, "Silver"
    DARKGRAY = 0xA9A9A9, "Dark Gray"
    DIMGRAY = 0x696969, "Dim Gray"
    GRAY = 0x808080, "Gray"
    LIGHTSLATEGRAY = 0x778899, "Light Slate Gray"
    SLATEGRAY = 0x708090, "Slate Gray"
    DARKSLATEGRAY = 0x2F4F4F, "Dark Slate Gray"
    BLACK = 0x000000, "Black"


class Qualification(_enums.TextChoices):
    """Qualification enum for the Brazilian Taxpayer Registry (CNPJ).

    Available in <https://www38.receita.fazenda.gov.br/cadsincnac/jsp/coleta/ajuda/topicos/Tabela_III_-_Qualificacao.htm> last access: 24/04/2024 at 10:06 AM
    """

    ADMINISTRATOR = "05", "Administrador"
    BOARD_MEMBER = "08", "Conselheiro de Administração"
    CURATOR = "09", "Curador"
    DIRECTOR = "10", "Diretor"
    INTERVENTOR = "11", "Interventor"
    INVENTORY_MANAGER = "12", "Inventariante"
    LIQUIDATOR = "13", "Liquidante"
    MOTHER = "14", "Mãe"
    FATHER = "15", "Pai"
    PRESIDENT = "16", "Presidente"
    ATTORNEY = "17", "Procurador"
    CONDOMINIUM_MANAGER = "19", "Síndico (Condomínio)"
    ASSOCIATED_COMPANY = "20", "Sociedade Consorciada"
    AFFILIATED_COMPANY = "21", "Sociedade Filiada"
    PARTNER = "22", "Sócio"
    CAPITALIST_PARTNER = "23", "Sócio Capitalista"
    NOMINATED_PARTNER = "24", "Sócio Comanditado"
    LIMITED_PARTNER = "25", "Sócio Comanditário"
    INDUSTRY_PARTNER = "26", "Sócio de Indústria"
    MANAGING_PARTNER = "28", "Sócio-Gerente"
    INCAPACITATED_PARTNER = (
        "29",
        "Sócio ou Acionista Incapaz ou Relativamente Incapaz (exceto menor)",
    )
    MINOR_PARTNER = "30", "Sócio ou Acionista Menor (Assistido/Representado)"
    OSTENSIVE_PARTNER = "31", "Sócio Ostensivo"
    NOTARY = "32", "Tabelião"
    INDIVIDUAL_REAL_ESTATE_OWNER = "34", "Titular de Empresa Individual Imobiliária"
    GUARDIAN = "35", "Tutor"
    FOREIGN_JURIDICAL_PARTNER = "37", "Sócio Pessoa Jurídica Domiciliado no Exterior"
    FOREIGN_PHYSICAL_PARTNER = (
        "38",
        "Sócio Pessoa Física Residente ou Domiciliado no Exterior",
    )
    DIPLOMAT = "39", "Diplomata"
    CONSUL = "40", "Cônsul"
    INTERNATIONAL_ORGANIZATION_REPRESENTATIVE = (
        "41",
        "Representante de Organização Internacional",
    )
    REGISTRY_OFFICER = "42", "Oficial de Registro"
    RESPONSIBLE = "43", "Responsável"
    FOREIGN_MINISTER_OF_STATE = "46", "Ministro de Estado das Relações Exteriores"
    RESIDENT_PHYSICAL_PARTNER = "47", "Sócio Pessoa Física Residente no Brasil"
    DOMICILED_JURIDICAL_PARTNER = "48", "Sócio Pessoa Jurídica Domiciliado no Brasil"
    ADMINISTRATIVE_PARTNER = "49", "Sócio-Administrador"
    ENTREPRENEUR = "50", "Empresário"
    POLITICAL_CANDIDATE = "51", "Candidato a Cargo Político Eletivo"
    CAPITAL_PARTNER = "52", "Sócio com Capital"
    NON_CAPITAL_PARTNER = "53", "Sócio sem Capital"
    FOUNDER = "54", "Fundador"
    FOREIGN_COMMANDITARY_PARTNER = "55", "Sócio Comanditado Residente no Exterior"
    FOREIGN_PHYSICAL_COMMANDITARY_PARTNER = (
        "56",
        "Sócio Comanditário Pessoa Física Residente no Exterior",
    )
    FOREIGN_JURIDICAL_COMMANDITARY_PARTNER = (
        "57",
        "Sócio Comanditário Pessoa Jurídica Domiciliado no Exterior",
    )
    INCAPACITATED_COMMANDITARY_PARTNER = "58", "Sócio Comanditário Incapaz"
    RURAL_PRODUCER = "59", "Produtor Rural"
    HONORARY_CONSUL = "60", "Cônsul Honorário"
    INDIGENOUS_RESPONSIBLE = "61", "Responsável Indígena"
    EXTRATERRITORIAL_INSTITUTIONS_REPRESENTATIVE = (
        "62",
        "Representante das Instituições Extraterritoriais",
    )
    TREASURY_STOCK = "63", "Cotas em Tesouraria"
    JUDICIAL_ADMINISTRATOR = "64", "Administrador Judicial"
    BRAZILIAN_RESIDENT_PHYSICAL_TITLEHOLDER = (
        "65",
        "Titular Pessoa Física Residente ou Domiciliado no Brasil",
    )
    FOREIGN_RESIDENT_PHYSICAL_TITLEHOLDER = (
        "66",
        "Titular Pessoa Física Residente ou Domiciliado no Exterior",
    )
    INCAPACITATED_PHYSICAL_TITLEHOLDER = (
        "67",
        "Titular Pessoa Física Incapaz ou Relativamente Incapaz (exceto menor)",
    )
    MINOR_PHYSICAL_TITLEHOLDER = (
        "68",
        "Titular Pessoa Física Menor (Assistido/Representado)",
    )
    FOREIGN_RESIDENT_ADMINISTRATOR = (
        "70",
        "Administrador Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_BOARD_MEMBER = (
        "71",
        "Conselheiro de Administração Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_DIRECTOR = "72", "Diretor Residente ou Domiciliado no Exterior"
    FOREIGN_RESIDENT_PRESIDENT = "73", "Presidente Residente ou Domiciliado no Exterior"
    FOREIGN_RESIDENT_ADMINISTRATIVE_PARTNER = (
        "74",
        "Sócio-Administrador Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_FOUNDER = "75", "Fundador Residente ou Domiciliado no Exterior"
    DOMICILED_BRAZILIAN_JURIDICAL_TITLEHOLDER = (
        "78",
        "Titular Pessoa Jurídica Domiciliada no Brasil",
    )
    DOMICILED_FOREIGN_JURIDICAL_TITLEHOLDER = (
        "79",
        "Titular Pessoa Jurídica Domiciliada no Exterior",
    )


class LegalNatureQualification(_enums.TextChoices):
    """Legal Nature Qualification enum for the Brazilian Taxpayer Registry (CNPJ).

    Available in <https://www38.receita.fazenda.gov.br/cadsincnac/jsp/coleta/ajuda/topicos/Tabela_IV_-_Natureza_Juridica_Quadro_de_Socios_e_Administradores.htm> last access: 24/04/2024 at 10:44 AM
    """

    ADMINISTRATOR = "05", "Administrador"
    BOARD_MEMBER = "08", "Conselheiro de Administração"
    DIRECTOR = "10", "Diretor"
    PRESIDENT = "16", "Presidente"
    ASSOCIATED_COMPANY = "20", "Sociedade Consorciada"
    AFFILIATED_COMPANY = "21", "Sociedade Filiada"
    PARTNER = "22", "Sócio"
    NOMINATED_PARTNER = "24", "Sócio Comanditado"
    LIMITED_PARTNER = "25", "Sócio Comanditário"
    INCAPACITATED_PARTNER = (
        "29",
        "Sócio ou Acionista Incapaz ou Relativamente Incapaz (exceto menor)",
    )
    MINOR_PARTNER = "30", "Sócio ou Acionista Menor (Assistido/Representado)"
    OSTENSIVE_PARTNER = "31", "Sócio Ostensivo"
    FOREIGN_JURIDICAL_PARTNER = "37", "Sócio Pessoa Jurídica Domiciliado no Exterior"
    FOREIGN_PHYSICAL_PARTNER = (
        "38",
        "Sócio Pessoa Física Residente ou Domiciliado no Exterior",
    )
    ADMINISTRATIVE_PARTNER = "49", "Sócio-Administrador"
    CAPITAL_PARTNER = "52", "Sócio com Capital"
    NON_CAPITAL_PARTNER = "53", "Sócio sem Capital"
    FOUNDER = "54", "Fundador"
    FOREIGN_COMMANDITARY_PARTNER = "55", "Sócio Comanditado Residente no Exterior"
    FOREIGN_PHYSICAL_COMMANDITARY_PARTNER = (
        "56",
        "Sócio Comanditário Pessoa Física Residente no Exterior",
    )
    FOREIGN_JURIDICAL_COMMANDITARY_PARTNER = (
        "57",
        "Sócio Comanditário Pessoa Jurídica Domiciliado no Exterior",
    )
    INCAPACITATED_COMMANDITARY_PARTNER = "58", "Sócio Comanditário Incapaz"
    RURAL_PRODUCER = "59", "Produtor Rural"
    TREASURY_STOCK = "63", "Cotas em Tesouraria"
    BRAZILIAN_RESIDENT_PHYSICAL_TITLEHOLDER = (
        "65",
        "Titular Pessoa Física Residente ou Domiciliado no Brasil",
    )
    FOREIGN_RESIDENT_PHYSICAL_TITLEHOLDER = (
        "66",
        "Titular Pessoa Física Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_ADMINISTRATOR = (
        "70",
        "Administrador Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_BOARD_MEMBER = (
        "71",
        "Conselheiro de Administração Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_DIRECTOR = "72", "Diretor Residente ou Domiciliado no Exterior"
    FOREIGN_RESIDENT_PRESIDENT = "73", "Presidente Residente ou Domiciliado no Exterior"
    FOREIGN_RESIDENT_ADMINISTRATIVE_PARTNER = (
        "74",
        "Sócio-Administrador Residente ou Domiciliado no Exterior",
    )
    FOREIGN_RESIDENT_FOUNDER = "75", "Fundador Residente ou Domiciliado no Exterior"
