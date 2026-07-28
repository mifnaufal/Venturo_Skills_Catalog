---
name: venturo-hermes-agent
description: "Manage Claude Code & OpenCode skills for Venturo via Hermes Agent CLI."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, Venturo, Skill-Authoring, CLI, Automation, AI-Coding-Agent]
    related_skills: [venturo-poster, venturo-claude-code, venturo-opencode]
---

# Venturo — Hermes Agent Skill Guide (v2.0)

Gunakan **Hermes Agent CLI** untuk manage, test, dan deploy skill Claude Code/OpenCode di Venturo Skills Catalog. Cocok buat automatisasi workflow deployment skill, test capability, dan orchestrate multi-agent coding task.

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md`

---

## Trigger Behavior

Ketika skill ini dimuat via `skill_view()` atau dipanggil lewat Hermes Agent, **langsung mulai flow interaksi via Hermes CLI**. Jangan lakukan manipulasi file sampai user konfirmasi action pilihan. Skill ini bukan untuk generate poster langsung, tapi buat manage skill file dan orchestrasi task via Hermes tools.

---

## CRITICAL: Skill Management (CREATE/UPDATE/DELETE/PATCH)

### Create Skill Baru

```python
skill_manage(
    action='create',
    name='venturo-new-skill',
    content='---\nname: venturo-new-skill\ndescription: "..."\nversion: 1.0.0\nauthor: Hermes Agent\n---\n\n# New Skill\nContent here..',
    category='autonomous-ai-agents'
)
```

Atau pakai path ke file SKILL.md:

```python
skill_manage(
    action='create',
    name='venturo-custom-skill',
    content=read_file(path='/path/to/custom/skill.md'),
    category='autonomous-ai-agents'
)
```

### Patch Skill (Update Content)

```python
skill_manage(
    action='patch',
    name='venturo-claude-code',
    path='/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/.opencode/skills/venturo-claude-code/SKILL.md',
    old_string='version: 1.0.0',
    new_string='version: 2.0.0'
)
```

Atau patch bagian tertentu dari file:

```python
skill_manage(
    action='patch',
    name='venturo-claude-code',
    old_string='## Verification (Smoke Test)\n\n```\nterminal(command="claude -p \'Verify: CLAUDE_VENTURO_OK\' --max-turns 2")\n```\n\nSuccess criteria:',
    new_string='## Verification (Smoke Test)\n\n```\nterminal(command="claude -p \'Verify: CLAUDE_VENTURO_v2_OK\' --max-turns 2")\n```\n\nNew verification steps added for v2.0.\n\nSuccess criteria:'
)
```

### Delete Skill (Hati-hati!)

```python
skill_manage(
    action='delete',
    name='venturo-temp-skill'
)
```

### Discovery Skill

```python
skills_list()  # Daftar semua skill available (termasuk venturo-* di katalog)
skill_view(name='venturo-claude-code')  # Tampil content full, cek readiness status
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
- `patch`: isi `old_string` dan `new_string` (atau gunakan `patch` mode dengan path)
- `test`: pakai smoke test command sesuai skill

---

## Command Pattern Via Hermes Tools

### List semua skill Venturo

```python
skills_list()
# Filter manual: grep "venturo" dari output output

# Atau listing spesifik skill
for skill in venturo-poster venturo-claude-code venturo-opencode venturo-claude-context venturo-hermes-agent; do
  skill_view(name=$skill)
done
```

### View skill spesifik

```python
skill_view(name='venturo-claude-code')
# Pastikan readiness_status = available
```

### Patch skill (update versi)

```python
skill_manage(
    action='patch',
    name='venturo-claude-code',
    path='/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/.opencode/skills/venturo-claude-code/SKILL.md',
    old_string='version: 1.0.0',
    new_string='version: 2.0.0'
)
```

### Test via smoke test — Multiple Ways

**Via terminal langsung:**
```python
terminal(command="claude -p 'Verify: HERMES_VENTURO_CLAUDE_OK' --max-turns 2", workdir="/home/alxyz/Downloads/Project/Venturo_Skills_Catalog")
```

**Via process untuk OpenCode:**
```python
terminal(command="opencode run 'Verify: HERMES_VENTURO_OPencode_OK'", workdir="/home/alxyz/Downloads/Project/Venturo_Skills_Catalog")
```

**Via batch test semua skill:**
```python
for skill in venturo-claude-code venturo-opencode venturo-claude-context venturo-hermes-agent; do
  echo "Testing $skill..."
  terminal(command="claude -p \"Test $skill OK\" --max-turns 2")
done
```

---

## Workflow Deployment: Test → Deploy → Verify

### Phase 1 — Test di Lingkungan Lokal

```bash
# Smoke test tiap skill
cd /home/alxyz/Downloads/Project/Venturo_Skills_Catalog

# Claude Code skill
claude -p "Test venturo-claude-code" --max-turns 2

# OpenCode skill
opencode run "Test venturo-opencode"

# Context skill
claude -p "Test venturo-claude-context" --max-turns 2

# Verify all SKILL.md files exist
find . -name "SKILL.md" -path "*/venturo*" | wc -l  # Should be 5
```

### Phase 2 — Commit & Push Git

```bash
cd /home/alxyz/Downloads/Project/Venturo_Skills_Catalog
git add .opencode/ .claude/
git commit -m "feat: update venturo Claude Code & OpenCode skills to v2.0"
git push origin main
```

### Phase 3 — Verify Remote/Session Lain

```bash
# Di session lain atau setelah pull
skill_view(name='venturo-claude-code')  # Pastikan readiness = available
skill_view(name='venturo-opencode')
```

---

## Multi-Agent Orchestration Pattern

Pattern kompleks di mana Hermes Agent orchestrasi Claude Code + OpenCode + venturo-poster:

```python
# Step 1: Verify semua skill terload
skills = ['venturo-poster', 'venturo-claude-code', 'venturo-opencode', 'venturo-hermes-agent']
for skill in skills:
    skill_view(name=skill)

# Step 2: Generate poster via venturo-poster skill (trigger Q&A flow)
# (User akan diminta select tier, sections, messaging)

# Step 3: Simultaneous Claude Code review
claude_session = terminal(command="claude -p 'Review packages_context.md dan verifikasi data yang digunakan venturo-poster' --max-turns 5")

# Step 4: OpenCode generate documentation
opencode_task = terminal(command="opencode run 'Generate dokumentasi lengkap Paket Enterprise sesuai data packages_context.md' --max-turns 8")

# Step 5: Wait and collect results
sleep 30
claude_result = process(action="log", session_id=claude_session)
opencode_result = process(action="log", session_id=opencode_task)

# Step 6: Validate
if "verified" in claude_result and "documentation" in opencode_result:
    print("✅ Semua task selesai!")
else:
    print("❌ Ada yang perlu dicek ulang")
```

---

## Flags & Environment Important

| Variable/Flag | Digunakan |
|---------------|-----------|
| `HERMES_API_KEY` | Auth API Hermes kalau dibutuhkan |
| `ANTHROPIC_API_KEY` | Auth alternatif untuk Claude Code |
| `OPENROUTER_API_KEY` | Auth untuk OpenCode model |
| `skill_manage(...)` | Manage skill via Python interface |
| `skill_view(...)` | Load skill content & metadata |
| `skills_list()` | Enumerate available skills |
| `terminal(...)` | Run Claude/OpenCode commands |
| `process(action=...)` | Handle background OpenCode sessions |
| `workdir` | Always set to Venturo project root |

---

## Checklist Usage (Hermes Agent Specific)

1. **List target skill**: `skills_list()` sebelum action — pastikan skill ada ✓
2. **View current content**: `skill_view(name='...')` sebelum patch — verifikasi content aktual ✓
3. **Validate `old_string`**: String harus match persis dengan content file ✓
4. **Test via smoke test**: Setelah patch/update, run verification di setiap skill ✓
5. **Commit descriptive**: Git message jelas dan bisa ditrack ✓
6. **Push & verify remote**: Pastikan skill load di session lain/CI ✓
7. **Backup sebelum delete/skill yang kritis**: Copi SKILL.md ke .bak file ✓

---

## Pitfall & Solusi

- **Skill pruned ([SKILL_PRUNED])** → Reload pakai `skill_view()`, kalau masih pruned, restore dari backup (.bak file yang ada di skills dir)
- **Path tidak ada** → Pastikan path absolut, check `ls -la path/to/file` before patch
- **Smoke test gagal** → Claude/OpenCode belum terinstall/auth, check `claude --version` atau `opencode --version` dulu
- **Permission denied** → Ganti ownership file atau pake sudo kalau perlu (`chmod 755 SKILL.md`)
- **Patch string tidak match** → Pake `full=true` di `skill_view()`untuk lihat content full sebelum patch
- **Multiple concurrent skill actions** → Serialkan via sleep/sequential agar ada konflik file

---

## Advanced: Batch Validation Script

Buat script otomatis untuk validate semua skill Venturo:

```python
def validate_venturo_skills():
    skills_to_check = [
        'venturo-poster',
        'venturo-claude-code', 
        'venturo-opencode',
        'venturo-claude-context',
        'venturo-hermes-agent'
    ]
    
    errors = []
    for skill in skills_to_check:
        try:
            view = skill_view(name=skill)
            if view.get('readiness_status') != 'available':
                errors.append(f"{skill}: readiness_status = {view.get('readiness_status')}")
        except Exception as e:
            errors.append(f"{skill}: Error - {str(e)}")
    
    if errors:
        print(f"❌ Ditemukan {len(errors)} error:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("✅ Semua skill Venturo siap dipakai!")
        return True

# Jalankan
validate_venturo_skills()
```

---

## Verification (Smoke Test)

```python
# Test create skill
skill_manage(
    action='create',
    name='venturo-hermes-test',
    content='---\nname: venturo-hermes-test\ndescription: "Test skill"\nversion: 1.0.0\nauthor: Hermes Agent\n---\n\n# Test\nVerify: HERMES_VENTURO_TEST_OK',
    category='autonomous-ai-agents'
)

# Test view
view = skill_view(name='venturo-hermes-test')
assert view['name'] == 'venturo-hermes-test'

# Test cleanup
skill_manage(action='delete', name='venturo-hermes-test')
```

Success criteria: Skill creation succeeds, view returns correct metadata, delete works without error, no validation failures.

---

## What NOT to Do

- **Do NOT** patch skill file dengan old_string yang tidak match — akan gagal silently di beberapa case
- **Do NOT** delete skill yang masih digunakan oleh workflow lain — backup dulu
- **Do NOT** patch tanpa smoke test — pastikan skill masih bekerja sesudahnya
- **Do NOT** multiple concurrent write operations ke SKILL.md file yang sama — antisipasi race condition
- **Do NOT** skip validation step sebelum deploy — semua skill wajib smoke test terlebih dahulu

---

**Catatan:** Skill ini bekerja sama dengan skill lain di katalog Venturo. Semua skill mengacu pada `packages_context.md` sebagai data source tunggal. Bisa digunakan bersama `venturo-poster`, `venturo-claude-code`, dan `venturo-opencode` untuk workflow lengkap management skill via Hermes Agent CLI. Siap deployment, testing, dan orchestration multi-agent.
