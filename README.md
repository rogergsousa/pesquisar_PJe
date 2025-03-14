# README do Projeto: Automatização da Extração de Dados do PJe

## Descrição do Projeto
Este projeto automatiza a extração de dados do sistema **PJe (Processo Judicial Eletrônico)** e gera relatórios com base nos números dos processos fornecidos em um arquivo Excel. O script utiliza ferramentas como **Playwright** para automação de navegador, **2Captcha** para resolver captchas e **Pandas** para manipulação de dados.

O objetivo principal é facilitar a consulta de informações judiciais, como o valor do processo e os últimos andamentos, diretamente no PJe TRT10, permitindo que esses dados sejam salvos em um arquivo Excel para posterior análise.

---

## Funcionalidades Principais
- **Conexão com Chrome existente**: Utiliza uma instância do navegador Google Chrome já aberta em modo de depuração.
- **Leitura de Processos**: Lê números de processos a partir de um arquivo Excel (`pesquisar no PJe.xlsx`).
- **Resolução de Captcha**: Resolve automaticamente o captcha utilizando o serviço [2Captcha](https://2captcha.com/).
- **Extração de Dados**: Extrai informações como o valor do processo e o último andamento judicial.
- **Atualização do Excel**: Atualiza o arquivo Excel com os dados coletados.
- **Controle de Execução**: Permite interromper a execução lendo um arquivo de controle (`control.txt`).

---

## Pré-requisitos

### 1. Dependências
Certifique-se de que as seguintes dependências estão instaladas:

- Python 3.8 ou superior
- Bibliotecas Python:
  - `playwright`
  - `pandas`
  - `twocaptcha`
  - `logging`

Instale as bibliotecas necessárias executando o comando abaixo:

```bash
pip install playwright pandas twocaptcha
```

Além disso, instale as dependências do Playwright:

```bash
playwright install
```

### 2. Configuração do Chrome
Para conectar ao navegador Chrome, siga as instruções abaixo:

1. Abra o PowerShell ou Terminal.
2. Execute o comando abaixo para iniciar o Chrome em modo de depuração:

   ```bash
   Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList '--remote-debugging-port=9222', '--user-data-dir="C:\Users\<SEU_USUARIO>\AppData\Local\Google\Chrome\User Data"', '--profile-directory="Default"'
   ```

   Substitua `<SEU_USUARIO>` pelo seu nome de usuário.

### 3. Arquivos Necessários
Os seguintes arquivos devem estar presentes na pasta `resource`:

- `pesquisar no PJe.xlsx`: Arquivo Excel contendo os números dos processos a serem consultados.
- `control.txt`: Arquivo de texto usado para controlar a execução do script. Se o conteúdo for `1`, o script será interrompido.

---

## Estrutura do Projeto

```
projeto-pje/
│
├── resource/
│   ├── pesquisar no PJe.xlsx    # Arquivo Excel com números de processos
│   └── control.txt              # Arquivo de controle
│
├── main.py                      # Script principal
└── README.md                    # Documentação do projeto
```

---

## Como Executar o Projeto

1. Configure o ambiente conforme descrito na seção **Pré-requisitos**.
2. Certifique-se de que o arquivo `pesquisar no PJe.xlsx` está preenchido corretamente com os números dos processos.
3. Defina sua chave de API do 2Captcha na variável de ambiente `APIKEY_2CAPTCHA`. Você pode configurar isso diretamente no terminal:

   ```bash
   export APIKEY_2CAPTCHA="sua_chave_api_aqui"
   ```

   Ou adicione a chave diretamente no código (não recomendado por questões de segurança):

   ```python
   api_key = 'sua_chave_api_aqui'
   ```

4. Execute o script principal:

   ```bash
   python main.py
   ```

5. O script iniciará a automação, navegando pelo PJe, resolvendo captchas e extraindo os dados. Os resultados serão salvos no mesmo arquivo Excel.

---

## Saída Esperada

Após a execução, o arquivo `pesquisar no PJe.xlsx` será atualizado com as seguintes colunas:

- **Processo**: Número do processo consultado.
- **Valor**: Valor monetário extraído do processo.
- **Último Andamento**: Última movimentação registrada no processo.

---

## Observações Importantes

1. **Tratamento de Erros**: O script foi projetado para lidar com erros inesperados durante a execução. Mensagens de log são exibidas no terminal para facilitar a depuração.
2. **Timeouts e Delays**: Foram incluídos tempos de espera (`time.sleep`) para garantir que as páginas carreguem completamente antes da extração de dados.
3. **Limitações**:
   - O script depende do serviço 2Captcha para resolver captchas. Certifique-se de ter créditos suficientes.
   - A automação pode falhar se houver mudanças significativas na interface do PJe.
4. **Segurança**: Não inclua informações sensíveis diretamente no código. Use variáveis de ambiente para armazenar chaves de API e outros dados confidenciais.

---

## Contribuições

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões de melhorias, crie uma issue ou envie um pull request.

---

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvido por:** Rogério G. de Sousa  
**Contato:** [rgsousa@gmail.com]  

--- 

> **Nota**: Este projeto é apenas para fins educacionais e de pesquisa. Certifique-se de seguir todas as leis e regulamentos aplicáveis ao usar este script.