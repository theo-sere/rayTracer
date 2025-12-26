# RayTracer

Un moteur de rendu par lancer de rayons (Ray Tracer) complet écrit en Python. Ce programme génère des images au format PPM en se basant sur une scène définie dans un fichier de configuration JSON, incluant la gestion des ombres et des reflets.

## 🚀 Fonctionnalités

- **Rendu de formes géométriques** : Supporte les sphères avec calcul d'intersection quadratique.
- **Système d'éclairage complet** : Gère les lumières Ambiantes, Ponctuelles et Directionnelles avec modèle de brillance spéculaire.
- **Effets Avancés** : Gestion des **ombres portées** et des **réflexions récursives** (miroirs).
- **Configuration flexible** : La scène est entièrement configurable via un fichier JSON (couleurs, positions, matériaux).
- **Sortie standard** : Génère les images au format `.ppm`.

## 📋 Prérequis

- Python 3.x
- Les dépendances listées dans le fichier `requirements.txt`.

## 🛠️ Installation

1.  Clonez le dépôt :

    ```bash
    git clone https://github.com/theo-sere/rayTracer
    cd rayTracer
    ```

2.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Utilisation

Le code source se trouve dans le dossier `src`.

1.  Placez-vous dans le répertoire des sources :

    ```bash
    cd src
    ```

2.  Lancez le script principal :

    ```bash
    python main.py
    ```

3.  L'image `image.ppm` sera générée à la racine du projet.

## ⚙️ Configuration de la scène

Le fichier `scene.json` à la racine du projet permet de modifier le rendu.

**Paramètres principaux :**

- `viewport_size` / `pixel_size` : Taille de la vue et résolution de l'image.
- `projection_plane_d` : Distance du plan de projection (focale).
- `spheres` : Liste des objets avec position, rayon, couleur, facteur `specular` (brillance) et `reflective` (réflexion).
- `lights` : Liste des sources lumineuses (types : `ambient`, `point`, `directional`).

## 🧠 Algorithmes

- **Intersections** : Résolution du discriminant pour les sphères.
- **Lumière** : Modèle de réflexion spéculaire et calcul d'ombrage via rayons secondaires vers les sources lumineuses.
- **Réflexion** : Algorithme récursif utilisant le vecteur réfléchi $\vec{R} = 2\vec{N}(\vec{N} \cdot \vec{L}) - \vec{L}$.
- **Précision** : Utilisation d'un `epsilon` ($0.001$) pour éviter les artefacts de surface (Shadow Acne).

## 👥 Auteurs

- **Lou KAIL**
- **Théo SÉRÉ**

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
