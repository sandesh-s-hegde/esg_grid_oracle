# 🌍 ESG Grid Oracle: Carbon-Aware Routing Node

**Author:** Sandesh S. Hegde  
**Version:**  

## 📖 Executive Summary

This artifact operationalizes the sustainability layer of the supply chain ecosystem. It serves as a **Sustainability Truth Layer**, designed to connect modern, AI-driven supply chain analytics (like the Digital Capacity Optimizer) with real-time international energy grid telemetry. By continuously monitoring the carbon intensity (gCO2eq/kWh) of European energy grids, this microservice empowers autonomous multi-agent systems to make deterministic, carbon-aware routing decisions—effectively performing spatial energy arbitrage across borders.

---

## 🎯 The Business Problem

With the introduction of strict global sustainability mandates (like the EU's CSRD), enterprise supply chains can no longer optimize purely for *Cost* and *Speed*. They must now account for **Scope 3 Emissions**. Traditional logistics digital twins fail to recognize that fleet assets (especially EVs and refrigerated units) are high-draw Distributed Energy Resources (DERs). Charging a fleet in a region currently powered by coal actively damages an enterprise's ESG posture, even if the logistics route is technically shorter.

---

## 🧮 Architectural Framework

This microservice acts as the intelligent environmental router. It is built on a strictly asynchronous, high-performance architecture:

### 1. In-Memory TTL Caching Engine
To prevent upstream API latency and reduce external compute costs, the API utilizes a **5-Minute Time-To-Live (TTL) Cache**. Grid carbon intensity updates in intervals, not milliseconds; this architectural pattern ensures AI agents receive instantaneous telemetry without hammering upstream data providers.

### 2. Zero-Trust Security & Idempotency
Enterprise endpoints are never left exposed. The system implements an **API Key Dependency Injection** model at the route level, ensuring secure, zero-trust communication. Strict CORS middleware protects against unauthorized browser-based cross-origin requests.

### 3. High-Throughput Batch Processing
When LLM agents evaluate multiple potential freight routes simultaneously, pinging the API for individual regions causes unnecessary network overhead. The API utilizes a vectorized approach, allowing the autonomous swarm to evaluate massive geographic regions (e.g., FR, DE, IE) in a single optimized payload.

### 4. Global Exception Interception
The system implements a **Global Exception Handler** to intercept unexpected server faults. Instead of throwing raw server HTML errors, it guarantees a structured JSON response, ensuring that downstream robotic and AI parsing engines do not break during failure states.

---

## 🚀 Key Features

### 🛡️ 1. Enterprise Security & Resilience
* **Strict Validation:** `pydantic` schemas enforce strict data typing and inject rich contextual examples directly into the Swagger UI.
* **Non-Root Execution:** The `Dockerfile` is hardened to run exclusively under an unprivileged user profile for maximum cloud security.
* **Continuous Integration:** Fully automated GitHub Actions CI pipeline running `pytest` and HTTPX validations on every push.

### 📊 2. Deep Health & Telemetry
* **Performance Middleware:** Injects exact millisecond execution times into the `X-Process-Time` HTTP header for distributed tracing.
* **Uptime Tracking:** The `/health` endpoint actively calculates system boot-time to help load balancers detect memory leaks or stale containers.

### 🤖 3. Agentic Integration
* **Deterministic Traffic Lighting:** Abstracts complex gCO2eq/kWh math into standardized `GREEN`, `AMBER`, and `RED` dispatch signals for rigid downstream AI and RPA consumption.
* **Swarm Ready:** Architected specifically to act as an external tool/node for LLM Swarms (Gemini/OpenAI) to reason against during automated freight negotiation.

---

## ⚙️ Technical Architecture

* **Language:** Python 3.12+
* **Framework:** FastAPI (Asynchronous ASGI)
* **Data Validation:** Pydantic 2.0
* **Testing:** Pytest & HTTPX (TestClient)
* **DevOps:** Docker Compose, `.dockerignore` optimized builds, GitHub Actions (CI/CD)

---

## 🚀 Installation & Usage

### Prerequisites
You need [Docker & Docker Compose](https://www.docker.com/) installed on your machine.

### Local Deployment

```bash
# 1. Clone the repository
git clone https://github.com/sandesh-s-hegde/esg-grid-oracle.git
cd esg-grid-oracle

# 2. Set your Environment Variables
# Create a .env file and populate it using .env.example
cp .env.example .env

# 3. Build and launch the container environment
make docker-up

# 4. Verify System Health
curl http://localhost:8000/health
```

### Developer Commands
A `Makefile` is included to standardize workflows:
* `make install` - Installs Python requirements.
* `make run` - Runs the application locally via Uvicorn.
* `make test` - Executes the `pytest` suite.

---

## ☁️ Production Infrastructure

This application is designed for containerized deployment in environments like Kubernetes, AWS ECS, or Render. 
* **Compute:** Containerized FastAPI web service.
* **Security:** Non-root execution profile (`appuser`).
* **CI/CD:** Automated testing pipeline via GitHub Actions on every push to `main` to ensure zero regression.

---

## 🔮 Roadmap & Project Status

This project is structured for incremental enterprise scale, moving from a foundational simulation API to a live, global telemetry ingestion engine.

| Phase | Maturity Level | Key Capabilities | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Foundation (v1.3)** | **FastAPI Gateway, TTL Caching, Batch Processing, Zero-Trust Auth, and CI/CD Pipeline.** | ✅ **Stable** |
| **Phase 2** | **Live Integrations** | Hot-swapping the stochastic simulation engine for live commercial APIs (e.g., WattTime, ElectricityMaps). | 🚧 Next |
| **Phase 3** | **Predictive AI** | Implementing local time-series models (ARIMA/Prophet) to forecast grid intensity 24 hours in advance. | 🚧 Planned |
| **Phase 4** | **Global Expansion** | Extending region support beyond the EU to cover NAMER (ERCOT, PJM) and APAC energy grids. | 💡 Vision |
| **Phase 5** | **Hardware-in-the-Loop** | Direct WebSocket integrations to dynamically curtail physical EV charger output based on grid signals. | 💡 Vision |

---

> ➡️ **Ecosystem Integration:** This repository acts as the "environmental conscience" of the logistics ecosystem. The brain dictating these actions is the **[Digital Capacity Optimizer](https://github.com/sandesh-s-hegde/digital_capacity_optimizer)**, which queries this API to calculate multi-modal routing logic.