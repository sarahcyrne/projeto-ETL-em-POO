import requests


class Extract():
    """
    Classe responsável por acessar a API do IBGE (agregados/SIDRA) e
    desserializar os dados retornados em formato JSON.

    Seguindo o princípio da responsabilidade única, essa classe SÓ cuida
    de extrair os dados da API — não formata, não salva, não trata nada.

    Adaptação feita para o desafio: em vez de deixar a URL "fixa" (só para
    a variável 4099 e o estado de Pernambuco, como foi mostrado em aula),
    o método extract_pnadc() agora recebe a variável e a localidade como
    PARÂMETROS. Assim, a mesma classe e o mesmo método servem para
    qualquer uma das três variáveis do desafio (desocupação, participação
    na força de trabalho e informalidade) e para qualquer estado — sem
    precisar duplicar código.
    """

    def __init__(self):
        pass

    def extract_pnadc(self, variavel, localidade="26", sexo="all"):
        """
        Consulta a Tabela 4093 do IBGE (PNAD Contínua trimestral) para uma
        variável e um estado (localidade) específicos.

        Parâmetros
        ----------
        variavel : int | str
            Código da variável a ser consultada. No desafio:
                4099  - Taxa de desocupação
                4096  - Taxa de participação na força de trabalho
                12466 - Taxa de informalidade
                
        localidade : int | str
            Código IBGE do estado (Unidade da Federação - N3).
            Padrão: "26" (Pernambuco, usado como exemplo em aula).
            Alguns códigos de estados do Nordeste:
                21 - Maranhão   | 22 - Piauí     | 23 - Ceará
                24 - Rio Grande do Norte | 25 - Paraíba
                26 - Pernambuco | 27 - Alagoas   | 28 - Sergipe | 29 - Bahia

        sexo : int | str
        Código da categoria de sexo (classificação 2 da tabela 4093).
        Padrão: "all" (traz as três categorias juntas na mesma resposta).
        Códigos do desafio:
            6794 - Total
            4    - Homens
            5    - Mulheres

        Retorna
        -------
        list[dict] : os dados brutos retornados pela API, em JSON.
        """
        url = (
            "https://servicodados.ibge.gov.br/api/v3/agregados/4093"
            "/periodos/201201-202601"
            f"/variaveis/{variavel}"
            f"?localidades=N3[{localidade}]&classificacao=2[{sexo}]"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
