# nara-auto-chimoku-classifier

本プロジェクトは、`nara-land-classifier` で訓練されたモデルを使用し、地図データから推定地目を自動的に分類・GeoJSON形式で出力するユーティリティです。

## 📁 ディレクトリ構成
```text
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
```text


## ▶️ 実行手順

1. 必要なファイルを `Input/`、`Model/` に配置してください。
2. `start_chimoku.bat` をダブルクリックして実行します。
3. `Output/predicted.geojson` に分類結果が出力されます。
4. `チェック.qgz` を使えばQGISで結果を可視化できます。

---

## 💡 使用環境・依存ライブラリ

以下のPythonライブラリを使用しています（`requirements.txt`にまとめても可）：

- `numpy`
- `torch`
- `pandas`
- `geopandas`
- `rasterio`
- `shapely`
- `matplotlib`

仮想環境を使う場合：

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## 📷 処理イメージ

![処理イメージ](2025-05-22_21h38_04.png)
