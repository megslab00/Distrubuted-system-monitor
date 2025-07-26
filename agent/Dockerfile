# Stage 1: Build the Go binary
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy all project files first.
# This allows 'go mod tidy' to see the imports in your main.go file.
COPY . .

# Tidy will now read main.go, find the imports, and fix your go.mod file.
RUN go mod tidy

# Build the binary statically linked
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o agent .

# Stage 2: Create a minimal final image
FROM alpine:latest

WORKDIR /root/
# Copy the binary from the builder stage
COPY --from=builder /app/agent .

# Command to run the agent
CMD ["./agent"]