"""
Script de répartition du dataset en train/val/test
Pour le project ZKA Marchés CI.
"""

import argparse
import random
import shutil
from pathlib import Path


def split_dataset(dataset_root, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """Répartit les images et labels en train/val/test.

    Args:
        dataset_root: Chemin racine du dataset
        train_ratio: Proportion pour l'entraînement (70%)
        val_ratio: Proportion pour la validation (20%)
        test_ratio: Proportion pour le test (10%)
    """
    print("🚀 Démarrage de la répartition du dataset...")

    dataset_root = Path(dataset_root)
    images_dir = dataset_root / "images"
    labels_dir = dataset_root / "labels"

    # Vérifier que les dossiers existent
    if not images_dir.exists():
        print(f"❌ Erreur: Le dossier {images_dir} n'existe pas!")
        return

    if not labels_dir.exists():
        print(f"⚠️  Avertissement: Le dossier {labels_dir} n'existe pas!")
        print("   Création du dossier labels...")
        labels_dir.mkdir(parents=True, exist_ok=True)

    # Créer les dossiers de destination
    print("\n📁 Création des dossiers train/val/test...")
    for split in ["train", "val", "test"]:
        (dataset_root / split / "images").mkdir(parents=True, exist_ok=True)
        (dataset_root / split / "labels").mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {split}/")

    # Lister toutes les images
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    images = []
    for ext in image_extensions:
        images.extend(list(images_dir.glob(f"*{ext}")))
        images.extend(list(images_dir.glob(f"*{ext.upper()}")))

    if len(images) == 0:
        print(f"\n❌ Erreur: Aucune image trouvée dans {images_dir}")
        return

    print(f"\n📊 {len(images)} images trouvées")

    # Mélanger aléatoirement
    random.shuffle(images)

    # Calculer les indices de séparation
    n_train = int(len(images) * train_ratio)
    n_val = int(len(images) * val_ratio)

    train_images = images[:n_train]
    val_images = images[n_train : n_train + n_val]
    test_images = images[n_train + n_val :]

    print("\n📦 Répartition:")
    print(f"   Train: {len(train_images)} images ({train_ratio * 100:.0f}%)")
    print(f"   Val:   {len(val_images)} images ({val_ratio * 100:.0f}%)")
    print(f"   Test:  {len(test_images)} images ({test_ratio * 100:.0f}%)")

    # Function de copie
    def copy_files(image_list, split):
        copied_images = 0
        copied_labels = 0
        missing_labels = []

        for img_path in image_list:
            label_path = labels_dir / (img_path.stem + ".txt")

            # Copier image
            shutil.copy(img_path, dataset_root / split / "images" / img_path.name)
            copied_images += 1

            # Copier label (si existe)
            if label_path.exists():
                shutil.copy(label_path, dataset_root / split / "labels" / label_path.name)
                copied_labels += 1
            else:
                missing_labels.append(img_path.name)

        return copied_images, copied_labels, missing_labels

    # Copier les fichiers
    print("\n📋 Copie des fichiers...")

    print("   Train...")
    train_img, train_lbl, train_miss = copy_files(train_images, "train")
    print(f"      Images: {train_img}, Labels: {train_lbl}")

    print("   Val...")
    val_img, val_lbl, val_miss = copy_files(val_images, "val")
    print(f"      Images: {val_img}, Labels: {val_lbl}")

    print("   Test...")
    test_img, test_lbl, test_miss = copy_files(test_images, "test")
    print(f"      Images: {test_img}, Labels: {test_lbl}")

    # Rapport final
    all_missing = train_miss + val_miss + test_miss

    print("\n✅ Dataset réparti avec succès!")
    print("\n📊 Résumé:")
    print(f"   Total images copiées: {train_img + val_img + test_img}")
    print(f"   Total labels copiés: {train_lbl + val_lbl + test_lbl}")

    if len(all_missing) > 0:
        print(f"\n⚠️  {len(all_missing)} images sans label:")
        for img in all_missing[:10]:  # Afficher les 10 premiers
            print(f"      - {img}")
        if len(all_missing) > 10:
            print(f"      ... et {len(all_missing) - 10} autres")
        print("\n   💡 Conseil: Annotez ces images avec LabelImg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Répartir le dataset en train/val/test")
    parser.add_argument(
        "dataset_root",
        type=str,
        nargs="?",
        default="../dataset_marches_ci",
        help="Chemin racine du dataset (défaut: ../dataset_marches_ci)",
    )
    parser.add_argument("--train", type=float, default=0.7, help="Proportion train (défaut: 0.7)")
    parser.add_argument("--val", type=float, default=0.2, help="Proportion val (défaut: 0.2)")
    parser.add_argument("--test", type=float, default=0.1, help="Proportion test (défaut: 0.1)")

    args = parser.parse_args()

    # Vérifier que les proportions somment à 1
    total = args.train + args.val + args.test
    if abs(total - 1.0) > 0.01:
        print(f"❌ Erreur: train + val + test doit égaler 1.0 (actuellement {total})")
        exit(1)

    split_dataset(args.dataset_root, args.train, args.val, args.test)
