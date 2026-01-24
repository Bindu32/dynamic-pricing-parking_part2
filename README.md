# 🚗 Dynamic Parking Pricing System – End-to-End Data Science & Deployment Project

## 📌 Project Summary

This project implements a **Dynamic Pricing System for Urban Parking Lots** using data science principles and real-time inspired logic.
The system dynamically adjusts parking prices based on:

* Parking occupancy
* Capacity
* Traffic conditions
* Queue length
* Competitive pricing

The solution is delivered as an **interactive Streamlit web application**, containerized using **Docker**, and deployed on **free cloud platforms**.

This project demonstrates **end-to-end engineering**:
data ingestion → pricing logic → visualization → containerization → public deployment.

---

## 🎯 Problem Statement

Static parking prices cause:

* Overcrowding during peak hours
* Underutilization during off-peak hours
* Revenue inefficiency
* Poor user experience

### Solution

Introduce **dynamic pricing**, similar to surge pricing models, to:

* Balance demand
* Optimize revenue
* Reduce congestion
* Improve fairness

---

## 🧱 Tech Stack

| Category         | Technology                           |
| ---------------- | ------------------------------------ |
| Language         | Python 3.10                          |
| Data Processing  | Pandas, NumPy                        |
| Visualization    | Bokeh                                |
| Web App          | Streamlit                            |
| Containerization | Docker                               |
| Deployment       | Streamlit Cloud, Hugging Face Spaces |
| Version Control  | Git, GitHub                          |

---

## 📂 Repository Structure

```
dynamic-pricing-parking_part2/
│
├── app.py / streamlit_app.py
├── dataset.csv
├── requirements.txt
├── runtime.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## 📁 File-by-File Explanation

### 1️⃣ `dataset.csv`

Contains parking lot operational data used as input for the pricing model.

**Important Columns**

* `SystemCodeNumber` – Parking lot identifier
* `Occupancy` – Number of occupied slots
* `Capacity` – Total parking capacity
* `TrafficConditionNearby` – low / medium / high
* `QueueLength` – Vehicles waiting
* `competitor_price` (optional)

---

### 2️⃣ `app.py` / `streamlit_app.py`

Main **Streamlit application file**.

**Responsibilities**

* Load dataset (file upload or default CSV)
* Execute dynamic pricing logic
* Display results in tables
* Render interactive visualizations

**Major Sections**

1. Page configuration
2. Dataset loading
3. Pricing pipeline
4. Run model button
5. Output table
6. Visualization
7. Key metrics

This file contains the **business logic + UI layer**.

---

### 3️⃣ Pricing Logic (Core Model)

**Step 1: Occupancy Rate**

```python
occupancy_rate = Occupancy / Capacity
```

**Step 2: Linear Pricing**

```python
linear_price = base_price * (1 + occupancy_rate)
```

**Step 3: Traffic Weight**

```python
traffic_map = {"low": 1.0, "medium": 1.5, "high": 2.0}
```

**Step 4: Dynamic Pricing**

```python
dynamic_price = base_price * \
                (1 + 1.5 * occupancy_rate) * \
                (1 + 0.2 * traffic_weight) * \
                (1 + 0.1 * queue_length)
```

**Step 5: Competitive Pricing**

```python
competitive_price = min(dynamic_price, competitor_price)
```

---

### 4️⃣ Visualization (Bokeh)

A line chart comparing:

* Linear Price
* Dynamic Price
* Competitive Price

Used to visually analyze pricing behavior across parking lots.

---

### 5️⃣ `requirements.txt`

Defines Python dependencies required to run the project.

Example:

```
streamlit==1.29.0
pandas
numpy==1.26.4
bokeh==2.4.3
```

Pinned versions ensure compatibility across environments.

---

### 6️⃣ `runtime.txt`

Specifies Python version for Streamlit Cloud.

```
python-3.10
```

Prevents incompatibility with newer Python releases.

---

### 7️⃣ `Dockerfile`

Defines the container image for the application.

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Ensures:

* Reproducibility
* Dependency isolation
* Cloud portability

---

### 8️⃣ `.dockerignore`

Prevents unnecessary files from being included in the Docker image.

Example:

```
__pycache__/
.git/
.env
```

---

## ▶️ Run Locally (Without Docker)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Access:

```
http://localhost:8501
```

---

## 🐳 Run with Docker (Local)

### Build Image

```bash
docker build -t parking-pricing-app .
```

### Run Container

```bash
docker run -p 8501:8501 parking-pricing-app
```

---

## ☁️ Deployment Strategy

### Streamlit Cloud

* GitHub repository connected
* Uses `runtime.txt` and `requirements.txt`
* Application runs successfully
* Known limitation: Bokeh + NumPy compatibility

---

## 🚀 Final Deployment: Hugging Face Spaces (Docker)

**Why Hugging Face Spaces**

* Free
* Public URL
* Docker support
* No dependency conflicts

**Deployment Type**

```
Hugging Face Spaces → Docker → Streamlit
```

**Push Code**

```bash
git add .
git commit -m "Deploy dynamic parking pricing app"
git push
```

Authentication uses Hugging Face access token.

---

## ✅ Deployment Status

* Dataset loads successfully
* Pricing model executes
* Dashboard renders
* Public access available
* Dockerized and reproducible

Deployment is **COMPLETE**.

---

## 📈 Resume Value

* End-to-end project ownership
* Real-world pricing logic
* Cloud deployment experience
* Docker and debugging skills

---

## 🔮 Future Enhancements

* Replace Bokeh with Plotly
* Real-time streaming integration
* ML-based optimization
* User authentication
* Kubernetes deployment

---

## 🏁 Conclusion

This project reflects real-world data engineering and deployment challenges.

> *"If it runs in the cloud, the project is complete."*

**A full-stack data science deployment project.**
