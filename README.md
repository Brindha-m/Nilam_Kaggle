<img width="200" height="200" alt="3147fb2d-77b0-4750-8951-ec3a92b44786" src="https://github.com/user-attachments/assets/fcc4a050-49c8-4cba-8ea7-6e76e5cfbb4c" />

<br>

**Nilam (Native Intelligence for Land and Agriculture Management) is an integrated AI-powered agricultural  multilingual chat assistance, leaf disease detection, and personalized crop recommendation system.**

## Modules Architecture

<img width="1242" height="961" alt="NILAM ARCH" src="https://github.com/user-attachments/assets/52861f5c-95d3-41ff-b3b1-8e8b7279fbe4" />


### 🌱 **Nilam Chat**
- **AI-Powered Assistant**: Powered by Google's Generative AI (Gemini).
- **Specialized in farming queries, crop advice and available in multiple Indian languages adding on with market trends and price analysis**

### 🍃 **Leafine**
- **Leaf Disease Detection**: Custom trained on our leafine dataset with improved YOLOv8 architecture Resnext-50 with XAI.
- **Recognize & Perceive the leaf illness and figure out how to treat them!**

### 🧠 **NilamSense**
- **Smart Crop Recommendation**: AI-driven crop selection system custom trained data collected from OWM (Open weather map), Data.gov.in, copernicus trained with bidirectional stacked LSTM.
- **Recommend suitable crops for a specific location**: EDA combined data is @ data/nilamdata.csv

<img width="1351" height="808" alt="Screenshot 2025-08-19 040743" src="https://github.com/user-attachments/assets/40e0a610-a778-4995-b66f-55fac4ec0c5c" />
<img width="1351" height="808" alt="Screenshot 2025-08-19 162233" src="https://github.com/user-attachments/assets/a66067be-80bc-4b88-a994-5d5267d86160" />
<img width="1351" height="808" alt="Screenshot 2025-08-19 040912" src="https://github.com/user-attachments/assets/3481ef28-3e1a-4b80-87c5-01d9f2b4c3e7" />

## 📋 Prerequisites

- Python 3.9 or higher
- Google Gemini API Key (for Nilam Chat)
- my .pkl file is more than 800mb lfs didn't support, so recommended to run simple_model.py locally (for Nilam Sense)

## 🛠️ Installation

1. **Clone the repository**
   
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys**
   - Create a `.streamlit/secrets.toml` file
   - Add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```
   
4. **Start the main application**
   ```bash
   streamlit run main.py
   ```
