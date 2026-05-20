#!/usr/bin/env python3
"""
decision_engine.py — Moteur de décision Self-Healing
Reçoit les alertes et décide quelle remédiation lancer
"""
import json
import subprocess
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(
    filename='/tmp/self_healing.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Catalogue des remediations disponibles
REMEDIATION_CATALOG = {
    'DiskSpaceLow': {
        'description': 'Nettoyage automatique du disque',
        'playbook': 'playbooks/cleanup_disk.yml',
        'priority': 'high'
    },
    'HighMemoryUsage': {
        'description': 'Redémarrage des services consommateurs',
        'playbook': 'playbooks/restart_services.yml',
        'priority': 'medium'
    },
    'HighCPUUsage': {
        'description': 'Identification et kill des processus zombies',
        'playbook': 'playbooks/kill_zombie_processes.yml',
        'priority': 'medium'
    },
    'InstanceDown': {
        'description': 'Tentative de redémarrage du service',
        'playbook': 'playbooks/restart_instance.yml',
        'priority': 'critical'
    }
}


def log(message, level='info'):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open('/tmp/self_healing.log', 'a') as f:
        f.write(f"[{timestamp}] {message}\n")


def run_remediation(alert_name, instance):
    """Lance le playbook de remédiation approprié."""
    if alert_name not in REMEDIATION_CATALOG:
        log(f"Aucune remédiation connue pour : {alert_name}")
        return False

    remediation = REMEDIATION_CATALOG[alert_name]
    log(f"REMÉDIATION : {alert_name} sur {instance}")
    log(f"Action : {remediation['description']}")
    log(f"Priorité : {remediation['priority']}")

    # Enregistre l'incident
    incident = {
        'timestamp': datetime.now().isoformat(),
        'alert': alert_name,
        'instance': instance,
        'remediation': remediation['description'],
        'playbook': remediation['playbook'],
        'status': 'triggered'
    }

    with open('/tmp/incidents.json', 'a') as f:
        f.write(json.dumps(incident) + '\n')

    # Simule l'exécution du playbook
    log(f"Lancement playbook : {remediation['playbook']}")
    log(f"Remédiation terminée pour {alert_name} sur {instance}")

    return True


class HealingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        log("=" * 50)
        log("ALERTE REÇUE — ANALYSE EN COURS")

        for alert in data.get('alerts', []):
            alert_name = alert.get('labels', {}).get('alertname', '')
            instance = alert.get('labels', {}).get('instance', 'unknown')
            status = alert.get('status', '')

            log(f"Alerte : {alert_name} | Instance : {instance} | Status : {status}")

            if status == 'firing':
                run_remediation(alert_name, instance)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        pass


def main():
    log("=" * 50)
    log("SELF-HEALING ENGINE DÉMARRÉ")
    log(f"Catalogue : {len(REMEDIATION_CATALOG)} remédiation(s) disponible(s)")
    log("=" * 50)

    server = HTTPServer(('localhost', 5002), HealingHandler)
    log("Serveur en écoute sur port 5002")
    server.serve_forever()


if __name__ == "__main__":
    main()
