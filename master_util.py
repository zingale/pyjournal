journal_master = r"""
\documentclass[11pt]{book}

% include figures
\usepackage{epsfig}

% prefer PDF to PNG
\DeclareGraphicsExtensions{%
  .pdf, .png}

% AMS symbols
\usepackage{amsmath,amssymb}

% cancel
\usepackage{cancel}

% Palatino font (and math symbols) -- looks nicer than the standard
% LaTeX font
\usepackage{mathpazo}

% san-serif font
\usepackage{helvet}

\usepackage{sectsty}

\allsectionsfont{\sffamily}

% URLs (special font for monospace)
\usepackage{inconsolata}
\usepackage[T1]{fontenc}

% geometry
\usepackage[margin=1in]{geometry}

% hyperlinks
\usepackage{hyperref}

% color package
\usepackage{color}

% custom hrule
\newcommand{\HRule}{\rule{\linewidth}{0.125mm}}

% skip a bit of space between paragraphs, to enhance readability
\usepackage{parskip}

% captions
\usepackage{caption}

\renewcommand{\captionfont}{\footnotesize}
\renewcommand{\captionlabelfont}{\footnotesize}
\setlength{\captionmargin}{3em}

\newcommand{\htag}[1]{{\tt \##1}}

\begin{document}

\frontmatter

\begin{titlepage}

\vskip 2in

\begin{center}
\ \\[2.5in]
{\Huge \textsf{\bfseries Research Journal}}
\end{center}

\vfill

\today

\end{titlepage}

\clearpage

\setcounter{tocdepth}{2}
\tableofcontents

\clearpage

\mainmatter

\input entries/chapters.tex

\end{document}
"""
