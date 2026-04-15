
# ============================================================
# 02_einleitung.tex
# ============================================================
einleitung = r"""
\chapter{Einleitung und Projektübersicht}

\begin{newbox}
  \textbf{Version 2.0 -- April 2026:} Dieses Dokument wurde vollständig überarbeitet und 
  um neue Module erweitert: Container-Sicherheit, Cloud-Security, KI-gestützte Erkennung, 
  NIS2-Compliance und Red/Blue Team Operations.
\end{newbox}

\section{Projektziel}

Das IT-Sicherheitslabor dient als praxisorientierte Lernumgebung für die Qualifizierung 
zum \textbf{IT-Fachtechniker} mit Schwerpunkt Netzwerk- und Systemsicherheit. Es bietet:

\begin{itemize}[leftmargin=*]
  \item[\faCheckCircle] Realistische Angriffs- und Verteidigungsszenarien
  \item[\faCheckCircle] Hands-on Erfahrung mit aktuellen Sicherheitstools (2026)
  \item[\faCheckCircle] Vorbereitung auf Zertifizierungen (CompTIA Security+, CEH, OSCP)
  \item[\faCheckCircle] Compliance-Training (NIS2, ISO 27001, BSI IT-Grundschutz)
  \item[\faCheckCircle] Container- und Cloud-Sicherheit (Docker, K3s, AWS, Azure)
\end{itemize}

\section{Laborumgebung -- Überblick}

\begin{table}[H]
\centering
\caption{Laborkomponenten Übersicht}
\begin{tabularx}{\textwidth}{|l|X|l|}
\hline
\rowcolor{primaryblue!20}
\textbf{Komponente} & \textbf{Beschreibung} & \textbf{Status} \\
\hline
Hypervisor & Proxmox VE 8.x / VirtualBox 7.x & \textcolor{accentgreen}{Aktiv} \\
\hline
Firewall & OPNsense 24.x + Fortinet FortiGate & \textcolor{accentgreen}{Aktiv} \\
\hline
IDS/IPS & Suricata 7.x + Zeek 6.x & \textcolor{accentgreen}{Aktiv} \\
\hline
SIEM & Wazuh 4.7 + OpenCTI 6.x & \textcolor{accentgreen}{Aktiv} \\
\hline
Honeypot & T-Pot 24.x + Beelzebub AI & \textcolor{accentgreen}{Aktiv} \\
\hline
Pentest-OS & Kali Linux 2026.1 & \textcolor{accentgreen}{Aktiv} \\
\hline
Active Directory & Windows Server 2025 + Entra ID & \textcolor{accentgreen}{Aktiv} \\
\hline
Container & Docker 26.x + K3s (Kubernetes) & \textcolor{accentorange}{NEU} \\
\hline
Cloud & AWS + Azure (Sandbox) & \textcolor{accentorange}{NEU} \\
\hline
KI-Sicherheit & ML Anomalieerkennung + LLM & \textcolor{accentorange}{NEU} \\
\hline
\end{tabularx}
\end{table}

\section{Netzwerktopologie}

\begin{figure}[H]
\centering
\begin{tikzpicture}[
  node distance=1.5cm,
  box/.style={rectangle, rounded corners, draw=primaryblue, fill=primaryblue!10, 
               minimum width=2.8cm, minimum height=0.8cm, font=\small\bfseries},
  redbox/.style={rectangle, rounded corners, draw=accentred, fill=accentred!10,
                  minimum width=2.8cm, minimum height=0.8cm, font=\small\bfseries},
  greenbox/.style={rectangle, rounded corners, draw=accentgreen, fill=accentgreen!10,
                    minimum width=2.8cm, minimum height=0.8cm, font=\small\bfseries},
  arrow/.style={->, >=stealth, thick}
]

\node[redbox] (internet) {Internet};
\node[box, below=of internet] (fw) {OPNsense FW};
\node[box, below left=of fw] (dmz) {DMZ VLAN10};
\node[box, below=of fw] (mgmt) {Mgmt VLAN20};
\node[box, below right=of fw] (prod) {Prod VLAN30};
\node[greenbox, below=of dmz] (pentest) {Kali Linux};
\node[greenbox, below=of mgmt] (siem) {Wazuh SIEM};
\node[greenbox, below=of prod] (ad) {Win Server 2025};

\draw[arrow] (internet) -- (fw);
\draw[arrow] (fw) -- (dmz);
\draw[arrow] (fw) -- (mgmt);
\draw[arrow] (fw) -- (prod);
\draw[arrow] (dmz) -- (pentest);
\draw[arrow] (mgmt) -- (siem);
\draw[arrow] (prod) -- (ad);

\end{tikzpicture}
\caption{Vereinfachte Netzwerktopologie des IT-Sicherheitslabors}
\end{figure}

\section{Versionshistorie}

\begin{table}[H]
\centering
\caption{Versionshistorie}
\begin{tabular}{|l|l|p{8cm}|}
\hline
\rowcolor{primaryblue!20}
\textbf{Version} & \textbf{Datum} & \textbf{Änderungen} \\
\hline
1.0 & 2025-10-16 & Erstversion: Grundlabor, Netzwerk, IDS/IPS, AD \\
\hline
1.5 & 2026-01-10 & Honeypots, ELK-Stack, Forensik-Module \\
\hline
2.0 & 2026-04-15 & Container, Cloud, KI, NIS2, Red/Blue Team, 15+ neue Tools \\
\hline
\end{tabular}
\end{table}
"""

with open(f"{chapters_dir}/02_einleitung.tex", "w", encoding="utf-8") as f:
    f.write(einleitung)

print("✅ 02_einleitung.tex erstellt")
