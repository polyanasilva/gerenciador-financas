# Gerenciador de FInanças

Um sistema pessoal de controle financeiro desenvolvido com [Streamlit](https://streamlit.io/), onde você pode registrar seus gastos e recebimentos, visualizar relatórios por categoria e exportar os dados em CSV. Criado com foco em simplicidade, segurança e organização. O projeto ainda está em processo de construção e melhorias

---

## ✨ Funcionalidades

- Tela de login com autenticação de usuários
- Formulário para registrar **gastos** e **recebimentos** com:
  - Data
  - Valor
  - Tipo (Gasto ou Recebimento)
  - Categoria (ex: Alimentação, Lazer, etc.)
  - Descrição livre
- Armazenamento automático em arquivos CSV mensais
- Visualização interativa dos registros:
  - Filtros por categoria e tipo
  - Totais de gastos, recebimentos e saldo
- Exportação dos dados filtrados para CSV

---

## Como rodar o projeto

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/financas-poly.git
cd financas-poly
```

2. Instale as dependências

```bash
pip install streamlit pandas
```

3. Rode o app

```bash
streamlit run main.py
```
## Estrutura do projeto

```bash
gerenciador-financas/
├── main.py               # App principal com Streamlit
├── users.csv             # Usuários cadastrados (autenticação)
├── dados/                # Arquivos CSV mensais
└── utils/
    └── auth.py           # Funções de login e criptografia