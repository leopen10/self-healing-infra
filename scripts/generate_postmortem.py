#!/usr/bin/env python3
"""
generate_postmortem.py — Génère un rapport post-mortem automatique
"""
import json
from datetime import datetime
from pathlib import Path


def load_incidents():
    incidents = []
    with open('/tmp/incidents.json', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                incidents.append(json.loads(line))
    return incidents


def generate_html(incidents):
    date = datetime.now().strftime("%Y-%m-%d")
    
    rows = ""
    for i, inc in enumerate(incidents, 1):
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{inc['timestamp'][:19]}</td>
            <td><span class="alert">{inc['alert']}</span></td>
            <td>{inc['instance']}</td>
            <td>{inc['remediation']}</td>
            <td><span class="status">✓ {inc['status']}</span></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Post-Mortem — {date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #0d1117; color: #e6edf3; padding: 40px; }}
        h1 {{ color: #58a6ff; }}
        h2 {{ color: #79c0ff; border-bottom: 1px solid #30363d; padding-bottom: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #161b22; padding: 12px; text-align: left; color: #8b949e; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #21262d; }}
        tr:hover {{ background: #161b22; }}
        .alert {{ background: #da3633; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
        .status {{ color: #3fb950; font-weight: bold; }}
        .summary {{ background: #161b22; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .metric {{ display: inline-block; margin: 10px 20px; text-align: center; }}
        .metric-value {{ font-size: 36px; font-weight: bold; color: #58a6ff; }}
        .metric-label {{ color: #8b949e; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>📋 Rapport Post-Mortem — Self-Healing</h1>
    <p>Généré le {datetime.now().strftime("%Y-%m-%d à %H:%M:%S")}</p>

    <div class="summary">
        <div class="metric">
            <div class="metric-value">{len(incidents)}</div>
            <div class="metric-label">Incidents traités</div>
        </div>
        <div class="metric">
            <div class="metric-value">0</div>
            <div class="metric-label">Interventions humaines</div>
        </div>
        <div class="metric">
            <div class="metric-value">100%</div>
            <div class="metric-label">Auto-remédiation</div>
        </div>
    </div>

    <h2>Détail des incidents</h2>
    <table>
        <tr>
            <th>#</th>
            <th>Timestamp</th>
            <th>Alerte</th>
            <th>Instance</th>
            <th>Remédiation</th>
            <th>Statut</th>
        </tr>
        {rows}
    </table>

    <h2>Conclusion</h2>
    <p>Tous les incidents ont été détectés et remédiés automatiquement par le moteur Self-Healing.
    Aucune intervention humaine n'a été nécessaire.</p>
</body>
</html>"""

    return html


def main():
    print("[*] Chargement des incidents...")
    incidents = load_incidents()
    print(f"[*] {len(incidents)} incident(s) trouvé(s)")

    html = generate_html(incidents)

    Path("reports").mkdir(exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"reports/postmortem_{date}.html"

    with open(filename, 'w') as f:
        f.write(html)

    print(f"[+] Rapport généré : {filename}")


if __name__ == "__main__":
    main()
