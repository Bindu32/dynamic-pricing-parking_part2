# Smart City Dynamic Parking Pricing System

An end-to-end **data analytics project** that demonstrates how urban parking systems can use **dynamic pricing and demand analytics** to optimize revenue and manage parking demand.

This project simulates real-world parking demand and applies **data-driven pricing strategies** based on occupancy, traffic conditions, and queue length.

A live analytics dashboard allows users to explore pricing trends, revenue impact, and spatial demand patterns across parking locations.

---
## Live Demo
[https://dynamic-pricing-parkingpart2-od6quqdnfpvbspqcioxmwt.streamlit.app/]

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
```
data ingestion → pricing logic → visualization → containerization → public deployment.
```
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
## Key Features

Dynamic Pricing Model  
A pricing algorithm adjusts parking prices based on occupancy, traffic conditions, and queue length.

Revenue Analytics  
Estimates total revenue under dynamic pricing scenarios.

Interactive Dashboard  
Built using Streamlit for real-time analytics and visualization.

Geospatial Demand Analysis  
Parking locations and demand intensity are visualized on an interactive city map.

Demand Heatmap  
Shows areas with high parking demand using spatial heatmaps.

Real-Time Simulation  
Optional demand simulation dynamically updates parking occupancy and pricing.

---
## 🏗 System Architecture
The project simulates a real-world analytics pipeline used in smart city infrastructure systems.
```
Parking Dataset
      │
      ▼
Data Pipeline
(Data Cleaning + Feature Engineering)
      │
      ▼
Dynamic Pricing Model
      │
      ▼
Revenue & Demand Analytics
      │
      ▼
Interactive Dashboard (Streamlit)
      │
      ▼
Geospatial Visualization (Folium Maps)
```

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
## Dashboard Preview
<img width="1429" height="641" alt="Screenshot 2026-03-12 103116" src="https://github.com/user-attachments/assets/75f1c003-f51a-4cec-a562-4d27fb160d88" />
<img width="1448" height="646" alt="Screenshot 2026-03-12 103105" src="https://github.com/user-attachments/assets/5a2d3f30-29e2-4ace-b567-62fef6bdb36c" />


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

## ☁️ Deployment
The application can be deployed using:
- Streamlit Community Cloud
- Hugging Face Spaces (Docker)
Both provide public URLs for accessing the dashboard without local installation.

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


---

## 📈 Project Value
This project demonstrates multiple industry-relevant skills:
- Data pipeline development
-  Demand-driven pricing analytics
- Interactive dashboard creation
- Geospatial data visualization
- Cloud deployment and containerization

It represents an end-to-end data analytics system, from raw data processing to public dashboard deployment.
---

## 🔮 Future Enhancements
Possible extensions include:
- Machine learning based demand forecasting
- Real-time parking sensor data integration
- Dynamic pricing optimization using reinforcement learning
- City-wide parking demand simulation
- Multi-city deployment

---

## 👩‍💻 Author

- Bindu Sri Majji
- Final Year Computer Science Student

Interested in:

- Data Analytics
- Data Science

