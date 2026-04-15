
import os

base_dir = "/home/user/overleaf_project"
chapters_dir = f"{base_dir}/chapters"
os.makedirs(chapters_dir, exist_ok=True)

# ============================================================
# KAPITEL 04 - Sicherheitstools
# ============================================================
cap04 = r"""
\chapter{Sicherheitstools und SIEM}

\section{Wazuh 4.7 -- SIEM und XDR}

Wazuh ist eine Open-Source-Sicherheitsplattform, die SIEM, XDR und SOAR-Funktionen vereint.

\subsection{Installation}

\begin{lstlisting}[language=bash, caption=Wazuh 4.7 All-in-One Installation]
# Wazuh Installer herunterladen
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.7/config.yml

# Konfiguration anpassen
nano config.yml
# nodes:
#   indexer:
#     - name: node-1
#       ip: 10.0.20.10
#   server:
#     - name: wazuh-1
#       ip: 10.0.20.10
#   dashboard:
#     - name: dashboard
#       ip: 10.0.20.10

# Installation starten
bash wazuh-install.sh -a

# Status pruefen
systemctl status wazuh-manager
systemctl status wazuh-indexer
systemctl status wazuh-dashboard
\end{lstlisting}

\subsection{Agenten-Deployment}

\begin{lstlisting}[language=bash, caption=Wazuh Agent auf Ubuntu deployen]
# Agent auf Ubuntu installieren
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --dearmor \
  -o /usr/share/keyrings/wazuh.gpg
echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] \
  https://packages.wazuh.com/4.x/apt/ stable main" \
  > /etc/apt/sources.list.d/wazuh.list
apt update && apt install -y wazuh-agent

# Agent konfigurieren
sed -i 's/MANAGER_IP/10.0.20.10/' /var/ossec/etc/ossec.conf

# Agent starten und registrieren
systemctl enable --now wazuh-agent
/var/ossec/bin/agent-auth -m 10.0.20.10
\end{lstlisting}

\begin{infobox}
  \textbf{Wazuh Dashboard:} Erreichbar unter \texttt{https://10.0.20.10} \\
  Standard-Login: \texttt{admin} / \texttt{SecurePassword123!}
\end{infobox}

\subsection{Eigene Regeln erstellen}

\begin{lstlisting}[language=xml, caption=Wazuh Custom Rules]
<!-- /var/ossec/etc/rules/local_rules.xml -->
<group name="custom,sshd,">
  <rule id="100001" level="10">
    <if_matched_sid>5716</if_matched_sid>
    <same_source_ip />
    <description>SSH Brute-Force: 5 Versuche von gleicher IP</description>
    <mitre>
      <id>T1110</id>
    </mitre>
    <group>authentication_failures,pci_dss_10.2.4,</group>
  </rule>
</group>
\end{lstlisting}

\section{OpenCTI 6.x -- Threat Intelligence}

\begin{lstlisting}[language=bash, caption=OpenCTI mit Docker Compose starten]
# Docker Compose herunterladen
git clone https://github.com/OpenCTI-Platform/docker.git opencti
cd opencti

# Umgebungsvariablen konfigurieren
cp .env.sample .env
nano .env
# OPENCTI_ADMIN_EMAIL=admin@lab.local
# OPENCTI_ADMIN_PASSWORD=SecurePass123!
# OPENCTI_ADMIN_TOKEN=$(uuidgen)
# MINIO_ROOT_USER=openctiuser
# MINIO_ROOT_PASSWORD=SecureMinioPass!

# Stack starten
docker compose up -d

# Status pruefen
docker compose ps
\end{lstlisting}

\section{MISP 2.4.x -- Malware Information Sharing}

\begin{lstlisting}[language=bash, caption=MISP Installation]
# MISP via Docker
git clone https://github.com/MISP/misp-docker.git
cd misp-docker
cp template.env .env
nano .env
# MISP_BASEURL=https://10.0.20.11
# MISP_ADMIN_EMAIL=admin@lab.local
# MISP_ADMIN_PASSPHRASE=SecurePass!

docker compose up -d

# MISP-OpenCTI Connector aktivieren
docker compose -f docker-compose-connectors.yml up -d connector-misp
\end{lstlisting}

\section{T-Pot 24.x Honeypot-Plattform}

\begin{lstlisting}[language=bash, caption=T-Pot 24.x Installation]
# Debian 12 Minimal als Basis
# Mindestanforderungen: 8 GB RAM, 128 GB SSD

# T-Pot herunterladen
git clone https://github.com/telekom-security/tpotce
cd tpotce

# Installation starten
sudo ./install.sh --type=standard

# Nach Neustart: Kibana Dashboard
# https://10.0.10.5:64297
# Benutzer: tsec / (gesetzt bei Installation)
\end{lstlisting}

\begin{warningbox}
  \textbf{Wichtig:} T-Pot MUSS im DMZ-VLAN (10.0.10.0/24) betrieben werden 
  und darf keinen Zugriff auf Produktionssysteme haben!
\end{warningbox}

\section{Coraza WAF mit OWASP CRS 4.x}

\begin{lstlisting}[language=bash, caption=Coraza WAF mit Nginx]
# Nginx + ModSecurity installieren
apt install -y nginx libnginx-mod-security2

# OWASP CRS 4.x herunterladen
git clone https://github.com/coreruleset/coreruleset /etc/nginx/modsec/crs
cp /etc/nginx/modsec/crs/crs-setup.conf.example \
   /etc/nginx/modsec/crs/crs-setup.conf

# ModSecurity Konfiguration
cat > /etc/nginx/modsec/main.conf << EOF
Include /etc/modsecurity/modsecurity.conf
Include /etc/nginx/modsec/crs/crs-setup.conf
Include /etc/nginx/modsec/crs/rules/*.conf
EOF

# Nginx Konfiguration
cat >> /etc/nginx/sites-available/default << EOF
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;
EOF

nginx -t && systemctl reload nginx
\end{lstlisting}

\section{Zeek 6.x Netzwerkanalyse}

\begin{lstlisting}[language=bash, caption=Zeek 6.x Installation und Konfiguration]
# Zeek installieren
echo 'deb http://download.opensuse.org/repositories/security:/zeek/\
  xUbuntu_22.04/ /' > /etc/apt/sources.list.d/zeek.list
apt update && apt install -y zeek-6.0

# Netzwerk-Interface konfigurieren
nano /opt/zeek/etc/node.cfg
# [zeek]
# type=standalone
# host=localhost
# interface=eth0

# Zeek starten
zeekctl deploy
zeekctl status

# Logs analysieren
tail -f /opt/zeek/logs/current/conn.log | zeek-cut id.orig_h id.resp_h proto
\end{lstlisting}
"""

with open(f"{chapters_dir}/04_sicherheitstools.tex", "w", encoding="utf-8") as f:
    f.write(cap04)
print("✅ 04_sicherheitstools.tex")
