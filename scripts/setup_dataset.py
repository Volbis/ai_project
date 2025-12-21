"""
Script d'initialisation rapide du dataset
Crée la structure de dossiers nécessaire
Pour le projet ZKA Marchés CI
"""

from pathlib import Path
import argparse

def setup_dataset(dataset_root):
    """
    Crée la structure de dossiers pour le dataset
    
    Args:
        dataset_root: Chemin racine du dataset
    """
    print("🚀 Initialisation du dataset ZKA Marchés CI...")
    print("=" * 60)
    
    dataset_root = Path(dataset_root)
    
    # Structure complète
    folders = [
        "images",
        "labels",
        "train/images",
        "train/labels",
        "val/images",
        "val/labels",
        "test/images",
        "test/labels",
    ]
    
    print("\n📁 Création de la structure de dossiers:")
    for folder in folders:
        folder_path = dataset_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {folder}/")
    
    # Créer fichier README
    readme_path = dataset_root / "README.md"
    if not readme_path.exists():
        readme_content = """# Dataset ZKA Marchés CI

## 📋 Structure

```
dataset_marches_ci/
├── images/          # Toutes les images collectées
├── labels/          # Tous les fichiers d'annotation
├── train/           # Données d'entraînement (70%)
│   ├── images/
│   └── labels/
├── val/             # Données de validation (20%)
│   ├── images/
│   └── labels/
└── test/            # Données de test (10%)
    ├── images/
    └── labels/
```

## 🎯 Classes (7)

0. **personne** - Piétons, clients, commerçants
1. **vehicule** - Motos, taxis, camions
2. **etal** - Stands de marché
3. **chariot** - Brouettes, chariots à bras
4. **obstacle** - Marchandises bloquant passage
5. **voie_bloquee** - Passage obstrué
6. **zone_dense** - Concentration >10 pers/m²

## 📸 Collecte de Données

### Où ?
- Marché d'Adjamé
- Marché de Treichville
- Marché de Cocody
- Marché de Yopougon

### Quand ?
- Matin (6h-10h)
- Midi (12h-14h)
- Soir (17h-19h)

### Objectif
- Minimum: 1000 images
- Recommandé: 3000 images
- Idéal: 5000+ images

## 🏷️ Annotation

1. **Outils**: LabelImg (recommandé) ou Roboflow
2. **Format**: YOLO (coordonnées normalisées)
3. **Placement**: 
   - Images → `images/`
   - Labels → `labels/`

## 🔧 Scripts Utiles

```bash
# Vérifier le dataset
python scripts/check_dataset.py

# Répartir train/val/test
python scripts/split_dataset.py

# Visualiser annotations
python scripts/visualize_annotations.py
```

## 📊 Objectif Qualité

- ✅ 1000+ images annotées
- ✅ Toutes classes représentées (>50 instances/classe)
- ✅ Variété conditions (lumière, angle, densité)
- ✅ Split 70/20/10 (train/val/test)

---

**Projet ZKA Marchés CI - ESATIC 2025**
"""
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"\n📄 Créé: README.md")
    
    # Créer fichier .gitignore
    gitignore_path = dataset_root / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = """# Images et labels (trop volumineux pour git)
*.jpg
*.jpeg
*.png
*.bmp
*.txt

# Sauf README
!README.md
!.gitignore

# Fichiers système
.DS_Store
Thumbs.db
"""
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print(f"📄 Créé: .gitignore")
    
    # Instructions finales
    print("\n" + "=" * 60)
    print("✅ Structure du dataset créée avec succès!")
    print(f"\n📂 Dossier: {dataset_root.absolute()}")
    
    print("\n📝 PROCHAINES ÉTAPES:")
    print("\n1️⃣  Collecter des photos:")
    print("   - Visiter les marchés d'Abidjan")
    print("   - Prendre 1000+ photos (différentes heures, angles)")
    print("   - Placer dans: dataset_marches_ci/images/")
    
    print("\n2️⃣  Annoter avec LabelImg:")
    print("   - Installer: pip install labelImg")
    print("   - Lancer: labelImg")
    print("   - Format: YOLO")
    print("   - Sauvegarder labels dans: dataset_marches_ci/labels/")
    
    print("\n3️⃣  Répartir le dataset:")
    print("   - Commande: python scripts/split_dataset.py")
    print("   - Résultat: train/ val/ test/ remplis automatiquement")
    
    print("\n4️⃣  Vérifier:")
    print("   - Commande: python scripts/check_dataset.py")
    print("   - Visualiser: python scripts/visualize_annotations.py")
    
    print("\n5️⃣  Entraîner YOLOv5:")
    print("   - Voir: GUIDE_ENTRAINEMENT.md")
    print("   - Commande: python train.py --data data/marches_ci.yaml ...")
    
    print("\n💡 Documentation complète:")
    print("   - GUIDE_ANNOTATION_IMAGES.md")
    print("   - GUIDE_ENTRAINEMENT.md")
    print("   - CAS_USAGE_MARCHES_CI.md")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialiser la structure du dataset")
    parser.add_argument(
        "dataset_root",
        type=str,
        nargs='?',
        default="../dataset_marches_ci",
        help="Chemin racine du dataset (défaut: ../dataset_marches_ci)"
    )
    
    args = parser.parse_args()
    setup_dataset(args.dataset_root)
