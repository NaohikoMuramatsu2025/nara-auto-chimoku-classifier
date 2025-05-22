# nara-auto-chimoku-classifier

本プロジェクトは、`nara-land-classifier` で訓練されたモデルを使用し、地図データから推定地目を自動的に分類・GeoJSON形式で出力するユーティリティです。

## 📁 ディレクトリ構成
'''text
nara-auto-chimoku-classifier/
│ start_chimoku.bat
│ チェック.qgz
│ 2025-05-22_21h38_04.png
│
├─Input/
│ ├─ corners.geojson
│ ├─ nara_4326.tif
│ └─ nara_fudekai_bound.gpkg
│
├─Model/
│ ├─ label_map.json
│ └─ land_classifier_model.pth
│
├─Output/
│ └─ predicted.geojson
│
└─python_src/
├─ config.ini
└─ land_use_guess_fixed.py
'''text


## ▶️ 実行手順

1. 必要なファイルを `Input/`, `Model/` に配置。
2. `start_chimoku.bat` をダブルクリック。
3. `Output/predicted.geojson` に分類結果が出力されます。

## 🔗 関連プロジェクト

- [`nara-land-classifier`](https://github.com/xxxxxx/nara-land-classifier)
