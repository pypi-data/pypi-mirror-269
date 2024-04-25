import random as _random

import validate_docbr as _validate_docbr
from faker.providers import BaseProvider as _BaseProvider

__all__ = ["PhoneProvider", "ProductProvider", "BrazilPersonProvider"]


class PhoneProvider(_BaseProvider):
    """A Faker provider for phone numbers.

    This provider is based on the Brazilian phone number format.
    """

    area_codes = {
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "21",
        "22",
        "24",
        "27",
        "28",
        "31",
        "32",
        "33",
        "34",
        "35",
        "37",
        "38",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "51",
        "53",
        "54",
        "55",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "71",
        "73",
        "74",
        "75",
        "77",
        "79",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "91",
        "92",
        "93",
        "94",
        "95",
        "96",
        "97",
        "98",
        "99",
    }

    def country_code(self) -> str:
        """Returns the Brazilian country code."""
        return "55"

    def area_code(self) -> str:
        """Returns a random area code from the Brazilian phone number format."""
        return _random.choice(tuple(self.area_codes))  # noqa: S311

    def phone_number(self) -> str:
        """Returns a random phone number without neither the country code nor the area code."""
        return f"9{self.numerify('@#######')}"


class ProductProvider(_BaseProvider):
    """A Faker provider for products."""

    words = [
        "Acelerador",
        "Adaptador",
        "Agitador",
        "Amortecedor",
        "Âncora",
        "Antena",
        "Aplicador",
        "Armadilha",
        "Aspirador",
        "Balança",
        "Barreira",
        "Batedor",
        "Bloqueador",
        "Bobina",
        "Bomba",
        "Cabo",
        "Caixa",
        "Câmara",
        "Candeeiro",
        "Capacitor",
        "Carga",
        "Carregador",
        "Carrinho",
        "Catalisador",
        "Chave",
        "Circuito",
        "Colchão",
        "Compressor",
        "Conector",
        "Controlador",
        "Conversor",
        "Corda",
        "Cortador",
        "Detector",
        "Dispositivo",
        "Distribuidor",
        "Divisor",
        "Dreno",
        "Embalagem",
        "Empilhador",
        "Enrolador",
        "Escova",
        "Espelho",
        "Estrutura",
        "Extrator",
        "Filtro",
        "Fita",
        "Fluxo",
        "Forro",
        "Frasco",
        "Frasqueira",
        "Gabinete",
        "Gerador",
        "Grade",
        "Guia",
        "Ilhós",
        "Injetor",
        "Interruptor",
        "Isolador",
        "Junta",
        "Lâmpada",
        "Lente",
        "Limitador",
        "Linha",
        "Luminária",
        "Manípulo",
        "Manta",
        "Máquina",
        "Martelo",
        "Máscara",
        "Medidor",
        "Módulo",
        "Mola",
        "Moldura",
        "Motor",
        "Mouse",
        "Núcleo",
        "Óculos",
        "Óleo",
        "Orifício",
        "Painel",
        "Parafuso",
        "Pedal",
        "Pilha",
        "Pino",
        "Placa",
        "Ponte",
        "Porta",
        "Pote",
        "Pulverizador",
        "Radiador",
        "Reator",
        "Recipiente",
        "Refletor",
        "Regulador",
        "Relevo",
        "Reservatório",
        "Resistor",
        "Roda",
        "Rolamento",
        "Sensor",
        "Seringa",
        "Sistema",
        "Suporte",
        "Tampa",
        "Tanque",
        "Tela",
        "Termostato",
        "Torno",
        "Transformador",
        "Transmissor",
        "Trava",
        "Tubo",
        "Unidade",
        "Válvula",
        "Ventilador",
        "Vidro",
        "Visor",
    ]

    modifiers = [
        "Avançado",
        "Básico",
        "Completo",
        "Especial",
        "Exclusivo",
        "Master",
        "Premium",
        "Profissional",
        "Sênior",
        "Standard",
        "Único",
        "Bom",
        "Ótimo",
        "Excelente",
        "Extra",
        "Super",
        "Ultra",
        "Mega",
        "Turbo",
        "Plus",
        "Max",
        "Prime",
        "Top",
        "Vip",
        "Gold",
        "Silver",
        "Platinum",
        "Diamond",
        "Black",
        "White",
        "Red",
        "Blue",
        "Green",
        "Yellow",
        "Orange",
        "Purple",
        "Pink",
        "Brown",
        "Grey",
        "Elegante",
        "Econômico",
        "Inovador",
        "Potente",
        "Compacto",
        "Confiável",
        "Versátil",
        "Moderno",
        "Clássico",
        "Estiloso",
        "Resistente",
        "Leve",
        "Robusto",
        "Premium",
        "Luxuoso",
        "Durável",
        "Inteligente",
        "Acessível",
        "Fácil",
        "Rápido",
        "Silencioso",
        "Seguro",
        "Eficiente",
        "Ecológico",
        "Confortável",
        "Original",
        "Divertido",
        "Gourmet",
        "Fresco",
        "Artesanal",
        "Saboroso",
        "Natural",
        "Orgânico",
    ]

    extra = [
        "Aconchegante",
        "Alegre",
        "Arrojado",
        "Arrojado",
        "Atemporal",
        "Atrevido",
        "Atrevido",
        "Autêntico",
        "Aventureiro",
        "Brilhante",
        "Brilhante",
        "Cativante",
        "Chique",
        "Cintilante",
        "Contemporâneo",
        "Criativo",
        "Desafiador",
        "Descolado",
        "Deslumbrante",
        "Dinâmico",
        "Divertido",
        "Dourado",
        "Elegante",
        "Empolgante",
        "Empolgante",
        "Encantador",
        "Encantador",
        "Energético",
        "Esplêndido",
        "Esplêndido",
        "Esplendoroso",
        "Esplendoroso",
        "Estonteante",
        "Estonteante",
        "Etnico",
        "Eufórico",
        "Excepcional",
        "Exótico",
        "Extraordinário",
        "Fantástico",
        "Fascinante",
        "Favorito",
        "Floral",
        "Futurista",
        "Geek",
        "Harmonioso",
        "Icônico",
        "Impactante",
        "Impecável",
        "Inesquecível",
        "Inovador",
        "Inspirador",
        "Irreverente",
        "Lúdico",
        "Luminoso",
        "Magnífico",
        "Maravilhoso",
        "Minimalista",
        "Original",
        "Ótimo",
        "Perfeito",
        "Personalizado",
        "Poderoso",
        "Premium",
        "Radiante",
        "Radiante",
        "Refinado",
        "Retrô",
        "Revigorante",
        "Sensacional",
        "Sofisticado",
        "Supremo",
        "Sustentável",
        "Tecnológico",
        "Útil",
        "Vencedor",
        "Versátil",
        "Vibrante",
        "Vintage",
        "Vital",
        "Vivaz",
    ]

    def product_name(self, extra_word_chance: float = 0.5) -> str:
        """Returns a random product name."""

        word_parts = [
            self.random_element(self.words),
            self.random_element(self.modifiers),
        ]

        if _random.random() < extra_word_chance:  # noqa: S311
            word_parts.append(self.random_element(self.extra))

        return " ".join(word_parts)


class BrazilPersonProvider(_BaseProvider):
    def cpf(self, *args, **kwargs) -> str:
        """Returns a valid CPF number."""
        return _validate_docbr.CPF().generate(*args, **kwargs)

    def cnpj(self, *args, **kwargs) -> str:
        """Returns a valid CNPJ number."""
        return _validate_docbr.CNPJ().generate(*args, **kwargs)

    def cnh(self, *args, **kwargs) -> str:
        """Returns a valid CNH number."""
        return _validate_docbr.CNH().generate(*args, **kwargs)

    def cns(self, *args, **kwargs) -> str:
        """Returns a valid CNS number."""
        return _validate_docbr.CNS().generate(*args, **kwargs)

    def pis(self, *args, **kwargs) -> str:
        """Returns a valid PIS number."""
        return _validate_docbr.PIS().generate(*args, **kwargs)

    def titulo_eleitoral(self, *args, **kwargs) -> str:
        """Returns a valid Titulo Eleitoral number."""
        return _validate_docbr.TituloEleitoral().generate(*args, **kwargs)

    def certidao(self, *args, **kwargs) -> str:
        """Returns a valid Certidao number."""
        return _validate_docbr.Certidao().generate(*args, **kwargs)

    def renavam(self, *args, **kwargs) -> str:
        """Returns a valid RENAVAM number."""
        return _validate_docbr.RENAVAM().generate(*args, **kwargs)
