from google.colab import userdata
import os

minha_api_key = userdata.get('GEMINI_API_KEY')

with open('interface.py', 'w') as f:
    f.write(f"""
import streamlit as st
from google import genai
from gtts import gTTS
import os

st.set_page_config(page_title="English Voice Buddy", page_icon="🎙️", layout="centered")

# Inicializa o cliente do Gemini
api_key = "{minha_api_key}"
client = genai.Client(api_key=api_key)

# PROMPTS ESTÁVEIS
PROMPT_CONVERSATION = "You are an advanced English conversation tutor. Speak ONLY in English. Format your response exactly like this: [TEXTO] Your natural response here (2-3 sentences). [AUDIO] The exact same text here for the audio player."

PROMPT_REPEAT = "Você é um tutor de inglês focado em ajudar iniciantes. Sua missão é dar o feedback em português do Brasil e passar a próxima frase para o aluno repetir. Separe estritamente o texto e o áudio usando este formato exato: [TEXTO] Parabéns, você foi ótimo! A sua próxima frase de treino é: 'Good afternoon'. [AUDIO] Good afternoon"

def resetar_chat():
    if "messages" in st.session_state:
        del st.session_state.messages

st.title("🎙️ English Voice Buddy")
st.subheader("Seu tutor de conversação inteligente")
st.markdown("---")

modo = st.selectbox(
    "Escolha o seu modo de aprendizado:",
    ["Conversation Mode (Advanced)", "Repeat & Learn Mode (Beginner)"],
    on_change=resetar_chat
)

# Inicializa o histórico se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []
    if "Advanced" in modo:
        st.session_state.messages.append({{"role": "assistant", "text": "Hello! I am your conversation tutor. What would you like to talk about today?", "audio_text": "Hello! I am your conversation tutor. What would you like to talk about today?", "lang": "en"}})
    else:
        st.session_state.messages.append({{"role": "assistant", "text": "Olá! Vamos treinar sua pronúncia. Escute a frase abaixo e repita no microfone:", "audio_text": "Good morning, how are you?", "lang": "en"}})

# Exibe o histórico de conversa na tela
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write("🎙️ *Você enviou uma resposta em áudio*")
    else:
        st.chat_message("assistant").write(msg["text"])

st.markdown("---")
st.write("### 🎙️ Sua vez de falar:")

audio_value = st.audio_input("Grave sua voz aqui:")

if audio_value:
    st.info("Processando sua voz com o Gemini...")
    
    filename = "user_input.wav"
    with open(filename, "wb") as f:
        f.write(audio_value.read())
        
    try:
        audio_upload = client.files.upload(file=filename)
        sys_instruction = PROMPT_CONVERSATION if "Advanced" in modo else PROMPT_REPEAT
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[audio_upload, "Process my spoken audio response according to your system rules."],
            config={{"system_instruction": sys_instruction}}
        )
        
        raw_text = response.text
        
        texto_tela = "Ok! Let's continue."
        texto_audio = "Let's continue."
        
        if "[TEXTO]" in raw_text and "[AUDIO]" in raw_text:
            partes = raw_text.split("[AUDIO]")
            texto_audio = partes[1].strip()
            texto_tela = partes[0].replace("[TEXTO]", "").strip()
        else:
            texto_tela = raw_text.replace("[TEXTO]", "").replace("[AUDIO]", "").strip()
            texto_audio = texto_tela
            
        texto_audio = texto_audio.replace("'", "").replace('"', '')
            
        st.session_state.messages.append({{"role": "user"}})
        st.session_state.messages.append({{
            "role": "assistant", 
            "text": texto_tela, 
            "audio_text": texto_audio,
            "lang": "en"
        }})
        
        if os.path.exists(filename):
            os.remove(filename)
            
        st.rerun()
        
    except Exception as e:
        # Se der erro de cota (429), exibe uma mensagem amigável para o usuário
        if "429" in str(e):
            st.error("⚠️ Muitas requisições seguidas! Por favor, aguarde cerca de 30 a 40 segundos antes de mandar o próximo áudio para a API liberar.")
        else:
            st.error(f"Erro no processamento: {{e}}")

# Player de áudio no rodapé
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    last_msg = st.session_state.messages[-1]
    
    tts = gTTS(text=last_msg["audio_text"], lang=last_msg["lang"])
    prof_audio = "professor_response.mp3"
    tts.save(prof_audio)
    
    st.write("🎧 **Ouça o professor (Pronúncia nativa em Inglês):**")
    # 💡 Removemos o autoplay daqui! O player só toca se o usuário clicar.
    st.audio(prof_audio, autoplay=False)
""")