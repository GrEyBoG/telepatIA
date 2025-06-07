from models import DataModel, DiagnosisModel
from api import call_agent_model, extract_from_input, transcribe_audio_url, diagnose_from_data
import gradio as gr
import json

#---------------------------
#     FORMATTERS
#---------------------------
def format_full_report(info, diagnosis):
    return f"""
<div style='padding: 10px; border-radius: 8px;'>
    <h4>🧑‍⚕️ <b>Información del paciente:</b></h4>
    <p><b>Nombre:</b> {info.patient_info.name}</p>
    <p><b>Edad:</b> {info.patient_info.age}</p>
    <p><b>ID:</b> {info.patient_info.id}</p>
    <h4>🩺 <b>Síntomas:</b></h4>
    <p>{', '.join(info.symptoms)}</p>
    <h4>📄 <b>Motivo de consulta:</b></h4>
    <p>{info.reason_for_consultation}</p>
    <h4>🧠 <b>Diagnóstico:</b></h4>
    <p>{diagnosis.diagnosis}</p>
    <h4>💊 <b>Tratamiento:</b></h4>
    <p>{diagnosis.treatment}</p>
    <h4>📝 <b>Recomendaciones:</b></h4>
    <p>{diagnosis.recomendations}</p>
</div>
"""

def format_diagnosis(resp):
    return f"""
🧠 *Diagnóstico:*\n{resp.diagnosis}

💊 *Tratamiento:*\n{resp.treatment}

📝 *Recomendaciones:*\n{resp.recomendations}
"""


#---------------------------
#     MAIN FUNCTION
#---------------------------
def process_message(message, audio_url, use_agent, history):
    history = history or []

    if not message and not audio_url:
        history.append(("Sistema", "Por favor escribe un mensaje o adjunta un link de audio"))
        return history

    user_input = message or audio_url
    history.append(("Usuario", user_input))

    try:
        if use_agent:
            response = call_agent_model(message, audio_url)
            if isinstance(response.response, dict):
                diag = DiagnosisModel(**response.response)
                formatted = format_diagnosis(diag)
                history.append(("Agente IA", formatted))
            else:
                history.append(("Agente IA", response.response))
            return history

        if audio_url:
            transcript = transcribe_audio_url(audio_url).response
            input_text = transcript
        else:
            input_text = message

        extract_result = extract_from_input(input_text)
        data_model = DataModel(**extract_result.response)

        diagnosis = diagnose_from_data(data_model).response
        diagnosis_model = DiagnosisModel(**diagnosis)

        formatted = format_full_report(data_model, diagnosis_model)
        history.append(("Sistema Médico", formatted))

        return history

    except Exception as e:
        history.append(("Error", f"Ocurrió un error: {str(e)}"))
        return history

#---------------------------
#     GRADIO INTERFACE
#---------------------------

with gr.Blocks() as demo:
    gr.Markdown("""# 🩺 Sistema de Diagnóstico Médico por IA""")

    with gr.Row():
        use_agent = gr.Checkbox(label="Usar Agente IA", value=False)

    with gr.Row():
        message_input = gr.Textbox(lines=2, label="Mensaje")
        audio_input = gr.Textbox(label="Link de audio (opcional)")

    chatbox = gr.Chatbot(label="Historial de Consulta", type="messages")
    send_btn = gr.Button("Enviar")
    state = gr.State([])

    def render_chat(history):
        return [{"role": "user" if role == "Usuario" else "assistant", "content": content} for role, content in history]

    send_btn.click(
        fn=process_message,
        inputs=[message_input, audio_input, use_agent, state],
        outputs=[state],
        show_progress=True
    ).then(
        fn=render_chat,
        inputs=[state],
        outputs=[chatbox],
        show_progress=True
    )

#---------------------------
#     LAUNCH APP
#---------------------------

if __name__ == "__main__":
    demo.launch(inbrowser=True)  # Esto fuerza que se abra el navegador
