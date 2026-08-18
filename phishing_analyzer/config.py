APP_NAME = "Phishing Log Analyzer"
APP_SUBTITLE = (
    "Internal phishing intake and reporting dashboard for suspicious emails, "
    "with header, link, attachment, and VirusTotal checks."
)

SUSPICIOUS_KEYWORDS = [
    "passwort",
    "password",
    "konto gesperrt",
    "account locked",
    "dringend",
    "urgent",
    "verify",
    "verifizieren",
    "login",
    "anmelden",
    "bestatigen",
    "confirm",
    "rechnung",
    "invoice",
    "zahlung",
    "payment",
    "aktualisieren",
    "update",
    "sicherheit",
    "security",
]

SUSPICIOUS_EXTENSIONS = {
    ".exe",
    ".scr",
    ".js",
    ".jse",
    ".vbs",
    ".vbe",
    ".wsf",
    ".ps1",
    ".psm1",
    ".bat",
    ".cmd",
    ".msi",
    ".lnk",
    ".iso",
    ".img",
    ".hta",
    ".jar",
    ".dll",
}

MACRO_EXTENSIONS = {".docm", ".xlsm", ".pptm"}
ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".gz", ".tar"}

URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly",
    "rebrand.ly",
    "ow.ly",
    "buff.ly",
}

SAFE_ACTION_HINTS = [
    "Use a sandbox for suspicious links",
    "Do not open risky attachments",
    "Escalate high-risk reports to SOC",
]

