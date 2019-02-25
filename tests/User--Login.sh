curl -X "POST" "http://127.0.0.1:5000/v1/auth/remote?response_type=token&client_id=Q1aymT0qkHpYLTNmYTrUpezQfmjy9PVzv8Wzg5uB&redirect_uri=http%3A%2F%2F127.0.0.1%3A9000%2Fauthorize&scope=user&state=json" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"joshua@viable.io\",\"password\":\"commons\"}"

