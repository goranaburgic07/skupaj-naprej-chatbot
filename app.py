import streamlit as st
import os
from groq import Groq

# Učitaj .env samo lokalno
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Barvno prilagođenje
st.markdown("""
<style>
    .stButton>button {
        background-color: #7b2cbf;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #9d4edd;
    }
    h1 {
        color: #7b2cbf;
    }
</style>
""", unsafe_allow_html=True)

# Inicializacija
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY ni najden!")
    st.stop()

client = Groq(api_key=api_key)
st.set_page_config(page_title="Skupaj Naprej Klepetalnik", page_icon="💬")

# Specializacija chatbota
KLUB_TEMA = """
Si klepetalnik za klub "Skupaj Naprej". Klub si prizadeva ustvariti odprto, vključujoče in spodbudno okolje, 
kjer se lahko člani povezujejo, učijo drug od drugega in razvijajo svoje interese ter veščine.

Vrednote kluba:
- Spoštovanje
- Medsebojna podpora
- Enakopravnost
- Odprtost do novih idej
- Timsko delo

Odgovarjaš SAMO na vprašanja povezana s klubom. Če te uporabnik vpraša nekaj kar NI povezano s klubom, 
vljudno odgovori: "Oprostite, sem klepetalnik kluba 'Skupaj Naprej' in lahko odgovarjam le na vprašanja 
povezana z našim klubom. Imate morda vprašanje o klubu?"

VSI odgovori morajo biti v SLOVENŠČINI.
"""

# Inicializacija zgodovine
if "messages" not in st.session_state:
    st.session_state.messages = []

# Naslov
st.title("💬 Klepetalnik Kluba Skupaj Naprej")
st.markdown("*Vaš prijazni pomočnik za vse informacije o klubu*")

# Prikaz zgodovine
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Vnosno polje
if prompt := st.chat_input("Postavite mi vprašanje o klubu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    api_messages = [{"role": "system", "content": KLUB_TEMA}]
    api_messages.extend(st.session_state.messages)
    
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                temperature=0.7,
                max_tokens=1024,
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Napaka: {str(e)}")

# Gumb za reset
if st.button(" Začni nov pogovor"):
    st.session_state.messages = []
    st.rerun()
