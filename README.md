# ContainerGuard AI

> **Multi-agent container security analysis, ready-to-apply remediation, contextual CVE triage, and executive-ready reporting.**

ContainerGuard AI was built and is orchestrated end-to-end in Airia AI. Airia AI coordinates the workflow's input, Claude Haiku 4.5 router, five model-backed specialist agents, built-in Python Docker Engine inventory node, user-specific memory, and final output. Together, these nodes transform Dockerfiles, vulnerability scans, SBOMs, runtime configuration, compliance questions, and CI/CD requirements into prioritized, copy-pastable security guidance. Historical trend and drift analysis is included when prior scan data is available.

## Try the Workflow

Want to test the published agent? **[Import and try ContainerGuard AI in the Airia AI Community](https://community.airia.ai/import-agent/ungc8ks9vj2JtFiXo7VOlCsBd3GCC3ghgW9TOjSJ48w)**.

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
- Docker Engine inventory through the built-in Python code node, with section-level error handling
- Memory-backed trends and configuration-drift detection
- Executive reporting with business impact and effort-versus-impact ranking

## Agents

| Component | Model | Role |
|---|---|---|
| Router | Claude Haiku 4.5 | Classifies the request and selects one of five routes |
| Agent 1 | Claude Haiku 4.5 | Dockerfile static analysis and ready-to-apply secure remediation |
| Agent 2 | GPT-4.1 | Enhanced CVE Hunter, SBOM/supply chain, runtime, and CI/CD |
| Agent 3 | GPT-4.1 | Focused CVE triage, attack paths, and remediation |
| Agent 4 | Claude Haiku 4.5 | Parallel focused CVE analysis and corroboration |
| Agent 5 | Claude Haiku 4.5 | Executive aggregation, trends, chain correlation, and action planning |

### Agent 1 — Dockerfile Static Analyzer

Returns a complete secure replacement in a strict five-part response: annotated rewrite; original-versus-secure comparison; build/tag/push commands; compatibility and migration guide; and testing checklist. It checks image pinning, root execution, stages, excess packages, `ADD`, unverified downloads, secrets, permissions, ports, and ownership.

### Agents 2–4 — CVE Hunters

Normalize CVEs and prioritize effective risk using exploitability, impact, container context, and business criticality. They identify attack chains and linchpin vulnerabilities, then provide exact upgrades, Dockerfile changes, commands, short-term mitigations, long-term fixes, and 1-hour/24-hour/7-day plans. Agent 2 provides SBOM, supply-chain, runtime-monitoring, and CI/CD capabilities. Agents 3 and 4 perform focused parallel analysis with different models.

### Agent 5 — Security Report Aggregator

Produces: Executive Summary; Current Risk Posture; Attack Chains; Historical Trend and Drift; Effort-versus-Impact Remediation Plan; Business and Compliance Narrative; Direct Leadership Answers; and a Seven-Day Plan with ownership hints.

## System Architecture

<p align="center">
  <a href="https://imgur.com/OoorMrF">
    <img src="https://i.imgur.com/OoorMrF.png" alt="Airia AI workflow with Input, Claude Haiku 4.5 Router, five AI agents, Python Docker scanner, user-specific memory, and Output" width="100%">
  </a>
</p>

<p align="center"><strong>Figure 1 — Container Security Agent Workflow</strong></p>

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
| Orchestration | Airia AI |
| Models | Claude Haiku 4.5 and GPT-4.1 |
| Code execution | Python 3 |
| Docker Engine inventory node | Docker SDK for Python using `docker.from_env()` against an engine reachable from the code runtime |
| Vulnerability scan inputs | Pasted Trivy or Grype text/JSON; these scanners are not shown as directly connected workflow nodes |
| SBOM inputs | Pasted SPDX, CycloneDX, or Syft JSON generated by tools such as Syft, Trivy, or Docker SBOM |
| Provenance | Cosign, in-toto, SLSA, Notation guidance |
| Runtime-monitoring output | Recommendations and generated guidance for Falco, Tracee, Tetragon, Sysdig, and eBPF |
| Policy output | Generated examples and recommendations for OPA/Rego, Kyverno, AppArmor, SELinux, and Seccomp |
| History | Airia AI user-specific memory |


## Setup and Testing

The complete workflow lives in Airia AI. There is no application repository to clone or local service to start.

1. **[Import and open the workflow in Airia AI](https://community.airia.ai/import-agent/ungc8ks9vj2JtFiXo7VOlCsBd3GCC3ghgW9TOjSJ48w).**
2. Choose one of the supported input options below.
3. Paste the input or prompt into the agent.
4. Review and validate the generated analysis before applying remediation.

Trivy, Grype, Syft, Docker, and Kubernetes are optional local tools used only to generate input for the workflow. They are not required for prompts that use pasted content or natural-language descriptions.

### Optional: Install Trivy to Generate CVE Scan Input

Skip this section if you already have Trivy output or plan to describe the vulnerability counts in plain language.

#### macOS

The official Homebrew installation is:

```bash
brew install trivy
trivy --version
```

If `brew` is not installed, install Homebrew from [brew.sh](https://brew.sh/) first, then run the commands above.

Generate text output to paste into Airia AI:

```bash
trivy image nginx:1.21
```

Generate JSON output to paste or upload:

```bash
trivy image nginx:1.21 --format json --output trivy-results.json
```

#### Windows PowerShell

Open **PowerShell** as your normal user and run this complete block. It downloads the latest official 64-bit Windows release of Trivy, extracts it under your user profile, adds that folder to your user PATH, and verifies the installation.

```powershell
$release = Invoke-RestMethod "https://api.github.com/repos/aquasecurity/trivy/releases/latest"
$asset = $release.assets |
  Where-Object { $_.name -match "Windows-64bit\.zip$" } |
  Select-Object -First 1

if (-not $asset) {
  throw "The latest Trivy release does not contain a Windows-64bit ZIP asset."
}

$installDir = Join-Path $env:LOCALAPPDATA "Programs\Trivy"
$zipPath = Join-Path $env:TEMP "trivy-windows-64bit.zip"

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $installDir -Force
Remove-Item $zipPath

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathEntries = @($userPath -split ";" | Where-Object { $_ })

if ($pathEntries -notcontains $installDir) {
  $newUserPath = ($pathEntries + $installDir) -join ";"
  [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
}

$env:Path = "$env:Path;$installDir"
trivy --version
```

Generate text output:

```powershell
trivy image nginx:1.21
```

Generate JSON output:

```powershell
trivy image nginx:1.21 --format json --output trivy-results.json
```

After the scan finishes, open the Airia AI workflow and either paste the terminal output, provide the JSON results, or describe the vulnerability totals.

For other operating systems and installation methods, use the [official Trivy installation guide](https://www.trivy.dev/docs/latest/getting-started/installation/).

## All Input Options for the Container Security Agent

### 1. Dockerfile Analysis

**What to input:**

```dockerfile
# Just paste your Dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
USER root
EXPOSE 80
CMD ["/bin/bash"]
```

**What the agent does:**

- Static security analysis
- Best-practice violation detection
- Copy-pastable remediation with a fixed Dockerfile and exact build commands

### 2. CVE Scan Results (Trivy/Grype)

**What to input:**

```text
# Paste output from:
trivy image nginx:1.21

# OR paste JSON from:
trivy image nginx:1.21 --format json

# OR just describe:
"I scanned nginx:1.21 and got 247 vulnerabilities, 12 CRITICAL, 45 HIGH"
```

**What the agent does:**

- AI-powered triage showing which five CVEs to fix first
- Exploitability scoring
- Attack-chain correlation
- Exact remediation steps

### 3. SBOM Files

**What to input:**

```text
# Paste an SBOM generated with:
syft nginx:latest -o json

# OR:
trivy sbom nginx:latest

# OR:
docker sbom nginx:latest

# Supported formats include SPDX, CycloneDX, and Syft JSON.
```

**What the agent does:**

- Supply-chain risk analysis
- License-compliance checking
- Dependency-confusion detection
- Provenance-verification guidance
- Component-to-CVE mapping

### 4. Runtime Configuration

**What to input:**

```text
# Paste output from:
docker inspect my-container

# OR:
kubectl get pod my-pod -o yaml

# OR describe:
"My container runs as root, has privileged mode, and mounts /var/run/docker.sock"
```

**What the agent does:**

- Runtime security assessment
- Falco-rule generation
- Privilege-escalation risk analysis
- AppArmor, SELinux, and Seccomp policy recommendations

### 5. CI/CD Pipeline Requests

**What to input:**

```text
"Create a GitHub Actions workflow for container security scanning"

"How do I add Trivy to my GitLab CI pipeline?"

"Generate a Jenkins pipeline that blocks builds with CRITICAL CVEs"

"I need a complete CI/CD security setup for Azure DevOps"
```

**What the agent does:**

- Copy-pastable pipeline YAML or configuration
- Security gates and thresholds
- Automated-remediation setup
- Policy-as-code examples

### 6. Compliance and Best Practices

**What to input:**

```text
"Check my setup against CIS Docker Benchmark"

"What are the NIST container security requirements?"

"Is my Kubernetes deployment PCI-DSS compliant?"

"Generate a security checklist for production containers"
```

**What the agent does:**

- Compliance gap analysis
- Benchmark mapping
- Remediation roadmap
- Policy templates

### 7. Natural-Language Queries

**What to input:**

```text
"Are any of my images vulnerable to Log4Shell?"

"What's the fastest way to scan 100 container images?"

"How do I detect container escape attempts in production?"

"Should I be worried about the latest nginx CVE?"

"Compare Trivy vs Grype vs Snyk - which should I use?"
```

**What the agent does:**

- Research and recommendations
- Tool comparisons
- Threat-intelligence guidance
- Strategic guidance

### 8. Mixed or Complex Scenarios

**What to input:**

```text
"Here's my Dockerfile [paste], my Trivy scan [paste], and my runtime config [paste].
Give me a complete security assessment."
```

**What the agent does:**

- Cross-layer correlation
- Attack-path visualization
- Comprehensive remediation planning
- Executive summary with business impact

### 9. Historical Analysis — Uses Memory

**What to input:**

```text
"How has my security posture changed over the last month?"

"Show me trends in my vulnerability counts"

"Am I getting better or worse at container security?"
```

**What the agent does:**

- Trend analysis using available memory
- Comparative insights
- Pattern recognition

If no prior scan data is available, the report establishes a baseline instead of inventing a trend.

### 10. Runtime Monitoring Setup

**What to input:**

```text
"Generate Falco rules for my production environment"

"How do I detect suspicious syscalls in containers?"

"Set up eBPF monitoring for container escapes"

"Create AppArmor/SELinux profiles for my app"
```

**What the agent does:**

- Custom Falco rules
- Falco, Tracee, and Tetragon recommendations
- Security-policy generation
- Deployment guidance

## Recommended Testing Workflow

### Start Simple

1. Paste a Dockerfile → see static analysis.
2. Run `trivy image nginx:latest` → paste the results → see AI triage.

### Then Advanced

3. Generate an SBOM with `syft nginx:latest -o json` → paste it → see supply-chain analysis.
4. Ask: `Create a GitHub Actions security workflow` → receive copy-pastable YAML.
5. Paste `docker inspect` output → receive a runtime security assessment.

### Go Complex

6. Combine a Dockerfile, Trivy scan, and runtime configuration → receive complete attack-path analysis.

## Quick Examples

```text
Create a complete CI/CD security pipeline for GitHub Actions.
Analyze this SBOM: [paste Syft output]
Generate Falco rules to detect container privilege escalation.
[Paste a Trivy scan with 200+ CVEs] Which should I fix first?
I run nginx:1.14 as root with host network mode. What are my risks?
```

## Python Scanner Code

The documented source for the Python Scripts node is available at [docker_engine_scanner.py](docker_engine_scanner.py). It is included for transparency; the node is already part of the Airia AI workflow, so users do not need to clone this repository or run the file to use the agent.

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

Each successfully collected entry includes normalized fields plus Docker SDK raw attributes. The node serializes the result as JSON for whichever downstream workflow nodes are connected to its output.

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
