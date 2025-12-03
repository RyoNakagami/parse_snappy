# Release Notes: {{RELEASE_VERSION}}

> このリリースは **beta-release-{{BETA_VERSION}}** での最終調整を反映した main リリースです。  
> 新機能追加は含まず、バージョン番号更新・リリースノート・微修正・テスト済み修正が中心です。

---

## 1. Version

- Main release version: `{{RELEASE_VERSION}}`
- Git tag: `v{{RELEASE_VERSION}}`

---

## 2. Summary / 概要

- バージョン番号更新 (`__version__.py`)  
- リリースノート更新  
- ドキュメント・サンプルコードの軽微な修正  
- 最終テストで確認された微修正  

> 注意: 新機能や大きな改善（enhance / feature）は develop ブランチで完了済みで、このリリースには含まれません。

---

## 3. Changelog / 修正点

### 修正 / Fixed

- NaN / inf / negative inputs の処理を安定化  
- サンプルコード・ドキュメントの typo 修正  
- 統計計算における minor rounding error 修正  

### Deprecated / 廃止予定

- なし

### Breaking Changes / 互換性注意

- なし（beta-release での最終微調整のみ）

---

## 4. Testing & Validation / テスト

- [ ] 単体テスト (pytest / unittest) 通過  
- [ ] 統計計算結果の確認済み（推定値・検定統計量の再現性）  
- [ ] Edge cases（NaN, inf, negative values）確認済み  
- [ ] ドキュメント・サンプルコードの動作確認済み  
