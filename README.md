# AI Agent Organization Bootstrap / AI開発組織Bootstrap

## これは何か / What this is

**日本語:** このリポジトリは、AI支援ソフトウェア開発のための governance bootstrap を収めています。アプリケーションフレームワークではなく、プロンプト集でもありません。Codex Supervisor、Claude candidate implementers、Codex Auditor、Antigravity Visual Pod、Local Tooling、Human Owner の権限を分ける、境界付きの運用契約です。

**English:** This repository contains a governance bootstrap for AI-assisted software development. It is not an application framework and not a prompt collection. It is a bounded operating contract for Codex Supervisor, Claude candidate implementers, Codex Auditor, Antigravity Visual Pod, Local Tooling, and Human Owner.

This repository is public. Committed content must be sanitized by design.

## 設計思想 / Design philosophy

**日本語:** 生成量を無条件に増やすのではなく、書き込み前の権限を小さくします。最初に workspace を分類し、implementation、audit、adoption、release の権限を分離します。raw artifacts は漏えいリスクを持つものとして扱い、LLM 判断の前に deterministic gates を優先します。

**English:** The design does not maximize generation blindly. It minimizes authority before writes, classifies the workspace first, separates implementation, audit, adoption, and release authority, treats raw artifacts as risky, and prefers deterministic gates before LLM judgment.

## なぜ必要か / Why this exists

**日本語:** LLM は有能ですが、既定では範囲を広げがちです。branch を切るだけでは、dirty worktree、古い project state、cloud-sync path に残る raw logs や local metadata の継承を防げません。candidate patches には audit bundles、base SHA identity、bounded revision loops が必要です。

**English:** LLMs are capable, but overbroad by default. Branches alone do not prevent inheritance of dirty worktrees or old project state. Cloud-sync paths can expose raw logs and local metadata. Candidate patches need audit bundles, base SHA identity, and bounded revision loops.

## 中核契約 / Core contracts

**日本語:** 中核契約は、classification 前に書かないこと、新規 project を隔離すること、dirty existing repo では停止すること、cloud-sync workspace には approval gate を置くことです。`.agent-runs/` は ignored raw runtime material とし、commit するのは sanitized summaries のみです。bootstrap self-audit は mechanical governance scope の範囲だけに限定されます。

**English:** Core contracts are: no writes before classification, new project isolation, dirty repo hard stop, cloud-sync approval gate, `.agent-runs/` as ignored raw runtime material, sanitized committed summaries only, and bootstrap self-audit only within the mechanical governance scope.

## ロール / Roles

**日本語:** Human Owner は merge、push、deploy、publish、production data、credentials、legal/privacy/brand decisions を管理します。Supervisor Codex は task routing、accepted patch adoption、verification、許可された local commit を担当し、deploy はしません。Codex Auditor は独立した read-only reviewer です。Candidate Implementer と Claude は patch-only の候補作成者です。Antigravity Visual Pod は UI/UX/graphic/browser review specialist で、既定では review-only です。Local Tooling Pod は deterministic evidence を生成します。

**English:** The Human Owner controls merge, push, deploy, publish, production data, credentials, and legal/privacy/brand decisions. Supervisor Codex routes tasks, adopts accepted patches, verifies work, and creates allowed local commits, but does not deploy. Codex Auditor is an independent read-only reviewer. Candidate Implementer and Claude produce patch-only candidates. Antigravity Visual Pod specializes in UI, UX, graphic, and browser review, defaulting to review-only. Local Tooling Pod generates deterministic evidence.

## Candidate Patch Governance

**日本語:** candidate patch は `candidate_objective_id`、target branch/worktree ownership、`candidate_base_sha`、`current_target_sha` の再検証で管理します。audit bundle は deterministic に生成し、Auditor は structured findings を返します。`needs_revision` は bounded loop で扱い、agent を切り替えても cross-agent attempt limit は reset しません。

**English:** Candidate patches are governed by a candidate objective, target branch/worktree ownership, `candidate_base_sha`, and `current_target_sha` revalidation. Audit bundles are generated deterministically. The Auditor returns structured findings. `needs_revision` is bounded, and cross-agent attempt limits do not reset when implementers change.

## Antigravity Visual Pod

**日本語:** Antigravity Visual Pod は UI/UX/graphic/browser review specialist です。既定は review-only and artifact-first で、candidate UI patch は明示 approval がある場合だけです。既定では commit、deploy、terminal、backend、auth、DB、package changes を行いません。

**English:** Antigravity Visual Pod is a UI, UX, graphic, and browser review specialist. Its default mode is review-only and artifact-first. Candidate UI patches require explicit approval. By default, it does not commit, deploy, use a terminal, or change backend, auth, database, or package files.

## Repository layout / リポジトリ構成

**日本語:** `bootstrap/ai-org-bootstrap-v0.4.md` は canonical source です。`.agent-org/runbook.md` は実行手順をまとめます。`.agent-org/policies/` は workspace、artifact retention、Ask Gate、staffing の短い派生 policy です。`.agent-org/templates/` は sanitized summary、Antigravity visual review、candidate audit bundle の field contract です。`.agent-org/history/` には raw logs ではなく sanitized run summaries だけを置きます。

**English:** `bootstrap/ai-org-bootstrap-v0.4.md` is the canonical source. `.agent-org/runbook.md` summarizes execution. `.agent-org/policies/` contains concise derived policies for workspace, artifact retention, Ask Gate, and staffing. `.agent-org/templates/` defines field contracts for sanitized summaries, Antigravity visual review, and candidate audit bundles. `.agent-org/history/` stores sanitized run summaries, not raw logs.

## 使い方 / Usage

**日本語:** existing repo bootstrap では、clean repo を確認して bootstrap branch を作成し、許可された governance files だけを変更します。new project bootstrap では、fresh local-only workspace を使い、初回 commit 前の branch 作成は任意です。candidate patch flow では、candidate output、deterministic gates、audit bundle、Auditor decision、adoption を分離します。raw artifacts は `.agent-runs/` に置き、commit しません。commit してはいけないものは secrets、credentials、raw prompts、raw stderr、screenshots、recordings、production personal/customer data、local absolute paths です。

**English:** For existing repo bootstrap, confirm a clean repo, create a bootstrap branch, and change only allowed governance files. For new project bootstrap, use a fresh local-only workspace; branch creation before the first commit is optional. Candidate patch flow separates candidate output, deterministic gates, audit bundle, Auditor decision, and adoption. Store raw artifacts under `.agent-runs/` and do not commit them. Do not commit secrets, credentials, raw prompts, raw stderr, screenshots, recordings, production personal/customer data, or local absolute paths.

## 非目標 / Non-goals

**日本語:** この bootstrap は autonomous deployment、secret handling、production data access、CI/provider configuration を提供しません。scanner が secrets の不存在を証明することも保証しません。これは governance layer であり、application code や deploy 設定ではありません。

**English:** This bootstrap does not provide autonomous deployment, secret handling, production data access, CI configuration, or provider configuration. It does not guarantee that scanners prove absence of secrets. It is a governance layer, not application code or deploy configuration.

## ライセンス / License

**日本語:** ライセンスは未選択です。`LICENSE` file が追加されるまで、再利用権を仮定しないでください。

**English:** License is not yet selected. Do not assume reuse rights until a `LICENSE` file is added.
