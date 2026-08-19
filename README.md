# Phishing Log Analyzer

Streamlit-Webanwendung zur Analyse und Bewertung verdächtiger E-Mails.
Zusätzlich gibt es einen Desktop-Launcher, der dieselbe Web-App in einem nativen Fenster startet.

## Highlights

- Upload von `.eml`-Dateien oder Screenshots
- Analyse von Headern, Absenderdaten, Links und Anhängen
- Heuristisches Risk-Scoring mit klaren Warnsignalen
- Optionaler VirusTotal-Check fuer bekannte URLs, IPs und Dateien
- Light- und Dark-Mode mit sauberer Umschaltung
- JSON-Export fuer Reporting und Nachverfolgung

## Projektstruktur

- `app.py` - Streamlit-Entrypoint
- `desktop_app.py` - Desktop-Launcher fuer die lokale App
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

## Desktop

```bash
python desktop_app.py
```

Der Desktop-Launcher startet dieselbe Web-App lokal und öffnet sie in einem nativen Qt-Fenster. Damit bleibt die Website-Version unverändert, du bekommst aber eine echte Desktop-App.

## Optional

- Setze `VIRUSTOTAL_API_KEY`, um externe Reputation-Checks zu aktivieren.
- Fuer OCR von Screenshots muss Tesseract lokal installiert sein.

## Hinweis

Die App fuehrt nur eine automatisierte Sicherheitsbewertung durch und ersetzt keine manuelle Analyse.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/05d01e36-c8a0-45b1-a1f1-19123b98a894" />
