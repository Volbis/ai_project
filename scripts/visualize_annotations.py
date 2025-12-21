"""
Script de visualisation des annotations
Affiche les boîtes et labels sur les images
Pour le projet ZKA Marchés CI
"""

import cv2
import argparse
from pathlib import Path
import random

# Classes du dataset Marchés CI
CLASS_NAMES = [
    'personne',
    'vehicule',
    'etal',
    'chariot',
    'obstacle',
    'voie_bloquee',
    'zone_dense'
]

# Couleurs pour chaque classe (BGR)
CLASS_COLORS = [
    (0, 255, 0),      # personne - Vert
    (255, 0, 0),      # vehicule - Bleu
    (0, 0, 255),      # etal - Rouge
    (255, 255, 0),    # chariot - Cyan
    (255, 0, 255),    # obstacle - Magenta
    (255, 128, 0),    # voie_bloquee - Orange
    (128, 0, 255)     # zone_dense - Violet
]

def visualize_image(img_path, label_path=None):
    """
    Visualise une image avec ses annotations
    
    Args:
        img_path: Chemin vers l'image
        label_path: Chemin vers le fichier label (optionnel)
    """
    # Charger image
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"❌ Impossible de charger l'image: {img_path}")
        return
    
    h, w = img.shape[:2]
    
    # Si pas de label spécifié, chercher dans le même dossier parent
    if label_path is None:
        label_path = img_path.parent.parent / 'labels' / (img_path.stem + '.txt')
    else:
        label_path = Path(label_path)
    
    # Dessiner les annotations si le fichier existe
    detection_count = 0
    if label_path.exists():
        try:
            with open(label_path) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    
                    cls = int(parts[0])
                    x, y, width, height = map(float, parts[1:5])
                    
                    # Convertir coordonnées YOLO → pixels
                    x1 = int((x - width/2) * w)
                    y1 = int((y - height/2) * h)
                    x2 = int((x + width/2) * w)
                    y2 = int((y + height/2) * h)
                    
                    # Vérifier validité
                    if cls < 0 or cls >= len(CLASS_NAMES):
                        continue
                    
                    # Dessiner boîte
                    color = CLASS_COLORS[cls]
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    
                    # Dessiner label
                    label = CLASS_NAMES[cls]
                    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    
                    # Fond du label
                    cv2.rectangle(img, 
                                (x1, y1 - label_size[1] - 10),
                                (x1 + label_size[0], y1),
                                color, -1)
                    
                    # Texte
                    cv2.putText(img, label, (x1, y1 - 5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    detection_count += 1
        
        except Exception as e:
            print(f"⚠️  Erreur lecture label: {e}")
    
    else:
        print(f"⚠️  Pas de fichier label: {label_path}")
    
    # Ajouter info en haut de l'image
    info_text = f"{img_path.name} - {detection_count} objets"
    cv2.putText(img, info_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Légende des classes (coin supérieur droit)
    legend_x = w - 200
    legend_y = 30
    for i, (name, color) in enumerate(zip(CLASS_NAMES, CLASS_COLORS)):
        y = legend_y + i * 25
        cv2.rectangle(img, (legend_x, y - 15), (legend_x + 20, y + 5), color, -1)
        cv2.putText(img, name, (legend_x + 25, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Afficher
    window_name = "ZKA Marchés - Annotations"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
    
    print(f"\n✅ Image: {img_path.name}")
    print(f"   Détections: {detection_count}")
    print(f"\n💡 Contrôles:")
    print(f"   - Appuyez sur ESPACE pour image suivante")
    print(f"   - Appuyez sur 'q' ou ESC pour quitter")
    print(f"   - Appuyez sur 's' pour sauvegarder")
    
    return img

def browse_dataset(dataset_root, split='train', random_order=False):
    """
    Parcourt les images du dataset
    
    Args:
        dataset_root: Chemin racine du dataset
        split: 'train', 'val' ou 'test'
        random_order: Ordre aléatoire si True
    """
    dataset_root = Path(dataset_root)
    images_dir = dataset_root / split / 'images'
    
    if not images_dir.exists():
        print(f"❌ Erreur: Le dossier {images_dir} n'existe pas!")
        return
    
    # Lister images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    for ext in image_extensions:
        images.extend(list(images_dir.glob(f"*{ext}")))
        images.extend(list(images_dir.glob(f"*{ext.upper()}")))
    
    if len(images) == 0:
        print(f"❌ Aucune image trouvée dans {images_dir}")
        return
    
    if random_order:
        random.shuffle(images)
    else:
        images.sort()
    
    print(f"🖼️  {len(images)} images trouvées dans {split}/")
    print("=" * 60)
    
    # Parcourir les images
    for i, img_path in enumerate(images):
        print(f"\n[{i+1}/{len(images)}]", end=' ')
        
        img = visualize_image(img_path)
        
        # Attendre input utilisateur
        key = cv2.waitKey(0) & 0xFF
        
        # 'q' ou ESC pour quitter
        if key == ord('q') or key == 27:
            print("\n👋 Fermeture...")
            break
        
        # 's' pour sauvegarder
        elif key == ord('s'):
            output_path = img_path.parent / f"annotated_{img_path.name}"
            cv2.imwrite(str(output_path), img)
            print(f"   💾 Sauvegardé: {output_path}")
        
        # ESPACE ou autre touche pour continuer
    
    cv2.destroyAllWindows()
    print("\n✅ Fin de la visualisation")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualiser les annotations du dataset")
    parser.add_argument(
        "dataset_root",
        type=str,
        nargs='?',
        default="../dataset_marches_ci",
        help="Chemin racine du dataset (défaut: ../dataset_marches_ci)"
    )
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=['train', 'val', 'test'],
        help="Split à visualiser (défaut: train)"
    )
    parser.add_argument(
        "--random",
        action='store_true',
        help="Ordre aléatoire"
    )
    parser.add_argument(
        "--image",
        type=str,
        help="Visualiser une image spécifique (chemin complet)"
    )
    
    args = parser.parse_args()
    
    if args.image:
        # Visualiser une image spécifique
        img_path = Path(args.image)
        if not img_path.exists():
            print(f"❌ Image non trouvée: {img_path}")
        else:
            visualize_image(img_path)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        # Parcourir le dataset
        browse_dataset(args.dataset_root, args.split, args.random)
