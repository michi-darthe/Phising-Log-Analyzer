# Phishing Log Analyzer

Streamlit-Webanwendung fuer den internen Phishing-Log-Analyse- und Reporting-Workflow.

## Highlights

- Upload von `.eml`-Dateien oder Screenshots
- Analyse von Headern, Absenderdaten, Links und Anhängen
- Heuristisches Risk-Scoring mit klaren Warnsignalen
- Optionaler VirusTotal-Check fuer bekannte URLs, IPs und Dateien
- Light- und Dark-Mode mit sauberer Umschaltung
- JSON-Export fuer Reporting und Nachverfolgung

## Projektstruktur

- `app.py` - Streamlit-Entrypoint
- `phishing_analyzer/parsing.py` - E-Mail- und Bildanalyse
- `phishing_analyzer/scoring.py` - Risk-Scoring und Signale
- `phishing_analyzer/virustotal.py` - API-Aufrufe und Normalisierung
- `phishing_analyzer/theme.py` - Light/Dark CSS-Theme
- `phishing_analyzer/ui.py` - Layout, Karten, Tabellen und Export

## Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Optional

- Setze `VIRUSTOTAL_API_KEY`, um externe Reputation-Checks zu aktivieren.
- Fuer OCR von Screenshots muss Tesseract lokal installiert sein.

## Hinweis

Die App fuehrt nur eine Sicherheitsbewertung durch und ersetzt keine manuelle Analyse durch das Security-Team.
