# RayTracer

Un moteur de rendu par lancer de rayons (Ray Tracer) simple écrit en Python. Ce programme génère des images au format PPM en se basant sur une scène définie dans un fichier de configuration JSON.

## 🚀 Fonctionnalités

* **Rendu de formes géométriques** : Supporte les sphères.
* **Système d'éclairage** : Gère plusieurs types de lumières (Ambiante, Ponctuelle, Directionnelle) et la spécularité.
* **Configuration flexible** : La scène est entièrement configurable via un fichier JSON.
* **Sortie standard** : Génère les images au format `.ppm`.

## 📋 Prérequis

* Python 3.x
* Les dépendances listées dans le fichier `requirements.txt`.

## 🛠️ Installation

1.  Clonez le dépôt :
    ```bash
    git clone <votre-url-repo>
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

3.  L'image `image.ppm` sera générée dans le dossier parent (racine du projet).

## ⚙️ Configuration de la scène

Le fichier `scene.json` à la racine du projet permet de modifier le rendu.

**Paramètres principaux :**
* `viewport_size` / `pixel_size` : Taille de la vue et résolution de l'image.
* `camera_position` : Position de la caméra (x, y, z).
* `spheres` : Liste des objets avec leur position, rayon, couleur et facteur spéculaire.
* `lights` : Liste des sources lumineuses (types : ambient, point, directional).

## 👥 Auteurs

* **Lou KAIL**
* **Théo SÉRÉ**

*(Basé sur le fichier LICENSE)*

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
