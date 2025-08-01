import gradio as gr
from src.agents.tutor_agent import TutorAgent

CSS = """
.gradio-container { max-width: 900px !important; margin: 20px auto !important; }
.gr-button { background-color: #4285f4 !important; color: white !important; border-radius: 8px !important; font-weight: bold; }
.chat-bubble { background-color: #f0f8ff !important; border-radius: 15px !important; padding: 10px !important; }
"""

# Initialize AI Tutor
try:
    tutor_agent = TutorAgent()
    agent_ready = tutor_agent.retriever is not None
except Exception as e:
    print(f"Setup error: {e}")
    tutor_agent = None
    agent_ready = False

def generate_roadmap_interface(grade, board, subject):
    """Generate roadmap when user clicks the button."""
    if not agent_ready:
        return "⚠️ Setup needed - check README for instructions"
    if not all([grade, board, subject]):
        return "Please select grade, board, and subject first"
    
    yield "🧠 Creating your learning plan..."
    roadmap = tutor_agent.generate_roadmap(grade, board, subject)
    yield roadmap

def chat_with_tutor(message, history, grade, board, subject):
    """Handle chat messages from kids."""
    if not agent_ready:
        bot_response = "🤖 Hi! I need to be set up first. Ask a grown-up to help!"
    else:
        bot_response = tutor_agent.chat_with_kid(message, grade, board, subject)
    
    history.append([message, bot_response])
    return "", history

with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 AI Tutor for Kids")
    gr.Markdown("🌟 Your friendly learning helper! 🌟")
    
    if not agent_ready:
        gr.Markdown("⚠️ **Setup required** - check README.md")
    
    # Common settings for both tabs
    with gr.Row():
        grade_dd = gr.Dropdown(label="📚 What grade are you in?", 
                              choices=["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"])
        board_dd = gr.Dropdown(label="🏫 What school board?", 
                              choices=["CBSE", "ICSE", "Karnataka"])
        subject_dd = gr.Dropdown(label="📖 What subject?", 
                                choices=["Science", "Math", "Social", "English"])
    
    with gr.Tabs():
        # Tab 1: Learning Plan
        with gr.TabItem("📅 My Learning Plan"):
            gr.Markdown("### Get your weekly study plan!")
            generate_btn = gr.Button("🚀 Create My Learning Plan!", size="lg")
            roadmap_output = gr.Markdown("Your learning plan will appear here...")
            
        # Tab 2: Chat with Tutor
        with gr.TabItem("💬 Ask Questions"):
            gr.Markdown("### Hi! I'm your AI tutor friend! Ask me anything! 😊")
            chatbot = gr.Chatbot(
                height=400,
                type="messages",
                placeholder="👋 Hi there! I'm ready to help you learn!",
                elem_classes=["chat-bubble"]
            )
            msg = gr.Textbox(
                placeholder="Type your question here... (like 'What is light?' or 'How do plants grow?')",
                label="💭 Your Question",
                lines=2
            )
            send_btn = gr.Button("💌 Send", size="sm")
            clear_btn = gr.Button("🧹 Clear Chat", size="sm")

    # Event handlers
    generate_btn.click(
        fn=generate_roadmap_interface,
        inputs=[grade_dd, board_dd, subject_dd],
        outputs=[roadmap_output]
    )
    
    # Chat functionality
    send_btn.click(
        fn=chat_with_tutor,
        inputs=[msg, chatbot, grade_dd, board_dd, subject_dd],
        outputs=[msg, chatbot]
    )
    
    msg.submit(  # Also send when Enter is pressed
        fn=chat_with_tutor,
        inputs=[msg, chatbot, grade_dd, board_dd, subject_dd],
        outputs=[msg, chatbot]
    )
    
    clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])

if __name__ == "__main__":
    print("🚀 Starting AI Tutor...")
    demo.launch(debug=True)
