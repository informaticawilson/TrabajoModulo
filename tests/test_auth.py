"""Pruebas para POST /auth/register."""


# --- Registro de usuarios ---------------------------------------------------

def test_register_success(client):
    response = client.post("/auth/register", json={"username": "nuevo_user", "password": "segura123"})
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "nuevo_user"
    assert "id" in body
    assert "password_hash" not in body


def test_register_duplicate_username(client):
    client.post("/auth/register", json={"username": "duplicado", "password": "pass1"})
    response = client.post("/auth/register", json={"username": "duplicado", "password": "pass2"})
    assert response.status_code == 409


def test_register_then_login(client):
    client.post("/auth/register", json={"username": "freshuser", "password": "mi_clave_456"})
    response = client.post("/auth/login", json={"username": "freshuser", "password": "mi_clave_456"})
    assert response.status_code == 200
    assert "access_token" in response.json()
