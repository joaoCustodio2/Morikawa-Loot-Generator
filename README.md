# Morikawa Loot Generator

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Linguagem](https://img.shields.io/badge/linguagem-Python-blue)
![Interface](https://img.shields.io/badge/interface-Tkinter-orange)

Uma ferramenta de desktop completa e intuitiva para Mestres de RPG, projetada para agilizar a criação de recompensas e a rolagem de dados. Crie, gerencie e sorteie itens com facilidade, mantendo o foco na sua história.

![Screenshot do Morikawa Loot](screenshot.png)

---

## Índice
1. [Principais Funcionalidades](#principais-funcionalidades)
2. [Como Instalar e Executar](#como-instalar-e-executar-para-usuários)
3. [Guia de Uso Detalhado](#guia-de-uso-detalhado)
    - [Aba: Gerador de Recompensa](#aba-gerador-de-recompensa)
    - [Aba: Manter Itens](#aba-manter-itens)
    - [Aba: Rolar Dados](#aba-rolar-dados)
4. [Entendendo os Arquivos](#entendendo-os-arquivos-do-programa)
5. [Para Desenvolvedores](#para-desenvolvedores)

---

## Principais Funcionalidades

- **Gerador de Recompensas Flexível:** Sorteie itens com base em 5 raridades (Comum, Incomum, Raro, Épico, Lendário) com pesos totalmente customizáveis.
- **Sorteio de Moedas:** Gere uma quantidade de moedas em um intervalo mínimo e máximo definido por você.
- **Gerenciador de Itens Completo (CRUD):** Adicione, edite e exclua itens da sua base de dados de forma visual e intuitiva.
- **Rolador de Dados:** Inclui dados padrão (d4, d6, d8, d10, d12, d20, d100) e um rolador de dados personalizado.
- **Histórico Persistente:** O programa salva automaticamente o conteúdo das caixas de resultado e sua lista de itens para a próxima vez que você abrir.
- **Interface Moderna:** Utiliza um tema customizado para uma aparência mais agradável, com opção de modo claro e escuro.
- **Atalhos de Teclado:** Funções otimizadas para agilizar o cadastro de itens, como usar as teclas `Enter` e `Delete`.

---

## Como Instalar e Executar (Para Usuários)

Para usar o programa, não é necessário instalar Python ou qualquer dependência. Basta seguir os passos abaixo:

1.  **Baixe a Versão Mais Recente:**
    * Vá para a seção de **[Releases](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO/releases/latest)** deste repositório.
    * Baixe o arquivo `.zip` (por exemplo, `Morikawa.Loot.v1.0.0.zip`).

2.  **Descompacte o Arquivo:**
    * Clique com o botão direito no arquivo `.zip` baixado e escolha "Extrair tudo..." ou "Unzip here".
    * Isso criará uma pasta com o nome do programa (ex: `Morikawa Loot`).

3.  **Mantenha os Arquivos Juntos (Importante!):**
    * Dentro da pasta que você extraiu, haverá o executável e outros arquivos. **Todos eles precisam ficar na mesma pasta para que o programa funcione corretamente.** A estrutura será parecida com esta:
        ```
        /Morikawa Loot/
        |
        |-- Morikawa Loot.exe  (O programa principal que você vai abrir)
        |-- loot_geral.csv     (Sua lista de itens!)
        |-- parametros.json    (Seus pesos de raridade salvos)
        |-- icone.ico
        |-- sv_ttk/            (Pasta do tema visual)
        |-- (e vários outros arquivos que o programa usa)
        ```

4.  **Execute o Programa:**
    * Dê um duplo clique no arquivo `Morikawa Loot.exe` para iniciar a aplicação. Pronto!

---

## Guia de Uso Detalhado

### Aba: Gerador de Recompensa
Nesta tela, você pode sortear itens e moedas para seus jogadores.

1.  **Configure as Probabilidades (Pesos):**
    * Marque as caixas de seleção (`Incluir?`) para as raridades que podem aparecer no sorteio.
    * Ajuste o "Peso" de cada raridade. Um número maior significa que a raridade tem mais chances de ser sorteada.
    * Clique em "Salvar Pesos como Padrão" para que suas configurações de peso sejam carregadas da próxima vez que abrir o programa.

2.  **Escolha as Quantidades:**
    * **Qtd. Itens:** Defina quantos itens serão sorteados.
    * **Min/Max Moedas:** Defina o intervalo para o sorteio de moedas.

3.  **Gerar Recompensa:**
    * Clique em "Gerar Recompensa Completa!" para ver o resultado na caixa de texto abaixo. Os itens aparecerão coloridos de acordo com sua raridade.

### Aba: Manter Itens
Aqui você gerencia sua base de dados de itens.

-   **Adicionar um Item:**
    1.  Clique no botão "Limpar Campos".
    2.  Digite o nome do novo item.
    3.  Selecione a raridade na caixa de seleção.
    4.  Clique em "Adicionar Novo" ou pressione a tecla `Enter`.
    * **Dica de agilidade:** Após adicionar um item, a raridade é mantida e o campo "Nome" é focado automaticamente, permitindo que você adicione vários itens da mesma raridade em sequência, apenas digitando o nome e apertando `Enter`.

-   **Editar um Item:**
    1.  Clique no item que deseja editar na lista. Seus dados aparecerão nos campos abaixo.
    2.  Altere o nome e/ou a raridade.
    3.  Clique em "Salvar Edição" ou pressione `Enter` no campo de nome.

-   **Excluir um Item:**
    1.  Clique no item que deseja remover na lista.
    2.  Clique em "Excluir Selecionado" ou pressione a tecla `Delete`.
    3.  Confirme a exclusão na janela que aparecerá.

### Aba: Rolar Dados
Um utilitário simples para rolagens de dados.

-   **Quantidade:** Defina quantos dados você quer rolar no campo "Rodar".
-   **Dados Padrão:** Clique em qualquer um dos botões (d4, d6, etc.) para uma rolagem rápida.
-   **Dado Personalizado:** Digite o número de lados no campo "Lados" e clique em "Rolar!".
-   O resultado e o histórico das rolagens aparecem na caixa de texto. Você pode limpar o histórico com o botão "Limpar Log de Rolagens".

---

## Entendendo os Arquivos do Programa

Ao usar o programa, ele irá ler e criar alguns arquivos na pasta dele. É importante que eles fiquem junto do `.exe`.

-   `Morikawa Loot.exe`: O programa executável.
-   `loot_geral.csv`: **Sua base de dados de itens.** Este é um arquivo de texto separado por vírgulas. Você pode abri-lo e editá-lo com programas como Excel, Google Sheets ou Bloco de Notas para adicionar muitos itens de uma vez. Apenas mantenha as colunas `nome_item` e `raridade`.
-   `parametros.json`: Salva suas configurações de "Peso" das raridades. É editado automaticamente pelo programa.
-   `historico.json`: Salva o texto das caixas de resultado para que elas não estejam vazias quando você reabrir o programa.
-   `rolagens_log.txt`: Um log permanente de todas as rolagens de dados feitas na aba "Rolar Dados", com data e hora.

---

## Para Desenvolvedores

Se você deseja executar ou modificar o projeto a partir do código-fonte:

1.  **Pré-requisitos:**
    * [Python 3](https://www.python.org/) instalado.

2.  **Instalação:**
    * Clone este repositório: `git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git`
    * Navegue até a pasta do projeto e instale as dependências:
        ```bash
        pip install sv-ttk
        ```

3.  **Execução:**
    * Para rodar o script, execute:
        ```bash
        python main.py
        ```