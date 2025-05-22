# -*- coding: utf-8 -*-
import os
import json
import configparser
import torch
import torch.nn as nn
from torchvision import transforms
from shapely.geometry import shape, mapping, box
from shapely.ops import transform as shapely_transform
from pyproj import Transformer
import fiona
import rasterio
from rasterio.mask import mask
from PIL import Image

# ===== 1. INI読み込み =====
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

tif_path = config["INPUT"]["NDVI_DIFF_TIF"]
gpkg_path = config["INPUT"]["GPKG"]
layer_name = config["INPUT"]["LAYER_NAME"]
bound_geojson = config["INPUT"]["BOUND_GEOJSON"]
out_geojson = config["OUTPUT"]["PREDICTED_GEOJSON"]
model_path = config["MODEL"]["MODEL_PATH"]
label_map_path = config["MODEL"]["LABEL_MAP"]
patch_size = int(config["MODEL"]["PATCH_SIZE"])
src_epsg = int(config["CRS"]["SOURCE_EPSG"])   # GPKG側
dst_epsg = int(config["CRS"]["TARGET_EPSG"])   # TIFF画像側

# ===== 2. ラベルマップ読み込み =====
with open(label_map_path, encoding="utf-8") as f:
    label_map = json.load(f)
inv_label_map = {v: k for k, v in label_map.items()}

# ===== 3. モデル定義と読込 =====
class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * (patch_size // 4) ** 2, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN(num_classes=len(label_map))
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((patch_size, patch_size)),
    transforms.ToTensor()
])

# ===== 4. bound.geojson 読込 + union =====
with fiona.open(bound_geojson, encoding="utf-8") as bound_src:
    bound_geom = [shape(feat["geometry"]) for feat in bound_src]
    bound_union = bound_geom[0]
    for g in bound_geom[1:]:
        bound_union = bound_union.union(g)

# ===== 5. Transformer定義（GPKG 6676 → TIFF 4326）=====
to_raster_crs = Transformer.from_crs(src_epsg, dst_epsg, always_xy=True)

results = []

# ===== 6. GPKG + TIFF 読込 =====
with fiona.open(gpkg_path, layer=layer_name, encoding="utf-8") as src_vec, \
     rasterio.open(tif_path) as src_ras:

    # TIFF画像の地理的範囲を shapely の box で取得
    raster_bounds = box(*src_ras.bounds)

    for feature in src_vec:
        geom = shape(feature["geometry"])
        geom_4326 = shapely_transform(lambda x, y: to_raster_crs.transform(x, y), geom)
        if not (geom_4326.intersects(bound_union) and geom_4326.intersects(raster_bounds)):
            continue
        try:
            out_image, out_transform = mask(src_ras, [mapping(geom_4326)], crop=True)
            patch = out_image[0]
            if patch.shape[0] == 0 or patch.shape[1] == 0:
                continue
            pil_image = Image.fromarray(patch).convert("L")
            input_tensor = transform(pil_image).unsqueeze(0).to(device)
            with torch.no_grad():
                output = model(input_tensor)
                pred_idx = torch.argmax(output, dim=1).item()
                pred_label = inv_label_map[pred_idx]
            properties = dict(feature["properties"])
            properties["predicted_land_type"] = pred_label
            new_feature = {
                "type": "Feature",
                "geometry": mapping(geom_4326),
                "properties": properties
            }
            results.append(new_feature)
        except Exception as e:
            print(f"スキップ: {e}")
        geom = shape(feature["geometry"])
        geom_4326 = shapely_transform(lambda x, y: to_raster_crs.transform(x, y), geom)

        if not (geom_4326.intersects(bound_union) and geom_4326.intersects(raster_bounds)):
            continue

        try:
            out_image, out_transform = mask(src_ras, [mapping(geom_4326)], crop=True)
            patch = out_image[0]
            if patch.shape[0] == 0 or patch.shape[1] == 0:
                continue

            pil_image = Image.fromarray(patch).convert("L")
            input_tensor = transform(pil_image).unsqueeze(0).to(device)
            with torch.no_grad():
                output = model(input_tensor)
                pred_idx = torch.argmax(output, dim=1).item()
                pred_label = inv_label_map[pred_idx]

            new_feature = {
                "type": "Feature",
                "geometry": mapping(geom_4326),
                "properties": {
                    "predicted_land_type": pred_label
                }
            }
            results.append(new_feature)

        except Exception as e:
            print(f"スキップ: {e}")

output_geojson = {
    "type": "FeatureCollection",
    "features": results
}
with open(out_geojson, "w", encoding="utf-8") as f:
    json.dump(output_geojson, f, ensure_ascii=False, indent=2)

print("分類結果をGeoJSONに保存しました。")
