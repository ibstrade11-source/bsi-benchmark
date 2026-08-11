from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src" / "bsi_benchmark"

GENERATORS = [
    "anthropic.py",
    "openai.py",
    "gemini.py",
    "groq.py",
    "deepseek.py",
    "openrouter.py",
    "gapgpt.py",
    "local.py",
    "bsi_api.py",
]

PROVIDERS = [
    "arxiv.py",
    "crossref.py",
    "openalex.py",
    "europepmc.py",
    "semantic_scholar.py",
]


def _imports_http_client(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "bsi_benchmark.network" and any(
                alias.name == "HttpClient" for alias in node.names
            ):
                return True
            if node.module == "bsi_benchmark.network.client" and any(
                alias.name == "HttpClient" for alias in node.names
            ):
                return True
    return False


def _contains_raw_http(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"requests", "httpx", "urllib.request"}:
                    violations.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module in {"requests", "httpx", "urllib.request"}:
                violations.append(node.module)

    return violations


def test_all_generators_use_central_http_client():
    generation = SRC / "generation"

    for filename in GENERATORS:
        path = generation / filename
        assert path.exists(), f"Missing generator: {path}"
        assert _imports_http_client(path), (
            f"{filename} does not import the centralized HttpClient"
        )
        assert not _contains_raw_http(path), (
            f"{filename} contains a direct HTTP library import"
        )


def test_all_providers_use_central_http_client():
    providers = SRC / "providers"

    for filename in PROVIDERS:
        path = providers / filename
        assert path.exists(), f"Missing provider: {path}"
        assert _imports_http_client(path), (
            f"{filename} does not import the centralized HttpClient"
        )
        assert not _contains_raw_http(path), (
            f"{filename} contains a direct HTTP library import"
        )


def test_raw_http_is_confined_to_network_client():
    allowed = SRC / "network" / "client.py"

    violations = []

    for path in SRC.rglob("*.py"):
        if path == allowed:
            continue
        if "__pycache__" in path.parts:
            continue

        raw = _contains_raw_http(path)
        if raw:
            violations.append(f"{path.relative_to(ROOT)}: {', '.join(raw)}")

    assert not violations, (
        "Direct HTTP implementations found outside network/client.py:\n"
        + "\n".join(violations)
    )


def test_central_http_client_exists():
    client = SRC / "network" / "client.py"
    retry = SRC / "network" / "retry.py"
    response = SRC / "network" / "response.py"

    assert client.exists()
    assert retry.exists()
    assert response.exists()
