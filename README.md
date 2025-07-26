#🚀 Distributed System Health Monitor


A Docker-powered monitoring system where lightweight Go agents collect health data (CPU, RAM, Disk) from multiple computers and send it to a central server for real-time tracking and analysis. This project is designed to simulate an SRE-style observability pipeline in a cloud-native environment.

✨ Key Features
Lightweight Go Agent: An efficient, low-overhead agent for collecting system metrics from multiple nodes.

Centralized Data Pipeline: Uses RabbitMQ as a robust message broker to queue data reliably from all agents.

Python Processing Service: A central worker that consumes, processes, and logs the incoming metrics.

AI Recovery Assistant: A simple FastAPI-based API that provides predefined solutions for known error patterns.

Fully Containerized: The entire multi-node system is orchestrated with Docker and Docker Compose for easy deployment and simulation.

⚙️ Architecture
The system follows a decoupled, message-driven architecture to ensure scalability and resilience.

Code snippet

graph TD
    subgraph Monitored Nodes
        Agent1[Go Agent on Node 1]
        Agent2[Go Agent on Node 2]
        Agent3[Go Agent on Node 3]
    end

    subgraph Central Services
        MQ[RabbitMQ Message Queue]
        Processor[Python Processor]
        AIAssistant[🤖 AI Recovery Assistant]
    end

    Agent1 --> MQ
    Agent2 --> MQ
    Agent3 --> MQ

    MQ --> Processor
🛠️ Tech Stack
Agent & Processor:

Go (gopsutil, amqp)

Python (pika, fastapi)

Message Broker:

RabbitMQ

Containerization:

Docker & Docker Compose

📋 Prerequisites
Ensure you have Docker and Docker Compose installed on your system.

Install Docker

🚀 Getting Started
Clone the repository:

Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
Build and run the system:
This single command will build the images for all services and start them in the background.

Bash

docker-compose up --build -d
The system is now running! The docker-compose.yml is configured to simulate 3 agents by default.

🔬 How to Check the System
You can observe the working application at three main places:

Live Logs:
See the real-time output from all services. You will see agents sending metrics and the processor receiving them.

Bash

docker-compose logs -f
(Press Ctrl + C to stop viewing logs.)

RabbitMQ Dashboard:
This is the visual control panel for your data pipeline.

URL: http://localhost:15672

Login: guest / guest

Go to the "Queues" tab to see messages being published and consumed.

AI Assistant API:
Check if the recovery assistant API is online.

URL: http://localhost:8000

🛑 Stopping the System
To stop and remove all running containers, run:

Bash

docker-compose down
📁 Project Structure
.
├── docker-compose.yml
├── agent/
│   ├── main.go
│   ├── go.mod
│   └── Dockerfile
├── processor/
│   ├── processor.py
│   ├── requirements.txt
│   └── Dockerfile
└── assistant/
    ├── assistant.py
    ├── requirements.txt
    └── Dockerfile
💡 Future Improvements
Full Observability Stack: Integrate Prometheus for metrics storage and Elasticsearch for log aggregation.

Visual Dashboard: Add Grafana to create dashboards for visualizing metrics and logs.

Alerting: Implement Prometheus Alertmanager for automated alerting on critical conditions (e.g., high CPU).

Automated Remediation: Extend the AI Assistant to trigger automated fixes (e.g., running an Ansible playbook) for known issues.

📄 License
Distributed under the MIT License. See LICENSE for more information.
