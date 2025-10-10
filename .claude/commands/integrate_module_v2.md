# 🧠 CLAUDE MODULE INGESTION COMMAND (Refined Version)

This document defines the refined ingestion process for integrating new standalone modules into the Clio Automation Toolkit ecosystem.

---

## 🎯 Purpose

To integrate independently developed Clio modules (e.g., `custom_fields_manager_app`, `billables_insight_service`, `notes_analyzer`) into a unified backend architecture — **without a monorepo** — while maintaining shared intelligence, gRPC interoperability, and Assistant discovery.

---

## 🧩 Core Principles

- **Polyrepo Architecture** — Each app evolves independently.
- **Dynamic Integration** — Modules register themselves automatically.
- **Single Intelligence Layer** — The OpenAI Assistant (via the Intelligence Service) interprets natural-language automation intents.
- **Consistent Protocol Contracts** — All domain logic exposed via gRPC, REST, and CLI.

---

## ⚙️ CLAUDE MODULE INGESTION COMMAND (v2)

### 1. **Audit Module Structure**
- Scan all `.py` files recursively.
- Identify:
  - Functions with side effects or data transformations.
  - Classes implementing domain logic or Clio API calls.
- Exclude:
  - `tests/`, `ui/`, and already shared utilities.
- Parse `pyproject.toml` to detect dependencies.
- Ensure all public functions are type-hinted.

🧩 *Output:* A summary of valid service candidates with dependency tree.

---

### 2. **Module Manifest Validation**

Each module **must include** a manifest file: `module_manifest.yaml`.

Example:
```yaml
domain: custom_fields
intents:
  - sync_custom_fields
  - update_custom_field_value
resources:
  - clio.CustomField
  - clio.Matter
version: 1.0.0
description: Manages custom fields and synchronizes values between Clio and external data sources.
```

🧠 The ingestion command will:
- Validate schema.
- Use `domain` to namespace gRPC and REST routes.
- Register `intents` with the Intelligence Service.
- Tag routes with OpenAPI `x-tagGroup`.

---

### 3. **gRPC Service Conversion**

- Create `.proto` definition under `/protos/<domain_name>.proto`
- Use `proto_package = "clio.<domain>"`
- Compile with `buf` or `grpc_tools` into `/generated/`
- Implement `servicer.py` from the extracted functional core

Example proto header:
```proto
syntax = "proto3";
package clio.custom_fields;
option python_package = "generated.clio.custom_fields";

service CustomFieldsService {
  rpc SyncCustomFields (SyncRequest) returns (SyncResponse);
}
```

---

### 4. **Intelligence Service Function Registration**

For each public function:
- Define OpenAI-compatible JSON Schema.
- Add metadata to `services/intelligence_service/app/functions/<domain_name>.py`.

Example YAML entry:
```yaml
- name: update_custom_field
  domain: custom_fields
  intent: UPDATE
  resource: CustomField
  description: Updates a Clio custom field for a given matter.
  examples:
    - "update 'Matter Stage' to 'Closed'"
    - "change client phone number field"
```

🧠 Auto-generate embeddings for `examples` (via ChromaDB or embeddings API) for faster intent routing.

---

### 5. **FastAPI Wiring**

Auto-generate a REST proxy from the gRPC definitions.

Example factory:
```python
from fastapi import APIRouter
from generated.clio.custom_fields import CustomFieldsServiceStub

def domain_router_factory(domain_name, grpc_stub):
    router = APIRouter(prefix=f"/{domain_name}", tags=[domain_name])
    # Proxy example
    @router.post("/sync")
    async def sync_custom_fields(request: dict):
        return await grpc_stub.SyncCustomFields(request)
    return router
```

Register router dynamically in the main app.

---

### 6. **CLI Command Registration**

Each module exposes a CLI group (via Click or Typer).

Example `pyproject.toml` entry point:
```toml
[project.entry-points."clio.modules"]
custom_fields = "custom_fields_manager.service:register"
```

At runtime:
```python
import pkg_resources
for entry_point in pkg_resources.iter_entry_points("clio.modules"):
    module = entry_point.load()
    module.register(grpc_server, fastapi_app, assistant_service)
```

This enables auto-discovery without monorepo coupling.

---

### 7. **Reuse & Deduplication**

- Compare module utilities against `/shared/utils.py`
- Maintain `shared-fingerprint.json` with content hashes.
- If overlap detected → relocate shared logic to `/shared/`.

---

### 8. **Function Mapping (for Assistant Discovery)**

Maintain a global map: `services/intelligence_service/app/function_map.yaml`

Example:
```yaml
- name: sync_custom_fields
  intent: SYNC
  domain: custom_fields
  resource: CustomField
  proto: clio.custom_fields.CustomFieldsService.SyncCustomFields
  cli_command: custom-fields sync
```

This file is the single source of truth for:
- Intent routing
- Domain association
- Tool registration

---

### 9. **Optional Enhancements**
- Auto-generate test scaffolds (`pytest + grpc.aio`)
- Auto-generate TypeScript SDK via OpenAPI
- Create `module_summary.json` for CI/CD ingestion

---

## 🧱 Summary Architecture

**Each module** exposes:
```
/module_root/
 ├── module_manifest.yaml
 ├── service.py
 ├── servicer.py
 ├── protos/
 │    └── <domain>.proto
 ├── cli/
 │    └── main.py
 ├── shared/
 └── tests/
```

All modules integrate through:
- gRPC server
- REST proxy (FastAPI)
- Assistant Intelligence Service
- CLI runtime

---

## ✅ Outcome

This refined design ensures:
- **Independent module evolution**
- **Seamless backend integration**
- **Shared intelligence and discovery**
- **gRPC + REST + CLI parity**
- **No monorepo dependency**

---
© 2025 Clio Automation Toolkit — Modular Intelligence Framework
