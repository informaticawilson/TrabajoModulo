"""Pruebas básicas de los 3 requisitos funcionales (RF-01, RF-02, RF-03)."""


def _get_token(client):
    response = client.post("/auth/login", json={"username": "demo", "password": "demo123"})
    return response.json()["access_token"]


# --- RF-03: Autenticación ---------------------------------------------------

def test_login_success(client):
    response = client.post("/auth/login", json={"username": "demo", "password": "demo123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    response = client.post("/auth/login", json={"username": "demo", "password": "incorrecta"})
    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/documents/search")
    assert response.status_code == 401


# --- RF-01: Carga de documentos ---------------------------------------------

def test_upload_requires_auth(client):
    response = client.post(
        "/documents",
        data={"title": "Contrato", "category": "legal"},
        files={"file": ("contrato.pdf", b"contenido", "application/pdf")},
    )
    assert response.status_code == 401


def test_upload_success(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/documents",
        data={"title": "Manual de Usuario", "category": "manuales"},
        files={"file": ("manual.pdf", b"contenido de prueba", "application/pdf")},
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Manual de Usuario"
    assert body["category"] == "manuales"


def test_upload_rejects_disallowed_extension(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/documents",
        data={"title": "Programa", "category": "otros"},
        files={"file": ("programa.exe", b"binario", "application/octet-stream")},
        headers=headers,
    )
    assert response.status_code == 400


# --- RF-02: Búsqueda y filtrado ---------------------------------------------

def test_search_finds_uploaded_document(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/documents",
        data={"title": "Reporte Financiero Q1", "category": "finanzas"},
        files={"file": ("reporte.pdf", b"contenido", "application/pdf")},
        headers=headers,
    )

    response = client.get("/documents/search?q=Financiero", headers=headers)
    assert response.status_code == 200
    results = response.json()
    assert any(doc["title"] == "Reporte Financiero Q1" for doc in results)


def test_search_no_match_returns_empty_list(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/documents/search?q=documento-que-no-existe", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_search_combines_text_and_category_filter(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/documents",
        data={"title": "Politica de Vacaciones", "category": "rrhh"},
        files={"file": ("politica.pdf", b"contenido", "application/pdf")},
        headers=headers,
    )

    # Coincide el texto pero no la categoría -> no debe aparecer
    response = client.get("/documents/search?q=Politica&category=finanzas", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


# --- DELETE /documents/{id} -------------------------------------------------

def _upload_doc(client, headers, title="Doc para borrar", category="prueba"):
    response = client.post(
        "/documents",
        data={"title": title, "category": category},
        files={"file": ("archivo.pdf", b"contenido", "application/pdf")},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_delete_document_success(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    doc_id = _upload_doc(client, headers)

    response = client.delete(f"/documents/{doc_id}", headers=headers)
    assert response.status_code == 204

    # Confirmar que ya no existe en búsqueda
    search = client.get("/documents/search?q=Doc para borrar", headers=headers)
    assert not any(doc["id"] == doc_id for doc in search.json())


def test_delete_document_not_found(client):
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/documents/999999", headers=headers)
    assert response.status_code == 404


def test_delete_document_requires_auth(client):
    response = client.delete("/documents/1")
    assert response.status_code == 401


# --- Paginación (limit / offset) -------------------------------------------

def _upload_n_docs(client, headers, n: int, prefix: str = "PagDoc"):
    """Sube n documentos con títulos predecibles."""
    for i in range(n):
        client.post(
            "/documents",
            data={"title": f"{prefix} {i + 1}", "category": "paginacion"},
            files={"file": (f"doc{i}.pdf", b"contenido", "application/pdf")},
            headers=headers,
        )


def test_pagination_limit_reduces_results(client):
    """limit=2 sobre 5 docs debe devolver exactamente 2 resultados."""
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    _upload_n_docs(client, headers, 5, prefix="LimDoc")

    response = client.get("/documents/search?category=paginacion&limit=2", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_pagination_offset_skips_results(client):
    """offset igual al total de docs debe devolver lista vacía."""
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    _upload_n_docs(client, headers, 3, prefix="OffDoc")

    # Traemos todos para saber cuántos hay en la categoría
    all_docs = client.get("/documents/search?category=paginacion&limit=100", headers=headers).json()
    total = len(all_docs)

    response = client.get(f"/documents/search?category=paginacion&offset={total}", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_pagination_limit_out_of_range_rejected(client):
    """limit=0 y limit=101 deben rechazarse con 422."""
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get("/documents/search?limit=0", headers=headers).status_code == 422
    assert client.get("/documents/search?limit=101", headers=headers).status_code == 422


def test_pagination_negative_offset_rejected(client):
    """offset=-1 debe rechazarse con 422."""
    token = _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get("/documents/search?offset=-1", headers=headers).status_code == 422
