import streamlit as st
from textblob import TextBlob
import random
import time

st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

if "history" not in st.session_state:
    st.session_state["history"] = []

st.markdown("""
<style>
body {
  margin: 0;
  overflow-x: hidden;
  animation: bgTransition 2s ease-in-out;
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}
@keyframes bgTransition {
  0% {opacity: 0.6;}
  100% {opacity: 1;}
}
@keyframes gradientMove {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}
.glitter-text {
  font-size: clamp(28px, 6vw, 65px);
  text-align: center;
  font-weight: bold;
  letter-spacing: 2px;
  background: linear-gradient(-45deg, #ff0080, #ff8c00, #40e0d0, #9b00ff);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientMove 5s ease infinite;
  margin-bottom: 20px;
  text-shadow: 0 0 20px rgba(255,255,255,0.3);
}
.card {
  background: rgba(255,255,255,0.85);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
  text-align: center;
  width: 90%;
  max-width: 500px;
  margin: 15px auto;
  backdrop-filter: blur(10px);
}
.rain {
  position: fixed;
  top: -10%;
  font-size: clamp(30px, 8vw, 60px);
  animation: fall linear infinite;
  opacity: 0.9;
  z-index: 0;
}
@keyframes fall {
  0% {transform: translateY(-10%);}
  100% {transform: translateY(110vh);}
}
.history-box {
  max-height: 300px;
  overflow-y: auto;
  padding: 5px;
  scroll-behavior: smooth;
}
@media (max-width: 600px) {
  .card {width: 95%; font-size: 16px;}
  .glitter-text {font-size: 36px;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='glitter-text'>🌈 Sentiment Analyzer Web App 🌈</div>", unsafe_allow_html=True)

user_input = st.text_input("Enter a sentence to analyze sentiment:")

if user_input:
    blob = TextBlob(user_input)
    score = blob.sentiment.polarity

    if score > 0:
        sentiment = "Positive 😊"
        color = "linear-gradient(135deg,#a8ff78,#78ffd6)"
        emoji = "😊"
    elif score < 0:
        sentiment = "Negative 😢"
        color = "linear-gradient(135deg,#ff9a9e,#fad0c4)"
        emoji = "😢"
    else:
        sentiment = "Neutral 😐"
        color = "linear-gradient(135deg,#f6d365,#fda085)"
        emoji = "😐"

    st.session_state["history"].append({"text": user_input, "sentiment": sentiment})

    st.markdown(f"""
        <script>
        document.body.style.background = "{color}";
        </script>
        <div class='card'>
            <h2 style='font-size:clamp(24px,5vw,40px);'>{sentiment}</h2>
            <div style='font-size:clamp(60px,12vw,100px);margin-top:10px;'>{emoji}</div>
        </div>
    """, unsafe_allow_html=True)

    emoji_html = ""
    for _ in range(40):
        left = random.randint(0, 100)
        duration = random.uniform(3, 8)
        emoji_html += f"<div class='rain' style='left:{left}%; animation-duration:{duration}s;'>{emoji}</div>"
    st.markdown(emoji_html, unsafe_allow_html=True)

if st.session_state["history"]:
    st.markdown("<h3 style='text-align:center;margin-top:30px;'>📝 Sentiment History</h3>", unsafe_allow_html=True)
    st.markdown("<div class='history-box'>", unsafe_allow_html=True)
    for entry in reversed(st.session_state["history"][-8:]):
        st.markdown(f"<div class='card'><b>{entry['text']}</b><br>{entry['sentiment']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    scores = [1 if "Positive" in x["sentiment"] else -1 if "Negative" in x["sentiment"] else 0 for x in st.session_state["history"]]
    avg = sum(scores) / len(scores)
    if avg > 0:
        overall = "🌟 Overall Mood: Positive 😊"
        gradient = "linear-gradient(135deg,#c3ff99,#00ff99)"
    elif avg < 0:
        overall = "💔 Overall Mood: Negative 😢"
        gradient = "linear-gradient(135deg,#ff758c,#ff7eb3)"
    else:
        overall = "🌤 Overall Mood: Neutral 😐"
        gradient = "linear-gradient(135deg,#fffbd5,#b20a2c)"
    st.markdown(f"<div class='card' style='margin-top:20px;background:{gradient};color:black;'><b>{overall}</b></div>", unsafe_allow_html=True)