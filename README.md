🛠️ Industrial Defect Inspector v2.0
Uma estação de trabalho de alto desempenho para análise de segmentação e inspeção de defeitos em superfícies industriais. Desenvolvido com Python e Dear PyGui, focado em processamento acelerado por GPU e visualização em tempo real de grandes datasets.

🌟 Destaques do Projeto
Performance GPU: Renderização de texturas e sobreposições processadas diretamente na memória de vídeo.

Alpha Blending Dinâmico: Controle deslizante para ajuste de transparência da máscara de defeito sobre a peça original.

Navegação Sincronizada: Alternância rápida entre amostras mantendo a integridade entre imagem original (.BMP) e máscara de segmentação (.PNG).

Processamento com Numpy: Cálculos matriciais rápidos para manipulação de canais RGBA.

📁 Estrutura do Dataset
O projeto está configurado para operar com datasets industriais (como MVTec AD, KolektorSDD), organizados da seguinte forma:

```plaintext
projeto-inspecao/
├── src/
│   ├── __init__.py    # Inicializador do pacote
│   ├── main.py        # Entrypoint (Interface Gráfica GPU)
│   └── utils.py       # Auditoria e Logs de integridade
├── data/              # Base de dados (3GB+ de imagens/máscaras)
├── pyproject.toml     # Configuração de dependências (uv)
└── README.md          # Documentação Técnica
```

🚀 Como Executar
Pré-requisitos
Este projeto utiliza o uv para gerenciamento ultra-rápido de dependências.

Instalação e Execução
Clone este repositório.

Certifique-se de que os dados estão no caminho configurado no main.py.

Execute o projeto:

```bash
# Sincronizar dependências e rodar
uv run src/main.py
```

### Bibliotecas Utilizadas

- `dearpygui`: Engine gráfica baseada em GPU (C++).

- `numpy`: Manipulação matemática de matrizes de pixels.

- `pillow`: Processamento e conversão de formatos de imagem.

## 🛠️ Funcionalidades Implementadas

- [x] Carregamento automático de pares Imagem/Máscara.

- [x] Interface reativa com troca de amostras em tempo real.

- [x] Sobreposição (Overlay) de defeitos com canal Alpha ajustável.

- [x] Redimensionamento automático de máscaras para garantir integridade do processamento.

### 🛠️ Novas Implementações de Impacto

- [x] **Arquitetura de Pacotes:** Organização em `src/` para facilitar a escalabilidade e manutenção do código.

- [x] **Auditoria Automatizada:** O sistema agora realiza um *check* de integridade no `utils.py` antes de iniciar a GUI, garantindo que cada `.bmp` (Original) possua seu respectivo `.png` (Máscara).

- [x] **Módulo de Log de Auditoria:**
  
  - **Verificação em Tempo Real:** Varredura recursiva nos 20 produtos do dataset.
  
  - **Persistência de Dados:** Geração automática do arquivo `integrity_log.txt` com o relatório detalhado de arquivos ausentes ou corrompidos.

- [x] **Interface Reativa (v2.1):** Integração dos resultados da auditoria diretamente no fluxo de navegação, evitando que o software tente carregar dados inexistentes.

## 🔮 Próximos Passos (Roadmap)

- [ ] Implementação de Zoom/Pan para inspeção de micro-defeitos.

- [ ] Tabela lateral com métricas (área do defeito em pixels, confiança do modelo).

- [ ] Integração com modelos de Deep Learning (Few-Shot Segmentation).

- [ ] Exportação de relatórios de inspeção em PDF/PNG.

---

**Desenvolvido por Charles Duarte** *Explorando o futuro da inspeção visual no chão de fábrica.*

:

---

## 🔍 Solução de Problemas (Troubleshooting)

### 1. "No item named tex_org" ou Erros de Tag

Se a interface abrir mas as imagens não aparecerem, verifique se o caminho no `DATA_DIR` dentro do `main.py` está correto. No Windows, use o prefixo `r` antes das aspas:

```python
DATA_DIR = r"D:\seu\caminho\aqui"
```

### 2. Performance em PCs sem Placa de Vídeo Dedicada

O projeto utiliza aceleração por GPU. Se notar lentidão ao arrastar o slider de Alpha:

- Certifique-se de que os drivers de vídeo (Intel HD Graphics ou similar) estão atualizados.

- O software exige suporte mínimo a **OpenGL 3.3** ou **DirectX 11**.

### 3. Diferença de tamanho entre BMP e PNG

O script possui uma rotina de `resize` automático via Pillow para evitar que o Numpy trave caso a máscara tenha dimensões diferentes da imagem original. Se a sobreposição parecer "deslocada", verifique se o dataset original não possui bordas assimétricas.

### 4. Erros de Memória com Datasets Gigantes

Embora o dataset possa ter 3GB, o script carrega apenas **um par de imagens por vez** na memória RAM/GPU. Se houver travamentos, feche outras aplicações que consumam muita memória de vídeo (como navegadores com muitas abas ou softwares CAD).

---

- .

### 🔍 Seção de Troubleshooting (Atualizada)

**Problemas com Imports:** Se receber um `ModuleNotFoundError` ao tentar rodar o script, certifique-se de estar usando o comando `uv run src/main.py`. O `uv` injeta automaticamente o diretório `src/` no ambiente, permitindo que o `main.py` reconheça o `utils.py` sem configurações extras.

**Relatórios de Erros:** Sempre que o sistema for iniciado, verifique a raiz do projeto pelo arquivo `integrity_log.txt`. Ele conterá a lista exata de quais amostras do seu dataset de 3GB precisam de correção manual.

### Dica de ouro para o seu Git:

Como você está trabalhando em um diretório chamado `D:\reposground\work\projeto-inspecao`, não esqueça de criar um arquivo chamado **`.gitignore`** na raiz do projeto e adicionar as seguintes linhas:

```plaintext
# Ignorar arquivos do Python
__pycache__/
*.py[cod]

# Ignorar o dataset (pois é muito grande para o Git)
data/

# Ignorar ambiente virtual do uv
.venv/
```

Isso garante que, quando você subir o código para o GitHub ou GitLab, o Git não tente fazer o upload dos 3GB de imagens, apenas dos seus scripts e do README.
