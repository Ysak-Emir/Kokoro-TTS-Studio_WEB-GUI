import gradio as gr
from kokoro import KPipeline
import soundfile as sf
import torch
import webbrowser
import os
from datetime import datetime
import numpy as np
import time

device = 'cuda' if torch.cuda.is_available() else 'cpu'

pipeline = KPipeline(lang_code='a', device=device, repo_id='hexgrad/Kokoro-82M')

SAVE_DIR = "saved voices"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

voice_map = {
    "Bella (Female - American)": "af_bella",
    "Sarah (Female - American)": "af_sarah",
    "Sky (Female - American)": "af_sky",
    "Heart (Female - American)": "af_heart",
    "Nicole (Female - American)": "af_nicole",
    "Nova (Female - American)": "af_nova",
    "Michael (Male - American)": "am_michael",
    "Fenrir (Male - American)": "am_fenrir",
    "Adam (Male - American)": "am_adam",
    "Eric (Male - American)": "am_eric",
    "Liam (Male - American)": "am_liam",
    "Onyx (Male - American)": "am_onyx",
    "Emma (Female - British)": "bf_emma",
    "Isabella (Female - British)": "bf_isabella",
    "Alice (Female - British)": "bf_alice",
    "Lily (Female - British)": "bf_lily",
    "George (Male - British)": "bm_george",
    "Lewis (Male - British)": "bm_lewis",
    "Daniel (Male - British)": "bm_daniel",
    "Kane (Male - British)": "bm_kane",
}

# CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

* {
    font-family: 'Montserrat', sans-serif !important;
}

.footer {
    text-align: center;
    margin-top: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

.footer a {
    color: #FF7043 !important;
    text-decoration: none;
}
"""

def generate_voice(text, voice_name, speed):
    clean_text = text.replace('\n', ' ').strip()
    voice_id = voice_map[voice_name]
    generator = pipeline(clean_text, voice=voice_id, speed=speed)
    
    all_audio = []
    for i, (gs, ps, audio) in enumerate(generator):
        all_audio.append(audio)
    
    if not all_audio:
        return None

    final_audio = np.concatenate(all_audio)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"voice_{voice_id}_{timestamp}.wav"
    filepath = os.path.join(SAVE_DIR, filename)
    
    sf.write(filepath, final_audio, 24000)
    sf.write("preview.wav", final_audio, 24000)
    
    return "preview.wav"

def close_app():
    print("Завершение работы по запросу пользователя...")
    time.sleep(0.5)
    os._exit(0)

with gr.Blocks(title="Kokoro TTS Studio WEB GUI") as demo:
    with gr.Row():
        with gr.Column(scale=4): 
            gr.Markdown("# 🎙️ Kokoro TTS Studio WEB GUI")
        with gr.Column(scale=0, min_width=150): 
            btn_close = gr.Button("❌ Выйти", variant="stop", size="sm")

    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Текст для озвучки", placeholder="Введите текст...", lines=5)
            voice_select = gr.Dropdown(choices=list(voice_map.keys()), value="Bella (Female - American)", label="Голос")
            speed_slider = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, step=0.1, label="Скорость")
            btn_gen = gr.Button("🚀 Сгенерировать и Сохранить", variant="primary")
        
        with gr.Column():
            output_audio = gr.Audio(
                label="Последний результат", 
                type="filepath", 
                elem_classes=["fixed-height-audio"],
                waveform_options=gr.WaveformOptions(
                    sample_rate=24000,
                    show_recording_waveform=True,
                )           
            )
            gr.Markdown(f"✅ Файлы сохраняются в папку: **`{SAVE_DIR}`**")

    gr.HTML("<br><hr>")
    gr.Markdown(
        "<div class='footer'>by GUI <a href='https://github.com/Ysak-Emir' target='_blank'>Ysak-Emir</a></div>"
    )

    btn_gen.click(generate_voice, inputs=[input_text, voice_select, speed_slider], outputs=output_audio)
    
    btn_close.click(
        fn=close_app, 
        inputs=None, 
        outputs=None, 
        js="() => { if (confirm('Вы действительно хотите выйти?')) { window.close(); setTimeout(() => { window.location.href = 'about:blank'; }, 500); } }"
    )

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:7860")
    demo.launch(
        server_name="127.0.0.1", 
        server_port=7860,
        theme=gr.themes.Soft(
            font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
            font_mono=[gr.themes.GoogleFont("Fira Code"), "ui-monospace", "Consolas", "monospace"],
        )
    )