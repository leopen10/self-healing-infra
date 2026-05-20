# Self-Healing Infrastructure

![CI](https://github.com/leopen10/self-healing-infra/actions/workflows/ci.yml/badge.svg)

Moteur d'auto-remédiation des incidents infrastructure — détection automatique,
remédiation par playbooks Ansible et génération de rapports post-mortem.

## Problème résolu

Les équipes ops passent leurs nuits à traiter les mêmes incidents répétitifs.
Ce projet implémente un moteur de décision qui détecte, analyse et remédie
automatiquement aux incidents courants — sans intervention humaine.

## Ce que fait ce projet

- **Moteur de décision** — reçoit les alertes Prometheus et décide quelle action lancer
- **Catalogue de remédiations** — 4 types d'incidents gérés automatiquement
- **Playbooks Ansible** — exécutent les corrections sur les serveurs
- **Rapport post-mortem** — génère un rapport HTML après chaque cycle

## Résultats prouvés

4 incidents traités        ✓
0 interventions humaines   ✓
100% auto-remédiation      ✓

## Incidents gérés automatiquement

| Alerte | Action | Priorité |
|---|---|---|
| DiskSpaceLow | Nettoyage automatique du disque | high |
| HighMemoryUsage | Redémarrage des services consommateurs | medium |
| HighCPUUsage | Kill des processus zombies | medium |
| InstanceDown | Tentative de redémarrage du service | critical |

## Stack technique

| Composant | Technologie |
|---|---|
| Moteur de décision | Python 3.12 |
| Remédiation | Ansible |
| Alertes | Prometheus / Alertmanager |
| Reporting | Python + HTML |

## Installation

```bash
git clone https://github.com/leopen10/self-healing-infra.git
cd self-healing-infra
pip install requests
```

## Usage

```bash
# Démarrer le moteur
python3 engine/decision_engine.py

# Simuler des alertes (dans un autre terminal)
python3 scripts/simulate_alert.py

# Générer le rapport post-mortem
python3 scripts/generate_postmortem.py

# Ouvrir le rapport
# Copier le chemin : wslpath -w reports/postmortem_*.html
```

## Architecture
Prometheus détecte une anomalie
↓
Alertmanager envoie l'alerte
↓
decision_engine.py analyse
↓
Playbook Ansible se lance
↓
Incident résolu automatiquement
↓
Rapport post-mortem généré

## Auteur

**Leonel Pengou** — Cloud & DevOps Engineer
[GitHub](https://github.com/leopen10) •
[LinkedIn](https://linkedin.com/in/leonel-magloire-pengou-mba)
