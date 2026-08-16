"""
Airia AI Docker Engine inventory node.

High-level purpose
------------------
This code is used inside a Python Scripts node in the Airia AI Container
Security Agent workflow. It collects Docker Engine inventory and runtime
metadata, converts the result to JSON, and exposes that JSON through the
`output` variable for downstream workflow agents.

You do not need to clone this repository or run this file to use the published
Airia AI workflow. This repository copy exists only to document the code used
by that workflow node.

What the node does
------------------
1. Imports the Docker SDK for Python when it is available.
2. Connects to a Docker Engine using the SDK's standard environment-based
   configuration through `docker.from_env()`.
3. Calls `client.ping()` to verify that the engine is reachable.
4. Inventories:
   - local images, tags, sizes, creation values, and raw image attributes;
   - running and stopped containers, including image, state, labels, and ports;
   - Docker volumes, drivers, mount points, labels, and scope;
   - Docker networks, drivers, scope, internal/attachable/ingress flags, and
     labels; and
   - Docker daemon information returned by `client.info()`.
5. Converts datetime-like values safely so the final object can be serialized.
6. Returns section-level warnings when one inventory call fails while
   preserving data collected successfully from the other sections.
7. Serializes the complete result into the `output` JSON string expected by
   downstream Airia AI workflow nodes.

Runtime requirements and security
---------------------------------
- The Python runtime must have the `docker` package installed.
- A Docker Engine must be reachable from the environment in which this node
  executes. The code does not automatically connect Airia AI to a user's local
  Docker Desktop installation.
- `docker.from_env()` honors standard Docker SDK environment configuration,
  such as DOCKER_HOST and related TLS variables.
- Access to a Docker socket or Docker API is highly privileged and should be
  provided only in a trusted, appropriately protected execution environment.
- The result includes raw Docker object attributes and daemon information.
  Treat the JSON as potentially sensitive operational data.

Output behavior
---------------
- A successful connection sets `status` to `success` and
  `engine_available` to `true`.
- Missing Docker SDK or an unreachable engine returns a structured error.
- Individual inventory failures are appended to `warnings`.
- An unexpected top-level failure is caught and serialized rather than raised
  to downstream nodes.
"""

import json
from datetime import datetime

try:
    import docker
except ImportError:
    docker = None


def safe_dt(value):
    """Convert datetime-like values to ISO string safely."""
    if isinstance(value, datetime):
        return value.isoformat()
    try:
        return str(value) if value is not None else None
    except Exception:
        return None


def scan_docker():
    result = {
        "status": "unknown",
        "message": "",
        "engine_available": False,
        "connection_method": None,
        "error": None,
        "images": [],
        "containers": [],
        "volumes": [],
        "networks": [],
        "info": None,
    }

    if docker is None:
        result["status"] = "error"
        result["message"] = "python 'docker' package is not installed in the runtime environment."
        result["error"] = "MissingDependency"
        return result

    # Try to connect using default environment configuration
    try:
        client = docker.from_env()
        # Force a simple call to verify connectivity
        client.ping()
        result["engine_available"] = True
        result["connection_method"] = "from_env"
        result["status"] = "success"
        result["message"] = "Successfully connected to Docker Engine using docker.from_env()."
    except Exception as e:
        result["engine_available"] = False
        result["status"] = "error"
        result["message"] = "Unable to connect to Docker Engine using docker.from_env(). Ensure Docker is running and accessible from this environment."
        result["error"] = str(e)
        return result

    # If we are here, we have a valid client
    try:
        # Images
        images = []
        for img in client.images.list():
            attrs = getattr(img, "attrs", {}) or {}
            created = attrs.get("Created") or attrs.get("created")
            images.append(
                {
                    "id": getattr(img, "id", None) or attrs.get("Id"),
                    "short_id": getattr(img, "short_id", None),
                    "tags": getattr(img, "tags", []) or attrs.get("RepoTags", []),
                    "size": attrs.get("Size"),
                    "virtual_size": attrs.get("VirtualSize"),
                    "created": safe_dt(created),
                    "raw": attrs,
                }
            )
        result["images"] = images
    except Exception as e:
        result.setdefault("warnings", []).append(
            {"section": "images", "message": "Failed to list images", "error": str(e)}
        )

    try:
        # Containers
        containers = []
        for c in client.containers.list(all=True):
            attrs = getattr(c, "attrs", {}) or {}
            network_settings = attrs.get("NetworkSettings", {}) or {}
            ports = network_settings.get("Ports", {}) or {}
            containers.append(
                {
                    "id": getattr(c, "id", None) or attrs.get("Id"),
                    "short_id": getattr(c, "short_id", None),
                    "name": getattr(c, "name", None) or attrs.get("Name"),
                    "image": attrs.get("Config", {}).get("Image"),
                    "status": attrs.get("State", {}).get("Status") or getattr(c, "status", None),
                    "created": safe_dt(attrs.get("Created")),
                    "ports": ports,
                    "labels": attrs.get("Config", {}).get("Labels", {}),
                    "state": attrs.get("State", {}),
                    "raw": attrs,
                }
            )
        result["containers"] = containers
    except Exception as e:
        result.setdefault("warnings", []).append(
            {"section": "containers", "message": "Failed to list containers", "error": str(e)}
        )

    try:
        # Volumes
        volumes = []
        vol_data = client.volumes.list()
        for v in vol_data:
            attrs = getattr(v, "attrs", {}) or {}
            volumes.append(
                {
                    "name": getattr(v, "name", None) or attrs.get("Name"),
                    "driver": attrs.get("Driver"),
                    "mountpoint": attrs.get("Mountpoint"),
                    "labels": attrs.get("Labels", {}),
                    "scope": attrs.get("Scope"),
                    "raw": attrs,
                }
            )
        result["volumes"] = volumes
    except Exception as e:
        result.setdefault("warnings", []).append(
            {"section": "volumes", "message": "Failed to list volumes", "error": str(e)}
        )

    try:
        # Networks
        networks = []
        for n in client.networks.list():
            attrs = getattr(n, "attrs", {}) or {}
            networks.append(
                {
                    "id": getattr(n, "id", None) or attrs.get("Id"),
                    "name": getattr(n, "name", None) or attrs.get("Name"),
                    "driver": attrs.get("Driver"),
                    "scope": attrs.get("Scope"),
                    "internal": attrs.get("Internal"),
                    "attachable": attrs.get("Attachable"),
                    "ingress": attrs.get("Ingress"),
                    "labels": attrs.get("Labels", {}),
                    "raw": attrs,
                }
            )
        result["networks"] = networks
    except Exception as e:
        result.setdefault("warnings", []).append(
            {"section": "networks", "message": "Failed to list networks", "error": str(e)}
        )

    try:
        # Docker daemon info
        info = client.info()
        result["info"] = info
    except Exception as e:
        result.setdefault("warnings", []).append(
            {"section": "info", "message": "Failed to retrieve Docker daemon info", "error": str(e)}
        )

    return result


# Entry point for the Python Scripts node
try:
    scan_result = scan_docker()
except Exception as e:
    output = json.dumps(
        {
            "status": "error",
            "message": "Unexpected failure while scanning Docker Engine.",
            "error": str(e),
        }
    )
else:
    # Ensure JSON-serializable output for downstream agents
    output = json.dumps(scan_result, default=str)
