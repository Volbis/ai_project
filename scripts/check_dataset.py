"""
Script de vérification du dataset
Affiche statistiques et détecte problèmes
Pour le project ZKA Marchés CI.
"""

import argparse
from collections import Counter
from pathlib import Path

# Classes du dataset Marchés CI
CLASS_NAMES = ["personne", "vehicle", "etal", "chariot", "obstacle", "voie_bloquee", "zone_dense"]


def check_dataset(dataset_root):
    """Vérifie la structure et le contenu du dataset.

    Args:
        dataset_root: Chemin racine du dataset
    """
    print("🔍 Vérification du dataset ZKA Marchés CI...")
    print("=" * 60)

    dataset_root = Path(dataset_root)

    if not dataset_root.exists():
        print(f"❌ Erreur: Le dossier {dataset_root} n'existe pas!")
        return

    total_images = 0
    total_labels = 0
    total_detections = 0
    all_class_counts = Counter()

    issues = []

    # Vérifier chaque split
    for split in ["train", "val", "test"]:
        print(f"\n📁 {split.upper()}:")

        images_dir = dataset_root / split / "images"
        labels_dir = dataset_root / split / "labels"

        if not images_dir.exists():
            print(f"   ⚠️  Dossier images manquant: {images_dir}")
            continue

        if not labels_dir.exists():
            print(f"   ⚠️  Dossier labels manquant: {labels_dir}")
            continue

        # Lister images et labels
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
        images = []
        for ext in image_extensions:
            images.extend(list(images_dir.glob(f"*{ext}")))
            images.extend(list(images_dir.glob(f"*{ext.upper()}")))

        labels = list(labels_dir.glob("*.txt"))

        print(f"   Images: {len(images)}")
        print(f"   Labels: {len(labels)}")

        total_images += len(images)
        total_labels += len(labels)

        # Vérifier correspondence images/labels
        images_no_label = []
        labels_no_image = []

        image_stems = {img.stem for img in images}
        label_stems = {lbl.stem for lbl in labels}

        images_no_label = image_stems - label_stems
        labels_no_image = label_stems - image_stems

        if images_no_label:
            print(f"   ⚠️  {len(images_no_label)} images sans label")
            issues.append(f"{split}: {len(images_no_label)} images sans label")

        if labels_no_image:
            print(f"   ⚠️  {len(labels_no_image)} labels sans image")
            issues.append(f"{split}: {len(labels_no_image)} labels sans image")

        # Analyzer distribution des classes
        class_counts = Counter()
        split_detections = 0
        empty_labels = []
        invalid_labels = []

        for label_file in labels:
            try:
                with open(label_file) as f:
                    lines = f.readlines()

                    if len(lines) == 0:
                        empty_labels.append(label_file.name)
                        continue

                    for line_num, line in enumerate(lines, 1):
                        parts = line.strip().split()

                        if len(parts) < 5:
                            invalid_labels.append(f"{label_file.name}:{line_num}")
                            continue

                        try:
                            class_id = int(parts[0])
                            x, y, w, h = map(float, parts[1:5])

                            # Vérifier validité
                            if class_id < 0 or class_id >= len(CLASS_NAMES):
                                invalid_labels.append(f"{label_file.name}:{line_num} (class {class_id} invalid)")
                                continue

                            if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                                invalid_labels.append(f"{label_file.name}:{line_num} (coordonnées hors limites)")
                                continue

                            class_counts[class_id] += 1
                            split_detections += 1

                        except ValueError:
                            invalid_labels.append(f"{label_file.name}:{line_num} (format invalid)")

            except Exception as e:
                invalid_labels.append(f"{label_file.name} (erreur: {e})")

        total_detections += split_detections
        all_class_counts.update(class_counts)

        if empty_labels:
            print(f"   ⚠️  {len(empty_labels)} labels vides")
            issues.append(f"{split}: {len(empty_labels)} labels vides")

        if invalid_labels:
            print(f"   ❌ {len(invalid_labels)} labels invalides")
            issues.append(f"{split}: {len(invalid_labels)} labels invalides")
            if len(invalid_labels) <= 5:
                for inv in invalid_labels:
                    print(f"      - {inv}")

        # Afficher distribution des classes
        if class_counts:
            print(f"   📊 Distribution des classes ({split_detections} détections):")
            for cls_id, count in sorted(class_counts.items()):
                percentage = (count / split_detections) * 100
                print(f"      {CLASS_NAMES[cls_id]:15} : {count:4d} ({percentage:5.1f}%)")

    # Résumé global
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ GLOBAL:")
    print(f"   Total images:     {total_images}")
    print(f"   Total labels:     {total_labels}")
    print(f"   Total détections: {total_detections}")

    if total_labels > 0:
        print("\n   📊 Distribution globale des classes:")
        for cls_id in range(len(CLASS_NAMES)):
            count = all_class_counts.get(cls_id, 0)
            percentage = (count / total_detections * 100) if total_detections > 0 else 0
            print(f"      {CLASS_NAMES[cls_id]:15} : {count:4d} ({percentage:5.1f}%)")

    # Vérifier équilibre
    print("\n   🎯 Qualité du dataset:")

    if total_images < 100:
        print(f"      ⚠️  Trop peu d'images ({total_images}). Recommandé: 1000+")
        issues.append("Dataset trop petit (< 100 images)")
    elif total_images < 500:
        print(f"      ⚠️  Dataset petit ({total_images}). Recommandé: 1000+")
    elif total_images < 1000:
        print(f"      ✅ Dataset correct ({total_images}). Idéal: 3000+")
    else:
        print(f"      ✅ Excellent! {total_images} images")

    # Vérifier classes
    for cls_id, cls_name in enumerate(CLASS_NAMES):
        count = all_class_counts.get(cls_id, 0)
        if count == 0:
            print(f"      ❌ Classe '{cls_name}' absente!")
            issues.append(f"Classe '{cls_name}' non représentée")
        elif count < 50:
            print(f"      ⚠️  Classe '{cls_name}' sous-représentée ({count}). Min: 50")
            issues.append(f"Classe '{cls_name}' sous-représentée ({count} < 50)")

    # Rapport final
    if issues:
        print(f"\n⚠️  {len(issues)} PROBLÈMES DÉTECTÉS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ AUCUN PROBLÈME DÉTECTÉ!")
        print("   Le dataset est prêt pour l'entraînement! 🚀")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vérifier le dataset ZKA Marchés CI")
    parser.add_argument(
        "dataset_root",
        type=str,
        nargs="?",
        default="../dataset_marches_ci",
        help="Chemin racine du dataset (défaut: ../dataset_marches_ci)",
    )

    args = parser.parse_args()
    check_dataset(args.dataset_root)
