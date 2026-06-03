# DataGuard 期末簡報：12頁完整細節規劃

---

## Slide 1 — Title

**標題：** DataGuard Rebuild — Final Report

**頁面內容：**

```
DataGuard Rebuild
A Schema-Driven CLI for Data Validation, Cleaning, and Conversion

學號 / 姓名 / 課程 / 日期

A reusable, testable data quality pipeline for CSV, JSON, and JSONL.
178 tests  |  97% coverage  |  5 transformers  |  2 report formats
```

**視覺設計建議：**
- 中央放簡單的資料流圖示：`[CSV / JSON / JSONL]` → `[DataGuard]` → `[Report / Clean Output]`
- 四個數字（178 / 97% / 5 / 2）用醒目方式排在下方，讓聽眾在第一頁就感受到工程規模

**為什麼這樣做：**
進度報告的 Slide 1 沒有放任何數字。期末的 Title slide 在副標題加上四個具體數字，讓評分老師在第一秒就知道「這個專案最終完成到什麼程度」，不需要等到後面的 testing slide 才知道。這是最低成本、最高效益的差異化方式。

---

## Slide 2 — Progress Since Week 11（Bridge Slide）

**標題：** Where We Left Off — and How Far We've Come

**頁面內容（左右對比版面）：**

```
Week 11 State (進度報告時)           →      Final State (今天)
─────────────────────────────────────────────────────────────────
3 core pathways established                 3 pathways + full feature set
type_cast / fill_missing / dedup            + date_format / field_map / 2 new strategies
JSON report only                            JSON + text report with Error Summary
clean → CSV output only                     clean → CSV / JSON / JSONL
82 tests, 95% coverage                      178 tests, 97% coverage
"Horizon" items listed                      2 delivered, 2 out of scope
```

**為什麼這樣做：**
這是最關鍵的架構決策。進度報告的 Slide 2 和本計畫的 Slide 2 都在講「資料品質問題」，那是第一次向聽眾介紹這個專案時必要的鋪陳。但期末報告的聽眾（教授）已經看過進度報告，再講一次問題背景就是重複。

「Bridge Slide」的功能是讓聽眾快速定位：我們上次到哪了、這次要展示什麼。左右對比的格式讓每一行都是「舊 vs. 新」，視覺上明確地說明這份報告聚焦的是增量，而不是完整重述。

---

## Slide 3 — Horizon Delivered

**標題：** The Promises We Made — and Kept

**頁面內容（四格卡片）：**

```
Week 11 Horizon Slide 說「未來要做」：

✅ Intelligent Field Mapping       ✅ Enhanced Reporting
   field_map: rename + drop           --format json | text
   YAML-driven column control         Error Summary section
   已在 Week 12 完成                   已在 Week 12 完成

❌ Cyber Schemas                   ❌ Threat-Hunting Demos
   (out of scope)                     (out of scope)
```

**頁面下方加一行：**
```
另外完成（非 Horizon 項目）：
date_format transformer / fill_missing forward_fill + mean / dedup keep=none /
float validator / JSON root validation / clean multi-format output / output error handling
```

**為什麼這樣做：**
進度報告的最後一頁（Slide 10）是 "The Horizon"，列出四個「未來方向」。期末報告最強的敘事結構是：「**我上次承諾的，我做到了。**」

這頁直接呼應那個承諾，讓期末報告和進度報告形成完整的前後對比。兩個未完成的 Horizon 項目誠實標示 ❌ 並說明原因，這比假裝全部完成更有說服力。頁面底部的「另外完成」清單則顯示這個專案超出了最初預期，是加分項目。

---

## Slide 4 — Complete CLI Reference

**標題：** Three Workflows — Complete and Extended

**頁面內容（三條流程線，分別展示完整指令）：**

**Validate（藍色）**
```bash
dataguard validate \
  --input data.csv \
  --schema schemas/employees.yaml \
  --report report.json \
  --format json|text          # ← NEW: text format 是新增的
```
→ 輸出：report file（JSON 或純文字）

**Clean（綠色）**
```bash
dataguard clean \
  --input raw.csv \
  --schema schemas/employees.yaml \
  --transforms transforms.yaml \
  --output clean.csv|json|jsonl   # ← NEW: 原本只有 CSV
  --report report.json \
  --format json|text              # ← NEW
```
→ 輸出：clean output + report file

**Convert（紫色）**
```bash
dataguard convert \
  --input data.csv \
  --output converted.json|jsonl   # 不做 validation，純格式轉換
```
→ 輸出：reformatted file

**頁面底部加一行說明：**
```
convert 不載入 schema，不產生 report；JSONL 採 best-effort（壞行跳過，有效行繼續）
```

**為什麼這樣做：**
進度報告的 Slide 4 已展示三條流程的概念。這頁的差異是：顯示**真實的完整指令**（包含所有 flags），並且標記哪些是新增的。聽眾不需要重新學習三個流程是什麼，但可以從 flags 的標注看到具體的進化。`--output` 支援 `.json` 和 `.jsonl` 以及 `--format text` 是真正新的能力，在這頁點出來就夠了。

---

## Slide 5 — System Architecture

**標題：** System Architecture: Seven Decoupled Modules

**頁面內容（模組架構圖）：**

```
                     ┌─────────────────────────────────────────┐
Input Files          │                  CLI                     │       Output
                     │  (cli.py: routes to appropriate modules) │
CSV / JSON / JSONL ──┤                                          ├──── Report File
                     └──────────────────┬──────────────────────┘     Clean Output
                                        │
              ┌─────────────────────────┼────────────────────────────┐
              │                         │                            │
         [parser]                  [schema]                   [transformer]
         csv_parser                loader                     type_cast
         json_parser               models                     date_format
         encoding                  validators/                fill_missing
         factory                   └ string                   dedup
                                   └ integer                  field_map
                                   └ float  ← NEW
                                   └ enum
                                   └ boolean
                                   └ date
                                   └ strict mode
              │                         │                            │
              └──────────────┬──────────┘────────────────────────────┘
                             │
                    [reporter]              [output_factory]
                    json_report             csv_writer
                    text_report ← NEW       json_writer
                    get_report_renderer()   jsonl_writer
                    Error Summary ← NEW     (factory pattern)
```

**為什麼這樣做：**
進度報告的 Slide 3 展示了 YAML Schema → CLI Engine → Output 的三角形概念圖，Slide 5 是 Week 7–11 的時間軸。這頁是真正的**技術架構圖**，是兩份 progress slides 都沒有完整展示的東西。七個模組明確分層，`← NEW` 標記讓評分老師一眼看出哪些是新增的。這是最重要的架構投影片，應該讓老師看到模組之間的邊界是清楚的。

---

## Slide 6 — Schema Validation Design

**標題：** Schema-Driven Validation: Six Validation Categories + Strict Mode

**頁面內容（左右兩欄）：**

**左欄：employees.yaml（真實 schema 檔案的精簡版）**
```yaml
schema:
  name: employees
  strict: true                   # ← 偵測 unknown columns
  columns:
    - name: employee_id
      type: string
      pattern: "^EMP-[0-9]{3}$"  # regex 驗證
    - name: age
      type: integer
      min: 18
      max: 65                    # 範圍驗證
    - name: score
      type: float                # ← NEW: 新增 float type
      required: false
      min: 0.0
      max: 100.0
    - name: status
      type: enum
      values: [ACTIVE, INACTIVE, LEAVE]
    - name: is_active
      type: boolean
      true_values: ["true","1","yes","Y"]
    - name: join_date
      type: string
      format: date
```

**右欄：Validation Error Codes**
```
REQUIRED_MISSING    — 必填欄位是空的
PATTERN_MISMATCH    — 不符合 regex
INVALID_INTEGER     — 無法轉成整數
INVALID_FLOAT       — 無法轉成浮點數  ← NEW
OUT_OF_RANGE        — 超出 min/max
INVALID_ENUM        — 不在允許值列表
INVALID_BOOLEAN     — 不在 true/false 值
INVALID_DATE_FORMAT — 日期格式不符
UNKNOWN_COLUMN      — strict mode 偵測到未定義欄位
```

**頁面底部加一段：JSON Root Validation（NEW）**
```
JSON 輸入的新防線：
- Root 不是 array  → ParseFailure（整個檔案拒絕）
- Array 內的元素不是 object  → ParseErrorItem（該元素跳過）
- JSONL 每行不是 object  → ParseErrorItem（該行跳過）
```

**為什麼這樣做：**
進度報告的 Slide 6 展示了驗證引擎的三個「環」（strict / expanded rules / unified reporting）。這頁改用更具體的 YAML + Error Codes 對照，讓聽眾直接看到「schema 長什麼樣」以及「會產生什麼錯誤代碼」。`float` validator 和 JSON root validation 是進度報告後才加的，用 `← NEW` 標記清楚點出增量。

---

## Slide 7 — Cleaning Pipeline: Complete Transformer Suite

**標題：** Cleaning Pipeline: Five Transformers, YAML-Driven Configs

**頁面內容（上半：pipeline 圖；下半：代表性真實 YAML）**

**上半：pipeline 流程**
```
Raw Records
    ↓
[field_map]      rename: emp_id → employee_id / drop: notes
    ↓
[dedup]          keys: [employee_id], keep: first|last|none
    ↓
[date_format]    source: ["%Y/%m/%d", "%m-%d-%Y"] → target: "%Y-%m-%d"
    ↓
[fill_missing]   strategy: default|drop_row|forward_fill|mean
    ↓
[type_cast]      "30" (string) → 30 (integer)
    ↓
Validation
    ↓
Clean Output（只有通過驗證的資料）
```

**下半：transformer_full_transforms.yaml（4-transformer integration fixture）**
```yaml
transforms:
  - operation: dedup
    keys: [employee_id]
    keep: first
  - operation: date_format
    column: join_date
    source_formats: ["%Y/%m/%d", "%m-%d-%Y"]
    target_format: "%Y-%m-%d"
  - operation: fill_missing
    column: age
    strategy: forward_fill
  - operation: type_cast
    column: age
    target_type: integer
```

**右側：每個 transformer 的「解決什麼問題」對應**
```
field_map    → 欄位名稱不統一（SourceIP vs source_ip vs src_ip）
dedup        → 重複資料（keep first/last/none）
date_format  → 日期格式不一致（多種來源格式 → 統一目標格式）
fill_missing → 空值處理（補預設值/前一筆值/平均值/刪除列）
type_cast    → 型別錯誤（"30" → 30）
```

**field_map_transforms.yaml（另一個真實 fixture）**
```yaml
transforms:
  - operation: field_map
    rename:
      emp_id: employee_id
    drop:
      - notes
```

**為什麼這樣做：**
進度報告的 Slide 7 只有 `type_cast`、`fill_missing`（基礎）、`dedup`（基礎）三個 transformer，並且是概念說明。這頁展示目前支援的五個 transformer，加上兩種新策略（`forward_fill`、`mean`）和新模式（`keep=none`）。`transformer_full_transforms.yaml` 展示四個 transformer 的整合測試 fixture，`field_map_transforms.yaml` 則展示欄位 rename/drop。右側的「解決什麼問題」欄把技術能力連回現實場景，這是讓評分老師理解設計價值的關鍵。

---

## Slide 8 — Reporting: From Errors to Actionable Feedback

**標題：** Dual Report Format: JSON for Systems, Text for Humans

**頁面內容（三欄版面）：**

**左欄：JSON Report（程式可讀）**
```json
{
  "summary": {
    "source_file": "data.csv",
    "schema_name": "employees",
    "total_rows": 10,
    "pass_count": 7,
    "error_count": 3,
    "parse_error_count": 0,
    "validation_error_count": 3
  },
  "error_summary": {
    "age": {"OUT_OF_RANGE": 2},
    "status": {"INVALID_ENUM": 1}
  },
  "details": [
    {"row": 3, "column": "age",
     "code": "OUT_OF_RANGE", "...": "..."}
  ]
}
```

**中欄：指令切換**
```bash
# JSON format（預設）
dataguard validate ... --format json

# Text format（新增）
dataguard validate ... --format text
```

**右欄：Text Report（人類可讀）**
```
=== DataGuard Validation Report ===
Source : data.csv
Schema : employees
Time   : 2026-06-02T...

Summary:
  Total rows : 2
  Passed     : 6
  Warnings   : 0
  Errors     : 8 (0 parse, 8 validation)

Validation Errors (8 shown, limit=20):
  Row 1, column 'name': STRING_TOO_SHORT
  Row 1, column 'status': INVALID_ENUM
  Row 1, column 'age': OUT_OF_RANGE
  Row 2, column 'age': INVALID_INTEGER

Error Summary:
  name: STRING_TOO_SHORT x1, STRING_TOO_LONG x1
  status: INVALID_ENUM x1
  age: OUT_OF_RANGE x1, INVALID_INTEGER x1
```

**頁面底部加一行：**
```
get_report_renderer("json"|"text") factory → 新增格式時不需修改 CLI
```

**為什麼這樣做：**
這是整份期末報告中「最純的新內容」。進度報告完全沒有提到 text report，`--format` flag 是 Week 12 之後才有的。這頁把兩種格式並排，讓聽眾直觀看到同一份資料呈現成不同格式的實際輸出，這比描述功能更有說服力。`get_report_renderer()` factory 在頁面底部一行帶過，讓有興趣的老師知道背後的設計，但不佔主要篇幅。

---

## Slide 9 — Testing Strategy and Coverage

**標題：** Testing Strategy: 82 → 178 Tests, Reliability by Design

**頁面內容（左右兩區塊）：**

**左區塊：三層測試金字塔**
```
         ▲ CLI Tests
        ╱ ╲   Click command behavior
       ╱   ╲  Error handling (ClickException)
      ╱─────╲
     ╱  Int. ╲  Integration Tests
    ╱  Tests  ╲  validate / clean / convert end-to-end
   ╱───────────╲  empty input / invalid input / edge cases
  ╱  Unit Tests ╲
 ╱───────────────╲ parser / schema / validators
╱                 ╲ transformer / reporter / output
```

**右區塊：測試成長時間軸**
```
Week 8  Validation layer          ──  ~30 tests
Week 9  Transformer foundation    ──  ~50 tests
Week 10 Clean flow                ──  ~65 tests
Week 11 Convert flow              ──  82 tests  | 95%
Week 12 text report + field_map   ──  100 tests | 95%
Post-12 all transformers + fixes  ──  125 tests | 95%
Final   schema coverage + errors  ──  178 tests | 97% ✓
```

**頁面底部：GitHub CI 流程**
```
Issue → Branch → PR → [GitHub Actions CI] → Merge to main
                            ↓
                     pytest -q (all 178 tests must pass)
                     main branch is always green
```

**為什麼這樣做：**
進度報告的 Slide 9 展示了 TDD 的「無限符號」圖（Write Test → Implement → Pass → Refactor → Regression）和 82 tests。這頁改用**時間軸**，讓測試成長的過程可見，而不只是呈現最終結果。從 82 到 178 的成長本身就是一個故事。右下角的 GitHub Actions CI 是進度報告完全沒有提到的新工程實踐，值得在這頁帶入。

---

## Slide 10 — Live Demo

**標題：** Live Demo: Validate, Clean, Convert

**頁面內容（三個 demo 區塊）：**

**Demo 1：Validate（展示 text format，這是新功能）**
```bash
dataguard validate \
  --input tests/fixtures/validate/invalid/csv_employees_invalid.csv \
  --schema schemas/employees.yaml \
  --report report.txt \
  --format text

# 預期：report.txt 包含 Error Summary、exit code 1
```
→ 現場展示 `report.txt` 的實際純文字內容

**Demo 2：Clean（展示 combined transformer pipeline）**
```bash
dataguard clean \
  --input tests/fixtures/clean/valid/csv_transformer_full_valid.csv \
  --schema schemas/employees.yaml \
  --transforms tests/fixtures/clean/config/transformer_full_transforms.yaml \
  --output clean.json \
  --report clean-report.json

# 展示：dedup + date_format + forward_fill + type_cast 的組合效果
# 輸出是 .json（不是 CSV），展示 multi-format output 新能力
```

**Demo 3：Convert（簡短展示）**
```bash
dataguard convert \
  --input tests/fixtures/convert/valid/csv_convert_valid.csv \
  --output converted.jsonl

# 展示：CSV → JSONL，純格式轉換，no schema needed
```

**為什麼這樣做：**
Demo 的內容是原計畫的，但有兩個調整：
1. Demo 1 改用 `--format text` 而不是預設 JSON，因為 text report 是新功能，現場看到清楚的純文字輸出比看 JSON 更有視覺衝擊力
2. Demo 2 改用 `transformer_full_transforms.yaml`（使用 `dedup` + `date_format` + `forward_fill` + `type_cast`），而不是基礎的 `clean_transforms.yaml`，這樣能展示 combined transformer pipeline，而不只是最基本的清理

---

## Slide 11 — Lessons Learned

**標題：** Lessons Learned: What the Code Taught Me

**頁面內容（五張卡片）：**

**卡片 1：模組邊界讓測試變得可能**
> Transformer 完全不碰 I/O，只接受 records list，回傳 records list。這讓每個 transformer 可以在沒有任何 file fixture 的情況下用 inline data 測試，是這個專案測試速度快的根本原因。

**卡片 2：Error path 測試和 happy path 一樣重要**
> Schema loader 的 YAML 解析錯誤、reporter 的 unknown format、transformer 的 invalid option——這些在 demo 時永遠不會出現，但它們是系統穩定性的保護層。期末前補上的錯誤路徑測試讓系統不只通過 happy path，也能穩定處理壞輸入與不支援選項。

**卡片 3：Schema-driven 設計的代價與收益**
> YAML 定義規則的代價是需要維護一個完整的 schema loader 和 validator registry。但收益是：新增一個 float validator 只需要新增一個 class 和 registry 中一行，不需要修改 CLI 或任何上層邏輯。

**卡片 4：小 PR 比大 PR 容易審查也容易回滾**
> 每個 Issue 對應一個 branch 對應一個 PR，每個 PR 只做一件事。這讓功能新增、測試補強與文件更新都能被清楚審查，也讓回滾範圍容易判斷。

**卡片 5：Factory pattern 讓擴充不需要修改 CLI**
> `get_report_renderer()` 和 `get_output_writer()` 兩個 factory 讓「新增 Excel 輸出格式」或「新增 Markdown report」只需要在 factory 加一個分支，CLI 完全不用動。

**為什麼這樣做：**
這頁是原計畫的結構，但每張卡片改為**帶具體例子**，而不是通用陳述。「Modular design makes testing easier」太抽象；「Transformer 只接受 records list，讓每個 transformer 可以用 inline data 測試」是可以被理解和驗證的具體主張。這讓 Lessons Learned 看起來是真正從這個專案中得到的，而不是通用的工程原則清單。

---

## Slide 12 — Future Work and Q&A

**標題：** Future Work — and What DataGuard Is Today

**頁面內容（上半：roadmap；下半：closing statement）：**

**上半：Roadmap（承接 Slide 3 的 Horizon Delivered）**
```
已完成 ──────────────────────────────────────────── 未來
   │                                                  │
validate / clean / convert                      Excel input
5 transformers                                  Streaming large files
JSON + text report                              datetime validator
float validator                                 Report dashboard / visualization
JSON root validation                            More transform operations
178 tests / 97% coverage                       Case-sensitive mode (已保留介面)
GitHub CI workflow                              WARNING severity level (已保留介面)
```

**下半：Closing Statement**
```
DataGuard is not just a CLI tool.
It is a testable and extensible data quality pipeline
with defined module boundaries, schema-driven rules,
and a GitHub workflow that keeps main always green.
```

**頁面右下角：Q&A**

**為什麼這樣做：**
原計畫的 Future Work 是獨立的 roadmap，和前面的內容沒有連結。這頁的設計是讓 roadmap 的起點就是「已完成」的完整清單，讓聽眾在看「未來要做什麼」之前，先看到「現在已經有什麼」。`case_sensitive` 和 `WARNING level` 的「已保留介面」說明顯示這個專案在設計時考慮了可擴充性——這兩個功能的介面已存在，只是目前不啟用。這比說「未來要加這個功能」更成熟，因為它說明了「設計已經為這個功能留了空間」。

---

## 12頁整體結構邏輯

```
Slide 1   ─ 第一印象：完整數字，讓老師知道終點在哪
Slide 2   ─ 橋接：上次到哪了、這次展示什麼
Slide 3   ─ 核心敘事：我們兌現了承諾，並且超出了承諾
────────── 以上 3 頁建立整體框架，不重複進度報告 ──────────
Slide 4   ─ CLI 使用方式（更新版，含新 flags）
Slide 5   ─ 架構（完整模組圖，進度報告沒有的）
Slide 6   ─ Schema Validation（加 float + JSON root，兩個新功能）
Slide 7   ─ Transformer Suite（完整版，進度報告只有一半）
Slide 8   ─ Reporting（完全新的內容，text report）
Slide 9   ─ Testing（更新數字 + GitHub CI）
────────── 以上 6 頁是技術主體，5–8 都有新內容 ──────────
Slide 10  ─ Demo（現場展示，永遠是新的）
Slide 11  ─ Lessons Learned（反思，期末特有）
Slide 12  ─ Future Work（呼應 Slide 3，形成完整敘事弧）
```
