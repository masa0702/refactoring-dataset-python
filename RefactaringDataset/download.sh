mkdir data
cd data
wget http://refactoring.encs.concordia.ca/oracle/api.php?json

# 新しいファイル名と拡張子を設定
new_filename="refactoring_oracl"
new_extension=".json"

# ファイルをリネーム
mv api.php?json "$new_filename$new_extension"