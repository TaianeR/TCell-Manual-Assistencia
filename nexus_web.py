import os
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader

# ─────────────────────────────────────────────
# Configuração da Página (DEVE ser o 1º comando Streamlit)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus IA – Assistente TCell",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS Customizado – Visual Premium Dark
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Fundo geral */
    html, body, .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 50%, #0a1628 100%);
        font-family: 'Inter', sans-serif;
        color: #e6edf3;
    }

    /* Remover header padrão do Streamlit */
    #MainMenu, header, footer { visibility: hidden; }

    /* Container principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 820px;
    }

    /* ── Mensagens de Chat ── */
    .chat-bubble {
        padding: 14px 18px;
        border-radius: 16px;
        margin-bottom: 12px;
        line-height: 1.65;
        font-size: 0.95rem;
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .user-bubble {
        background: linear-gradient(135deg, #1e3a5f, #1a4a7a);
        border: 1px solid #2a5a9f;
        border-bottom-right-radius: 4px;
        margin-left: 15%;
        box-shadow: 0 4px 15px rgba(30, 120, 220, 0.2);
    }

    .nexus-bubble {
        background: linear-gradient(135deg, #161b22, #1c2333);
        border: 1px solid #30363d;
        border-bottom-left-radius: 4px;
        margin-right: 15%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* Rótulos das mensagens */
    .bubble-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
        opacity: 0.65;
    }

    .user-label  { color: #79c0ff; }
    .nexus-label { color: #3fb950; }

    /* Divider do histórico */
    .chat-divider {
        border: none;
        border-top: 1px solid #21262d;
        margin: 20px 0;
    }

    /* Input de texto */
    .stChatInput > div > div > textarea {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        color: #e6edf3 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
    }

    .stChatInput > div > div > textarea:focus {
        border-color: #1f6feb !important;
        box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.15) !important;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%) !important;
        border-right: 1px solid #21262d !important;
    }

    [data-testid="stSidebar"] * {
        color: #c9d1d9 !important;
    }

    /* Spinner */
    .stSpinner > div { border-top-color: #3fb950 !important; }

    /* Botão de limpar chat */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a5f, #1a4a7a);
        border: 1px solid #2a5a9f;
        color: #79c0ff !important;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 8px 18px;
        width: 100%;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1a4a7a, #1e6eb0);
        border-color: #3d8bca;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31,111,235,0.3);
    }

    /* Info / warning boxes */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid #30363d !important;
        background: #161b22 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Cabeçalho Principal
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1.5rem 0 0.5rem 0;'>
    <div style='font-size:3rem; margin-bottom:8px;'>🔧</div>
    <h1 style='margin:0; font-size:2rem; font-weight:700;
               background: linear-gradient(90deg, #3fb950, #79c0ff, #d2a8ff);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;
               background-clip:text;'>
        Nexus IA
    </h1>
    <p style='color:#8b949e; font-size:0.9rem; margin-top:6px; letter-spacing:0.05em;'>
        Assistente Técnico Premium · TCell Manutenção de Smartphones
    </p>
</div>
<hr style='border:none; border-top:1px solid #21262d; margin: 1rem 0 1.5rem 0;'>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Carregar API Key (dos Streamlit Secrets ou ambiente)
# ─────────────────────────────────────────────
api_key = st.secrets.get("GOOGLE_API_KEY", None) or os.environ.get("GOOGLE_API_KEY", None)

if not api_key:
    st.error("⚠️ **Chave de API não configurada.** Entre em contato com o administrador do sistema.", icon="🔑")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# ─────────────────────────────────────────────
# Barra Lateral – Informações e Controles
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 Nexus IA")
    st.markdown("**Versão:** 1.0")
    st.markdown("**Motor:** Google Gemini")
    st.markdown("---")
    st.markdown("### 📚 Sobre")
    st.markdown("""
    O **Nexus IA** é o assistente técnico especialista em manutenção de smartphones da **TCell**.

    Ele foi treinado com o *Manual Premium de Assistência Técnica* e pode responder dúvidas sobre:
    - 🛠️ Diagnósticos e reparos
    - 📱 Troca de telas e baterias
    - 🔌 Recuperação de conectores
    - 💰 Precificação de serviços
    - ⚡ Segurança e ferramentas ESD
    """)
    st.markdown("---")

    if st.button("🗑️ Limpar Conversa", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; opacity:0.5; text-align:center;'>TCell © 2026</div>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# Carregar e Cachear o Manual Técnico
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner="📖 Carregando manual técnico TCell...")
def carregar_contexto():
    """Carrega e processa o e-book do manual técnico uma única vez."""
    caminho = os.path.join(os.path.dirname(__file__), "Ebook_Manual_Premium_Celular.md")
    if os.path.exists(caminho):
        loader = TextLoader(caminho, encoding="utf-8")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        partes = splitter.split_documents(docs)
        contexto = "\n\n".join([d.page_content for d in partes])
        return contexto
    return ""

contexto_manual = carregar_contexto()

# ─────────────────────────────────────────────
# Inicializar Modelo Gemini
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.35,
        max_output_tokens=2048,
    )

llm = get_llm()

# ─────────────────────────────────────────────
# Gerenciar Histórico do Chat
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Mensagem de boas-vindas automática do Nexus
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Olá! Sou o **Nexus IA**, seu assistente técnico especialista em manutenção de smartphones da TCell. 👋\n\n"
            "Pode me perguntar sobre:\n"
            "- 🔧 Diagnóstico e reparos técnicos\n"
            "- 📱 Troca de telas LCD, OLED e AMOLED\n"
            "- 🔋 Substituição e diagnóstico de baterias\n"
            "- 🔌 Recuperação de conectores de carga\n"
            "- ⚡ Segurança ESD e organização de bancada\n"
            "- 💰 Precificação e atendimento premium\n\n"
            "Em que posso te ajudar hoje?"
        )
    })

# ─────────────────────────────────────────────
# Renderizar Histórico de Mensagens
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='chat-bubble user-bubble'>
            <div class='bubble-label user-label'>Você</div>
            {msg['content']}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='chat-bubble nexus-bubble'>
            <div class='bubble-label nexus-label'>🔧 Nexus IA</div>
            {msg['content']}
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Campo de Entrada do Usuário
# ─────────────────────────────────────────────
pergunta = st.chat_input("Digite sua dúvida técnica aqui...", key="user_input")

if pergunta:
    # Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": pergunta})
    st.markdown(f"""
    <div class='chat-bubble user-bubble'>
        <div class='bubble-label user-label'>Você</div>
        {pergunta}
    </div>""", unsafe_allow_html=True)

    # Gera a resposta do Nexus
    with st.spinner("🔧 Nexus pensando..."):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             "Você é o Nexus IA, um assistente técnico especialista em manutenção de smartphones da TCell. "
             "Responda de forma clara, profissional e didática em português do Brasil. "
             "Use o contexto do manual técnico abaixo para responder com precisão. "
             "Se não encontrar a resposta no manual, use seu conhecimento geral de forma segura e honesta. "
             "Formate sua resposta com emojis e markdown quando apropriado para torná-la mais legível."
             "\n\nContexto do Manual TCell:\n{context}"),
            ("human", "{question}")
        ])
        chain = prompt_template | llm
        try:
            resposta = chain.invoke({
                "context": contexto_manual,
                "question": pergunta
            })
            conteudo = resposta.content
        except Exception as e:
            conteudo = f"❌ Erro ao processar sua pergunta: {e}"

    # Adiciona e exibe a resposta do Nexus
    st.session_state.messages.append({"role": "assistant", "content": conteudo})
    st.markdown(f"""
    <div class='chat-bubble nexus-bubble'>
        <div class='bubble-label nexus-label'>🔧 Nexus IA</div>
        {conteudo}
    </div>""", unsafe_allow_html=True)
