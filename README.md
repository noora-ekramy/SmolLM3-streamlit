# SmolLM3 Streamlit Chat Interface

A beautiful and interactive chat interface for testing the SmolLM3-3B model with all available API parameters.

![SmolLM3 Chat Interface](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI API](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white)

## 🌟 Features

### 💬 Interactive Chat Interface
- Real-time streaming responses
- Beautiful chat UI with user and assistant avatars
- Chat history preservation during session
- Typing indicators

### 🎛️ Complete Parameter Control
- **Temperature** (0.0 - 2.0): Control creativity vs focus
- **Top P** (0.0 - 1.0): Nucleus sampling for diversity
- **Max Tokens** (1 - 1000): Response length control
- **Seed**: Reproducible outputs
- **Stop Sequences**: Custom stopping criteria
- **Frequency Penalty** (-2.0 - 2.0): Reduce repetition
- **Presence Penalty** (-2.0 - 2.0): Encourage new topics

### 🎯 Quick Presets
- **Creative**: High temperature and top_p for creative writing
- **Focused**: Low temperature for factual, precise responses
- **Balanced**: Moderate settings for general conversation
- **Reset**: Return to default values

### 🔧 Advanced Features
- Environment variable support for API tokens
- Real-time parameter display
- Error handling and user feedback
- Responsive design for different screen sizes

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Token

**Option A: Environment Variable**
```bash
export HF_TOKEN=your_huggingface_token_here
```

**Option B: Create .env file**
```bash
cp env_template.txt .env
# Edit .env and add your token
```

**Option C: Enter in the App**
- Run the app and enter your token in the sidebar

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Start Chatting!
- Open your browser to the provided URL (usually http://localhost:8501)
- Configure parameters in the sidebar
- Start chatting with SmolLM3!

## 📖 Usage Guide

### Getting Your Hugging Face Token
1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Create a new token with `Read` permissions
3. Copy the token and use it in the app

### Parameter Explanations

| Parameter | Range | Description |
|-----------|-------|-------------|
| **Temperature** | 0.0 - 2.0 | Controls randomness. 0 = deterministic, higher = more creative |
| **Top P** | 0.0 - 1.0 | Nucleus sampling. Lower = focus on likely tokens |
| **Max Tokens** | 1 - 1000 | Maximum response length |
| **Seed** | 0 - 1000000 | Fixed seed for reproducible outputs |
| **Stop Sequences** | Text | Comma-separated sequences where generation stops |
| **Frequency Penalty** | -2.0 - 2.0 | Positive values reduce repetition |
| **Presence Penalty** | -2.0 - 2.0 | Positive values encourage new topics |

### Tips for Best Results

**For Creative Writing:**
- Temperature: 0.8 - 1.2
- Top P: 0.9 - 0.95
- Frequency Penalty: 0.1 - 0.3

**For Factual Questions:**
- Temperature: 0.1 - 0.3
- Top P: 0.8 - 0.9
- Frequency Penalty: 0.0

**For Code Generation:**
- Temperature: 0.2 - 0.5
- Top P: 0.9
- Stop Sequences: "```", "\n\n"

## 🛠️ Technical Details

### API Endpoint
- Base URL: `https://av7tzsihe44dbvby.us-east-1.aws.endpoints.huggingface.cloud/v1/`
- Model: `HuggingFaceTB/SmolLM3-3B`
- Compatible with OpenAI API format

### Dependencies
- **Streamlit**: Web interface framework
- **OpenAI**: API client for communication
- **python-dotenv**: Environment variable management

### File Structure
```
SmolLM3-streamlit/
├── app.py              # Main Streamlit application
├── test.py             # Command-line testing script
├── requirements.txt    # Python dependencies
├── env_template.txt    # Environment variable template
└── README.md          # This file
```

## 🐛 Troubleshooting

### Common Issues

**"No API token provided"**
- Make sure you've set the HF_TOKEN environment variable or entered it in the sidebar

**"Error: 401 Unauthorized"**
- Check that your Hugging Face token is valid and has the correct permissions

**"Connection timeout"**
- Check your internet connection
- The Hugging Face endpoint might be temporarily unavailable

**Slow responses**
- The model endpoint might be under heavy load
- Try reducing max_tokens for faster responses

### Getting Help
If you encounter issues:
1. Check the Streamlit console for error messages
2. Verify your API token is correctly set
3. Try the command-line test script (`python test.py`) to isolate issues

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this chat interface!

---

**Happy chatting with SmolLM3! 🤖✨**
