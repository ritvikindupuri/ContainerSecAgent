# Enterprise Container Security Agent v5.00

> **Multi-agent container security analysis, one-click remediation, contextual CVE triage, and executive-ready reporting.**

Enterprise Container Security Agent is a published Airia workflow that transforms Dockerfiles, vulnerability scans, SBOMs, runtime configuration, compliance questions, and CI/CD requirements into prioritized, copy-pastable security guidance. A Claude Haiku 4.5 router selects a specialist path, five model-backed agents correlate evidence, a Python node inventories a live Docker Engine, and user-specific memory enables trend and drift analysis.

Version **5.00** is the current published workflow and includes the SBOM, supply-chain, runtime-monitoring, and CI/CD capabilities introduced in **v4.0**.

## Try the Workflow

Want to test the published agent? **[Import and try Enterprise Container Security Agent in the Airia Community](https://community.airia.ai/import-agent/ungc8ks9vj2JtFiXo7VOlCsBd3GCC3ghgW9TOjSJ48w)**.

> [View a complete sample report generated from a real Trivy scan](SAMPLE_OUTPUT_FROM_AGENT.md)

## Key Features

- Production-ready Dockerfile rewrites with before/after comparisons, commands, annotations, and migration guidance
- Bulk triage of 10–100+ CVEs into 1-hour, 24-hour, and next-sprint priorities
- Exploitability scoring using CVSS, EPSS when available, public-exploit evidence, runtime exposure, and business context
- Cross-layer attack-chain analysis with linchpin vulnerabilities and high-leverage chain breakers
- SPDX, CycloneDX, and Syft JSON SBOM analysis
- Dependency-confusion, typosquatting, provenance, SLSA, signing, and license checks
- Falco rules, eBPF strategies, and AppArmor, SELinux, and Seccomp guidance
- CI/CD templates for GitHub Actions, GitLab, Jenkins, CircleCI, and Azure DevOps
- CIS Docker, NIST, PCI-DSS, and production-container guidance
- Live Docker Engine inventory with section-level error handling
- Memory-backed trends and configuration-drift detection
- Executive reporting with business impact and effort-versus-impact ranking

## Agents

| Component | Model | Role |
|---|---|---|
| Router | Claude Haiku 4.5 | Classifies the request and selects one of five routes |
| Agent 1 | Claude Haiku 4.5 | Dockerfile static analysis and one-click secure remediation |
| Agent 2 | GPT-4.1 | Enhanced CVE Hunter, SBOM/supply chain, runtime, and CI/CD |
| Agent 3 | GPT-4.1 | Focused CVE triage, attack paths, and remediation |
| Agent 4 | Claude Haiku 4.5 | Parallel focused CVE analysis and corroboration |
| Agent 5 | Claude Haiku 4.5 | Executive aggregation, trends, chain correlation, and action planning |

### Agent 1 — Dockerfile Static Analyzer

Returns a complete secure replacement in a strict five-part response: annotated rewrite; original-versus-secure comparison; build/tag/push commands; compatibility and migration guide; and testing checklist. It checks image pinning, root execution, stages, excess packages, `ADD`, unverified downloads, secrets, permissions, ports, and ownership.

### Agents 2–4 — CVE Hunters

Normalize CVEs and prioritize effective risk using exploitability, impact, container context, and business criticality. They identify attack chains and linchpin vulnerabilities, then provide exact upgrades, Dockerfile changes, commands, short-term mitigations, long-term fixes, and 1-hour/24-hour/7-day plans. Agent 2 adds v4.0 SBOM, supply-chain, runtime, and CI/CD capabilities. Agents 3 and 4 perform focused parallel analysis with different models.

### Agent 5 — Security Report Aggregator

Produces: Executive Summary; Current Risk Posture; Attack Chains; Historical Trend and Drift; Effort-versus-Impact Remediation Plan; Business and Compliance Narrative; Direct Leadership Answers; and a Seven-Day Plan with ownership hints.

## System Architecture

<p align="center"><strong>Figure 1 — Published Airia Multi-Stage Container Security Workflow v5.00</strong></p>

<p align="center">
  <a href="https://imgur.com/OoorMrF">
    <img src="https://i.imgur.com/OoorMrF.png" alt="Airia workflow with Input, Claude Haiku 4.5 Router, five AI agents, Python Docker scanner, user-specific memory, and Output" width="100%">
  </a>
</p>

### Flow-by-Flow Explanation

1. **Input** — a Dockerfile, CVE scan, SBOM, runtime configuration, CI/CD request, compliance question, historical query, or mixed evidence enters the workflow.
2. **Router** — Claude Haiku 4.5 classifies the request and selects the relevant route.
3. **Dockerfile route** — Agent 1 creates a hardened Dockerfile with explanations, build commands, and migration steps.
4. **Enhanced CVE route** — Agent 2 performs contextual CVE analysis and relevant SBOM, supply-chain, runtime, or CI/CD work.
5. **Parallel CVE routes** — Agents 3 and 4 independently analyze vulnerability evidence using GPT-4.1 and Claude Haiku 4.5.
6. **Python route** — the code node uses `docker.from_env()` and `ping()`, then inventories images, containers, ports, states, volumes, networks, labels, and daemon information.
7. **Resilient collection** — section failures become warnings without discarding successful evidence; JSON is passed downstream.
8. **Aggregation** — Agent 5 correlates Dockerfile, CVE, SBOM, runtime, compliance, and historical findings.
9. **Memory** — user-specific scan history enables trend, drift, new-versus-fixed, and recurring-finding analysis.
10. **Output** — the workflow returns engineering remediation, executive risk translation, leadership answers, and a time-bucketed plan.

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Airia |
| Models | Claude Haiku 4.5 and GPT-4.1 |
| Code execution | Python 3 |
| Docker access | Docker SDK for Python and Docker Engine API |
| Vulnerability inputs | Trivy and Grype |
| SBOM | SPDX, CycloneDX, Syft, Trivy SBOM, Docker SBOM |
| Provenance | Cosign, in-toto, SLSA, Notation guidance |
| Runtime | Falco, Tracee, Tetragon, Sysdig, eBPF guidance |
| Policy | OPA/Rego, Kyverno, AppArmor, SELinux, Seccomp |
| History | Airia user-specific memory |

## Setup

The published workflow runs in Airia. Local tools generate inputs and give the Python node Docker Engine visibility.

### Clone and verify Docker

```bash
git clone https://github.com/ritvikindupuri/ContainerSecAgent.git
cd ContainerSecAgent
docker version
docker info
docker run --rm hello-world
```

### Python Docker scanner

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip docker
export DOCKER_HOST='unix:///var/run/docker.sock'
python -c 'import docker; c=docker.from_env(); print(c.ping()); print(c.version()["Version"])'
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip docker
python -c "import docker; c=docker.from_env(); print(c.ping()); print(c.version()['Version'])"
```

> Docker socket access is effectively administrative. Use it only in a trusted environment and never expose an unauthenticated Docker TCP endpoint.

### Trivy

```bash
trivy --version
trivy image nginx:1.21
trivy image nginx:1.21 --format json --output trivy-results.json
trivy image --format cyclonedx --output sbom.cdx.json nginx:1.21
```

### Syft and Grype

```bash
curl -sSfL https://get.anchore.io/syft | sh -s -- -b "$HOME/.local/bin"
curl -sSfL https://get.anchore.io/grype | sh -s -- -b "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
syft nginx:latest -o syft-json=sbom.syft.json
syft nginx:latest -o cyclonedx-json=sbom.cdx.json
syft nginx:latest -o spdx-json=sbom.spdx.json
grype nginx:1.21 -o json > grype-results.json
```

Review downloaded installation scripts before running them in production.

## All Input Options and Testing

### 1. Dockerfile Analysis

```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
USER root
EXPOSE 80
CMD ["/bin/bash"]
```

Returns static analysis, violations, and a one-click secure Dockerfile.

### 2. CVE Scan Results (Trivy/Grype)

```bash
trivy image nginx:1.21
trivy image nginx:1.21 --format json
```

```text
I scanned nginx:1.21 and got 247 vulnerabilities, 12 CRITICAL, 45 HIGH. Which five should I fix first?
```

Returns AI triage, exploitability scoring, attack chains, and exact remediation.

### 3. SBOM Files — New in v4.0

```bash
syft nginx:latest -o syft-json
trivy image --format cyclonedx nginx:latest
docker sbom nginx:latest
```

```text
Analyze this SBOM for vulnerable and transitive dependencies, dependency confusion, typosquatting, license risk, and missing provenance. Map components to CVEs and provide verification commands: [paste SBOM]
```

### 4. Runtime Configuration — New in v4.0

```bash
docker inspect my-container
kubectl get pod my-pod -o yaml
```

```text
My container runs as root, has privileged mode, and mounts /var/run/docker.sock. Assess the attack paths and give me exact hardening changes.
```

Returns runtime assessment, Falco rules, privilege-escalation analysis, and AppArmor/SELinux/Seccomp guidance.

### 5. CI/CD Requests — New in v4.0

```text
Create a GitHub Actions workflow for container security scanning.
How do I add Trivy to my GitLab CI pipeline?
Generate a Jenkins pipeline that blocks builds with CRITICAL CVEs.
I need a complete CI/CD security setup for Azure DevOps.
```

Returns copy-pastable configuration, security gates, remediation automation, and policy-as-code.

### 6. Compliance and Best Practices

```text
Check my setup against the CIS Docker Benchmark.
What are the NIST container security requirements?
Is my Kubernetes deployment PCI-DSS compliant?
Generate a security checklist for production containers.
```

### 7. Natural-Language Queries

```text
Are any of my images vulnerable to Log4Shell?
What's the fastest way to scan 100 container images?
How do I detect container escape attempts in production?
Should I be worried about the latest nginx CVE?
Compare Trivy vs Grype vs Snyk—which should I use?
```

### 8. Mixed and Complex Scenarios

```text
Here's my Dockerfile: [paste]. Here's my Trivy scan: [paste]. Here's my runtime configuration: [paste]. Give me a complete cross-layer security assessment, attack paths, remediation plan, and executive summary.
```

### 9. Historical Analysis

```text
How has my security posture changed over the last month?
Show me trends in my vulnerability counts.
Am I getting better or worse at container security?
```

Memory provides comparative metrics when history exists; otherwise the report establishes a baseline.

### 10. Runtime Monitoring — New in v4.0

```text
Generate Falco rules for my production environment.
How do I detect suspicious syscalls in containers?
Set up eBPF monitoring for container escapes.
Create AppArmor and SELinux profiles for my app.
```

## Recommended Testing Workflow

1. Paste a Dockerfile and inspect the secure rewrite.
2. Run `trivy image nginx:latest`, paste it, and review AI triage.
3. Run `syft nginx:latest -o syft-json`, paste it, and review supply-chain analysis.
4. Ask: `Create a GitHub Actions workflow for container security scanning.`
5. Paste `docker inspect` output and review the runtime assessment.
6. Combine Dockerfile + Trivy + SBOM + runtime data for a complete attack-path and executive report.

## Quick Examples

```text
Create a complete CI/CD security pipeline for GitHub Actions.
Analyze this SBOM: [paste Syft output]
Generate Falco rules to detect container privilege escalation.
[Paste a Trivy scan with 200+ CVEs] Which should I fix first?
I run nginx:1.14 as root with host network mode. What are my risks?
```

## Python Scanner Output

```json
{
  "status": "success",
  "message": "Successfully connected to Docker Engine using docker.from_env().",
  "engine_available": true,
  "connection_method": "from_env",
  "error": null,
  "images": [],
  "containers": [],
  "volumes": [],
  "networks": [],
  "info": {},
  "warnings": []
}
```

Each entry includes normalized fields plus Docker SDK raw attributes for downstream analysis.

## Security Considerations

- Docker socket access is administrative access to the host.
- Prefer read-only inputs and never paste secrets into prompts or reports.
- Verify AI-generated fixes and test rebuilt images before production.
- Validate current CVE exploit and patch status with authoritative sources.
- Use pinned, supported images and reproducible digests where practical.
- Sign images and verify provenance before deployment.

## Sample Output

See [Sample Output from Agent](SAMPLE_OUTPUT_FROM_AGENT.md) for an end-to-end report from a real Trivy scan of an end-of-life Node/Debian image.

## License

Add the chosen license in a `LICENSE` file before distribution.
