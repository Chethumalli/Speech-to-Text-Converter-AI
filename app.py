import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

recognizer = sr.Recognizer()

st.set_page_config(
    page_title="AI Speech to Text",
    page_icon="🎙️",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0f172a,#1e293b);
color:white;
}

.title{
text-align:center;
font-size:42px;
font-weight:700;
color:#38bdf8;
margin-bottom:30px;
}

.card{
background:#1e293b;
padding:25px;
border-radius:12px;
box-shadow:0px 4px 15px rgba(0,0,0,0.4);
}

.result{
background:#0f172a;
padding:20px;
border-radius:10px;
border-left:6px solid #38bdf8;
font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="title">🎙️ AI Speech to Text Converter</div>', unsafe_allow_html=True)

# ---------- Convert any file to WAV ----------
def convert_to_wav(uploaded_file):

    suffix = uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix="."+suffix) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    audio = AudioSegment.from_file(temp_path)

    wav_path = temp_path + ".wav"
    audio.export(wav_path, format="wav")

    return wav_path


# ---------- Layout ----------
left, right = st.columns([2,2])

transcription_text = ""

# ---------- Upload Section ----------
with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📂 Drag & Drop Audio / Video")

    uploaded_file = st.file_uploader(
        "Upload any file containing speech",
        type=["mp3","wav","m4a","flac","ogg","mp4","mov","mkv"]
    )

    if uploaded_file:

        st.audio(uploaded_file)

        with st.spinner("Processing speech..."):

            wav_file = convert_to_wav(uploaded_file)

            with sr.AudioFile(wav_file) as source:
                audio_data = recognizer.record(source)

            try:
                transcription_text = recognizer.recognize_google(audio_data)

            except:
                st.error("❌ Could not understand speech")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- Output Section ----------
with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📄 Extracted Text")

    if transcription_text:

        st.markdown(
            f'<div class="result">{transcription_text}</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            "⬇ Download TXT",
            transcription_text,
            file_name="speech.txt",
            mime="text/plain"
        )

    else:

        st.info("Upload an audio/video file to see the transcription")

    st.markdown('</div>', unsafe_allow_html=True)