
import os

base_dir = "/home/user/overleaf_project"
chapters_dir = f"{base_dir}/chapters"
os.makedirs(chapters_dir, exist_ok=True)

# ============================================================
# 00_titlepage.tex
# ============================================================
titlepage = r"""
\begin{titlepage}
\begin{tikzpicture}[remember picture, overlay]
  % Hintergrund oben
  \fill[xsikomblue] (current page.north west) rectangle ([yshift=-8cm]current page.north east);
  % Hintergrund unten
  \fill[lightgray!50] (current page.south west) rectangle ([yshift=3cm]current page.south east);
  % Goldlinie
  \draw[xsikomgold, line width=3pt] 
    ([yshift=-8cm]current page.north west) -- ([yshift=-8cm]current page.north east);
\end{tikzpicture}

\vspace*{1.5cm}

{\centering
  {\color{white}\fontsize{14}{16}\selectfont\textbf{XSIKOM-PROJECTS}}\\[0.3cm]
  {\color{xsikomgold}\fontsize{11}{13}\selectfont Innovative IT Solutions \& Security}\\[2.5cm]
  
  {\color{white}\fontsize{28}{32}\selectfont\textbf{IT-Sicherheitslabor}}\\[0.4cm]
  {\color{white}\fontsize{20}{24}\selectfont\textbf{Projektdokumentation}}\\[0.4cm]
  {\color{xsikomgold}\fontsize{16}{18}\selectfont Version 2.0 --- April 2026}\\[3cm]
  
  \begin{tcolorbox}[
    colback=white,
    colframe=xsikomgold,
    width=12cm,
    arc=5pt,
    boxrule=1.5pt
  ]
  \centering
  \begin{tabular}{ll}
    \textbf{Projekt:}    & IT-Sicherheitslabor \\
    \textbf{Version:}    & 2.0 (2026-04-15) \\
    \textbf{Status:}     & \textcolor{accentgreen}{\textbf{Aktuell}} \\
    \textbf{Autor:}      & Xsikom-Projects \\
    \textbf{Klassif.:}   & \textcolor{accentred}{Vertraulich} \\
    \textbf{Nächste Rev.:} & Oktober 2026 \\
  \end{tabular}
  \end{tcolorbox}
  
  \vfill
  
  {\color{darkgray}\small IT-Fachtechniker Qualifizierung | Netzwerk \& Sicherheit}\\[0.3cm]
  {\color{darkgray}\small \faGlobe\ xsikom-projects.de \quad \faEnvelope\ info@xsikom-projects.de}
}
\end{titlepage}
\newpage
"""

with open(f"{chapters_dir}/00_titlepage.tex", "w", encoding="utf-8") as f:
    f.write(titlepage)

# ============================================================
# 01_toc.tex
# ============================================================
toc = r"""
\tableofcontents
\newpage
\listoffigures
\listoftables
\newpage
"""

with open(f"{chapters_dir}/01_toc.tex", "w", encoding="utf-8") as f:
    f.write(toc)

print("✅ 00_titlepage.tex + 01_toc.tex erstellt")
