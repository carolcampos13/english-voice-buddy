![Capa do Projeto](capa.png)

# 🎙️ English Voice Buddy - Tutor de Inglês com IA

Um aplicativo web interativo que funciona como um tutor de inglês personalizado utilizando Inteligência Artificial multimodal. O projeto oferece dois modos dinâmicos de aprendizado baseados totalmente em interações por voz.

---

## 🚀 Funcionalidades

- **Conversation Mode (Advanced):** O tutor interage inteiramente em inglês, mantendo um diálogo fluido e natural de 2 a 3 frases e encerrando com perguntas estimulantes. Ao final de cada bloco, ele analisa a fala do usuário e fornece dicas gramaticais (`💡 Quick Tip`).
- **Repeat & Learn Mode (Beginner):** Focado em pronúncia para iniciantes. O tutor dá feedbacks e instruções em português, mas dita frases curtas em inglês para o usuário praticar a repetição.
- **Processamento Multimodal Nativo:** Utiliza o modelo Gemini para "ouvir" e analisar diretamente os arquivos de áudio enviados pelo usuário.
- **Canais Separados de Áudio/Texto:** Arquitetura lógica desenvolvida para isolar os idiomas de leitura e escrita, garantindo que o sintetizador de voz (gTTS) reproduza as frases em inglês com pronúncia nativa e sem sotaques indesejados.

---

## 🛠️ Tecnologias Utilizadas

- **Python** (Lógica principal do ecossistema)
- **Streamlit** (Interface Web e captura nativa de microfone)
- **Google GenAI SDK** (Integração multimodal com o modelo `gemini-2.5-flash`)
- **gTTS (Google Text-to-Speech)** (Sintetização de voz para as respostas do tutor)

---

## 🔑 Configuração de Segurança

O projeto foi desenvolvido seguindo boas práticas de segurança da informação. Nenhuma chave de API ou credencial está exposta no código. O sistema consome a chave do Gemini através de variáveis de ambiente seguras (`Secrets`).