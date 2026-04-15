
import os
import zipfile

# ============================================================
# IT-Sicherheitslabor - Overleaf LaTeX Projekt
# Alle Dateien zusammen für Overleaf
# ============================================================

base_dir = "/home/user/overleaf_project"
os.makedirs(base_dir, exist_ok=True)

# ============================================================
# 1. main.tex - Hauptdatei
# ============================================================
main_tex = r"""
\documentclass[12pt,a4paper]{report}

% ---- Pakete ----
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{tcolorbox}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{mdframed}
\usepackage{fontawesome5}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{microtype}
\usepackage{setspace}
\usepackage{float}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{tabularx}
\usepackage{pdfpages}
\usepackage{appendix}
\usepackage{glossaries}
\usepackage{makeidx}
\usepackage{tocbibind}
\usepackage{parskip}

\pgfplotsset{compat=1.18}
\usetikzlibrary{shapes,arrows,positioning,fit,calc}

% ---- Seitenränder ----
\geometry{
  top=2.5cm,
  bottom=2.5cm,
  left=3cm,
  right=2.5cm
}

% ---- Farben ----
\definecolor{primaryblue}{RGB}{0,82,147}
\definecolor{secondaryblue}{RGB}{0,120,215}
\definecolor{accentred}{RGB}{200,30,30}
\definecolor{accentgreen}{RGB}{0,150,80}
\definecolor{accentorange}{RGB}{230,120,0}
\definecolor{lightgray}{RGB}{245,245,245}
\definecolor{darkgray}{RGB}{60,60,60}
\definecolor{codebg}{RGB}{30,30,30}
\definecolor{codetext}{RGB}{220,220,220}
\definecolor{xsikomblue}{RGB}{10,60,130}
\definecolor{xsikomgold}{RGB}{200,160,0}

% ---- Hyperref ----
\hypersetup{
  colorlinks=true,
  linkcolor=primaryblue,
  urlcolor=secondaryblue,
  citecolor=accentgreen,
  pdftitle={IT-Sicherheitslabor Dokumentation v2.0},
  pdfauthor={Xsikom-Projects},
  pdfsubject={IT-Sicherheit, Netzwerk, Penetration Testing},
  pdfkeywords={IT-Sicherheit, Labor, Netzwerk, Forensik, Pentesting}
}

% ---- Code-Listing Stil ----
\lstdefinestyle{bashstyle}{
  backgroundcolor=\color{codebg},
  basicstyle=\ttfamily\footnotesize\color{codetext},
  breaklines=true,
  breakatwhitespace=true,
  captionpos=b,
  commentstyle=\color{accentgreen},
  keywordstyle=\color{secondaryblue}\bfseries,
  stringstyle=\color{accentorange},
  numberstyle=\tiny\color{gray},
  numbers=left,
  numbersep=8pt,
  frame=single,
  framesep=5pt,
  rulecolor=\color{darkgray},
  tabsize=2,
  showstringspaces=false,
  xleftmargin=15pt,
  xrightmargin=5pt,
}

\lstdefinestyle{yamlstyle}{
  backgroundcolor=\color{lightgray},
  basicstyle=\ttfamily\footnotesize\color{darkgray},
  breaklines=true,
  frame=single,
  rulecolor=\color{primaryblue},
  numbers=left,
  numberstyle=\tiny\color{gray},
  tabsize=2,
  showstringspaces=false,
}

\lstset{style=bashstyle}

% ---- Header/Footer ----
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primaryblue}{\small\textbf{IT-Sicherheitslabor v2.0}}}
\fancyhead[R]{\textcolor{darkgray}{\small Xsikom-Projects | April 2026}}
\fancyfoot[C]{\textcolor{darkgray}{\thepage}}
\fancyfoot[R]{\textcolor{lightgray}{\small\textit{Vertraulich}}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.2pt}

% ---- Kapitelformat ----
\titleformat{\chapter}[block]
  {\normalfont\huge\bfseries\color{primaryblue}}
  {\thechapter.}{20pt}{\huge}
\titleformat{\section}
  {\normalfont\Large\bfseries\color{secondaryblue}}
  {\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{darkgray}}
  {\thesubsection}{1em}{}

% ---- Infoboxen ----
\tcbuselibrary{skins,breakable}
\newtcolorbox{infobox}[1][]{
  colback=secondaryblue!10,
  colframe=secondaryblue,
  fonttitle=\bfseries,
  title={\faInfoCircle\ Information},
  #1
}
\newtcolorbox{warnbox}[1][]{
  colback=accentred!10,
  colframe=accentred,
  fonttitle=\bfseries,
  title={\faExclamationTriangle\ Warnung},
  #1
}
\newtcolorbox{tipbox}[1][]{
  colback=accentgreen!10,
  colframe=accentgreen,
  fonttitle=\bfseries,
  title={\faLightbulb\ Tipp},
  #1
}
\newtcolorbox{newbox}[1][]{
  colback=xsikomgold!15,
  colframe=xsikomgold,
  fonttitle=\bfseries,
  title={\faStar\ NEU in v2.0},
  #1
}

% ---- Glossar ----
\makeglossaries
\makeindex

% ---- Abkürzungen ----
\newacronym{cia}{CIA}{Confidentiality, Integrity, Availability}
\newacronym{ids}{IDS}{Intrusion Detection System}
\newacronym{ips}{IPS}{Intrusion Prevention System}
\newacronym{siem}{SIEM}{Security Information and Event Management}
\newacronym{apt}{APT}{Advanced Persistent Threat}
\newacronym{waf}{WAF}{Web Application Firewall}
\newacronym{vpn}{VPN}{Virtual Private Network}
\newacronym{iam}{IAM}{Identity and Access Management}
\newacronym{soc}{SOC}{Security Operations Center}
\newacronym{cve}{CVE}{Common Vulnerabilities and Exposures}
\newacronym{cvss}{CVSS}{Common Vulnerability Scoring System}
\newacronym{mitre}{MITRE}{MITRE ATT\&CK Framework}

% ============================================================
\begin{document}
% ============================================================

\include{chapters/00_titlepage}
\include{chapters/01_toc}
\include{chapters/02_einleitung}
\include{chapters/03_netzwerk}
\include{chapters/04_sicherheitstools}
\include{chapters/05_angriffe}
\include{chapters/06_container}
\include{chapters/07_cloud}
\include{chapters/08_ki_sicherheit}
\include{chapters/09_forensik}
\include{chapters/10_wartung}
\include{chapters/11_compliance}
\include{chapters/12_schulung}
\include{chapters/13_anhang}

\printglossaries
\printindex

\end{document}
"""

with open(f"{base_dir}/main.tex", "w", encoding="utf-8") as f:
    f.write(main_tex)

print("✅ main.tex erstellt")
