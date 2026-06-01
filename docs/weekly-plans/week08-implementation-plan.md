# Week 8 Implementation Plan: Validate Rule Expansion

## Summary

Week 8 延續 `week7-scaffold` 的開發模式，聚焦在單一垂直切片 `validate`，不同時展開 `clean` 或 `convert`。

本週目標不是做更多流程，而是把 `validate` 從「最小可跑」提升到「有代表性的 schema 驗證能力 + 更完整的測試證據」。

建議本週 branch：
- `week8-validate-rules`

建議開發節奏：
- 每個功能一組 `test:` commit
- 緊接一組對應的 `feat:` commit
- 每次只完成一個可驗證行為
- 每完成一組 validator 或一組整合測試就 push 一次

Week 8 收尾標準：
- 全套 `pytest` 通過
- `validate` 支援更多 validator
- JSON report 能反映新錯誤碼與摘要
- 有可展示的測試證據與 fixtures

---

## Week 8 Scope

本週只做 `validate` 擴充，主功能分成 4 組：

1. `string` 規則補強
2. `enum` 驗證
3. `boolean` 驗證
4. `date/format` 驗證

同時補強 3 類 engine 行為：

1. optional 欄位空值時不跑後續 validator
2. `required` 失敗時不重複報其他型別錯誤
3. parser error 與 validation result 的整合方向要先定義清楚，並至少在測試中覆蓋 validate flow 的行為

---

## Feature Breakdown

### 1. String Validation Enhancement

目標：
- 讓 `string` validator 除了 `pattern` 外，也支援 `min_length`、`max_length`

需要支援的 schema 欄位：
- `min_length`
- `max_length`
- `pattern`

預期行為：
- 長度小於 `min_length` 時回傳 error
- 長度大於 `max_length` 時回傳 error
- `pattern` 不符合時回傳 error
- optional 欄位若值為空，不報長度或 pattern 錯誤

建議錯誤碼：
- `STRING_TOO_SHORT`
- `STRING_TOO_LONG`
- `PATTERN_MISMATCH`

---

### 2. Enum Validation

目標：
- 使用 schema 的 `values` 讓欄位只能接受固定集合中的值

需要支援的 schema 欄位：
- `values`
- `case_sensitive`

目前決策註記：
- `case_sensitive` 保留在 schema/model 設計中，但目前不實作大小寫不敏感比對，也不更動現有大小寫敏感行為。

預期行為：
- 值存在於 `values` 中時通過
- 值不在 `values` 中時失敗
- 若未特別處理，先採 `case_sensitive: true` 為預設
- optional 欄位空值時略過

建議錯誤碼：
- `INVALID_ENUM`

建議範例欄位：
- `status`
  - `ACTIVE`
  - `INACTIVE`
  - `LEAVE`

---

### 3. Boolean Validation

目標：
- 使用 schema 的 `true_values` / `false_values` 驗證布林欄位

需要支援的 schema 欄位：
- `true_values`
- `false_values`

預期行為：
- 值在 `true_values` 內時通過
- 值在 `false_values` 內時通過
- 其他值失敗
- optional 欄位空值時略過

建議錯誤碼：
- `INVALID_BOOLEAN`

建議範例欄位：
- `is_active`
  - true set: `["true", "1", "yes", "Y"]`
  - false set: `["false", "0", "no", "N"]`

---

### 4. Date / Format Validation

目標：
- 先加入一種清楚、可測、適合展示的日期格式驗證

建議本週採用方式：
- `type: string`
- `format: date`

預期行為：
- 僅接受固定日期格式
- 本週先不要做多格式解析與轉換
- optional 欄位空值時略過

建議固定格式：
- `%Y-%m-%d`

建議錯誤碼：
- `INVALID_DATE_FORMAT`

建議範例欄位：
- `join_date`

---

## Engine Behavior Changes

### 1. Required Precedence

目標：
- `required` 錯誤優先於其他 validator

預期行為：
- 若欄位缺失或值為空，直接產生 `REQUIRED_MISSING`
- 不再對同欄位繼續做 `string`、`enum`、`boolean`、`date` 驗證

---

### 2. Optional Empty Handling

目標：
- optional 欄位若沒有值，不應產生型別錯誤

預期行為：
- 欄位不存在或值為空時，若 `required=False`，直接略過驗證
- 不產生 `INVALID_ENUM`、`INVALID_BOOLEAN`、`INVALID_DATE_FORMAT` 等錯誤

---

### 3. Result Shape Stability

目標：
- 維持目前 `validate` 的輸出模型穩定，讓 Week 8 只是擴規則，不破壞既有 JSON report 結構

預期行為：
- 每個錯誤仍保留：
  - `row`
  - `column`
  - `value`
  - `level`
  - `code`
  - `message`
- `error_summary` 能正確統計新錯誤碼

---

## Files and Modules Impacted

主要會碰到的模組：

- `src/dataguard/schema/validators/string.py`
- `src/dataguard/schema/validators/`
- `src/dataguard/schema/registry.py`
- `src/dataguard/schema/engine.py`
- `schemas/employees.yaml`
- `tests/unit/schema/validators/`
- `tests/unit/schema/`
- `tests/integration/test_validate_flow.py`
- `tests/fixtures/validate/`

本週不碰：
- `transformer/`
- `convert`
- `clean`

---

## Week 8 Commit Strategy

延續 Week 7 的模式，採小步提交。

建議 commit sequence：

1. `test: add string length validation cases`
2. `feat: add min and max length checks for string validator`

3. `test: add enum validator cases`
4. `feat: add enum schema validator`

5. `test: add boolean validator cases`
6. `feat: add boolean schema validator`

7. `test: add date format validator cases`
8. `feat: add date format validation`

9. `test: add engine handling cases for required and optional fields`
10. `feat: refine validation engine precedence and empty handling`

11. `test: add validate integration cases for week8 rules`
12. `feat: extend validate fixtures and schema for week8 coverage`

13. `chore: document week8 testing evidence`

原則：
- 一次 commit 只做一個小功能
- `test:` 永遠先於對應 `feat:`
- fixture 和 schema 若只是支援測試，可放在 `test:` 或 `chore:`
- 每完成一組 validator 就 push

---

## Testing Strategy

Week 8 要明確使用以下 software testing 方法：

### 1. Test-Driven Development (TDD)

每個功能固定流程：

1. 先寫 failing test
2. 跑單一測試確認失敗原因正確
3. 補最小實作
4. 跑單一測試確認通過
5. 跑相關模組測試
6. 跑全套測試避免回歸
7. commit

---

### 2. Equivalence Class Testing

每個 validator 至少測三類：

- valid
- invalid
- empty or optional

例子：
- enum
  - `ACTIVE` -> pass
  - `UNKNOWN` -> fail
  - `""` with optional column -> skip / pass

---

### 3. Boundary Value Testing

主要用在：

- `min_length`
- `max_length`

例子：
- `min_length = 3`
  - 長度 2 -> fail
  - 長度 3 -> pass
  - 長度 4 -> pass

- `max_length = 8`
  - 長度 7 -> pass
  - 長度 8 -> pass
  - 長度 9 -> fail

---

### 4. Input Space Partitioning

依輸入來源和情境切測試空間：

- CSV
- JSON
- JSONL

每種格式至少包含：
- valid
- invalid
- edge

---

### 5. Integration Testing

用 `click` CLI flow 驗證整條 `validate` 路徑：

- parser
- schema loader
- validator
- engine
- reporter
- CLI exit code

---

### 6. Regression Testing

每完成一個小功能就回跑：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

目標：
- 新功能通過
- 舊功能不退化

---

## Detailed Test Plan

### A. Unit Tests: String Validator

測試案例：
- pattern match -> `OK`
- pattern mismatch -> `PATTERN_MISMATCH`
- length below min -> `STRING_TOO_SHORT`
- length equal min -> `OK`
- length above max -> `STRING_TOO_LONG`
- length equal max -> `OK`

---

### B. Unit Tests: Enum Validator

測試案例：
- value in allowed set -> `OK`
- value not in allowed set -> `INVALID_ENUM`
- optional empty value -> skip / `OK`
- case sensitivity behavior -> 明確驗證一次

---

### C. Unit Tests: Boolean Validator

測試案例：
- true set value -> `OK`
- false set value -> `OK`
- invalid token -> `INVALID_BOOLEAN`
- optional empty value -> skip / `OK`

---

### D. Unit Tests: Date Format Validator

測試案例：
- valid `YYYY-MM-DD` -> `OK`
- invalid separator -> `INVALID_DATE_FORMAT`
- invalid date string -> `INVALID_DATE_FORMAT`
- optional empty value -> skip / `OK`

---

### E. Registry Tests

測試案例：
- enum schema returns enum validator
- boolean schema returns boolean validator
- date/format schema returns correct validator
- unsupported validator type still raises error

---

### F. Engine Tests

測試案例：
- required missing -> `REQUIRED_MISSING`
- required missing does not trigger secondary type error
- optional empty field does not trigger validator error
- mixed valid / invalid / missing records all handled correctly

---

### G. Integration Tests

至少加入以下情境：

1. valid CSV with new rule fields -> exit code `0`
2. invalid CSV enum value -> exit code `1`
3. invalid CSV boolean value -> exit code `1`
4. invalid CSV date format -> exit code `1`
5. valid JSON -> exit code `0`
6. valid JSONL -> exit code `0`
7. malformed JSONL line + validation errors -> report still valid JSON
8. `--limit` limits detail output count
9. `error_summary` includes new error codes

---

## Schema and Fixture Plan

### Schema Update

擴充 `schemas/employees.yaml`，加入下列示範欄位：

- `employee_id`
  - string + pattern
- `name`
  - string + `min_length` / `max_length`
- `status`
  - enum values
- `is_active`
  - boolean true/false sets
- `join_date`
  - string + `format: date`
- `age`
  - integer + range

---

### Fixture Plan

在 `tests/fixtures/validate/` 擴充：

- `valid/csv_employees_valid.csv`
- `invalid/csv_employees_invalid.csv`
- `valid/json_employees_valid.json`
- `invalid/json_employees_invalid.json`
- `valid/jsonl_employees_valid.jsonl`
- `edge/jsonl_employees_edge_bad_line.jsonl`

fixtures 要覆蓋：
- enum 非法值
- boolean 非法 token
- 日期格式錯誤
- 長度不足 / 過長
- optional 空值
- JSONL 壞行

---

## Verification Commands

單一功能開發時建議使用：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/validators/test_string.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/validators/test_numeric.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/unit/schema/test_engine.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/integration/test_validate_flow.py -q
```

收尾驗證：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

---

## Week 8 Deliverables

Week 8 完成後應能明確展示：

- `validate` 已不只支援 `string` / `integer`
- 已新增 `string length`、`enum`、`boolean`、`date format`
- engine 已處理 required precedence 與 optional empty behavior
- 有擴充後的 schema fixture
- 有更多 integration tests
- 有完整測試證據可以作為 week8 GitHub branch 的進度說明

---

## Out of Scope

Week 8 不包含：

- `convert` flow
- `clean` flow
- `transformer` module
- text report renderer
- advanced multi-format date parsing
- schema migration or backward-compat refactor

---

## Success Criteria

Week 8 視為完成的條件：

- 所有新增 validator 都有 unit tests
- engine 新行為有 tests
- validate flow 有更多 integration coverage
- 全套 pytest 通過
- 可用 GitHub commit history 清楚展示 TDD 開發節奏
- branch 可作為 `week8` 的獨立進度提交與展示材料

---

## Notes for Execution

本週實作要刻意維持 Week 7 的風格：

- 小步前進
- 一次一個行為
- 先測試再實作
- commit 訊息清楚
- 每個 commit 都要能說明「這一步新增了什麼可驗證能力」

不要在 Week 8 提前做 Week 9 之後的內容。先把 `validate` 做厚，讓 `week8` 成為一個完整、穩定、可展示的中間里程碑。
