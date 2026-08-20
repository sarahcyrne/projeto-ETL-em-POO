from src.extract import Extract
from src.load import Load

VARIAVEIS = {
    "4099": "taxa_desocupacao",
    "4096": "taxa_participacao_forca_trabalho",
    "12466": "taxa_informalidade",
}

ESTADOS = {
    "26": "pernambuco",
    "23": "ceara",
    "25": "paraiba",
}

extract = Extract()
load = Load()

for codigo_variavel, nome_variavel in VARIAVEIS.items():
    for codigo_estado, nome_estado in ESTADOS.items():
        print(f"Extraindo {nome_variavel} - {nome_estado}...")

        dados = extract.extract_pnadc(
            variavel=codigo_variavel,
            localidade=codigo_estado,
        )

        nome_arquivo = f"{nome_estado}_{nome_variavel}"
        load.load_json(nome_arquivo, dados)

        print(f"Arquivo salvo: {nome_arquivo}.json\n")

print("Extração concluída!")
