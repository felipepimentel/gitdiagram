# Integração com StackSpot AI

Este documento descreve a integração do GitDiagram com a StackSpot AI como uma alternativa ao Claude para geração e modificação de diagramas de sistema.

## Configuração

### Variáveis de Ambiente

Para usar a StackSpot AI, você precisa configurar as seguintes variáveis de ambiente:

```bash
STACKSPOT_API_KEY=seu_api_key_aqui
STACKSPOT_API_URL=https://api.stackspot.com/v1  # Opcional, usa este valor por padrão
```

## Uso

A integração com a StackSpot AI é opcional e pode ser ativada por requisição. Para usar a StackSpot AI em vez do Claude, adicione o parâmetro `use_stackspot: true` em suas requisições.

### Exemplo de Requisição

```json
{
  "username": "usuario",
  "repo": "repositorio",
  "instructions": "Instruções para o diagrama",
  "use_stackspot": true,
  "api_key": "chave_api_opcional"
}
```

## Funcionalidades

A integração com a StackSpot AI suporta todas as funcionalidades principais do GitDiagram:

1. **Geração de Diagramas**
   - Análise de estrutura do projeto
   - Geração de explicações detalhadas
   - Criação de diagramas Mermaid.js
   - Mapeamento de componentes para arquivos

2. **Modificação de Diagramas**
   - Alteração de diagramas existentes
   - Preservação de explicações e contexto
   - Manutenção de eventos de clique

## Limites e Considerações

- O limite de tokens é o mesmo do Claude (200k tokens)
- A contagem de tokens usa a API da StackSpot quando disponível
- Fallback para estimativa simples de tokens quando necessário
- Mesmo sistema de rate limiting do Claude

## Diferenças do Claude

1. **API**
   - Endpoint diferente para chamadas
   - Estrutura de resposta ligeiramente diferente
   - Sistema próprio de contagem de tokens

2. **Configuração**
   - Chave de API diferente
   - URL base configurável
   - Validação de configuração no início

## Tratamento de Erros

O serviço da StackSpot inclui:
- Validação de chave de API
- Timeout em chamadas (30s para chamadas principais, 5s para contagem de tokens)
- Fallback para estimativa de tokens
- Tratamento de erros de rede e API

## Exemplos de Código

### Usando o Serviço

```python
from app.services.stackspot_service import StackSpotService

# Inicializar o serviço
stackspot = StackSpotService()

# Fazer uma chamada
response = stackspot.call_stackspot_api(
    system_prompt="Instruções do sistema",
    data={"key": "value"},
    api_key="opcional"
)
```

### Contagem de Tokens

```python
# Usando a API da StackSpot (com fallback)
token_count = stackspot.count_tokens("Texto para contar tokens")
```

## Manutenção

Para manter a integração:

1. **Monitoramento**
   - Verificar logs de erro
   - Monitorar rate limits
   - Acompanhar uso de tokens

2. **Atualizações**
   - Manter URLs atualizadas
   - Verificar mudanças na API
   - Atualizar estimativas de tokens

3. **Testes**
   - Testar com diferentes tamanhos de entrada
   - Verificar fallbacks
   - Validar respostas

## Troubleshooting

### Problemas Comuns

1. **Erro de Autenticação**
   - Verificar STACKSPOT_API_KEY
   - Confirmar formato do token
   - Checar validade da chave

2. **Timeout**
   - Verificar conexão
   - Reduzir tamanho da entrada
   - Tentar novamente

3. **Contagem de Tokens**
   - Verificar acesso ao endpoint
   - Usar estimativa como fallback
   - Ajustar limites se necessário 