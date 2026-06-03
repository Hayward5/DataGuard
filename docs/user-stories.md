# DataGuard 使用情境與操作說明

> 本文件以 User Story 的方式說明 DataGuard 目前已完成且可使用的功能。
> 每個 Story 包含情境說明、使用目的、CLI 指令範例，以及預期的執行結果。
> 適合非資訊專業人員快速了解這個工具能做什麼、如何使用。
>
> **最後更新：Issue #13**

---

## 什麼是 DataGuard？

DataGuard 是一個命令列工具（CLI），專門處理結構化資料的驗證、清理與格式轉換。
它支援 CSV、JSON、JSONL 三種格式，並透過 YAML 設定檔描述資料的規則。

**三條主要工作流程：**

| 指令 | 用途 |
|------|------|
| `dataguard validate` | 驗證資料是否符合規則，輸出報告 |
| `dataguard clean` | 清理資料後輸出合法資料列與報告 |
| `dataguard convert` | 在不同格式之間轉換，不做驗證 |

---

## User Story 1：驗證 CSV 資料是否符合規則

**情境：**
我是一位資料工程師，收到一份員工 CSV 檔案，需要確認每一筆資料是否符合公司定義的欄位規則（必填、型別、範圍、格式等）。

**我想要做什麼：**
自動檢查欄位是否合法，並取得一份清楚的錯誤報告。

**CLI 指令：**
```bash
dataguard validate \
  --input employees.csv \
  --schema schemas/employees.yaml \
  --report report.json \
  --format json
```

**結果：**
- 產生 `report.json`，內容包含總筆數、通過數、錯誤數、各欄位錯誤代碼與詳細清單
- 資料全部合法 → exit code `0`
- 有任何錯誤 → exit code `1`（可用於 CI 或 shell script 自動判斷）

---

## User Story 2：用純文字格式快速閱讀驗證結果

**情境：**
我不想打開 JSON 檔案，只想在終端機直接看到驗證摘要，或把結果存成純文字檔案給不懂程式的人看。

**我想要做什麼：**
改用人類可讀的文字格式輸出報告。

**CLI 指令：**
```bash
dataguard validate \
  --input employees.csv \
  --schema schemas/employees.yaml \
  --report report.txt \
  --format text
```

**結果：**
產生 `report.txt`，內容範例：
```
=== DataGuard Validation Report ===
Source : employees.csv
Schema : employees
Time   : 2026-05-17T...

Summary:
  Total rows : 10
  Passed     : 7
  Warnings   : 0
  Errors     : 3 (0 parse, 3 validation)

Validation Errors (3 shown, limit=20):
  Row 2, column 'age': OUT_OF_RANGE - Value out of range
  Row 4, column 'status': INVALID_ENUM - Invalid enum value
  Row 6, column 'join_date': INVALID_DATE_FORMAT - Invalid date format

Error Summary:
  age: OUT_OF_RANGE x1
  status: INVALID_ENUM x1
  join_date: INVALID_DATE_FORMAT x1
```

目前決策註記：`Warnings` 欄位保留在報告格式中，但目前 validators 不產生 warning，因此預期為 `0`，暫不更動此行為。

> 備註：`--format json` 為預設值，不指定時輸出 JSON 格式。

---

## User Story 3：驗證 JSON 或 JSONL 格式的資料

**情境：**
我的資料來源是 API 輸出的 JSON 或每行一筆的 JSONL，不是 CSV，但我也需要驗證欄位規則。

**我想要做什麼：**
對 JSON / JSONL 資料執行同樣的 schema 驗證。

**JSON 驗證：**
```bash
dataguard validate \
  --input employees.json \
  --schema schemas/employees.yaml \
  --report report.json
```

**JSONL 驗證：**
```bash
dataguard validate \
  --input employees.jsonl \
  --schema schemas/employees.yaml \
  --report report.json
```

**結果：**
程式根據副檔名自動選擇 parser，驗證流程與 CSV 完全相同，報告格式一致。

---

## User Story 4：同時回報解析錯誤與資料驗證錯誤

**情境：**
我收到一份 JSONL 檔案，裡面有幾行格式壞掉（不是有效的 JSON），也有幾行格式正確但內容不符合 schema。我想要一次看到全部問題。

**我想要做什麼：**
取得一份同時包含解析錯誤（parse error）與驗證錯誤（validation error）的完整報告。

**CLI 指令：**
```bash
dataguard validate \
  --input employees_mixed.jsonl \
  --schema schemas/employees.yaml \
  --report report.json
```

**結果：**
`report.json` 中會同時包含：
- `parse_errors`：列出哪些行解析失敗
- `validation_error_count`：驗證錯誤數
- `error_summary`：各欄位的錯誤代碼統計
- `details`：逐筆錯誤明細

---

## User Story 5：清理資料並只輸出合法資料列

**情境：**
我有原始員工資料，裡面有重複筆數、空值欄位、字串型態的數字。我需要整理後輸出乾淨的 CSV，不要把壞掉的資料留在裡面。

**我想要做什麼：**
先套用資料轉換規則，再重新驗證，只輸出沒有錯誤的資料列。

**CLI 指令：**
```bash
dataguard clean \
  --input raw_employees.csv \
  --schema schemas/employees.yaml \
  --transforms transforms.yaml \
  --output clean_employees.csv \
  --report clean-report.json
```

**結果：**
- `clean_employees.csv`：清理後通過驗證的合法資料（輸出格式由副檔名決定）
- `clean-report.json`：清理後的驗證結果報告
- 若資料有錯誤（但被過濾掉）→ exit code `1`
- 所有資料通過驗證 → exit code `0`

> 備註：`--output` 支援 `.csv`、`.json`、`.jsonl`，副檔名決定輸出格式。

---

## User Story 6：自動去除重複資料

**情境：**
資料中可能因系統問題出現重複的員工記錄，我只想保留每個 `employee_id` 第一次出現的資料。

**我想要做什麼：**
透過設定自動去重，不需要手動整理 CSV。

**Transforms 設定（`transforms.yaml`）：**
```yaml
transforms:
  - operation: dedup
    keys: [employee_id]
    keep: first   # first：保留第一筆 / last：保留最後一筆 / none：全部刪除
```

**搭配 clean 指令：**
```bash
dataguard clean \
  --input raw_employees.csv \
  --schema schemas/employees.yaml \
  --transforms transforms.yaml \
  --output clean.csv \
  --report report.json
```

**結果：**

| `keep` 設定 | 行為 |
|-------------|------|
| `first` | 每個 key 保留第一筆出現的記錄 |
| `last` | 每個 key 保留最後一筆出現的記錄 |
| `none` | 只要有重複 key，所有相關記錄全部刪除（無一保留） |

---

## User Story 7：自動補齊空白欄位

**情境：**
資料中有些員工的 `is_active` 欄位是空的，但 schema 要求這個欄位是必填。我想在驗證前先補上預設值。

**我想要做什麼：**
設定欄位的預設填補策略，避免因空值造成驗證失敗。

**Transforms 設定：**
```yaml
transforms:
  - operation: fill_missing
    column: is_active
    strategy: default
    value: "false"
```

若希望直接刪除含有空值的資料列：
```yaml
transforms:
  - operation: fill_missing
    column: is_active
    strategy: drop_row
```

**結果：**

| 策略 | 行為 |
|------|------|
| `default` | 空值欄位填入指定 `value` |
| `drop_row` | 含空值的整列被移除 |
| `forward_fill` | 空值填入前一筆非空值；若前面都是空值則保留空值 |
| `mean` | 空值填入該欄位所有有效數值的平均值（數字欄位限定） |

---

## User Story 8：自動轉換欄位資料型態

**情境：**
CSV 讀進來的 `age` 是字串 `"30"`，但 schema 期待它是整數 `30`。字串格式導致驗證失敗。

**我想要做什麼：**
在驗證前自動將欄位轉換成正確的型態。

**Transforms 設定：**
```yaml
transforms:
  - operation: type_cast
    column: age
    target_type: integer
```

**目前支援的目標型態：**

| 型態 | 說明 |
|------|------|
| `integer` | 轉為整數 |
| `float` | 轉為浮點數 |
| `string` | 轉為字串 |
| `boolean` | 轉為布林（支援 true/false/1/0/yes/no/y/n） |

**結果：**
轉換失敗的欄位會保留原始值，不會中斷流程。

---

## User Story 9：重命名欄位並刪除不需要的欄位

**情境：**
資料來源的欄位名稱叫 `emp_id`，但 schema 規定欄位名稱必須是 `employee_id`。同時資料中有 `internal_notes` 這類不應出現在輸出中的欄位。

**我想要做什麼：**
在 clean 流程中先修正欄位名稱，再刪除多餘欄位，讓資料符合 schema 的期待結構。

**Transforms 設定：**
```yaml
transforms:
  - operation: field_map
    rename:
      emp_id: employee_id
      dept: department
    drop:
      - internal_notes
      - raw_input
```

**CLI 指令：**
```bash
dataguard clean \
  --input raw_employees.csv \
  --schema schemas/employees.yaml \
  --transforms transforms.yaml \
  --output clean.csv \
  --report report.json
```

**結果：**
- `emp_id` 欄位重命名為 `employee_id`
- `internal_notes` 欄位從所有資料列中移除
- Schema validation 針對整理後的欄位執行

---

## User Story 10：組合多個轉換步驟

**情境：**
真實世界的資料通常同時有多種問題：欄位名稱不對、有空值、型態是字串、還有重複資料。我需要一次處理全部。

**我想要做什麼：**
在同一份 YAML 中定義多個轉換步驟，依序套用。

**Transforms 設定：**
```yaml
transforms:
  - operation: field_map
    rename:
      emp_id: employee_id
    drop:
      - internal_notes
  - operation: dedup
    keys: [employee_id]
    keep: first
  - operation: fill_missing
    column: is_active
    strategy: default
    value: "false"
  - operation: type_cast
    column: age
    target_type: integer
```

**結果：**
程式會依照 YAML 中的順序，依序執行每一個轉換步驟，最後再進行 schema 驗證並輸出結果。

---

## User Story 11：自動轉換日期格式

**情境：**
資料來源的日期格式不一致，有些欄位是 `2026/04/15`，有些是 `04-15-2026`，但 schema 要求格式必須是 `2026-04-15`。

**我想要做什麼：**
在驗證前自動把各種日期格式統一轉換成目標格式，不需要手動整理原始資料。

**Transforms 設定：**
```yaml
transforms:
  - operation: date_format
    column: join_date
    source_formats:
      - "%Y/%m/%d"
      - "%m-%d-%Y"
    target_format: "%Y-%m-%d"
```

**結果：**
- 程式依序嘗試 `source_formats` 中的格式，第一個成功解析的就採用
- 成功則輸出 `target_format` 指定的格式
- 所有格式都無法解析時保留原始值，不中斷流程

---

## User Story 12：清理後輸出 JSON 或 JSONL 格式

**情境：**
我想清理資料後直接輸出 JSON，供 API 或下游系統使用，不需要再手動轉換格式。

**我想要做什麼：**
讓 `clean` 的輸出格式由 `--output` 的副檔名自動決定，支援 CSV、JSON、JSONL。

**輸出為 JSON：**
```bash
dataguard clean \
  --input raw_employees.csv \
  --schema schemas/employees.yaml \
  --transforms transforms.yaml \
  --output clean.json \
  --report report.json
```

**輸出為 JSONL：**
```bash
dataguard clean \
  --input raw_employees.csv \
  --schema schemas/employees.yaml \
  --transforms transforms.yaml \
  --output clean.jsonl \
  --report report.json
```

**結果：**
- `clean.json`：合法資料列的 JSON array 格式
- `clean.jsonl`：合法資料列的 JSONL（每行一筆）格式
- 輸出格式完全由副檔名決定，不需要額外參數

---

## User Story 13：將 CSV、JSON、JSONL 格式互相轉換

**情境：**
我有 CSV 格式的資料，但下游系統需要 JSON。或者我有 JSONL 日誌，要轉成 CSV 給 Excel 分析。

**我想要做什麼：**
只做純格式轉換，不需要 schema 驗證，不需要 cleaning。

**CSV 轉 JSON：**
```bash
dataguard convert \
  --input data.csv \
  --output data.json
```

**JSON 轉 JSONL：**
```bash
dataguard convert \
  --input data.json \
  --output data.jsonl
```

**JSONL 轉 CSV：**
```bash
dataguard convert \
  --input data.jsonl \
  --output data.csv
```

**結果：**
程式根據副檔名自動選擇 parser 和 writer，完成格式轉換。不需要指定格式，不需要 schema，也不會產生驗證報告。

**目前支援的格式組合：**

| 輸入 | 輸出 |
|------|------|
| CSV | JSON、JSONL |
| JSON | CSV、JSONL |
| JSONL | CSV、JSON |

---

## User Story 14：限制報告中顯示的錯誤數量

**情境：**
大型資料集可能有幾百筆錯誤，我不需要看全部，只想先確認前幾筆錯誤的類型。

**我想要做什麼：**
限制 report 中錯誤明細的顯示數量。

**CLI 指令：**
```bash
dataguard validate \
  --input employees.csv \
  --schema schemas/employees.yaml \
  --report report.json \
  --limit 5
```

**結果：**
- `report.json` 的 `summary` 仍顯示完整的總錯誤數
- `details` 只列出前 5 筆錯誤明細
- `--limit` 預設值為 `20`，可依需要調整
- `validate` 和 `clean` 兩個指令都支援此選項

---

## 完整指令參數速查

### validate
```bash
dataguard validate \
  --input <資料檔案路徑>     # 必填，支援 .csv / .json / .jsonl
  --schema <schema 路徑>     # 必填，YAML 格式
  --report <報告輸出路徑>    # 必填
  --format <json|text>       # 選填，預設 json
  --limit <數字>             # 選填，預設 20
```

### clean
```bash
dataguard clean \
  --input <資料檔案路徑>     # 必填，支援 .csv / .json / .jsonl
  --schema <schema 路徑>     # 必填，YAML 格式
  --transforms <transforms 路徑>  # 必填，YAML 格式
  --output <輸出檔案路徑>   # 必填，支援 .csv / .json / .jsonl，副檔名決定輸出格式
  --report <報告輸出路徑>    # 必填
  --format <json|text>       # 選填，預設 json
  --limit <數字>             # 選填，預設 20
```

### convert
```bash
dataguard convert \
  --input <資料檔案路徑>     # 必填，支援 .csv / .json / .jsonl
  --output <輸出檔案路徑>    # 必填，副檔名決定輸出格式
```

---

## 目前完成狀態

| 功能 | 狀態 |
|------|------|
| validate 指令 | ✅ 完成 |
| clean 指令 | ✅ 完成 |
| convert 指令 | ✅ 完成 |
| JSON 報告格式 | ✅ 完成 |
| Text 報告格式（含 Error Summary） | ✅ 完成 |
| type_cast transformer | ✅ 完成 |
| fill_missing transformer | ✅ 完成（default、drop_row、forward_fill、mean） |
| dedup transformer | ✅ 完成（first、last、none） |
| field_map transformer | ✅ 完成（rename、drop） |
| date_format transformer | ✅ 完成 |
| float validator / score 欄位 | ✅ 完成（employees schema optional score: 0.0-100.0） |
| CSV / JSON / JSONL 輸入 | ✅ 完成 |
| CSV / JSON / JSONL 輸出（validate、convert、clean） | ✅ 完成 |
| 自動化測試 | ✅ 178 tests，97% coverage |
