
# ============================================================
# KAPITEL 07 - Cloud-Sicherheit
# ============================================================
cap07 = r"""
\chapter{Cloud-Sicherheit: AWS und Azure}

\section{Shared Responsibility Model}

\begin{table}[H]
\centering
\caption{Shared Responsibility Model}
\begin{tabular}{|l|c|c|c|}
\hline
\rowcolor{primaryblue!20}
\textbf{Komponente} & \textbf{IaaS} & \textbf{PaaS} & \textbf{SaaS} \\
\hline
Daten & Kunde & Kunde & Kunde \\
\hline
Anwendungen & Kunde & Kunde & Anbieter \\
\hline
Runtime & Kunde & Anbieter & Anbieter \\
\hline
Middleware & Kunde & Anbieter & Anbieter \\
\hline
Betriebssystem & Kunde & Anbieter & Anbieter \\
\hline
Virtualisierung & Anbieter & Anbieter & Anbieter \\
\hline
Netzwerk/Storage & Anbieter & Anbieter & Anbieter \\
\hline
Physische Infrastruktur & Anbieter & Anbieter & Anbieter \\
\hline
\end{tabular}
\end{table}

\section{AWS Sicherheit mit Prowler}

\subsection{Prowler -- AWS Security Assessment}

\begin{lstlisting}[language=bash, caption=Prowler AWS Security Scan]
# Prowler installieren
pip3 install prowler

# AWS Credentials konfigurieren
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region: eu-central-1

# Vollstaendigen Scan starten
prowler aws

# Spezifische Checks
prowler aws --checks s3_bucket_public_access_block_enabled
prowler aws --checks iam_root_mfa_enabled
prowler aws --checks ec2_instance_imdsv2_enabled

# Compliance-Scan (CIS AWS Benchmark)
prowler aws --compliance cis_1.5_aws

# HTML-Report generieren
prowler aws -M html -o /tmp/prowler-report
\end{lstlisting}

\subsection{AWS IAM Best Practices}

\begin{lstlisting}[language=json, caption=AWS IAM Policy -- Least Privilege]
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEC2ReadOnly",
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:List*"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "eu-central-1"
        }
      }
    },
    {
      "Sid": "DenyRootActions",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:DeleteUser",
        "iam:AttachUserPolicy"
      ],
      "Resource": "*"
    }
  ]
}
\end{lstlisting}

\subsection{AWS CloudTrail und GuardDuty}

\begin{lstlisting}[language=bash, caption=AWS CloudTrail aktivieren]
# CloudTrail aktivieren
aws cloudtrail create-trail \
  --name lab-audit-trail \
  --s3-bucket-name lab-cloudtrail-logs \
  --include-global-service-events \
  --is-multi-region-trail \
  --enable-log-file-validation

aws cloudtrail start-logging --name lab-audit-trail

# GuardDuty aktivieren
aws guardduty create-detector --enable \
  --finding-publishing-frequency FIFTEEN_MINUTES

# GuardDuty Findings anzeigen
aws guardduty list-findings \
  --detector-id $(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)
\end{lstlisting}

\section{Azure Sicherheit mit Defender}

\subsection{Microsoft Defender for Cloud}

\begin{lstlisting}[language=bash, caption=Azure CLI -- Defender aktivieren]
# Azure CLI anmelden
az login

# Defender for Cloud aktivieren
az security pricing create \
  --name VirtualMachines \
  --tier Standard

az security pricing create \
  --name SqlServers \
  --tier Standard

az security pricing create \
  --name AppServices \
  --tier Standard

# Security Score anzeigen
az security secure-score list

# Empfehlungen anzeigen
az security task list --query "[].{Task:name, State:state}" -o table
\end{lstlisting}

\subsection{Azure Entra ID (ehem. Azure AD) Haertung}

\begin{lstlisting}[language=powershell, caption=Azure Entra ID Sicherheit]
# Azure PowerShell Modul
Install-Module -Name Az -AllowClobber -Force
Connect-AzAccount

# MFA fuer alle Benutzer erzwingen
$policy = Get-AzureADMSConditionalAccessPolicy
# Conditional Access Policy: MFA Required

# Privilegierte Rollen mit PIM
# Azure Portal -> Entra ID -> Privileged Identity Management
# -> Azure AD roles -> Assignments

# Risky Sign-ins analysieren
Get-AzureADAuditSignInLogs `
  -Filter "riskLevel eq 'high'" `
  -Top 50 | Select-Object UserDisplayName, IpAddress, Location
\end{lstlisting}

\section{Infrastructure as Code Sicherheit}

\subsection{Checkov -- IaC Security Scanner}

\begin{lstlisting}[language=bash, caption=Checkov IaC Scanning]
# Checkov installieren
pip3 install checkov

# Terraform scannen
checkov -d ./terraform/

# Kubernetes YAML scannen
checkov -d ./k8s/ --framework kubernetes

# Dockerfile scannen
checkov -f ./Dockerfile --framework dockerfile

# CI/CD Integration (GitHub Actions)
# - name: Run Checkov
#   uses: bridgecrewio/checkov-action@master
#   with:
#     directory: .
#     framework: terraform
#     soft_fail: false
\end{lstlisting}

\subsection{Terrascan -- Policy as Code}

\begin{lstlisting}[language=bash, caption=Terrascan fuer Terraform]
# Terrascan installieren
curl -L "https://github.com/tenable/terrascan/releases/latest/\
  download/terrascan_Linux_x86_64.tar.gz" | tar -xz
mv terrascan /usr/local/bin/

# Terraform-Code scannen
terrascan scan -t aws -i terraform -d ./terraform/

# Kubernetes-Manifeste scannen
terrascan scan -t k8s -i k8s -d ./k8s/

# Report generieren
terrascan scan -t aws -i terraform \
  -o json > terrascan_report.json
\end{lstlisting}

\begin{infobox}
  \textbf{Cloud Security Tipp:} Verwende immer das Prinzip der geringsten 
  Rechte (Least Privilege) fuer Cloud-IAM-Rollen und aktiviere MFA fuer 
  alle privilegierten Konten!
\end{infobox}
"""

with open(f"{chapters_dir}/07_cloud.tex", "w", encoding="utf-8") as f:
    f.write(cap07)
print("✅ 07_cloud.tex")
