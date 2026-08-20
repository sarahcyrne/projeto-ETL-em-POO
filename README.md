# Projeto Integrador – Extração de Dados do IBGE (PNAD Contínua)

## Integrantes do grupo
- Caliel Feijó
- Giulia Ferreira
- Sarah Cyrne Ferreira

## Descrição

Este projeto dá continuidade à solução construída em aula (Aula 02 –
Engenharia de Dados), que utiliza a API de Agregados do IBGE
(`servicodados.ibge.gov.br`) e Programação Orientada a Objetos (POO) em
Python para extrair dados da **Tabela 4093 do SIDRA**:

> Pessoas de 14 anos ou mais de idade, total, na força de trabalho, ocupadas,
> desocupadas, fora da força de trabalho, em situação de informalidade e
> respectivas taxas e níveis, por sexo.

## Estrutura do projeto (igual à criada em aula)

```
.
├── src/
│   ├── __init__.py
│   ├── extract.py      # Classe Extract: acessa a API e retorna o JSON
│   └── load.py          # Classe Load: salva os dados em arquivo .json
├── main.py               # Executa a extração e o salvamento dos dados
├── requirements.txt
├── .gitignore
└── README.md
```

Cada classe tem uma única responsabilidade (princípio da responsabilidade
única, apresentado em aula):
- **`Extract`** só extrai os dados da API;
- **`Load`** só salva os dados em disco (arquivo `.json`).

## O que foi adaptado em relação ao código da aula

Em aula, o método `extract_pnadc()` tinha a URL fixa, apenas para a
variável **4099** (taxa de desocupação) e o estado de **Pernambuco**
(`N3[26]`). Para resolver o desafio proposto (extrair outros estados e
outras variáveis **sem duplicar código**), o método foi adaptado para
receber `variavel` e `localidade` como parâmetros:

```python
def extract_pnadc(self, variavel, localidade="26"):
    url = (
        "https://servicodados.ibge.gov.br/api/v3/agregados/4093"
        "/periodos/201201-202601"
        f"/variaveis/{variavel}"
        f"?localidades=N3[{localidade}]&classificacao=2[all]"
    )
    response = requests.get(url)
    data = response.json()
    return data
```

Assim, a mesma classe/método é reutilizado para:

| Variável | Código |
|---|---|
| Taxa de desocupação | 4099 |
| Taxa de participação na força de trabalho | 4096 |
| Taxa de informalidade | 12466 |

E para os estados que o grupo quiser consultar, bastando informar o
código IBGE da Unidade da Federação (ex.: 26 = Pernambuco, 23 = Ceará,
25 = Paraíba etc.).

No `main.py`, dois dicionários (`VARIAVEIS` e `ESTADOS`) definem quais
variáveis e quais estados serão extraídos, e um laço `for` percorre todas
as combinações, chamando sempre o mesmo método `extract_pnadc()` e
salvando cada resultado em um arquivo `.json` diferente (ex.:
`pernambuco_taxa_desocupacao.json`, `ceara_taxa_informalidade.json`, etc.).

## Como executar

```bash
# 1. Clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Executar o projeto
python main.py
```

Ao final, o script gera um arquivo `.json` para cada combinação de
estado + variável, na raiz do projeto.

## Como adicionar mais estados ou variáveis

Basta editar os dicionários `ESTADOS` e `VARIAVEIS` no início do
`main.py` — não é necessário alterar `extract.py` nem `load.py`:

```python
ESTADOS = {
    "26": "pernambuco",
    "23": "ceara",
    "25": "paraiba",
    "21": "maranhao",   # exemplo de novo estado
}
```

Códigos IBGE de estado (Unidade da Federação - N3) mais usados no
Nordeste: 21-Maranhão, 22-Piauí, 23-Ceará, 24-Rio Grande do Norte,
25-Paraíba, 26-Pernambuco, 27-Alagoas, 28-Sergipe, 29-Bahia.

## Observação

A pasta do ambiente virtual (`.venv`) **não deve ser enviada** ao
repositório — ela já está listada no `.gitignore`.
