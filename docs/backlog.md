# DataGuard 未完成項目清單

**建立日期：2026-05-17**
**目前狀態：178 tests passing，97% coverage**

本文件記錄目前已完成的原始缺口、仍建議改善的項目與保留不更動的設計決策，
供下一位工程師接手時快速了解剩餘工作。

---

## 一、已完成的原始功能與 fixture 缺口

### 1. 自動偵測檔案編碼（encoding detection）- 已完成

**說明：**
`CsvParser.parse()` 與 `JsonParser.parse()` 已在未傳入 encoding 時呼叫 `detect_encoding()`。
目前已有 UTF-16LE CSV / JSON validate integration coverage。

**狀態：**
已完成，暫無需修改。

### 2. Schema `type: float` 驗證器 - 已完成

**說明：**
已新增 `FloatValidator`，registry 已支援 `type: float`，並有 unit tests。
`schemas/employees.yaml` 也已加入 optional `score` float 欄位，並有 integration test 覆蓋。

**狀態：**
已完成，暫無需修改。

---

### 3. `clean/edge/` fixtures - 已完成

**說明：**
`tests/fixtures/clean/edge/` 已存在，並包含 CSV / JSON / JSONL 空輸入 fixtures。

**狀態：**
已完成，暫無需修改。

---

### 4. `convert/invalid/` fixtures - 已完成

**說明：**
`tests/fixtures/convert/invalid/` 已存在，並包含 JSON 語法錯誤與 invalid root fixture。

**狀態：**
已完成，暫無需修改。

---

### 5. `csv_clean_invalid.csv` integration test - 已完成

**說明：**
`tests/integration/test_clean_flow.py` 已引用 `csv_clean_invalid.csv`，並覆蓋 invalid CSV clean flow。

**狀態：**
已完成，暫無需修改。

---

## 二、保留但目前不更動的設計項目

### 6. `case_sensitive` 欄位保留但目前不更動

**說明：**
`src/dataguard/schema/models.py` 的 `ColumnSchema` 有 `case_sensitive: bool = True`，
但 `EnumValidator` 和 `StringValidator` 都沒有讀取此欄位。
使用者在 schema 設定 `case_sensitive: false` 不會有任何效果。

**目前決策：**
此欄位使用機會不高，先保留為未來擴充保留欄位，但目前不實作、不移除，也不更動現有大小寫敏感驗證行為。README 已同步註記此限制。

---

### 7. `WARNING` level 保留但目前不更動

**說明：**
`ValidationResult.level` 支援 `Literal["PASS", "WARNING", "ERROR"]`，
`assemble_report()` 也計算 `warning_count`，
但目前沒有任何 validator 產生 `level="WARNING"`，report 中的 `warning_count` 永遠為 0。

**目前決策：**
此功能使用機會不高，先保留 report/model 結構相容性，但目前不定義 warning 規則、不產生 warning，也不移除 `WARNING`。README 已同步註記此限制。

---

## 三、已完成的測試缺口

### 8. Boolean schema 缺少 `true_values` / `false_values` 的錯誤測試 - 已完成

**說明：**
`tests/unit/schema/test_loader.py` 已驗證缺少 `true_values` / `false_values` 會拋出 `SchemaFailure`。

---

### 9. Schema registry 拒絕未知型別的測試 - 已完成

**說明：**
`tests/unit/schema/test_registry.py` 已驗證未知 `type` 會拋出 `ValueError`。

---

### 10. Transformer loader 傳遞 `FileNotFoundError` 的測試 - 已完成

**說明：**
`tests/unit/transformer/test_transformer_loader.py` 已驗證 missing transform config 會傳遞 `FileNotFoundError`。

---

## 四、已完成的 CLI 錯誤處理改善

### 11. 輸出錯誤處理 - 已完成

**說明：**
`src/dataguard/exceptions.py` 已定義 `OutputFailure`，CLI 寫 output/report 失敗時已轉成清楚的 `click.ClickException`。

**狀態：**
已完成，並新增 CLI tests 覆蓋 `validate` report、`clean` output/report、`convert` output 寫入失敗情境。

---

## 五、目前仍建議改善的項目

### 12. README transformer 清單與目前功能同步

**說明：**
README 的 transformer operations 清單已同步目前程式，包含 `field_map` 與 `date_format`。

**狀態：**
已完成，暫無需修改。

### 13. 補 coverage 小缺口 - 已完成

**說明：**
目前 coverage 為 97%，缺口主要集中在 schema loader 異常路徑、reporter unknown format、transformer 少數錯誤分支。

**已完成內容：**
- ✅ 補 schema loader invalid YAML / invalid schema shape tests (4 個測試)
- ✅ 補 reporter unknown format test (4 個測試)
- ✅ 補 transformer unsupported option error branch tests (6 個測試)

**新增測試檔案：**
- `tests/unit/schema/test_loader.py` +4 tests (YAML 解析錯誤、schema 結構錯誤、columns 結構錯誤、不支援 format)
- `tests/unit/reporter/test_reporter_init.py` +4 tests (JSON/Text 格式返回，未知格式錯誤處理)
- `tests/unit/transformer/test_type_cast.py` +2 tests (不支援的目標類型)
- `tests/unit/transformer/test_dedup.py` +2 tests (不支援的 keep 模式)
- `tests/unit/transformer/test_fill_missing.py` +2 tests (不支援的填補策略)

**狀態：**
已完成 (Issue #29 / PR #29, 2026-06-02)，測試覆蓋率約提升 2-4%。

---

## 優先建議執行順序

| 優先 | 項目 | 理由 |
|------|------|------|
| ✅ 完成 | #13 補 coverage 小缺口 | 提升 schema/reporter/transformer error branch 信心 |
| 保留 | #6 case_sensitive | 保留但目前不更動、不實作 |
| 保留 | #7 WARNING level | 保留但目前不更動、不產生 warning |

## 較大的 future work

- Excel input
- streaming large files
- datetime validator
