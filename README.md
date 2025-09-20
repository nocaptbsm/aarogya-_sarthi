<p align="center">
  <img src="https://raw.githubusercontent.com/user-attachments/assets/b2462e92-31d0-4054-9721-399a0ed34fa9" alt="Aarogya Sarthi Logo" width="150"/>
</p>

<h1 align="center">Aarogya Sarthi (आरोग्य सारथी) 🩺🤖</h1>

<p align="center">
  <strong>Our official solution for the Smart India Hackathon (SIH), engineered to bridge the public healthcare information gap in Odisha through conversational AI.</strong>
  <br/>
  <br/>
  <a href="https://www.sih.gov.in/"><img src="https://img.shields.io/badge/Smart%20India-Hackathon-blue"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.9+-blue.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Framework-Rasa-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Deployment-Docker-blueviolet.svg"></a>
  <a href="https://github.com/your-team-repo/Aarogya-Sarthi/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>

---

## 📖 The Challenge: SIH Problem Statement

This project is our dedicated solution to the following challenge posed by the Government of Odisha.

* **ID:** `ID25049`
* **Title:** AI-Driven Public Health Chatbot for Disease Awareness.
* **Organization:** Government of Odisha
* **Department:** Electronics & IT Department
* **Description:** Create a multilingual AI chatbot to educate rural and semi-urban populations about preventive healthcare, disease symptoms, and vaccination schedules. The chatbot should integrate with government health databases and provide real-time alerts for outbreaks.

---

## 💡 Our Solution: Aarogya Sarthi

**Aarogya Sarthi** is a purpose-built AI health companion designed to empower every citizen of Odisha with instant, reliable, and accessible health information. We deliver this through the platforms they already know and trust—**WhatsApp and SMS**—in their native language, serving as a true digital health `Sarthi` (charioteer).

### ✨ Our Unique Approach

* **1. Zero Friction Onboarding:** By leveraging WhatsApp & SMS, we eliminate the digital literacy barriers and app-download fatigue common in rural areas.
* **2. Hyper-Local Intelligence:** Our AI is trained on data specific to Odisha's health landscape, understanding local dialects (Odia), regional diseases, and the state’s healthcare network.
* **3. A Beacon of Trust:** In an era of misinformation, our chatbot integrates directly with official government health databases, ensuring every piece of information is authenticated and reliable.
* **4. Engineered for State-Wide Scale:** Our architecture is not just a prototype; it's a production-ready system built with Docker and Kubernetes to serve millions of users reliably during critical public health events.

---

## 📱 How It Works: A Sneak Peek

See Aarogya Sarthi in action! The user experience is designed to be as simple and natural as texting a friend.

*(Pro-Tip: Replace the image below with a short GIF of your chatbot working. It's highly effective!)*

<p align="center">
  <img src="https://raw.githubusercontent.com/user-attachments/assets/6e2b963a-8fa3-4c91-a5f1-39775a7ab13c" alt="Aarogya Sarthi Demo" width="300"/>
</p>

---

## 🚀 Key Features

* **🌐 Multilingual & Accessible:** Fluent in **Odia**, Hindi, and English to ensure no one is left behind.
* **🏥 Comprehensive Health Info:** Provides verified information on disease symptoms, preventive care, maternal/child health, and vaccination schedules.
* **🚨 Real-time Outbreak Alerts:** Connects to state health APIs to broadcast timely alerts about potential outbreaks in a user's locality.
* **🧠 Intelligent & Empathetic:** Powered by an advanced NLP engine to understand user intent, handle colloquialisms, and provide clear, helpful responses.
* **🚫 Diagnosis Disclaimer:** Ethically designed to inform and educate, never to diagnose. It consistently guides users to consult with healthcare professionals.

---

## 🛠️ Technology Stack & Architecture

We have chosen a modern, open-source, and scalable tech stack for a robust and maintainable solution.

* **NLP Framework:** **Rasa** (for its powerful, open-source dialogue management)
* **Backend:** **Python (FastAPI)** (for high-performance API services)
* **Messaging Gateway:** **Twilio** API for WhatsApp & SMS
* **Database:** **PostgreSQL**
* **Deployment:** **Docker** & **Kubernetes**

**System Architecture Flow:**
```
User (WhatsApp/SMS) -> Twilio Gateway -> Webhook -> Rasa NLP Engine -> Core Application Logic -> Govt. Health APIs/DB -> Response to User
```

---

## 📈 Scalability & Deployment Plan

* **Containerization:** The entire application is containerized using **Docker**, ensuring consistency and portability.
* **Orchestration:** We will use **Kubernetes** to automate deployment, scaling, and management, allowing us to seamlessly handle state-wide user traffic.
* **CI/CD Pipeline:** A **GitHub Actions** workflow automates testing and deployment, enabling rapid and reliable updates to the service.

---

## 🛡️ Data Privacy & Ethical AI

* **Data Privacy:** We are committed to complying with India's **Digital Personal Data Protection (DPDP) Act**. All user data is encrypted in transit and at rest, and personally identifiable information is anonymized.
* **Bias Mitigation:** Our NLP models are continuously monitored and retrained with diverse datasets to ensure fair and unbiased responses for all citizens.

---

## 🌌 Future Vision

We envision Aarogya Sarthi as a foundational piece of Odisha's digital health future.

* **Phase 4: ABDM Integration:** Integrate with the **Ayushman Bharat Digital Mission (ABDM)**, allowing users to link their ABHA number for personalized health information and services via the **Unified Health Interface (UHI)**.
* **Phase 5: Predictive Analytics:** Develop a dashboard for health officials that uses anonymized query data to identify symptom hotspots and predict potential outbreaks.
* **Phase 6: Voice-Enabled Service:** Integrate a voice module to make the service fully accessible to users with low literacy levels.

---

## ▶️ Demo & Presentation

* **Video Demo:** [Link to Your YouTube Project Demo]
* **Presentation Slides:** [Link to Your Project PPT/PDF]

---

## 🏆 Our Team: [Team Name Here]

Meet the innovators behind Aarogya Sarthi!

| Name             | Role                     | GitHub Profile                               |
| ---------------- | ------------------------ | -------------------------------------------- |
| [Abhishek Ranjan] | Team Leader / Backend Dev | [Link to GitHub]                             |
| [Avinash Pandey]  | NLP / ML Specialist      | [Link to GitHub]                             |
| [Manoj k]  | Full Stack Developer     | [Link to GitHub]                             |
| [Yaashik H]  | DevOps / Cloud Engineer  | [Link to GitHub]                             |
| [Lavli]  | UI/UX & QA               | [Link to GitHub]                             |
| [Prashant Kumar]  | Domain Researcher        | [Link to GitHub]                             |

---

## 🏁 Getting Started (For Developers)

Follow these steps to set up the project locally.

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-team-repo/Aarogya-Sarthi.git](https://github.com/your-team-repo/Aarogya-Sarthi.git)
    cd Aarogya-Sarthi
    ```
2.  **Set up environment variables:**
    Create a `.env` file from the `.env.example` and add your configuration details.
3.  **Run with Docker Compose (Recommended):**
    ```sh
    docker-compose up --build
    ```
4.  **Train the Rasa model (if needed):**
    ```sh
    docker-compose exec rasa rasa train
    ```

---

## 🤝 Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` file for guidelines on how to get involved.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 🙏 Acknowledgements

We extend our sincere gratitude to:
* **Smart India Hackathon** for this incredible innovation platform.
* **Government of Odisha** for presenting this critical real-world challenge.
* Our mentors for their invaluable guidance and support.
