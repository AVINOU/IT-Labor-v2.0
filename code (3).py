
# ============================================================
# 03_netzwerk.tex
# ============================================================
netzwerk = r"""
\chapter{Netzwerkarchitektur und Konfiguration}

\section{IP-Adressplan}

\begin{table}[H]
\centering
\caption{VLAN- und IP-Adressplan}
\begin{tabular}{|l|l|l|l|p{4cm}|}
\hline
\rowcolor{primaryblue!20}
\textbf{VLAN} & \textbf{Name} & \textbf{Subnetz} & \textbf{Gateway} & \textbf{Dienste} \\
\hline
10 & DMZ & 10.0.10.0/24 & 10.0.10.1 & Webserver, Honeypot \\
\hline
20 & Management & 10.0.20.0/24 & 10.0.20.1 & SIEM, Monitoring \\
\hline
30 & Produktion & 10.0.30.0/24 & 10.0.30.1 & AD, Fileserver \\
\hline
40 & Pentest & 10.0.40.0/24 & 10.0.40.1 & Kali, Angriffssysteme \\
\hline
50 & Container & 10.0.50.0/24 & 10.0.50.1 & Docker, K3s \\
\hline
60 & Cloud-GW & 10.0.60.0/24 & 10.0.60.1 & VPN zu AWS/Azure \\
\hline
99 & Quarantäne & 10.0.99.0/24 & 10.0.99.1 & Isolierte Systeme \\
\hline
\end{tabular}
\end{table}

\section{OPNsense Firewall Konfiguration}

\begin{lstlisting}[language=bash, caption=OPNsense Grundkonfiguration via CLI]
# OPNsense Konsole -- Grundeinrichtung
# 1. Interface-Zuweisung
set interfaces wan em0
set interfaces lan em1
set interfaces opt1 em2  # DMZ

# 2. IP-Adressen setzen
set interfaces lan ipv4 address 10.0.20.1/24
set interfaces opt1 ipv4 address 10.0.10.1/24

# 3. Firewall-Regeln via opnsense-shell
opnsense-shell firewall add rule \
  --interface lan \
  --action block \
  --source 10.0.40.0/24 \
  --destination 10.0.30.0/24 \
  --description "Pentest-VLAN blockiert Prod"
\end{lstlisting}

\section{WireGuard VPN Einrichtung}

\begin{lstlisting}[language=bash, caption=WireGuard VPN Server Setup]
# WireGuard installieren
apt install -y wireguard

# Schluessel generieren
wg genkey | tee /etc/wireguard/server_private.key | \
  wg pubkey > /etc/wireguard/server_public.key

# Konfiguration erstellen
cat > /etc/wireguard/wg0.conf << EOF
[Interface]
Address = 10.200.0.1/24
ListenPort = 51820
PrivateKey = $(cat /etc/wireguard/server_private.key)
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT

[Peer]
PublicKey = <CLIENT_PUBLIC_KEY>
AllowedIPs = 10.200.0.2/32
EOF

# Dienst starten
systemctl enable --now wg-quick@wg0
\end{lstlisting}

\begin{infobox}
  \textbf{Zero Trust Netzwerk:} Ab Version 2.0 wird das Zero-Trust-Prinzip 
  umgesetzt: Kein Gerät wird automatisch vertraut -- jede Verbindung wird 
  authentifiziert, autorisiert und verschlüsselt.
\end{infobox}

\section{Suricata 7.x IDS/IPS}

\begin{lstlisting}[language=bash, caption=Suricata 7.x Installation und Konfiguration]
# Suricata 7.x installieren
add-apt-repository ppa:oisf/suricata-stable
apt update && apt install -y suricata

# Konfiguration anpassen
nano /etc/suricata/suricata.yaml
# HOME_NET: "[10.0.0.0/8]"
# af-packet: interface: eth0
# outputs: eve-log: enabled: yes

# Regeln aktualisieren (inkl. ET Pro)
suricata-update
suricata-update list-sources
suricata-update enable-source et/open
suricata-update enable-source ptresearch/attackdetection

# Suricata starten
systemctl enable --now suricata

# Live-Logs
tail -f /var/log/suricata/eve.json | jq .
\end{lstlisting}
"""

with open(f"{chapters_dir}/03_netzwerk.tex", "w", encoding="utf-8") as f:
    f.write(netzwerk)

print("✅ 03_netzwerk.tex erstellt")
