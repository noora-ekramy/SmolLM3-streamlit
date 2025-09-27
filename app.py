import streamlit as st
import os
from openai import OpenAI
import time
import re
from typing import Generator, Dict, Any
from dotenv import load_dotenv

# Import cost calculator
from cost_calculator import cost_calculator_page

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="trex1.5 AI Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #161616; 
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .stApp {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
    .tagline {
        font-size: 20px;
        font-weight: bold;
        color: #a4ffff;
        text-align: center;
        margin-top: -10px;
    }
    .subtagline {
        font-size: 19px;
        color: #fcfcfc;
        text-align: center;
        padding:20px;
        margin-bottom: 20px;
    }
     .header {
        font-size: 39px;
        font-weight: bold;
        color: #65daff;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    .stChat > div {
        padding-top: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .chat-message.user {
        flex-direction: row-reverse;
        background-color: rgba(101, 218, 255, 0.1);
    }
    .chat-message.assistant {
        background-color: rgba(164, 255, 255, 0.05);
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 0 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        background-color: rgba(101, 218, 255, 0.2);
        color: #65daff;
    }
    .chat-message.user .avatar {
        background-color: rgba(164, 255, 255, 0.2);
        color: #a4ffff;
    }
    .thinking-text {
        color: #cccccc;
        font-style: italic;
        font-weight: normal;
        margin-bottom: 10px;
        padding: 8px;
        background-color: rgba(255, 255, 255, 0.02);
        border-left: 3px solid #666;
        border-radius: 4px;
    }
    .response-text {
        color: white;
        font-weight: normal;
    }
    .sidebar-section {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .stSlider > div > div > div > div {
        color: #65daff;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        # Try to get from environment variable first
        env_token = os.getenv("HF_TOKEN")
        st.session_state.api_key = env_token if env_token else ""

def create_openai_client(api_key: str) -> OpenAI:
    """Create OpenAI client with custom base URL"""
    return OpenAI(
        base_url="https://av7tzsihe44dbvby.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key=api_key
    )

def get_response(client: OpenAI, messages: list, params: Dict[str, Any], stream: bool = True) -> Generator[str, None, None] | str:
    """Get response from the API, either streaming or non-streaming"""
    try:
        chat_completion = client.chat.completions.create(
            model="HuggingFaceTB/SmolLM3-3B",
            messages=messages,
            stream=stream,
            **params
        )
        
        if stream:
            for chunk in chat_completion:
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            return chat_completion.choices[0].message.content
                
    except Exception as e:
        if stream:
            yield f"Error: {str(e)}"
        else:
            return f"Error: {str(e)}"

def parse_thinking_and_response(text: str) -> tuple[str, str]:
    """Parse thinking and response from text"""
    # Look for thinking patterns like <thinking>...</thinking> or similar
    thinking_patterns = [
        r'<thinking>(.*?)</thinking>',
        r'<think>(.*?)</think>',
        r'\*thinking\*(.*?)\*/thinking\*',
        r'\[thinking\](.*?)\[/thinking\]'
    ]
    
    thinking = ""
    response = text
    
    for pattern in thinking_patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            thinking = matches[0].strip()
            response = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE).strip()
            break
    
    return thinking, response

def display_chat_message(role: str, content: str, show_thinking: bool = True):
    """Display a chat message with custom styling and thinking separation"""
    avatar = "U" if role == "user" else "A"
    css_class = "user" if role == "user" else "assistant"
    
    if role == "assistant" and show_thinking:
        thinking, response = parse_thinking_and_response(content)
        
        content_html = ""
        if thinking:
            content_html += f'<div class="thinking-text">Thinking: {thinking}</div>'
        content_html += f'<div class="response-text">{response}</div>'
    else:
        content_html = f'<div class="response-text">{content}</div>'
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div class="avatar">{avatar}</div>
        <div style="flex: 1;">
            <div style="font-weight: bold; margin-bottom: 0.5rem; color: #65daff;">
                {'You' if role == 'user' else 'trex1.5'}
            </div>
            {content_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def chat_page():
    """Chat interface page"""
    # Title and description with custom styling
    st.markdown('<div class="header">trex1.5?????? Chat Interface</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Advanced AI Chat with Customizable Parameters</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtagline">Chat with trex1.5 model with full parameter control</div>', unsafe_allow_html=True)
    
    # Sidebar for API configuration and parameters
    with st.sidebar:
        st.header("Configuration")
        
        # API Key section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("API Authentication")
        
        # Check if token is available from environment
        env_token = os.getenv("HF_TOKEN")
        if env_token and not st.session_state.api_key:
            st.session_state.api_key = env_token
        
        if st.session_state.api_key:
            if env_token:
                st.success("Using HF_TOKEN from .env file")
                # Show option to override with manual input
                manual_override = st.checkbox("Override with manual token", value=False)
                if manual_override:
                    api_key = st.text_input(
                        "Hugging Face Token",
                        type="password",
                        value="",
                        help="Enter your Hugging Face API token to override .env file"
                    )
                    if api_key:
                        st.session_state.api_key = api_key
                else:
                    api_key = st.session_state.api_key
            else:
                st.success("API token configured")
                api_key = st.text_input(
                    "Hugging Face Token",
                    type="password",
                    value=st.session_state.api_key,
                    help="Enter your Hugging Face API token"
                )
                st.session_state.api_key = api_key
        else:
            st.warning("No API token found in .env file")
            api_key = st.text_input(
                "Hugging Face Token",
                type="password",
                value="",
                help="Enter your Hugging Face API token"
            )
            st.session_state.api_key = api_key
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Response Options section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Response Options")
        
        # Stream parameter
        enable_streaming = st.checkbox("Enable Streaming", value=True, help="Stream responses in real-time or get complete response at once")
        
        # Show thinking parameter
        show_thinking = st.checkbox("Show Thinking Process", value=True, help="Display model's thinking process separately from the response")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model parameters section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("Model Parameters")
        
        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness. Higher values make output more creative, lower values more focused."
        )
        
        # Top P
        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.05,
            help="Controls diversity via nucleus sampling. Lower values focus on most likely tokens."
        )
        
        # Max Tokens
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=1,
            max_value=1000,
            value=150,
            step=10,
            help="Maximum number of tokens to generate in the response."
        )
        
        # Seed
        use_seed = st.checkbox("Use Fixed Seed", value=False)
        seed = None
        if use_seed:
            seed = st.number_input(
                "Seed",
                min_value=0,
                max_value=1000000,
                value=42,
                step=1,
                help="Seed for reproducible outputs."
            )
        
        # Stop sequences
        stop_sequences = st.text_area(
            "Stop Sequences",
            value="",
            placeholder="Enter stop sequences separated by commas\ne.g., \\n\\n, ., !",
            help="Comma-separated list of sequences where the model should stop generating."
        )
        
        # Parse stop sequences
        stop = None
        if stop_sequences.strip():
            stop = [seq.strip() for seq in stop_sequences.split(",") if seq.strip()]
        
        # Frequency Penalty
        frequency_penalty = st.slider(
            "Frequency Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            help="Penalizes repeated tokens. Positive values discourage repetition."
        )
        
        # Presence Penalty
        presence_penalty = st.slider(
            "Presence Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            help="Penalizes tokens that have appeared. Positive values encourage new topics."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    
    # Display chat messages
    if st.session_state.messages:
        st.subheader("Chat History")
        for message in st.session_state.messages:
            display_chat_message(message["role"], message["content"], show_thinking)
    else:
        st.info("Start a conversation with trex1.5! Enter your message below.")
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not st.session_state.api_key:
            st.error("Please provide a Hugging Face API token. Check your .env file or enter it manually in the sidebar.")
            return
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt, show_thinking)
        
        # Prepare API parameters
        api_params = {
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        
        if seed is not None:
            api_params["seed"] = seed
        
        if stop:
            api_params["stop"] = stop
        
        # Create client and get response
        client = create_openai_client(st.session_state.api_key)
        
        # Display assistant response
        with st.container():
            message_placeholder = st.empty()
            
            try:
                if enable_streaming:
                    # Streaming response
                    full_response = ""
                    
                    # Show typing indicator
                    with message_placeholder:
                        st.markdown('<div style="color: #cccccc; font-style: italic;">trex1.5 is typing...</div>', unsafe_allow_html=True)
                    
                    # Stream the response
                    for chunk in get_response(client, st.session_state.messages, api_params, stream=True):
                        full_response += chunk
                        
                        # Update the display with accumulated response
                        with message_placeholder:
                            display_chat_message("assistant", full_response + "▌", show_thinking)
                        
                        # Small delay for better UX
                        time.sleep(0.01)
                    
                    # Final display without cursor
                    with message_placeholder:
                        display_chat_message("assistant", full_response, show_thinking)
                else:
                    # Non-streaming response
                    with message_placeholder:
                        st.markdown('<div style="color: #cccccc; font-style: italic;">trex1.5 is generating response...</div>', unsafe_allow_html=True)
                    
                    full_response = get_response(client, st.session_state.messages, api_params, stream=False)
                    
                    with message_placeholder:
                        display_chat_message("assistant", full_response, show_thinking)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                with message_placeholder:
                    display_chat_message("assistant", error_msg, show_thinking)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Display current parameters in an expander
    with st.expander("Current Parameters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Basic Parameters:**")
            st.write(f"• Temperature: {temperature}")
            st.write(f"• Top P: {top_p}")
            st.write(f"• Max Tokens: {max_tokens}")
            st.write(f"• Streaming: {'Enabled' if enable_streaming else 'Disabled'}")
        
        with col2:
            st.write("**Penalty Parameters:**")
            st.write(f"• Frequency Penalty: {frequency_penalty}")
            st.write(f"• Presence Penalty: {presence_penalty}")
            st.write(f"• Seed: {seed if seed is not None else 'Random'}")
            st.write(f"• Show Thinking: {'Yes' if show_thinking else 'No'}")
        
        with col3:
            st.write("**Stop Sequences:**")
            if stop:
                for seq in stop:
                    st.write(f"• '{seq}'")
            else:
                st.write("• None")

def main():
    """Main application function with page navigation"""
    initialize_session_state()
    
    # Navigation in sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose Page",
        ["Chat Interface", "Cost Calculator"],
        index=0
    )
    
    # Route to appropriate page
    if page == "Chat Interface":
        chat_page()
    elif page == "Cost Calculator":
        cost_calculator_page()

if __name__ == "__main__":
    main()
