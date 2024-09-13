# Desynced MOD Localization Extractor

## Description
Desynced MOD Localization Extractor is a Python script that extracts translatable strings from Desynced MOD files and generates localization templates.

### Features
- Extract strings from multiple MOD ZIP files
- Duplicate removal based on comparison with existing language files
- Generate JSONC files for multi-language support
- Handle comments in JSON

### Usage
```
python desynced_localization_extractor.py <MOD_ZIP_FILE> [<MOD_ZIP_FILE> ...] [--base_lang BASE_LANG_FILE] [--lang LANG_CODE]
```

### Options
- `<MOD_ZIP_FILE>`: MOD ZIP file to process (multiple files can be specified)
- `--base_lang BASE_LANG_FILE`: Base language file for comparison (often found in `mods/main.zip` under the `languages` folder.)
- `--lang LANG_CODE`: Language code for output (default: `en`)

### License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

## 概要
Desynced MOD Localization Extractor は、Desynced ゲームのMODファイルから翻訳可能な文字列を抽出し、ローカライゼーションテンプレートを生成するPythonスクリプトです。

### 機能

- 複数のMODのZIPファイルから文字列を抽出
- 既存の言語ファイルとの比較による重複をチェックして削除

### 使用方法
```
python desynced_localization_extractor.py <MOD_ZIP_FILE> [<MOD_ZIP_FILE> ...] [--base_lang BASE_LANG_FILE] [--lang LANG_CODE]
```


### オプション

- `<MOD_ZIP_FILE>`: 処理するMOD ZIPファイル（複数指定可）
- `--base_lang BASE_LANG_FILE`: 比較対象の基本言語ファイル（通常は`mods/main.zip` 内の `languages` フォルダにjsonが格納されています。）
- `--lang LANG_CODE`: 出力する言語コード（デフォルト: `en`）

### ライセンス

このプロジェクトは Apache License 2.0 のもとで公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

---
