# Progress Report — 2026-05-17

## 本期開發重點

Week 12 完成三條核心 CLI flow 與 GitHub 工作流程正規化後，本期的目標是**補齊所有原始設計規格中尚未完成的功能**，並同時對文件與程式之間的已知衝突進行系統性修正。

開發方式延續 Issue → branch → PR → CI → merge 的流程。本期共完成 5 個功能 PR、1 個文件對齊 PR，以及 2 份文件更新，測試數從 100 成長至 125，覆蓋率維持 95%。

---

## 已完成功能

### Issue #5：補齊剩餘 Transformer 操作

Phase 3 設計文件定義了完整的 transformer 功能集，但 Week 12 結束時仍有四個操作尚未實作。本次全數補齊：

**`date_format` transformer（新增）**

`src/dataguard/transformer/date_format.py` 新增 `date_format()` 函式。
支援 `source_formats` 列表，依序嘗試解析；第一個成功的格式即轉換為 `target_format`。
所有格式都無法解析時保留原始值，不中斷流程。欄位缺失時靜默略過。

```yaml
transforms:
  - operation: date_format
    column: join_date
    source_formats: ["%Y/%m/%d", "%m-%d-%Y"]
    target_format: "%Y-%m-%d"
```

**`fill_missing` 擴充：`forward_fill` 與 `mean` 策略**

`src/dataguard/transformer/fill_missing.py` 新增兩個策略：
- `forward_fill`：空值欄位填入前一筆非空值；第一列就是空值時保留原始值
- `mean`：計算欄位所有有效數值的平均值後填補；無有效數值時保留原始值

**`dedup` 擴充：`keep=none` 策略**

`src/dataguard/transformer/dedup.py` 新增 `keep=none`：
只要 key 有重複，所有相關列全部刪除，不保留任何一筆。
與 `keep=first`（保留第一筆）、`keep=last`（保留最後一筆）並列為三種去重模式。

**整合測試**

新增 `csv_transformer_full_valid.csv` 與 `transformer_full_transforms.yaml` fixture，
驗證 `dedup → date_format → fill_missing → type_cast` 四種操作組合使用的 end-to-end 流程。

---

### Issue #7：補齊 Phase 5 Fixture 與 Integration Test 缺口

對照 Phase 5 設計文件的 fixture matrix，補齊所有缺少的 fixture 與對應測試：

**新增 fixture：**
- `tests/fixtures/validate/invalid/json_employees_invalid.json`
- `tests/fixtures/validate/invalid/jsonl_employees_invalid.jsonl`
- `tests/fixtures/validate/edge/csv_employees_edge_empty.csv`
- `tests/fixtures/convert/edge/csv_convert_edge_empty.csv`
- `tests/fixtures/convert/edge/jsonl_convert_edge_bad_line.jsonl`
- `tests/fixtures/clean/valid/json_clean_valid.json`
- `tests/fixtures/clean/invalid/json_clean_invalid.json`
- `tests/fixtures/clean/invalid/jsonl_clean_invalid.jsonl`

**新增 integration tests：**
- `validate`：JSON invalid、JSONL invalid、empty CSV
- `convert`：empty CSV 輸出空結果、JSONL 壞行跳過有效行繼續轉換
- `clean`：JSON valid 輸入、JSON invalid 過濾、JSONL invalid 過濾

---

### Issue #9：對齊 Phase 4 與 CLI 文件規格

透過比對五份設計文件（Phase 1-5、CLI Flows、Phase 4）與目前程式行為，找出六個文件與程式的衝突點。本次修正其中五個純文件衝突，不改動任何程式碼：

- **Exit code**：Phase 4 原寫 runtime errors 使用 exit code `2`，統一改為 `1`（CLI usage error 保留 `2`）
- **`--report` 必填**：Phase 4 原標示為選填，更新為必填
- **convert JSONL 行為**：CLI Flows 文件隱含 parse error 應 exit `1`，明確補充 JSONL 採用 best-effort conversion
- **clean 流程順序**：Phase 4 原描述為先 validate 再 transform，更新為目前實際流程：transform → validate → filter → output
- **JSON report 範例**：CLI Flows 文件範例為舊格式，更新為目前 `render_json_report()` 的實際輸出結構

---

### Issue #11：補上 Text Report Error Summary 區段

`src/dataguard/reporter/text_report.py` 的 `render_text_report()` 新增 Error Summary 區段，
列出各欄位的錯誤代碼與計數，與 JSON report 的 `error_summary` 對齊。
只有在 `report.error_summary` 不為空時才輸出此區段。

```
Error Summary:
  age: INVALID_INTEGER x2, OUT_OF_RANGE x1
  status: INVALID_ENUM x1
```

---

### Issue #13：`clean` 輸出支援 JSON / JSONL 格式

`src/dataguard/cli.py` 的 `clean` command 移除原本寫死的 `write_csv_output()`，
改為呼叫已存在的 `get_output_writer()` factory，依 `--output` 副檔名自動選擇輸出格式。

這讓 `clean` 的輸出行為與 `convert` 對齊：

```bash
# 輸出 CSV
dataguard clean ... --output clean.csv

# 輸出 JSON
dataguard clean ... --output clean.json

# 輸出 JSONL
dataguard clean ... --output clean.jsonl
```

---

## 文件更新

### docs 目錄結構重組

將 `docs/plan/` 改為 `docs/weekly-plans/`，`docs/plans/` 改為 `docs/project-specs/`，
週報從根目錄移至 `docs/progress-reports/` 並統一命名（移除 `draft` 後綴，統一兩位數週次）。

### user-stories.md 更新

補充本期所有新功能的使用情境說明：
- User Story 2（text report）：新增 Error Summary 輸出範例
- User Story 5（clean）：更新輸出格式說明支援 CSV / JSON / JSONL
- User Story 6（dedup）：補上 `keep: none` 說明
- User Story 7（fill_missing）：補上 `forward_fill` 和 `mean` 策略
- 新增 User Story 11：date_format transformer
- 新增 User Story 12：clean 輸出 JSON / JSONL 格式

### backlog.md 建立

整理目前已知但尚未完成的功能缺口、Phase 5 fixture 缺口與設計遺留問題，
附上優先執行順序建議，供後續工程師接手時參考。

---

## 開發方法

本期延續測試驅動開發（TDD）。每個新功能都先寫失敗的 unit tests，確認 RED，再實作最小版本，確認 GREEN，最後補整合測試。

所有功能都透過 GitHub Issue → branch → PR → CI → merge 流程推進，`main` 在整個開發期間保持可通過測試的狀態。

---

## 測試結果

最新一次完整驗證使用：

`UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`

```
125 passed
Coverage 95%
```

| 里程碑 | 測試數 |
|--------|--------|
| Week 12 結束 | 100 |
| Issue #5（transformer 補齊） | 113 |
| Issue #7（Phase 5 fixtures） | 121 |
| Issue #11（text report error summary） | 123 |
| Issue #13（clean output formats） | 125 |

---

## 目前專案狀態

目前專案已具備：

- `validate`、`clean`、`convert` 三條完整 CLI workflow
- CSV / JSON / JSONL 輸入；CSV / JSON / JSONL 輸出
- JSON 與 text 兩種報告格式（text 含 Error Summary）
- 完整 transformer 層：`type_cast`、`date_format`、`fill_missing`（4 種策略）、`dedup`（3 種模式）、`field_map`（rename + drop）
- Phase 5 設計的 fixture matrix 大部分完成
- Phase 4 / CLI Flows 設計文件已與實際程式行為對齊
- 125 個自動化測試，覆蓋率 95%
- `docs/backlog.md` 記錄所有已知未完成項目

剩餘工作詳見 `docs/backlog.md`。
