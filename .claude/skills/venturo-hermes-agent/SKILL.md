---
name: venturo-hermes-agent
description: "Manage Claude Code & OpenCode skills for Venturo via Hermes Agent CLI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, Venturo, Skill-Authoring, CLI, Automation, AI-Coding-Agent]
    related_skills: [venturo-poster, venturo-claude-code, venturo-opencode]
---

# Venturo — Hermes Agent Skill Guide

Gunakan **Hermes Agent CLI** untuk manage, test, dan deploy skill Claude Code/OpenCode di Venturo Skills Catalog. Cocok buat automatisasi workflow deployment skill, test capability, dan orchestrate multi-agent coding task.

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md`

---

## Trigger Behavior

Ketika skill ini dimuat, **langsung mulai flow interaksi via Hermes CLI**. Jangan lakukan manipulasi file sampai user konfirmasi action pilihan. Skill ini bukan buat generate poster langsung, tapi buat manage skill file dan orchestrasi task via Hermes tools.

---

## CRITICAL: Skill Management (CREATE/UPDATE)

### Buat Skill Baru

```python
skill_manage(
    action='create',
    name='venturo-new-skill',
    content='---\nname: venturo-new-skill\ndescription: "..."\nversion: 1.0.0\nauthor: Hermes Agent\n---\n\n# New Skill\nContent here..',
    category='autonomous-ai-agents'
)
```

Patch skill yang ada:

```python
skill_manage(
    action='patch',
    name='venturo-claude-code',
    old_string='<!-- OLD CONTENT -->',
    new_string='<!-- NEW CONTENT -->'
)
```

### Discovery Skill

```python
skills_list()  # Daftar semua skill available
skill_view(name='venturo-claude-code')  # Tampil content full, cek readiness
```

---

## Task Spesifik Venturo (Trigger Flow Style)

### Step 1: Pilih Action

| Action | Description |
|--------|-------------|
| `list` | Daftar semua skill Venturo (`venturo-*`) |
| `view` | Tampil content skill tertentu |
| `create` | Buat skill baru Venturo |
| `patch` | Update skill yang ada |
| `delete` | Hapus skill Venturo (hati-hati!) |
| `test` | Run smoke test skill |

### Step 2: Pilih Skill Target

Untuk action `view`/`patch`/`delete`:
- `venturo-poster` (existing)
- `venturo-claude-code` (baru)
- `venturo-opencode` (baru)
- `venturo-claude-context` (baru)
- `venturo-hermes-agent` (ini)

### Step 3: Parameter Sesuai Action

- `create`: isi `content`, `category`, `tags`
- `patch`: isi `old_string` dan `new_string`
- `test`: pakai smoke test command sesuai skill

---

## Command Pattern Via Hermes Tools

### List semua skill Venturo

```python
skills_list(category='autonomous-ai-agents')
# Filter dengan grep "venturo" dari output
```

### View skill spesifik

```python
skill_view(name='venturo-claude-code')
```

### Patch skill (update versi)

```python
skill_manage(
    action='patch',
    name='venturo-claude-code',
    path='/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/.opencode/skills/venturo-claude-code/SKILL.md',
    old_string='version: 1.0.0',
    new_string='version: 1.0.1'
)
```

### Test via smoke test

```python
# Via terminal langsung
terminal(command="claude -p 'Verify: HERMES_VENTURO_CLAUDE_OK' --max-turns 2")
```

---

## Workflow Deployment: Test → Deploy

### Phase 1 — Test Lokal

```bash
# Smoke test tiap skill
for skill in venturo-claude-code venturo-opencode venturo-claude-context; do
  terminal(command="claude -p \"Test $skill\" --max-turns 2")
done

# Validate file existance
find /home/alxyz/Downloads/Project/Venturo_Skills_Catalog -name "SKILL.md" | grep venturo
```

### Phase 2 — Commit & Push

```bash
cd /home/alxyz/Downloads/Project/Venturo_Skills_Catalog && git add .opencode/.claude && git commit -m 'feat: add venturo hermes agent skill' && git push origin main
```

### Phase 3 — Verify Remote

```bash
skill_view(name='venturo-claude-code') # Pastikan readiness = available
```

---

## Flags & Environment Important

| Variable/Flag | Digunakan |
|---------------|-----------|
| `HERMES_API_KEY` | Auth API Hermes |
| `skill_manage(...)` | Manage skill via interface |
| `terminal(...)` | Run Claude/OpenCode command |
| `process(action=...)` | Handle background OpenCode session |

---

## Checklist Usage (Hermes Agent Specific)

1. List target skill: `skills_list()` sebelum action ✓
2. View current content: `skill_view(name='...')` sebelum patch ✓
3. Validate `old_string`: Pastikan match dengan content aktual ✓
4. Test via smoke test: Setelah patch/update, run verification ✓
5. Commit descriptive: Git message jelas ✓
6. Push & verify remote: Pastikan skill load di session lain ✓

---

## Pitfall & Solusi

- **Skill pruned ([SKILL_PRUNED])** → Reload pakai `skill_view()`, kalau masih pruned, restore dari backup (.bak)
- **Path tidak ada** → Pastikan path absolut, check `ls -la path/to/file`
- **Smoke test gagal** → Claude/OpenCode belum terinstall/auth, check `claude --version` atau `opencode --version`
- **Permission denied** → Ganti ownership file atau pake sudo kalau perlu

---

## Verification (Smoke Test)

```python
skill_manage(
    action='create',
    name='venturo-hermes-test',
    content='---\nname: venturo-hermes-test\ndescription: "Test skill"\nversion: 1.0.0\nauthor: Hermes Agent\n---\n\n# Test\nVerify: HERMES_VENTURO_TEST_OK',
    category='autonomous-ai-agents'
)

skill_view(name='venturo-hermes-test')
skill_manage(action='delete', name='venturo-hermes-test')
```

Success criteria: Create succeeds, view returns correct content, delete works, no errors.

---

**Catatan:** Skill ini bekerja sama dengan skill lain di katalog Venturo. Semua skill mengacu pada `packages_context.md`. Bekerja bersama `venturo-poster`, `venturo-claude-code`, dan `venturo-opencode` untuk workflow lengkap.</text>