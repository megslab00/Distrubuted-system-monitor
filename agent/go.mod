module agent

go 1.22

require (
	github.com/shirou/gopsutil/v3 v3.24.5
	github.com/streadway/amqp v1.1.0
)
// ... other indirect dependencies will be added by `go mod tidy`