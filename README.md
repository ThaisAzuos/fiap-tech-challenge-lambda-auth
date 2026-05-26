# fiap-tech-challenge-lambda-auth

## 🎯 Propósito
Este repositório implementa uma função AWS Lambda serverless para autenticação de usuários via CPF e geração de JSON Web Tokens (JWT) com algoritmo RS256. A função é exposta através de um AWS API Gateway.

## 🛠️ Tech Stack
- **Linguagem**: Python 3.9+
- **Framework**: AWS Lambda
- **Serviços AWS**: Lambda, API Gateway, ECR, IAM
- **Ferramentas**: Terraform, Docker
- **Bibliotecas Python**: `psycopg2` (para PostgreSQL), `pyjwt`, `cryptography`
- **Observabilidade**: New Relic Lambda Layer

## 📊 Arquitetura
```mermaid
graph TD
    User[Usuário] --> |POST /authenticate {cpf}| APIGateway[API Gateway]
    APIGateway --> Lambda[AWS Lambda: fiap-tech-challenge-lambda-auth]
    Lambda --> |Consulta CPF| RDS[RDS PostgreSQL]
    Lambda --> |Gera JWT RS256| Lambda
    Lambda --> |Retorna {token, expiry}| APIGateway
    Lambda -- Logs & Metrics --> NewRelic[New Relic Platform]
```

## 🚀 Quick Start (Setup Local)
Para desenvolver e testar a função Lambda localmente, você pode usar Docker.

1.  **Pré-requisitos**: Docker, Python 3.9+, `pip`, `aws-cli`.
2.  **Instalar dependências**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar variáveis de ambiente**: Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis (para testes locais, não para produção):
    ```
    DB_HOST=your_local_db_host
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
    ```
    **Nota**: A `JWT_PRIVATE_KEY` deve ser a chave privada RSA completa, incluindo os cabeçalhos `BEGIN/END` e com quebras de linha (`\n`).
4.  **Executar testes**:
    ```bash
    pytest tests/
    ```
5.  **Build e execução local (via Docker)**:
    ```bash
    docker build -t lambda-auth .
    docker run -p 9000:8080 -e DB_HOST=$DB_HOST -e DB_NAME=$DB_NAME -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -e JWT_PRIVATE_KEY="$JWT_PRIVATE_KEY" lambda-auth:latest
    ```
    Após iniciar o container, você pode testar a função Lambda localmente enviando uma requisição POST para `http://localhost:9000/2015-03-31/functions/function/invocations`.

## 📋 Deploy (CI/CD com GitHub Actions)
Este repositório utiliza GitHub Actions para automação de CI/CD.
O workflow `main.yml` (localizado em `.github/workflows/main.yml`) executa as seguintes etapas:
1.  **`build-and-test`**:
    *   Instala dependências Python.
    *   Executa testes unitários (`pytest`).
    *   Autentica no AWS ECR.
    *   Constrói a imagem Docker da Lambda e a envia para o ECR.
2.  **`terraform-plan`**:
    *   Inicializa o Terraform.
    *   Valida a configuração do Terraform.
    *   Gera um plano de execução do Terraform, passando variáveis sensíveis via GitHub Secrets.
3.  **`terraform-apply`**:
    *   **Aprovação Manual**: Para deploys na branch `main` (ou ambiente `production`), é necessária uma aprovação manual (configurada via GitHub Environments).
    *   Aplica o plano gerado, provisionando ou atualizando a função Lambda e o API Gateway na AWS.

**Configuração Necessária no GitHub:**
*   **Secrets**: Configure os seguintes GitHub Secrets no seu repositório:
    *   `AWS_ACCOUNT_ID`: O ID da sua conta AWS.
    *   `DB_HOST`: Host do seu RDS PostgreSQL (obtido do output do `fiap-tech-challenge-db-terraform`).
    *   `DB_NAME`: Nome do banco de dados.
    *   `DB_USER`: Usuário do banco de dados.
    *   `DB_PASSWORD`: Senha do banco de dados.
    *   `JWT_PRIVATE_KEY`: Sua chave privada RS256 para assinar JWTs.
    *   `NEWRELIC_LAMBDA_LAYER_ARN`: O ARN completo do New Relic Lambda Layer para Python na sua região e versão de runtime (ex: `arn:aws:lambda:us-east-1:451483290750:layer:NewRelicPython39:XX`).
*   **IAM Roles**: Crie os seguintes IAM Roles na AWS e configure-os para serem assumidos pelo GitHub Actions:
    *   `github-actions-lambda-auth-ecr-role`: Com permissões para ECR.
    *   `github-actions-lambda-auth-terraform-role`: Com permissões para gerenciar Lambda, API Gateway, IAM, CloudWatch.
*   **Environments**: Crie um ambiente chamado `production` (ou o nome que você usou no workflow) nas configurações do seu repositório GitHub e adicione "Required reviewers" para aprovação manual.

## 🔗 Links Relacionados
- [Aplicação Principal (fiap-tech-challenge-app)](../fiap-tech-challenge-app/README.md)
- [Infraestrutura Kubernetes (fiap-tech-challenge-k8s-terraform)](../fiap-tech-challenge-k8s-terraform/README.md)
- [Banco de Dados Terraform (fiap-tech-challenge-db-terraform)](../fiap-tech-challenge-db-terraform/README.md)
- [Documentação Geral da Fase 3](../../docs/Fase03/QuickStart-Fase3d-3e.md)
