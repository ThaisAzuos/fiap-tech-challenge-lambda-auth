# ADR 001 — Papel do Auth Service na Arquitetura de Microsserviços (Fase 4)

**Status:** Aceita
**Data:** 2026-07-10
**Fase:** Tech Challenge Fase 4 — FIAP SOAT

---

## Contexto

Na Fase 3, este serviço (`fiap-tech-challenge-lambda-auth`) já existia como uma função Lambda independente, autenticando por CPF e emitindo JWT (RS256), consumida pelo monólito `fiap-tech-challenge-app`. Com a decomposição em microsserviços na Fase 4 (ver ADR-005 em `fiap-tech-challenge-app`), passam a existir três serviços de negócio (OS Service, Billing Service, Execution Service) que precisam autenticar/autorizar requisições.

## Decisão

Manter este serviço sem alterações funcionais, atuando como **Auth Service compartilhado** pelos três microsserviços de negócio da Fase 4:

- Continua emitindo JWT assinado com chave privada RS256 via `POST /authenticate`.
- Os três serviços de negócio validam o token **localmente**, usando a chave pública já distribuída, sem chamada síncrona a este serviço a cada requisição — apenas no momento do login.
- Nenhuma mudança de infraestrutura ou de contrato de API é necessária neste repositório para a Fase 4.

## Alternativas consideradas

- **Migrar a autenticação para dentro do OS Service**: rejeitada; o serviço já funciona de forma independente e sem estado desde a Fase 3, e mantê-lo separado reforça a arquitetura de microsserviços exigida na Fase 4 (é, na prática, um quarto serviço independente, com seu próprio repositório e infraestrutura).
- **Introduzir validação síncrona centralizada (um serviço "gateway" de auth chamado a cada requisição)**: rejeitada por adicionar latência e um ponto único de falha; a validação local via chave pública já usada na Fase 3 é suficiente e mais resiliente.

## Consequências

- Este repositório não precisa de mudanças de código nesta fase, apenas de documentação atualizada explicando seu papel no novo desenho (ver README).
- O diagrama geral de arquitetura da Fase 4 (mantido em `fiap-tech-challenge-app/docs/arquitetura/fase4-visao-geral.md`) referencia este serviço como Auth Service.
