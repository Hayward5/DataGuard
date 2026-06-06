# Post-Week 12 Issue/PR Progress Report

## Purpose

Week 12 之後，DataGuard 的開發方式從每週進度文件改為 GitHub issue-driven workflow。
所有新增功能、bug fix、fixture 補強、文件對齊與測試覆蓋改善，都透過以下流程完成：

```text
Issue -> branch -> PR -> CI/test verification -> merge to main
```

本文件整理 Week 12 之後已關閉的 issues 與相對應的 merged PRs，讓後續開發者可以快速理解每一項變更的目的、實作內容與測試結果。

---

## Overall Progress Summary

從 Issue #1 到 Issue #29，專案完成了 15 組 issue/PR 工作項目。
這些工作把 DataGuard 從 Week 11 的三條基本 CLI flow，推進到更完整的資料品質工具：

- reporting 從 JSON-only 擴充為 JSON + text，並加入 Error Summary
- transformer layer 從基礎操作擴充為完整 cleaning pipeline
- parser 與 CLI runtime 對壞輸入、非 UTF-8、空輸入與寫檔失敗有更清楚的處理
- schema validation 新增 `type: float`
- test fixtures 從 happy path 擴充到 valid / invalid / edge / error-path coverage
- docs 與實際 CLI 行為重新對齊

目前 main branch 的本地驗證結果：

```text
178 tests passed
97% coverage
```

驗證指令：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run --extra dev pytest -q
```

---

## Issue/PR Timeline

### Issue #1 / PR #2 — Text Report Output

**Issue:** `feat: add text report output`

**PR:** `feat: add text report output`

**Goal**

讓 `validate` 和 `clean` 支援 `--format text`，讓使用者可以直接閱讀純文字 validation report，而不只輸出 JSON。

**Completed Work**

- 新增 `render_text_report()`
- 新增 `get_report_renderer()` factory
- 將 `validate` 與 `clean` 的 `--format` 擴充為 `json|text`
- 保持 `json` 作為預設值，避免破壞既有行為
- 新增 text report unit tests 與 CLI integration tests

**Main Impact**

Reporting layer 從 machine-readable JSON 擴充為同時支援 human-readable text。

**PR Verification**

```text
90 passed
95% coverage
```

---

### Issue #3 / PR #4 — Field Map Transformer

**Issue:** `feat: add field map transformer`

**PR:** `feat: add field map transformer`

**Goal**

新增 `field_map` transformer，讓 `clean` 可以在 YAML transform config 中重命名欄位與刪除不需要的欄位。

**Completed Work**

- 新增 `src/dataguard/transformer/field_map.py`
- 支援 `rename`：來源欄位名稱轉為目標欄位名稱
- 支援 `drop`：移除指定欄位
- 在 transformer engine registry 註冊 `field_map`
- 新增 field_map unit tests
- 新增 clean integration test 與對應 fixture/config

**Main Impact**

Transformer layer 補上欄位結構控制能力，讓 clean flow 可以處理來源資料欄位名稱不一致的情境。

**PR Verification**

```text
100 passed
95% coverage
```

---

### Issue #5 / PR #6 — Remaining Transformer Operations

**Issue:** `feat: 補齊剩餘 transformer 操作`

**PR:** `feat: 補齊剩餘 transformer 操作`

**Goal**

補齊 Phase 3 設計中尚未完成的 transformer 行為，讓 cleaning pipeline 更完整。

**Completed Work**

- 新增 `date_format`
- `fill_missing` 新增 `forward_fill`
- `fill_missing` 新增 `mean`
- `dedup` 新增 `keep=none`
- 在 transformer engine 註冊 `date_format`
- 新增 unit tests 與 combined transformer integration test
- 新增 `csv_transformer_full_valid.csv`
- 新增 `transformer_full_transforms.yaml`

**Main Impact**

Clean flow 從基本資料修正，擴充為可組合的完整 transformation pipeline。

**PR Verification**

```text
113 passed
0 failed
```

---

### Issue #7 / PR #8 — Phase 5 Fixture and Integration Coverage

**Issue:** `test: 補齊 Phase 5 fixture 與 integration test 缺口`

**PR:** `test: 補齊 Phase 5 fixture 與 integration test 缺口`

**Goal**

補齊 validate、convert、clean 三個 flow 的 valid / invalid / edge fixtures 與 integration tests。

**Completed Work**

- validate 新增 JSON / JSONL invalid fixtures
- validate 新增 empty CSV edge fixture
- convert 新增 edge fixture 目錄與測試
- clean 新增 JSON valid fixture
- clean 新增 JSON / JSONL invalid fixtures
- 新增 validate / convert / clean integration tests

**Main Impact**

Integration coverage 從主要 happy path 擴充到更多格式與異常資料情境。

**PR Verification**

```text
121 passed
0 failed
```

---

### Issue #9 / PR #10 — Documentation Alignment

**Issue:** `docs: 對齊 Phase 4 與 CLI 文件規格`

**PR:** `docs: 對齊 Phase 4 與 CLI 文件規格`

**Goal**

將設計文件與目前已完成且測試覆蓋的 CLI 行為對齊。

**Completed Work**

- 將 runtime error exit code 對齊為 `1`
- 保留 CLI usage error exit code `2`
- 將 `validate` / `clean` 的 `--report` 文件改為必填
- 補上 convert JSONL best-effort behavior
- 將 clean flow 文件順序改為 `transform -> validate -> filter -> output/report`
- 更新 JSON report 範例為目前實際格式

**Main Impact**

降低文件與實作不一致的風險，讓後續開發者可以信任 project specs。

**PR Verification**

Documentation-only PR, no production code or tests changed.

---

### Issue #11 / PR #12 — Text Report Error Summary

**Issue:** `feat: 補上 text report Error Summary 區段`

**PR:** `feat: 補上 text report Error Summary 區段`

**Goal**

讓 text report 也輸出 `Error Summary`，與 JSON report 的 `error_summary` 對齊。

**Completed Work**

- 在 `render_text_report()` 新增 Error Summary 區段
- 只在 `report.error_summary` 不為空時顯示
- 新增 text report unit tests

**Main Impact**

Text report 不只列出逐筆錯誤，也能快速呈現「哪個欄位發生哪些錯誤」。

**PR Verification**

```text
123 passed
0 failed
```

---

### Issue #13 / PR #14 — Clean Output JSON / JSONL Support

**Issue:** `feat: clean 輸出支援 JSON / JSONL 格式`

**PR:** `feat: clean 輸出支援 JSON / JSONL 格式`

**Goal**

讓 `clean --output` 支援 `.csv`、`.json`、`.jsonl`，並依副檔名自動選擇 writer。

**Completed Work**

- `clean` 改用 `get_output_writer()`
- 移除固定使用 CSV writer 的限制
- 新增 JSON / JSONL clean output integration tests

**Main Impact**

Clean flow 的 output behavior 與 convert flow 的 writer factory 設計對齊。

**PR Verification**

```text
125 passed
0 failed
```

---

### Issue #15 / PR #16 — Core Test Gap Coverage

**Issue:** `feat : 補齊核心測試缺口`

**PR:** `test: 補齊核心測試缺口`

**Goal**

補齊既有核心行為的測試缺口，不新增 production behavior。

**Completed Work**

- clean invalid CSV integration test
- boolean schema 缺少 `true_values` / `false_values` 的 loader test
- unknown validator type 的 registry test
- missing transforms file 的 loader test

**Main Impact**

把已存在但尚未被測試保護的錯誤路徑納入 regression suite。

**PR Verification**

```text
129 passed
96% coverage
```

---

### Issue #17 / PR #18 — Parser Encoding Detection

**Issue:** `feat: 整合自動編碼偵測至 parser`

**PR:** `feat: 整合自動編碼偵測`

**Goal**

將既有 `detect_encoding()` 整合到 CSV / JSON parser，使 parser 可以處理非 UTF-8 輸入。

**Completed Work**

- `CsvParser.parse()` 在未指定 encoding 時呼叫 `detect_encoding()`
- `JsonParser.parse()` 在未指定 encoding 時呼叫 `detect_encoding()`
- 明確傳入 encoding 時優先使用指定值
- 新增 UTF-16LE CSV / JSON fixtures
- 新增 parser unit tests 與 validate integration tests

**Main Impact**

DataGuard 對真實世界多來源資料更穩定，不再假設所有輸入都是 UTF-8。

**PR Verification**

```text
135 passed
96% coverage
```

---

### Issue #19 / PR #20 — Float Validator

**Issue:** `feat: 新增 schema type: float 驗證器`

**PR:** `feat: 新增 schema type: float 驗證器`

**Goal**

讓 YAML schema 可以定義 `type: float` 欄位，並支援 min/max range validation。

**Completed Work**

- 新增 `FloatValidator`
- 在 validator registry 中加入 `type: float`
- 匯出 `FloatValidator`
- 新增 13 個 float validator unit tests
- 更新 registry tests

**Main Impact**

Schema validation 能驗證浮點數欄位，補齊與 `type_cast target_type: float` 之間的功能落差。

**PR Verification**

```text
148 passed
```

---

### Issue #21 / PR #22 — JSON / JSONL Root Validation

**Issue:** `feat: 補強 JSON / JSONL parser 根結構驗證`

**PR:** `feat: 補強 JSON / JSONL parser 根結構驗證`

**Goal**

讓 JSON / JSONL parser 明確驗證輸入結構，避免錯誤資料靜默傳入下游。

**Completed Work**

- JSON root 不是 array 時拋出 `ParseFailure`
- JSON array 內非 object 元素記為 `ParseErrorItem`
- JSONL 每行解析後非 dict 時記為 `ParseErrorItem`
- 新增 parser unit tests
- 新增 validate / convert CLI integration tests

**Main Impact**

Parser layer 從只檢查 JSON syntax，提升為同時檢查 root shape 與 row shape。

**PR Verification**

```text
154 passed
```

---

### Issue #23 / PR #24 — Clean Edge Fixtures and Empty Input Handling

**Issue:** `test: 補齊 clean/edge/ fixtures 與空輸入整合測試`

**PR:** `Issue 23 clean edge fixtures`

**Goal**

新增 clean edge fixtures，並驗證 clean flow 對 0 筆資料的行為。

**Completed Work**

- 新增 `tests/fixtures/clean/edge/`
- 新增 empty CSV / JSON / JSONL fixtures
- 新增 clean empty input integration tests
- 修正 JSON parser 對空內容的處理：0 bytes 回傳 0 筆 records，而非 fatal parse failure
- 補齊 empty content unit tests

**Main Impact**

Clean flow 可以穩定處理空輸入，這是資料 pipeline 常見但容易被忽略的 edge case。

**PR Verification**

```text
159 passed
```

---

### Issue #25 / PR #26 — Convert Invalid Fixtures

**Issue:** `test: 補齊 convert/invalid/ fixtures 與具名錯誤情境測試`

**PR:** `test: 補齊 convert/invalid/ fixtures，改用具名 fixture 取代 tmp_path`

**Goal**

將 convert 錯誤情境測試從即時建立 tmp files 改為具名 fixtures，提高可讀性與維護性。

**Completed Work**

- 新增 `tests/fixtures/convert/invalid/`
- 新增 `json_convert_invalid_syntax.json`
- 新增 `json_convert_invalid_root.json`
- 更新 convert integration tests 使用具名 fixtures

**Main Impact**

錯誤情境 fixture 被正式納入 repo，後續開發者可以直接看到 invalid input 長什麼樣。

**PR Verification**

```text
159 passed
```

---

### Issue #27 / PR #28 — Output Write Failure Handling

**Issue:** `fix: 補強 CLI 輸出寫入失敗的錯誤處理`

**PR:** `fix: 補強 CLI 輸出寫入錯誤處理`

**Goal**

讓 CLI 在 output/report 寫入失敗時，回傳清楚一致的 user-facing error，而不是底層 Python I/O exception。

**Completed Work**

- 新增 `_write_report_file()`
- 新增 `_write_output_file()`
- 將寫檔 `OSError` 包成 `OutputFailure`
- 在 CLI command 邊界轉成 `click.ClickException`
- 新增 4 個 CLI tests 覆蓋 validate / clean / convert 寫檔失敗

**Main Impact**

Runtime failure handling 更完整，使用者能看到明確訊息：

```text
Failed to write report file: <path>
Failed to write output file: <path>
```

**PR Verification**

```text
163 passed
96% coverage
```

---

### Issue #29 / PR #30 — Coverage Error-Path Tests

**Issue:** `補充 coverage 缺口：schema loader、reporter 與 transformer 錯誤路徑測試`

**PR:** `test: 新增 coverage 錯誤路徑測試，補強 schema loader、reporter 與 transformer 錯誤處理`

**Goal**

補強 schema loader、reporter、transformer 的錯誤處理路徑測試，提升 coverage 並保護 failure behavior。

**Completed Work**

- 新增 schema loader 異常路徑測試
  - invalid YAML
  - non-dict schema
  - non-list columns
  - unsupported format
- 新增 reporter unknown format tests
- 新增 transformer unsupported option tests
  - unsupported `type_cast target_type`
  - unsupported `dedup keep`
  - unsupported `fill_missing strategy`
- 更新 `nextstep.txt`
- 更新 `docs/backlog.md`

**Main Impact**

測試重點從功能 happy path 擴充到 error path，降低後續修改破壞錯誤處理邏輯的風險。

**PR Verification**

PR 內記錄新增 14 個 error-path tests，並要求完整 pytest 與 CI 通過。
目前 main branch 本地驗證為：

```text
178 passed
97% coverage
```

---

## Category Summary for Future Developers

### Reporting

- Issue #1 / PR #2: 新增 text report
- Issue #11 / PR #12: text report 新增 Error Summary

Reporter layer 現在支援 JSON 與 text，並透過 `get_report_renderer()` 分派。

### Transformer Capability

- Issue #3 / PR #4: 新增 `field_map`
- Issue #5 / PR #6: 補齊 `date_format`、`forward_fill`、`mean`、`keep=none`

Transformer layer 現在可透過 YAML config 組合多個 record-to-record operations。

### Parser and Runtime Robustness

- Issue #17 / PR #18: encoding detection
- Issue #21 / PR #22: JSON / JSONL root validation
- Issue #23 / PR #24: empty input handling
- Issue #27 / PR #28: output/report write failure handling

這些變更讓 DataGuard 對壞輸入、空輸入、非 UTF-8 與寫檔失敗更穩定。

### Schema Validation

- Issue #19 / PR #20: 新增 `type: float`

Schema layer 現在支援 string、integer、float、enum、boolean、date format 與 strict unknown-column checks。

### Fixtures, Coverage, and Docs

- Issue #7 / PR #8: Phase 5 fixtures and integration tests
- Issue #9 / PR #10: docs alignment
- Issue #13 / PR #14: clean output JSON / JSONL support
- Issue #15 / PR #16: core test gaps
- Issue #25 / PR #26: convert invalid fixtures
- Issue #29 / PR #30: coverage error-path tests

這些工作讓測試資料、文件與實際行為更一致，也讓 regression suite 更完整。

---

## Final State After Issue/PR Work

截至目前 main branch，DataGuard 已具備：

- three CLI workflows: `validate`, `clean`, `convert`
- JSON and text validation reports
- Error Summary in both report paths
- CSV / JSON / JSONL parsing and output writing
- encoding detection for parser input
- schema validators including `float`
- strict schema checking for unknown columns
- five transformer operations:
  - `field_map`
  - `dedup`
  - `date_format`
  - `fill_missing`
  - `type_cast`
- clean output in CSV / JSON / JSONL
- parser-level handling for invalid JSON roots and non-object rows
- runtime write failure handling through clear CLI errors
- named fixtures for valid / invalid / edge cases
- 178 passing tests and 97% coverage

The most important process change is that each meaningful post-Week 12 change is traceable through a closed issue, a merged PR, and a verification record. This makes the repository easier to audit, explain, and continue developing.
