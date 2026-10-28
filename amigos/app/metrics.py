from prometheus_client import Counter, Histogram
from flask import Response, request
import time

# Definición de métricas de Prometheus
REQUEST_COUNT = Counter(
    'flask_http_request_total', 
    'Total HTTP Requests', 
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_duration_seconds', 
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)