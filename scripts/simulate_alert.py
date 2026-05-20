#!/usr/bin/env python3
"""
simulate_alert.py — Simule une alerte Prometheus pour tester le moteur
"""
import requests
import json
from datetime import datetime


def simulate_alert(alert_name, instance, status="firing"):
    """Simule une alerte Prometheus vers le moteur de décision."""
    
    payload = {
        "alerts": [
            {
                "status": status,
                "labels": {
                    "alertname": alert_name,
                    "instance": instance,
                    "severity": "warning"
                },
                "annotations": {
                    "summary": f"Test alerte {alert_name}",
                    "description": f"Simulation d'alerte sur {instance}"
                },
                "startsAt": datetime.now().isoformat()
            }
        ]
    }

    try:
        response = requests.post(
            'http://localhost:5002',
            json=payload,
            timeout=5
        )
        print(f"[✓] Alerte {alert_name} envoyée → réponse : {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[!] Moteur non démarré — lance d'abord decision_engine.py")


def main():
    print("=" * 50)
    print("SIMULATION D'ALERTES — SELF-HEALING TEST")
    print("=" * 50)

    alertes = [
        ("DiskSpaceLow", "192.168.1.40:9100"),
        ("HighMemoryUsage", "192.168.1.40:9100"),
        ("HighCPUUsage", "localhost:9100"),
        ("InstanceDown", "192.168.1.41:9100"),
    ]

    for alert_name, instance in alertes:
        simulate_alert(alert_name, instance)

    print("=" * 50)
    print("Vérifie les logs : cat /tmp/self_healing.log")
    print("Vérifie les incidents : cat /tmp/incidents.json")


if __name__ == "__main__":
    main()
