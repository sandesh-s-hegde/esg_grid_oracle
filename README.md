# ESG Grid Oracle: Carbon-Aware Routing Node

## 🌍 Product Vision
The **ESG Grid Oracle** is a decoupled, API-first microservice designed to transform static logistics networks into **Grid-Integrated Supply Chains**. By continuously monitoring the real-time carbon intensity (gCO2eq/kWh) of international energy grids, this Oracle empowers autonomous multi-agent systems to make deterministic, carbon-aware routing decisions—effectively performing spatial energy arbitrage across borders.

## 🎯 The Problem Space
With the introduction of strict global sustainability mandates (like the EU's CSRD), enterprise supply chains can no longer optimize purely for *Cost* and *Speed*. They must now account for **Scope 3 Emissions**. Traditional logistics digital twins fail to recognize that fleet assets (especially EVs and refrigerated units) are high-draw Distributed Energy Resources (DERs). Charging a fleet in a region currently powered by coal actively damages an enterprise's ESG posture, even if the logistics route is technically shorter.

## 💡 The Solution
This microservice acts as the "Sustainability Truth Layer" for our autonomous Digital Capacity Twin. Instead of hardcoding routes, our LLM-powered procurement agents query this Oracle in real-time before dispatching assets. 

If the German grid is currently red (high fossil fuel mix), the Oracle signals the AI agent to dynamically reroute capacity from the French grid (high nuclear/renewables mix), dynamically shedding carbon load without human intervention.

## 🚀 Key Capabilities
* **Real-Time Telemetry Simulation:** Continuously calculates and serves stochastic carbon intensity profiles for major European grid regions (DE, FR, IE, UK, NL).
* **Deterministic Traffic Lighting:** Abstracts complex gCO2eq/kWh math into standardized `GREEN`, `AMBER`, and `RED` dispatch signals for rigid downstream robotic process automation (RPA) consumption.
* **Agentic Integration:** Architected specifically to act as an external tool/node for LLM Swarms (Gemini/OpenAI) to reason against during automated freight negotiation.
* **Enterprise Scalability:** Built on a lightweight, containerized FastAPI foundation, designed for zero-downtime deployment and seamless hot-swapping to live data providers (e.g., WattTime, ElectricityMaps) in production.

## 📈 Business Impact
* **Automated Compliance:** Provides a programmatic trail of carbon-optimized dispatching for ESG audits.
* **Scope 3 Reduction:** Actively minimizes the carbon footprint of outsourced transportation logistics.
* **Zero-Touch Orchestration:** Removes the human bottleneck from sustainable decision-making during high-stress supply chain shock events.