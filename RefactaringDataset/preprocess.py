import json
import requests
import re
import csv

# 入力JSONファイルのパスと出力JSONファイルのパス
input_json_file = "data/refactoring_oracl.json"  # 入力JSONファイルのパス
output_json_file = "data/shape_refactoring_oracl.json"  # 出力JSONファイルのパス

def delete_fp_data(input_json_file_path: str, output_file_json_path: str) -> dict:
    try:
        with open(input_json_file_path, "r") as infile:
            input_json = json.load(infile)
    except FileNotFoundError:
        print(f"Not found '{input_json_file_path}")
        exit(1)
   
    for item in input_json:
        item["refactorings"] = [refactoring for refactoring in item["refactorings"] if refactoring.get("validation") != "FP"]    

    with open(output_json_file_path, "r") as outfile:
        json.dump(input_json, outfile, indent=2)
    print(f"\"refactorings\" フィールド内の\"validation\" フィールドが\"FP\"の要素を削除したJSONを '{output_json_file}' に保存しました。")
