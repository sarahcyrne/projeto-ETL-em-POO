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

Em aula, o método extract_pnadc() tinha uma URL fixa, apenas para a variável 4099 (taxa de desocupação), o estado de Pernambuco (N3[26]) e todas as categorias de sexo juntas. Para resolver o desafio proposto (extrair outras variáveis, estados e categorias de sexo, sem duplicar código), o método foi adaptado para receber variavel, localidade e sexo como parâmetros:

```python
def extract_pnadc(self, variavel, localidade="26", sexo="all"):
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
```

Assim, a mesma classe/método é reutilizado para:

| Variável | Código |
|---|---|
| Taxa de desocupação | 4099 |
| Taxa de participação na força de trabalho | 4096 |
| Taxa de informalidade | 12466 |

| Sexo	| Código
|---|---|
| Total	| 6794
| Homens	| 4
| Mulheres | 5

E para os estados que o grupo quiser consultar, bastando informar o
código IBGE da Unidade da Federação (ex.: 26 = Pernambuco, 23 = Ceará,
25 = Paraíba etc.).

Também foi adicionado tratamento de erro com raise_for_status(), para que uma falha na API não interrompa a extração das demais combinações — isso é tratado no main.py, que percorre variáveis, estados e categorias de sexo em loop, capturando e reportando erros individualmente sem travar o processo inteiro.

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
estado + variável + categoria de sexo, na raiz do projeto.

## Como adicionar estados, variáveis ou categorias de sexo

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

A pasta do ambiente virtual (`.venv`) **não deve ser enviada** ao repositório — ela já está listada no `.gitignore`.

Os arquivos `.json` gerados pela extração (um para cada combinação de estado, variável e sexo) também estão no `.gitignore` e não são versionados no repositório. Eles são criados automaticamente ao rodar `python main.py`, então não é necessário — nem recomendado — subi-los manualmente pro Git: bastar executar o projeto localmente para gerá-los novamente a qualquer momento.
