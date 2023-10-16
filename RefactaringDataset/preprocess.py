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

def save_csv(save_file_name: str, save_fieldnames: list) -> None:
    with open(save_file_name, 'w', newline='') as csv_file:
        filenames = save_fieldnames
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
def save_code_data(commit_line: str) -> None     
    if commit_line.startswith('@@'):
        # 変更のブロックが始まったら、前のブロックを保存
        if change_description:
            before_code = '\n'.join(before_code)
            refactor_code = '\n'.join(refactor_code)
            writer.writerow({'File': filename, 'Change_Description': change_description, 'Before_Code': before_code, 'Refactor_Code': refactor_code})
        
        # 新しい変更ブロックの説明を取得
        change_description = commit_line
        
        # 変更前と変更後のコードを初期化
        before_code = []
        refactor_code = []
    elif commit_line.startswith('-'):
        before_code.append(commit_line[1:])
    elif commit_line.startswith('+'):
        refactor_code.append(commit_line[1:])
    else:
        before_code.append(commit_line)
        refactor_code.append(commit_line)
                                
# GitHubコミットのURLとアクセストークンを指定
commit_url = "https://github.com/realm/realm-java/commit/6cf596df183b3c3a38ed5dd9bb3b0100c6548ebb"
access_token = "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"  # ここにGitHubのアクセストークンを設定

# コミットURLからリポジトリの情報を抽出
match = re.search(r'^https://github\.com/([^/]+)/([^/]+)/commit/(\w+)$', commit_url)
if match:
    username, repo, sha = match.groups()
    api_url = f"https://api.github.com/repos/{username}/{repo}/commits/{sha}"
    
    # GitHub APIへのリクエストヘッダにアクセストークンを含める
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # GitHub APIからコミット情報を取得
    commit_response = requests.get(api_url, headers=headers)
    
    if commit_response.status_code == 200:
        commit_data = commit_response.json()
        commit_message = commit_data['commit']['message']
        files = commit_data['files']
        
        # 変更前と変更後のコードをCSVファイルに保存
        save_file_name = 'commit_changes.csv'
        fieldnames = ['File', 'Change_Description', 'Before_Code', 'Refactor_Code']
        save_csv(save_file_name, fieldnames)
        # with open('commit_changes.csv', 'w', newline='') as csvfile:
        #     fieldnames = ['File', 'Change_Description', 'Before_Code', 'Refactor_Code']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
            
            for file in files:
                filename = file['filename']
                patch = file['patch'].splitlines()
                before_code = []
                refactor_code = []
                change_description = None
                
                for line in patch:
                    save_code_data(line)
                    # if line.startswith('@@'):
                    #     # 変更のブロックが始まったら、前のブロックを保存
                    #     if change_description:
                    #         before_code = '\n'.join(before_code)
                    #         refactor_code = '\n'.join(refactor_code)
                    #         writer.writerow({'File': filename, 'Change_Description': change_description, 'Before_Code': before_code, 'Refactor_Code': refactor_code})
                        
                    #     # 新しい変更ブロックの説明を取得
                    #     change_description = line
                        
                    #     # 変更前と変更後のコードを初期化
                    #     before_code = []
                    #     refactor_code = []
                    # elif line.startswith('-'):
                    #     before_code.append(line[1:])
                    # elif line.startswith('+'):
                    #     refactor_code.append(line[1:])
                    # else:
                    #     before_code.append(line)
                    #     refactor_code.append(line)
                
                # # 最後の変更ブロックを保存
                # if change_description:
                #     before_code = '\n'.join(before_code)
                #     refactor_code = '\n'.join(refactor_code)
                #     writer.writerow({'File': filename, 'Change_Description': change_description, 'Before_Code': before_code, 'Refactor_Code': refactor_code})
                
        print(f"コミットメッセージ: {commit_message}")
        print("変更前と変更後のコードを commit_changes.csv に保存しました。")
    else:
        print(f"Failed to fetch commit details from {commit_url}. Status code: {commit_response.status_code}")
else:
    print("Invalid GitHub commit URL format.")
