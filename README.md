<!-- Banner do Projeto -->
<p align="center">
  <img src="https://github.com/user-attachments/assets/746cf2e3-c3fb-4f3d-92bf-1b9d9d85d509" alt="API Labor Banner" width="60%" />

<h1 align="center">API Labor</h1>
<p align="center">
  <b>BackEnd do projeto <a href="https://github.com/LeoBP1987/labor">Labor</a>: Organize, automatize e evolua sua rotina de tarefas de forma simples e eficiente.</b>
  <br>
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/LeoBP1987/api-labor">
</p>

---

> 🛠️ **Este repositório é o BackEnd (API) do projeto [Labor](https://github.com/LeoBP1987/labor)**  
> Para a interface web (FrontEnd), acesse o repositório [Labor](https://github.com/LeoBP1987/labor).

---

## ✨ Sobre o Projeto

A **API Labor** é uma API RESTful desenvolvida em Python, responsável pelo gerenciamento de tarefas, rotinas recorrentes, planejamento semanal e autenticação de usuários.  
Ela fornece toda a estrutura e dados para o FrontEnd do sistema Labor, disponível em [Labor](https://github.com/LeoBP1987/labor).

Ideal para quem deseja automatizar a rotina, controlar tarefas repetitivas e ter uma visão clara das atividades semanais, seja para uso pessoal, times, ou integração em outras aplicações.

---

## 🗄️ Banco de Dados Híbrido

Uma das características técnicas mais importantes da API Labor é sua arquitetura de banco de dados híbrida:

- **Usuários:** armazenados em banco de dados relacional (**PostgreSQL**).
- **Tarefas, repetições e planejamento semanal:** armazenados em banco de dados não relacional (**MongoDB**).

Isso permite o melhor aproveitamento de cada tecnologia, garantindo robustez no controle de usuários e flexibilidade na gestão de tarefas e rotinas.

---

## 🔐 Autenticação

A autenticação de usuários utiliza o protocolo **OAuth2** (Resource Owner Password Credentials), fornecendo tokens de acesso no padrão JWT para garantir segurança nas operações e fácil integração com o frontend.

---

## 🛠️ Endpoints Customizados e Operações em Massa

Além dos endpoints RESTful tradicionais (CRUD), a API Labor implementa ações personalizadas e sobrescreve métodos em suas ViewSets para permitir:

- **Criação, atualização e exclusão de múltiplos objetos em uma única requisição** (por exemplo, deletar várias tarefas ou repetições de uma só vez).
- **Ações customizadas para operações complexas**, como montagem automática de semana, execução em lote de repetições, etc.
- **Filtros avançados** para facilitar buscas específicas e operações eficientes.

Esses recursos tornam o uso da API mais eficiente e flexível para integrações, automações e uso avançado.

---

## 🖼️ Funcionalidades

<div align="center">
  <img src="https://github.com/user-attachments/assets/1bb405c9-1cf8-4795-8e97-c9028c0fb040" alt="Funcionalidades" width="20%"/>
</div>

- **Tarefas**: CRUD completo para gerenciamento de tarefas.
- **Repetições**: Cadastre rotinas semanais recorrentes automaticamente.
- **Semana**: Gere planejamentos semanais automáticos.
- **Autenticação OAuth2**: Segurança e flexibilidade por tokens.
- **Gestão de Usuários**: Cadastro, login, recuperação e alteração de senha.
- **Filtros inteligentes**: Encontre tarefas por usuário, data ou descrição.
- **Endpoints Especiais**: Automatize execuções e planejamentos.
- **Operações em Massa**: Realize ações sobre múltiplos registros em uma única chamada.

---

## 🏗️ Modelos de Dados

| Tarefas              | Repetições                     | Semana                                            |
|----------------------|-------------------------------|---------------------------------------------------|
| `usuario` (int)      | `usuario` (int)               | `usuario` (int)                                   |
| `descricao` (str)    | `descricao` (str)             | `indicador` (str: "A" semana atual, "B" próxima)  |
| `agendamento` (date) | `repeticoes` (list de int)    | `segunda` ... `domingo` (date)                    |
| `comentarios` (str)  |                               |                                                   |

---

## 🚀 Exemplos de Uso

### Criando uma Repetição

```json
{
  "usuario": 1,
  "descricao": "Exercício físico",
  "repeticoes": [1, 3, 5] // Segunda, Quarta, Sexta
}
```

### Montando a Semana

- Use o endpoint especial para gerar automaticamente a agenda semanal baseada nas rotinas cadastradas.

### Excluindo múltiplas repetições

```json
// Exemplo de payload para exclusão em massa
["id_repeticao_1", "id_repeticao_2", "id_repeticao_3"]
```
- Basta enviar uma requisição DELETE para o endpoint de exclusão em lote.

---

## 🖥️ Tecnologias

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/OAuth2-009688?style=for-the-badge&logo=oauth&logoColor=white"/>
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens"/>
</p>

---

## ⚡ Instalação e Uso

```bash
git clone https://github.com/LeoBP1987/api-labor.git
cd api-labor
pip install -r requirements.txt
# Configure variáveis de ambiente para PostgreSQL, MongoDB e OAuth2
python manage.py runserver
```

---

## 🧪 Testes

Execute os testes automatizados:
```bash
python manage.py test
```

---

## 📢 Integração com o FrontEnd

Este backend foi projetado para ser consumido pelo FrontEnd do Labor:  
👉 [https://github.com/LeoBP1987/labor](https://github.com/LeoBP1987/labor)

Você pode rodar ambos localmente para uma experiência completa de desenvolvimento!

---

## 🙋‍♂️ Contribuição e Contato

Sinta-se à vontade para abrir issues, enviar PRs ou sugerir melhorias!  
Desenvolvido por [LeoBP1987](https://github.com/LeoBP1987)

<p align="center">
  <img src="https://user-images.githubusercontent.com/3369400/233833168-1e5cd3b8-5c5e-4e9e-8f2b-1e57e9b8b9c2.png" alt="Organização" width="30%"/>
</p>