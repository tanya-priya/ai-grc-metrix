# 🤖 AI GRC Metrix

**AI GRC Metrix** is an intelligent, automated Governance, Risk, and Compliance (GRC) monitoring and analytics dashboard built using Python and Streamlit. It leverages Artificial Intelligence to evaluate compliance frameworks, analyze risk vectors, and generate real-time metrics for executive decision-making.

---

## 🚀 Key Features

* **AI-Driven Risk Assessment:** Automatically flags potential compliance violations and calculates real-time risk scores using LLMs.
* **Dynamic Compliance Dashboards:** Interactive visualization of core GRC frameworks (e.g., SOC2, ISO 27001, GDPR, NIST, DORA, DPDP Act).
* **Automated Reporting:** Generates audit-ready summaries and metrics with single-click exports.
* **Intuitive UI/UX:** Built entirely with a sleek Streamlit interface for effortless navigation without front-end friction.

---

## 🛠️ Tech Stack

* **Frontend/Dashboard:** Streamlit
* **Core Language:** Python 3.12.3
* **Data Processing:** Pandas
* **AI/LLM Integration:** Google Gemini
* **Visualizations:** Plotly / Altair

---

## ⚙️ Installation & Setup

Follow these steps to run **AI GRC Metrix** locally:

### 1. Clone the Repository
```bash
git clone https://github.com/tanya-priya/ai-grc-metrix.git
cd ai-grc-metrix
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add any necessary AI secrets or API keys:
```env
OPENAI_API_KEY=your_api_key_here
```

### 5. Run the Streamlit Application
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```text
├── README.md               
├── requirements.txt        
├── app.py                 
├── .venv/                  
├── __pycache__/
└── docs/                  
```

---

## 🤝 Contributing

Contributions are welcome! If you want to improve the AI logic, add compliance templates, or enhance the dashboard visualization:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.
