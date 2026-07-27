# CI/CD Improvement & Popup Fix Plan

## Branch
- Target branch: `cicd-improvements` (already created)
- Base branch: `main`

## Changes

### 1. CI/CD: Add `git pull --rebase` to `update_posts.yml`

**File:** `.github/workflows/update_posts.yml`

**Problem:** When a post is created via the web browser (`write.html`), it pushes a new `.md` file, triggering both `update_posts.yml` and `generate_audio.yml` simultaneously. The `generate_audio.yml` workflow includes `git pull --rebase origin main` before its push (line 83), but `update_posts.yml` does `git push` without pulling first. This means concurrent pushes from both workflows can cause a non-fast-forward error in `update_posts.yml`.

**Fix:** Add `git pull --rebase origin main` before `git push` in the commit step of `update_posts.yml`, matching the pattern already used in `generate_audio.yml`.

### 2. Fix the "Do you want to write another post?" popup in `write.html`

**File:** `write.html`

**Problem:** Lines 930-934 use `confirm('Post published! Do you want to write another post?')` which is a blocking modal dialog. It's disruptive, offers no useful action beyond clearing the form, and if the user clicks Cancel the form stays filled — requiring manual clearing anyway.

**Fix:** Replace the blocking `confirm()` with a non-blocking inline notification using the existing `showStatus()` mechanism. The status message will auto-dismiss after 5 seconds (existing behavior), but include a "Write another post" button that clears the form on click. This avoids interrupting the user's workflow while still providing a clear action.

**Implementation:**
- Remove the `setTimeout` block with `confirm()` (lines 929-934)
- Replace with a `showStatus()` call that includes a "Write another post" button
- The button onclick handler calls `clearForm()`

## Verification

1. Verify `update_posts.yml` has `git pull --rebase origin main` before `git push`
2. Verify `write.html` no longer uses `confirm()` for post-publish flow
3. Verify the "Write another post" button calls `clearForm()`
4. Verify no other functionality changed (no layout, no JS behavior changes beyond the popup)