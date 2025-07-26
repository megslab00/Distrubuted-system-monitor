package main

import (
	"encoding/json"
	"log"
	"os"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
	"github.com/streadway/amqp"
)

// MetricData holds all the metrics for a given node.
type MetricData struct {
	NodeID     string  `json:"node_id"`
	CPUUsage   float64 `json:"cpu_usage"`
	RAMUsage   float64 `json:"ram_usage"`
	DiskUsage  float64 `json:"disk_usage"`
	NetSent    uint64  `json:"net_sent"`
	NetRecv    uint64  `json/:"net_recv"`
	Timestamp  string  `json:"timestamp"`
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	// Get RabbitMQ URL from environment variable, with a default
	rabbitMQURL := os.Getenv("RABBITMQ_URL")
	if rabbitMQURL == "" {
		rabbitMQURL = "amqp://guest:guest@localhost:5672/"
	}

    // Get a unique Node ID from the environment (e.g., container hostname)
    nodeID := os.Getenv("HOSTNAME")
    if nodeID == "" {
        nodeID = "local-node"
    }
    log.Printf("🚀 Starting agent for node: %s", nodeID)

	conn, err := amqp.Dial(rabbitMQURL)
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"metrics_queue", // name
		true,            // durable
		false,           // delete when unused
		false,           // exclusive
		false,           // no-wait
		nil,             // arguments
	)
	failOnError(err, "Failed to declare a queue")

	// Collect metrics every 10 seconds
	ticker := time.NewTicker(10 * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		// Collect Metrics
		c, _ := cpu.Percent(0, false)
		r, _ := mem.VirtualMemory()
		d, _ := disk.Usage("/")
		n, _ := net.IOCounters(false)

		data := MetricData{
            NodeID:     nodeID,
			CPUUsage:   c[0],
			RAMUsage:   r.UsedPercent,
			DiskUsage:  d.UsedPercent,
			NetSent:    n[0].BytesSent,
			NetRecv:    n[0].BytesRecv,
			Timestamp:  time.Now().UTC().Format(time.RFC3339),
		}

		body, err := json.Marshal(data)
		if err != nil {
			log.Printf("Error marshalling JSON: %s", err)
			continue
		}

		err = ch.Publish(
			"",     // exchange
			q.Name, // routing key
			false,  // mandatory
			false,  // immediate
			amqp.Publishing{
				ContentType: "application/json",
				Body:        body,
			})

		if err != nil {
			log.Printf("Failed to publish a message: %s", err)
		} else {
			log.Printf("✅ Sent metrics for node %s", nodeID)
		}
	}
}