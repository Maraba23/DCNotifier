# DCNotifier

Uma biblioteca Python leve e poderosa para enviar mensagens e notificações de erro para canais do Discord via webhooks, com integração especial para aplicações Django.

## Índice

- [Instalação](#instalação)
- [Início Rápido](#início-rápido)
- [Recursos](#recursos)
- [Uso Básico](#uso-básico)
- [Envio de Mensagens Avançadas](#envio-de-mensagens-avançadas)
- [Notificação de Erros](#notificação-de-erros)
- [Integração com Django](#integração-com-django)
- [Referência da API](#referência-da-api)
- [Exemplos Completos](#exemplos-completos)

## Instalação

```bash
pip install dcnotifier
```

## Início Rápido

```python
from dcnotifier import DCNotifier

# Inicialize o notificador
notifier = DCNotifier(webhook="https://discord.com/api/webhooks/seu_webhook_url")

# Envie uma mensagem simples
notifier.send_message("Olá do DCNotifier!")

# Envie uma mensagem com embed
notifier.send_message(
    content="Mensagem com embed",
    embed_params={
        "title": "Título do Embed",
        "description": "Descrição do embed",
        "color": 3447003  # Azul
    }
)

# Notifique um erro (ideal para blocos try/except)
try:
    # Seu código aqui
    1/0
except Exception as e:
    notifier.notify_error(e)
```

## Recursos

- 🚀 API simples e intuitiva
- 🔌 Integração pronta para Django
- 🧩 Suporte completo para recursos do Discord (embeds, campos, imagens, etc.)
- 🔔 Notificações de erro detalhadas e personalizáveis
- 🔄 Method chaining para APIs fluentes
- 📊 Formatação rica para relatórios de erro

## Uso Básico

### Inicialização

```python
from dcnotifier import DCNotifier

# Inicialização básica
notifier = DCNotifier(webhook="https://discord.com/api/webhooks/seu_webhook_url")

# Inicialização com nome e avatar personalizados
notifier = DCNotifier(
    webhook="https://discord.com/api/webhooks/seu_webhook_url",
    username="Bot de Notificações",
    avatar_url="https://exemplo.com/avatar.png"
)
```

### Mensagens Simples

```python
# Enviar mensagem de texto
notifier.set_content("Olá, mundo!").send()

# Alternativa usando send_message
notifier.send_message("Olá, mundo!")

# Mensagem com nome personalizado para esta mensagem específica
notifier.set_content("Mensagem importante!").set_username("Alerta").send()
```

## Envio de Mensagens Avançadas

### Trabalhando com Embeds

```python
# Adicionar um embed básico
embed = notifier.add_embed(
    title="Título do Embed",
    description="Esta é uma descrição do embed",
    color=3447003,  # Azul
    url="https://exemplo.com",
    timestamp=datetime.now()
)

# Adicionar campos ao embed
notifier.add_embed_field(embed, "Campo 1", "Valor 1")
notifier.add_embed_field(embed, "Campo 2", "Valor 2", inline=True)
notifier.add_embed_field(embed, "Campo 3", "Valor 3", inline=True)

# Adicionar autor
notifier.set_embed_author(
    embed,
    name="Nome do Autor",
    icon_url="https://exemplo.com/autor.png",
    url="https://exemplo.com/perfil"
)

# Adicionar rodapé
notifier.set_embed_footer(
    embed,
    text="Rodapé do Embed",
    icon_url="https://exemplo.com/footer.png"
)

# Adicionar imagem e miniatura
notifier.set_embed_thumbnail(embed, "https://exemplo.com/thumbnail.png")
notifier.set_embed_image(embed, "https://exemplo.com/image.png")

# Enviar a mensagem
notifier.send()
```

### Method Chaining

```python
# Você pode encadear métodos para uma API mais fluente
notifier.set_content("Aqui está um relatório importante") \
    .set_username("Sistema de Relatórios") \
    .set_avatar_url("https://exemplo.com/relatorio.png") \
    .send()
```

## Notificação de Erros

O ponto forte do DCNotifier é a capacidade de notificar erros de forma detalhada:

```python
try:
    # Código que pode gerar uma exceção
    result = complicated_function()
except Exception as e:
    # Notificação básica de erro
    notifier.notify_error(e)
    
    # OU notificação detalhada
    notifier.notify_error(
        error=e,
        request=django_request,  # Opcional, para integração com Django
        extra_info={
            "Função": "complicated_function",
            "Parâmetros": "param1=valor1, param2=valor2",
            "ID do Usuário": user.id
        },
        include_traceback=True  # Padrão é True
    )
```

## Integração com Django

O DCNotifier foi projetado para ser facilmente integrado com aplicações Django:

### Configuração

```python
# settings.py
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/seu_webhook_url"
```

### Middleware de Captura de Exceções

```python
# middleware.py
from dcnotifier import DCNotifier
from django.conf import settings

class DiscordErrorNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.notifier = DCNotifier(webhook=settings.DISCORD_WEBHOOK_URL)

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        self.notifier.notify_error(
            error=exception,
            request=request,
            extra_info={
                "View": request.resolver_match.view_name if getattr(request, 'resolver_match', None) else "Unknown"
            }
        )
        return None
```

### Uso em Views

```python
# views.py
from dcnotifier import DCNotifier
from django.conf import settings
from django.http import JsonResponse

notifier = DCNotifier(webhook=settings.DISCORD_WEBHOOK_URL)

def api_view(request):
    try:
        # Lógica da view
        result = process_data(request.POST)
        return JsonResponse({"status": "success", "data": result})
    except Exception as e:
        notifier.notify_error(e, request=request)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
```

## Referência da API

### Classe DCNotifier

#### Inicialização

```python
DCNotifier(webhook: str, username: Optional[str] = None, avatar_url: Optional[str] = None)
```

| Parâmetro   | Tipo   | Descrição                                   |
|-------------|--------|---------------------------------------------|
| webhook     | str    | URL do webhook do Discord                   |
| username    | str    | Nome a ser exibido para as mensagens        |
| avatar_url  | str    | URL do avatar a ser usado                   |

#### Métodos Principais

| Método                   | Descrição                                       |
|--------------------------|------------------------------------------------|
| `clear()`                | Limpa todos os dados da mensagem                |
| `set_content(content)`   | Define o conteúdo de texto da mensagem          |
| `set_username(username)` | Define o nome de exibição para esta mensagem    |
| `set_avatar_url(url)`    | Define a URL do avatar para esta mensagem       |
| `send()`                 | Envia a mensagem configurada                    |
| `send_message(content, embed_params)` | Método rápido para enviar mensagens simples |
| `notify_error(error, request, extra_info, include_traceback)` | Envia notificação de erro |

#### Métodos para Embeds

| Método                                | Descrição                            |
|---------------------------------------|------------------------------------|
| `add_embed(title, description, color, url, timestamp)` | Adiciona um novo embed |
| `add_embed_field(embed, name, value, inline)` | Adiciona um campo ao embed |
| `set_embed_author(embed, name, icon_url, url)` | Define o autor do embed |
| `set_embed_footer(embed, text, icon_url)` | Define o rodapé do embed |
| `set_embed_thumbnail(embed, url)` | Define a miniatura do embed |
| `set_embed_image(embed, url)` | Define a imagem do embed |

#### Exceções

| Exceção                 | Descrição                                |
|-------------------------|------------------------------------------|
| `DCNotifierException`   | Exceção base para a biblioteca           |
| `WebhookError`          | Erro na requisição do webhook            |

## Exemplos Completos

### Sistema de Monitoramento

```python
import time
from dcnotifier import DCNotifier

notifier = DCNotifier(webhook="https://discord.com/api/webhooks/seu_webhook_url")

def monitor_system():
    try:
        # Simula verificação de sistema
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        
        # Cria embed para o relatório
        embed = notifier.add_embed(
            title="Relatório de Sistema",
            color=get_status_color(cpu_usage, memory_usage, disk_usage),
            timestamp=datetime.now()
        )
        
        # Adiciona campos com estatísticas
        notifier.add_embed_field(embed, "CPU", f"{cpu_usage}%", inline=True)
        notifier.add_embed_field(embed, "Memória", f"{memory_usage}%", inline=True)
        notifier.add_embed_field(embed, "Disco", f"{disk_usage}%", inline=True)
        
        # Define rodapé
        notifier.set_embed_footer(embed, "Sistema de Monitoramento v1.0")
        
        # Envia relatório
        notifier.send()
        
    except Exception as e:
        # Se houver erro no monitoramento, notifica
        notifier.notify_error(e, extra_info={"Componente": "Monitor de Sistema"})

# Executa monitoramento a cada hora
while True:
    monitor_system()
    time.sleep(3600)
```

### Middleware Django Avançado

```python
# middleware.py
import time
from dcnotifier import DCNotifier
from django.conf import settings

class PerformanceMonitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.notifier = DCNotifier(
            webhook=settings.DISCORD_WEBHOOK_URL,
            username="Monitor de Performance"
        )
        self.slow_threshold = 1.0  # segundos
        
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        # Notifica se a resposta for muito lenta
        if duration > self.slow_threshold:
            embed = self.notifier.add_embed(
                title="⚠️ Requisição Lenta Detectada",
                description=f"Uma requisição levou {duration:.2f}s para ser processada",
                color=16776960  # Amarelo
            )
            
            # Adiciona informações da requisição
            self.notifier.add_embed_field(
                embed, 
                "Detalhes da Requisição",
                f"**Método:** {request.method}\n"
                f"**Path:** {request.path}\n"
                f"**View:** {request.resolver_match.view_name if getattr(request, 'resolver_match', None) else 'Unknown'}\n"
                f"**Usuário:** {request.user if request.user.is_authenticated else 'Anônimo'}"
            )
            
            # Define rodapé com timestamp
            self.notifier.set_embed_footer(embed, "Monitoramento de Performance")
            
            # Envia notificação
            self.notifier.send()
            
        return response
```

---

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests no repositório do projeto: [https://github.com/seu-usuario/dcnotifier](https://github.com/maraba23/dcnotifier)

## Licença

Este projeto está licenciado sob a Licença Apache-2.0 - veja o arquivo LICENSE para detalhes.