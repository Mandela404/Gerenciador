# Gerenciador de Tarefas com Interface Gráfica (customtkinter)

Este projeto é um **gerenciador de tarefas** com uma interface gráfica moderna feita com `customtkinter`. Ele oferece informações sobre uso de CPU, memória, GPU, redes e permite matar processos manualmente. Inclui suporte a **dois idiomas**: Português e Inglês.

---

## Funcionalidades

- Visualização de:
  - Uso de CPU
  - Memória RAM
  - GPUs (via GPUtil)
  - Atividade de rede (dados enviados/recebidos)
  - Tarefas em execução
  - Gráfico histórico (CPU/Memória)
- Comparativo de uso entre CPU, GPU e Memória
- Suporte a dois idiomas (PT/EN) com troca em tempo real
- Interface escura, moderna e responsiva
- Botão para encerrar/matar tarefas selecionadas

---

## Como usar

1. **Clone o repositório ou baixe os arquivos**
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Execute o programa:**
   ```bash
   python Taks.py
   ```

---

## Dependências
As dependências estão listadas no `requirements.txt`, mas resumidamente:

- `customtkinter`: UI moderna
- `psutil`: acesso a informações do sistema
- `GPUtil`: leitura de dados da GPU (NVIDIA)
- `matplotlib`: renderização de gráficos

---

## Screenshots (opcional)
Adicione aqui capturas de tela se desejar demonstrar o visual da interface.

---

## Autor
**Seu Nome ou GitHub**

Sinta-se livre para contribuir com melhorias!

