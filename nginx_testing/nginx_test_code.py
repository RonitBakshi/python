upstream backend {
        least_conn;
        server localhost:8001;
        server localhost:8002;
        server localhost:8003;
        server localhost:8004;
    }

    server {
        listen 80;
        server_name generation.chatreal.ai;

        location /v1/chat/completions {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

	    # extend the timeout for answer form VLLM endpoint to 10 minutes
            proxy_read_timeout 600s;

	    # Retry on specific conditions
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        }
}