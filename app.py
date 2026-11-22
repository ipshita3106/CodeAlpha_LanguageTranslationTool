import streamlit as st
import streamlit.components.v1 as components
import json
import html

from translator import translate_text

st.set_page_config(
    page_title="LinguaAI - Smart Translator",
    page_icon="🌍",
    layout="centered"
)

# Language options
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru"
}

# Initialize session state
if "translation_result" not in st.session_state:
    st.session_state.translation_result = None

if "result_language" not in st.session_state:
    st.session_state.result_language = "en"

if "source" not in st.session_state:
    st.session_state.source = "English"

if "target" not in st.session_state:
    st.session_state.target = "Hindi"


# Swap language function
def swap_languages():
    source = st.session_state.source
    target = st.session_state.target

    st.session_state.source = target
    st.session_state.target = source


# Page styling
st.markdown("""
<style>

.stApp {
    background-color: #F3E8D5;
}

.main .block-container {
    max-width: 850px;
    padding-top: 3rem;
}

/* Headings and labels */
h1, h2, h3, p, label {
    color: #493727 !important;
}

/* Text input */
.stTextArea textarea {
    background-color: #FBF7EF !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #000000 !important;
    border: 1px solid #D9C7AC !important;
    border-radius: 12px !important;
}

.stTextArea textarea::placeholder {
    color: #9A8B79 !important;
    -webkit-text-fill-color: #9A8B79 !important;
    opacity: 1 !important;
}

/* Language dropdown */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FBF7EF;
    border-radius: 10px;
    border-color: #D9C7AC;
    color: #000000;
}

/* Buttons */
.stButton button {
    background-color: #72543B;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.5rem;
}

.stButton button:hover {
    background-color: #493727;
    color: white;
    border: none;
}

/* Translation result box */
.result-box {
    background-color: #FBF7EF;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #D9C7AC;
    min-height: 90px;
    overflow-wrap: anywhere;
    box-sizing: border-box;
}

</style>
""", unsafe_allow_html=True)


# Header
st.title("🌍 LinguaAI")
st.caption("Your words, in every language.")

st.divider()


# Text input
st.subheader("Enter your text here")

input_text = st.text_area(
    "Text to translate",
    placeholder="Type or paste the text you want to translate...",
    height=150,
    label_visibility="collapsed",
    key="user_input"
)

col1, col2 = st.columns([4, 1])

with col1:
    st.caption(f"Characters: {len(input_text)}")

with col2:
    if st.button("Clear text"):
        st.session_state.user_input = ""
        st.session_state.translation_result = None
        st.rerun()

# Language selection
st.write("")
st.subheader("Language Tools")

col1, col2, col3 = st.columns([5, 1, 5])

with col1:
    st.selectbox(
        "From",
        list(languages.keys()),
        key="source"
    )

with col2:
    st.write("")
    st.write("")
    st.button(
        "⇄",
        use_container_width=True,
        on_click=swap_languages
    )

with col3:
    st.selectbox(
        "To",
        list(languages.keys()),
        key="target"
    )


# Translate button
st.write("")

translate_button = st.button(
    "Translate →",
    use_container_width=True
)


# Translation process
if translate_button:

    if not input_text.strip():
        st.session_state.translation_result = None
        st.warning("Please enter some text.")

    elif st.session_state.source == st.session_state.target:
        st.session_state.translation_result = None
        st.warning("Please select two different languages.")

    else:
        try:
            with st.spinner("Translating your text..."):

                result = translate_text(
                    input_text,
                    languages[st.session_state.source],
                    languages[st.session_state.target]
                )

                st.session_state.translation_result = result
                st.session_state.result_language = languages[
                    st.session_state.target
                ]

        except Exception as error:
            st.session_state.translation_result = None
            st.error(str(error))


# Translation result
st.divider()

st.subheader("Translated Result")

result = st.session_state.translation_result

if result:

    # Display complete result inside one HTML container
    safe_result = html.escape(result).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="result-box">
            <div style="
                color: #000000;
                font-size: 18px;
                line-height: 1.6;
                overflow-wrap: anywhere;
            ">
                {safe_result}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

 # Copy and Listen buttons
col1, col2 = st.columns(2)

with col1:
    st.code(result, language=None)

with col2:
    components.html(
        f"""
        <button onclick="listenText()"
        style="background:#72543B;color:white;border:none;
        padding:12px;border-radius:10px;width:100%;
        cursor:pointer;font-size:15px;">
        🔊 Listen
        </button>

        <script>
        function listenText() {{
            const text = {json.dumps(result)};
            const speech = new SpeechSynthesisUtterance(text);
            speech.lang = {json.dumps(st.session_state.result_language)};
            speech.rate = 0.9;

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(speech);
        }}
        </script>
        """,
        height=55
    )

# Footer
st.divider()

st.caption("LinguaAI © 2026 | Breaking Language Barriers")