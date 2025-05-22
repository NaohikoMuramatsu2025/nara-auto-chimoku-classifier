
# nara-auto-chimoku-classifier

本プロジェクトは、`nara-land-classifier` で訓練されたモデルを使用し、地図データから推定地目を自動的に分類・GeoJSON形式で出力するユーティリティです。

---
## 📸 推定結果のスクリーンショット

以下は、分類器を実行した際のフォルダ構成のスクリーンショットです。

![推定実行後のフォルダ構成](2025-05-22_21h38_04.png)

---

## 📁 構成フォルダ

| フォルダ名        | 内容                                                                 |
|------------------|----------------------------------------------------------------------|
| `入力` (`input`) | 入力ファイル（GeoTIFF、GPKG等）                                     |
| `モデル` (`model`)| 学習済みのモデルデータ（`.pth`）や分類マップ。<br>※ 他都市で作成したモデルを使用しています。詳細は下記参照。 |
| `出力` (`output`)| GeoJSON形式などで出力された分類結果                                   |
| `python_src`     | 推定処理を行うPythonコード群                                           |

---

## 🧠 モデル作成と分類マップの見方

### 学習済みモデル（`.pth`）について

- モデルは他の都市の地番情報と空中写真をもとに学習したものであり、再利用しています。
- この分類器では **PyTorch** を利用した推定を行います。

#### モデル作成の一般的な手順

1. 地番図などのポリゴンデータをカテゴリラベルに整備。
2. 空中写真などのラスタ画像と位置を合わせる。
3. 教師あり学習でモデルを作成（分類器 `.pth` を出力）。

> ※ 本リポジトリには学習スクリプトは含まれていませんが、推定は可能です。

---

### 分類マップの見方（例：`label_map.json`）

```json
{
  "0": "田",
  "1": "畑",
  "2": "宅地",
  "3": "山林",
  "4": "雑種地"
}
```

推定された結果ファイル（GeoJSON）に含まれるカテゴリIDはこのマップに基づいています。QGISなどで読み込むことで視覚的に確認できます。

---

## 📁 ディレクトリ構成

```text
nara-auto-chimoku-classifier/
├── start_chimoku.bat
├── チェック.qgz
├── 2025-05-22_21h38_04.png
│
├── Input/
│   ├── corners.geojson
│   ├── nara_4326.tif
│   └── nara_fudekai_bound.gpkg
│
├── Model/
│   ├── label_map.json
│   └── land_classifier_model.pth
│
├── Output/
│   └── predicted.geojson
│
└── python_src/
    ├── config.ini
    └── land_use_guess_fixed.py

## ▶️ 実行手順 / How to Run
```bash
# スクリプト起動
start_chimoku.bat
```

または、直接Pythonスクリプトを実行：

```bash
python python_src/land_use_guess_fixed.py
```

---

- [nara-land-classifier GitHub リポジトリ](https://github.com/NaohikoMuramatsu2025/nara-land-classifier)

