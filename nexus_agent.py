import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredImageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Função para carregar Documentos (PDF, TXT, MD, etc.)
def carregar_documento(caminho_arquivo):
    if caminho_arquivo.endswith('.pdf'):
        loader = PyPDFLoader(caminho_arquivo)
        paginas = loader.load()
    elif caminho_arquivo.endswith(('.txt', '.md', '.html')):
        loader = TextLoader(caminho_arquivo, encoding='utf-8')
        paginas = loader.load()
    else:
        raise ValueError("Formato de arquivo não suportado. Use PDF, TXT, MD ou HTML.")
    
    # Divide o texto em pedaços menores para o Nexus processar
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_divididos = text_splitter.split_documents(paginas)
    return docs_divididos

# 2. Função para carregar Imagens (Visão Computacional)
def carregar_imagem(caminho_imagem):
    # Correção do erro de digitação original
    loader = UnstructuredImageLoader(caminho_imagem)
    imagem_processada = loader.load()
    return imagem_processada

# 3. Função principal para rodar o Nexus IA
def rodar_nexus():
    print("=== Inicializando Nexus IA ===")
    
    # Verifica se a chave de API do Gemini está configurada
    if "GOOGLE_API_KEY" not in os.environ:
        print("\n⚠️ AVISO: A variável de ambiente GOOGLE_API_KEY não foi encontrada.")
        print("Defina a chave no seu terminal:")
        print("  No Windows (cmd): set GOOGLE_API_KEY=sua_chave_aqui")
        print("  No PowerShell: $env:GOOGLE_API_KEY=\"sua_chave_aqui\"\n")
        api_key = input("Ou digite a sua Google API Key aqui para continuar: ").strip()
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        else:
            print("Não é possível continuar sem uma API Key.")
            return

    # Inicializa o modelo Gemini (gemini-1.5-flash)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    # Carregar o manual local se existir para RAG (Contexto)
    contexto = ""
    caminho_manual = "Ebook_Manual_Premium_Celular.md"
    if os.path.exists(caminho_manual):
        print(f"Carregando contexto de: {caminho_manual}...")
        docs = carregar_documento(caminho_manual)
        contexto = "\n\n".join([doc.page_content for doc in docs])
        print("Manual carregado com sucesso!")
    else:
        print("Manual local não encontrado. O Nexus responderá com seu conhecimento geral.")

    # Loop de perguntas
    print("\nNexus IA pronto! Faça suas perguntas (ou digite 'sair' para encerrar):")
    while True:
        pergunta = input("\nVocê: ").strip()
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando Nexus IA. Até logo!")
            break
        
        if not pergunta:
            continue
            
        print("Nexus pensando...")
        
        # Cria o prompt do chat
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é o Nexus IA, um assistente técnico especialista em manutenção de smartphones da TCell. "
                       "Use o seguinte contexto do manual técnico para responder de forma precisa, profissional e didática "
                       "às dúvidas. Se não souber a resposta ou se ela não estiver no manual, use seu conhecimento geral "
                       "sobre manutenção de celulares de forma segura.\n\nContexto:\n{context}"),
            ("human", "{question}")
        ])
        
        # Executa a chamada do modelo
        chain = prompt | llm
        try:
            resposta = chain.invoke({"context": contexto, "question": pergunta})
            print(f"\nNexus: {resposta.content}")
        except Exception as e:
            print(f"\n❌ Erro ao chamar o modelo: {e}")

if __name__ == "__main__":
    rodar_nexus()
