# TCell - Manual Premium de Assistência Técnica

Este repositório contém os materiais, notas técnicas e recursos do **Manual Premium de Assistência Técnica TCell**, focado na manutenção de alta performance de smartphones.

## 📋 Estrutura do Projeto

*   `Ebook_Manual_Premium_Celular.md` e `.html`: Conteúdo base do e-book detalhando os fundamentos.
*   `Prompts_Midjourney_Capitulo_1.md`: Guia de referências visuais e prompts para geração de imagens da bancada e processos.
*   [recursos.md](file:///c:/Users/Taiane/Documents/Nexus%20Ia/recursos.md): Catálogo de ferramentas, insumos e equipamentos de segurança essenciais.
*   `anotacoes/`: Pasta dedicada ao registro de práticas de bancada e procedimentos efetuados.
    *   [Técnica-01.md](file:///c:/Users/Taiane/Documents/Nexus%20Ia/anotacoes/T%C3%A9cnica-01.md): Modelo/Template para documentação de reparos.
*   [nexus_agent.py](file:///c:/Users/Taiane/Documents/Nexus%20Ia/nexus_agent.py): Script de Inteligência Artificial usando LangChain e Gemini para conversar com o manual técnico.

---

## 🚀 Os 6 Pilares da TCell

1.  **Capítulo 1: O Berço do Especialista – Organização e Segurança de Elite**
    *   Montagem de bancada antiestática (ESD), mapeamento de parafusos (*Long Screw Damage*) e manuseio de baterias de íons de lítio.
2.  **Capítulo 2: Anatomia Revelada – Desmontagem Segura e Diagnóstico Sem Erros**
    *   Mapeamento de conectores, blindagens e abertura profissional de aparelhos.
3.  **Capítulo 3: O Santo Graal dos Reparos I – Troca de Telas com Acabamento de Fábrica**
    *   Substituição de telas LCD/OLED/AMOLED e uso de adesivos específicos (B-7000/T-7000).
4.  **Capítulo 4: O Santo Graal dos Reparos II – Recuperando Conectores de Carga e Soldagem Essencial**
    *   Reparos Tipo-C/Micro-USB usando estação de retrabalho e solda quente.
5.  **Capítulo 5: Revivendo o Aparelho – Diagnóstico e Substituição de Baterias**
    *   Remoção química de colas, choque em baterias adormecidas e segurança térmica.
6.  **Capítulo 6: O Segredo do Lucro – Precificação Estratégica, Garantia e Atendimento Premium**
    *   Gestão financeira da assistência e fidelização de clientes.

---

## 🛠️ Como Contribuir e Usar as Anotações

Para documentar um novo reparo efetuado em sua bancada:
1. Vá até a pasta `anotacoes/`.
2. Duplique o arquivo [Técnica-01.md](file:///c:/Users/Taiane/Documents/Nexus%20Ia/anotacoes/T%C3%A9cnica-01.md).
3. Renomeie para a numeração/nome do seu reparo (ex: `Técnica-02-Troca-Tela-A32.md`).
4. Preencha os campos com os dados do serviço.

---

## 🤖 Agente de Inteligência Artificial (Nexus IA)

O arquivo [nexus_agent.py](file:///c:/Users/Taiane/Documents/Nexus%20Ia/nexus_agent.py) permite interagir com a IA (Google Gemini) de forma que ela use os dados do seu manual do e-book para responder a perguntas técnicas.

### Pré-requisitos (Instalação)
No terminal da pasta do seu projeto, instale as bibliotecas necessárias do Python:
```bash
pip install langchain langchain-community langchain-google-genai pypdf unstructured
```

### Como Executar
1. Defina sua chave de API do Gemini nas variáveis de ambiente ou digite-a quando o script solicitar ao iniciar.
2. Execute o script com o comando:
   ```bash
   python nexus_agent.py
   ```

---

## 📦 Como Enviar para o GitHub

Caso queira inicializar este repositório no seu GitHub, siga os passos abaixo no terminal:

```bash
# 1. Inicializar o repositório local
git init

# 2. Adicionar todos os arquivos ao versionamento
git add .

# 3. Criar o primeiro commit
git commit -m "Initial commit: TCell project structure"

# 4. Renomear a branch principal para main
git branch -M main

# 5. Adicionar a URL do seu repositório remoto no GitHub
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git

# 6. Enviar os arquivos para o GitHub
git push -u origin main
```
