
# ============================================================
# KAPITEL 06 - Container-Sicherheit
# ============================================================
cap06 = r"""
\chapter{Container-Sicherheit: Docker und Kubernetes}

\section{Docker Hardening}

\subsection{Sichere Docker-Konfiguration}

\begin{lstlisting}[language=bash, caption=Docker Daemon Hardening]
# Docker Daemon sicher konfigurieren
cat > /etc/docker/daemon.json << EOF
{
  "icc": false,
  "userns-remap": "default",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "no-new-privileges": true,
  "live-restore": true,
  "userland-proxy": false,
  "seccomp-profile": "/etc/docker/seccomp-profile.json"
}
EOF

systemctl restart docker

# Docker Bench Security ausfuehren
docker run --rm --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /usr/bin/containerd:/usr/bin/containerd:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker/docker-bench-security
\end{lstlisting}

\subsection{Sichere Dockerfiles}

\begin{lstlisting}[language=docker, caption=Sicheres Dockerfile Beispiel]
# Schlechtes Beispiel (NICHT verwenden!)
# FROM ubuntu:latest
# RUN apt install -y python3
# CMD python3 app.py

# Gutes Beispiel -- Sicheres Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
# Nicht-root User erstellen
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --chown=appuser:appuser . .

# Read-only Filesystem
USER appuser
EXPOSE 8080

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
\end{lstlisting}

\section{Trivy -- Container Image Scanning}

\begin{lstlisting}[language=bash, caption=Trivy Image Scanning]
# Trivy installieren
apt install -y wget apt-transport-https gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | \
  gpg --dearmor > /usr/share/keyrings/trivy.gpg
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] \
  https://aquasecurity.github.io/trivy-repo/deb generic main" \
  > /etc/apt/sources.list.d/trivy.list
apt update && apt install -y trivy

# Image scannen
trivy image nginx:latest
trivy image --severity HIGH,CRITICAL python:3.12-slim

# Filesystem scannen
trivy fs /path/to/project

# IaC scannen (Dockerfile, K8s YAML)
trivy config ./k8s/

# CI/CD Integration
trivy image --exit-code 1 --severity CRITICAL myapp:latest
\end{lstlisting}

\section{K3s -- Leichtgewichtiges Kubernetes}

\subsection{K3s Installation}

\begin{lstlisting}[language=bash, caption=K3s Installation und Konfiguration]
# K3s Server installieren
curl -sfL https://get.k3s.io | sh -s - \
  --disable traefik \
  --disable servicelb \
  --write-kubeconfig-mode 644

# Status pruefen
systemctl status k3s
kubectl get nodes
kubectl get pods -A

# K3s Agent auf weiteren Nodes
K3S_TOKEN=$(cat /var/lib/rancher/k3s/server/node-token)
curl -sfL https://get.k3s.io | K3S_URL=https://10.0.50.10:6443 \
  K3S_TOKEN=$K3S_TOKEN sh -
\end{lstlisting}

\subsection{Kubernetes RBAC}

\begin{lstlisting}[language=yaml, caption=Kubernetes RBAC Konfiguration]
# ServiceAccount erstellen
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-serviceaccount
  namespace: production
---
# Role mit minimalen Rechten
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-serviceaccount
  namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
\end{lstlisting}

\section{Falco -- Runtime Security}

\begin{lstlisting}[language=bash, caption=Falco Installation und Regeln]
# Falco installieren
curl -fsSL https://falco.org/repo/falcosecurity-packages.asc | \
  gpg --dearmor -o /usr/share/keyrings/falco-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/falco-archive-keyring.gpg] \
  https://download.falco.org/packages/deb stable main" \
  > /etc/apt/sources.list.d/falcosecurity.list
apt update && apt install -y falco

# Falco starten
systemctl enable --now falco

# Eigene Regeln erstellen
cat >> /etc/falco/rules.d/custom_rules.yaml << EOF
- rule: Shell in Container
  desc: Erkennt Shell-Zugriff in Container
  condition: >
    spawned_process and container and
    proc.name in (shell_binaries)
  output: >
    Shell im Container gestartet
    (user=%user.name container=%container.name
    image=%container.image.repository proc=%proc.name)
  priority: WARNING
  tags: [container, shell, mitre_execution]
EOF

# Logs analysieren
journalctl -u falco -f
\end{lstlisting}

\section{Kyverno -- Policy Engine}

\begin{lstlisting}[language=bash, caption=Kyverno Policies]
# Kyverno installieren
kubectl create -f https://github.com/kyverno/kyverno/releases/download/\
  v1.11.0/install.yaml

# Policy: Keine privilegierten Container
cat << EOF | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-privileged
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Privilegierte Container sind nicht erlaubt!"
      pattern:
        spec:
          containers:
          - =(securityContext):
              =(privileged): "false"
EOF
\end{lstlisting}
"""

with open(f"{chapters_dir}/06_container.tex", "w", encoding="utf-8") as f:
    f.write(cap06)
print("✅ 06_container.tex")
