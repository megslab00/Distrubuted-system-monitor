
# 🖥️ Distributed System Health Monitor

A Docker-powered monitoring system where lightweight agents collect health data (CPU, RAM, Disk) from multiple computers and send it to a central server for real-time tracking and analysis.

---

## 🗂️ Table of Contents

- [📖 About The Project](#-about-the-project)
- [✨ Key Features](#-key-features)
- [⚙️ Architecture](#-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [🔬 Usage](#-usage)
- [💡 Future Improvements](#-future-improvements)
- [📄 License](#-license)

---

## 📖 About The Project

This project simulates a professional SRE-style observability pipeline. It collects system health metrics (CPU, memory, ping) from multiple distributed nodes and pushes them through RabbitMQ to a centralized processor. The entire system is containerized with Docker and orchestrated using Docker Compose for easy setup and scaling.

---

## ✨ Key Features

- **Lightweight Python Agent** to collect system metrics using `psutil` and `ping3`.
- **RabbitMQ Message Queue** to handle reliable communication between nodes.
- **Central Processing Service** that logs and processes all incoming data.
- **Dockerized Setup** that runs consistently across all environments.
- **Simulates Multi-Machine Setup** using multiple agent containers.

---

## ⚙️ Architecture

```

+------------------+       +------------------+       +------------------+
\|   Agent Node 1   |       |   Agent Node 2   |       |   Agent Node 3   |
\|   (Python App)   |       |   (Python App)   |       |   (Python App)   |
+--------+---------+       +--------+---------+       +--------+---------+
\|                          |                          |
\|                          |                          |
+-----------+--------------+--------------+-----------+
\|      RabbitMQ Message Queue            |
+----------------+-----------------------+
|
+--------v--------+
\|   Metric Logger  |
\|  (Python Script) |
+------------------+

````

---

## 🛠️ Tech Stack

| Component         | Technology        |
|------------------|-------------------|
| Agents           | Python, psutil, ping3 |
| Message Broker   | RabbitMQ           |
| Processor        | Python, pika       |
| Orchestration    | Docker, Docker Compose |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

# Build and run everything
docker-compose up --build -d
````

---

## 🔬 Usage

### 1. View Real-Time Logs

```bash
docker-compose logs -f
```

### 2. Open RabbitMQ Dashboard

* URL: [http://localhost:15672](http://localhost:15672)
* Username: `guest`
* Password: `guest`

### 3. Stop the System

```bash
docker-compose down
```

---

## 💡 Future Improvements

* Integrate Grafana for live dashboards
* Store data in Prometheus or InfluxDB
* Enable alerting with thresholds
* Add authentication between services
* Deploy on cloud with auto-scaling

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

````
