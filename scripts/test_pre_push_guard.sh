#!/bin/bash
# Regression suite for .githooks/pre-push (records-path guard).
#
# Self-contained: builds throwaway repos under mktemp and drives the hook
# both directly (crafted stdin lines) and through real `git push` runs via
# core.hooksPath. The hook is always invoked with `sh`, so on Debian-family
# CI runners this doubles as a dash/POSIX check. Covers the rebase
# false-positive fix, commit-level walk semantics (add-then-delete),
# main-endpoint discrimination, break-glass, fail-closed unverifiable
# paths, and the 2026-07-31 adversarial-review attacks (forged/stale
# comparator, origin/main ref shadowing, refspec-less fetch, fork-to-
# upstream introduction, missing-tree walk errors, replacement refs).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK="$ROOT/.githooks/pre-push"
S="$(mktemp -d "${TMPDIR:-/tmp}/prepush-guard-test.XXXXXX")"
trap 'rm -rf "$S"' EXIT
ZERO40=0000000000000000000000000000000000000000
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@t
export GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@t
unset THESIS_ALLOW_RECORDS_PUSH

pass=0; fail=0
check() { # check <name> <expected_rc> <actual_rc> [stderr_file must_contain]
    local name=$1 want=$2 got=$3
    if [ "$got" = "$want" ]; then
        if [ $# -ge 5 ] && ! grep -q "$5" "$4"; then
            echo "FAIL $name (rc ok, missing output: $5)"; fail=$((fail+1)); return
        fi
        echo "PASS $name"; pass=$((pass+1))
    else
        echo "FAIL $name (want rc=$want got rc=$got)"; sed 's/^/    /' "${4:-/dev/null}"
        fail=$((fail+1))
    fi
}
hook() { # hook <clone_dir> <remote_name> <line...> -> rc in $rc, stderr in $S/err
    local d=$1 rn=$2; shift 2
    printf '%s\n' "$@" | (cd "$d" && sh "$HOOK" "$rn" ignored-url 2>"$S/err")
    rc=$?
}
commit_file() { # commit_file <dir> <path> <content> <msg>
    mkdir -p "$1/$(dirname "$2")"
    echo "$3" > "$1/$2"
    git -C "$1" add -A
    git -C "$1" commit -qm "$4"
}

# ---- setup: origin whose main gains an attested-style recorder commit
git init -q --bare "$S/origin.git"
git -C "$S/origin.git" symbolic-ref HEAD refs/heads/main
git clone -q "$S/origin.git" "$S/seed" 2>/dev/null
commit_file "$S/seed" records/seed.txt r0 "init records"
commit_file "$S/seed" src/a.txt a "init src"
git -C "$S/seed" push -q origin HEAD:main
INIT=$(git -C "$S/seed" rev-parse HEAD)

git clone -q "$S/origin.git" "$S/dev" 2>/dev/null
git -C "$S/dev" checkout -qb feat
commit_file "$S/dev" src/b.txt b "feat: src change"
git -C "$S/dev" push -q origin feat
OLD_REMOTE=$(git -C "$S/dev" rev-parse feat)

commit_file "$S/seed" records/r1.txt r1 "Record forecast surfaces"
git -C "$S/seed" push -q origin main
git -C "$S/dev" fetch -q origin
git -C "$S/dev" rebase -q origin/main feat
LOCAL=$(git -C "$S/dev" rev-parse feat)
TIP=$(git -C "$S/dev" rev-parse origin/main)

# ---- 1: the motivating false positive — rebased branch, no own records
hook "$S/dev" origin "refs/heads/feat $LOCAL refs/heads/feat $OLD_REMOTE"
check "01 rebased branch over recorder commits allowed" 0 $rc

# ---- 2-4: a branch's own records commit blocks; break-glass overrides
commit_file "$S/dev" records/evil.txt evil "touch records"
LOCAL2=$(git -C "$S/dev" rev-parse feat)
hook "$S/dev" origin "refs/heads/feat $LOCAL2 refs/heads/feat $OLD_REMOTE"
check "02 own records commit blocks (existing ref)" 1 $rc "$S/err" "records/evil.txt"
hook "$S/dev" origin "refs/heads/feat $LOCAL2 refs/heads/feat $ZERO40"
check "03 own records commit blocks (new ref)" 1 $rc "$S/err" "records/evil.txt"
printf '%s\n' "refs/heads/feat $LOCAL2 refs/heads/feat $OLD_REMOTE" \
    | (cd "$S/dev" && THESIS_ALLOW_RECORDS_PUSH=1 sh "$HOOK" origin x 2>"$S/err")
check "04 break-glass overrides with notice" 0 $? "$S/err" "THESIS_ALLOW_RECORDS_PUSH=1"
git -C "$S/dev" reset -q --hard "$LOCAL"

# ---- 5-8: pushes to main are judged on every published commit
git -C "$S/dev" checkout -q main
git -C "$S/dev" merge -q --ff-only origin/main
commit_file "$S/dev" records/r2.txt r2 "local records on main"
hook "$S/dev" origin "refs/heads/main $(git -C "$S/dev" rev-parse main) refs/heads/main $TIP"
check "05 main push publishing a records commit blocks" 1 $rc "$S/err" "records/r2.txt"
git -C "$S/dev" reset -q --hard "$TIP"
commit_file "$S/dev" src/d.txt d "src on main"
hook "$S/dev" origin "refs/heads/main $(git -C "$S/dev" rev-parse main) refs/heads/main $TIP"
check "06 main push with src-only commit allowed" 0 $rc
# propagating current main to a remote that lacks the recorder commits
# must still block — a branch-contribution check would see nothing here
hook "$S/dev" origin "refs/heads/main $TIP refs/heads/main $INIT"
check "07 main to stale remote still blocks (endpoint range kept)" 1 $rc "$S/err" "records/r1.txt"
# add-then-delete on a main push: endpoint trees match, commits still red
git -C "$S/dev" reset -q --hard "$TIP"
commit_file "$S/dev" records/hidden.txt h "add hidden record"
git -C "$S/dev" rm -q records/hidden.txt
git -C "$S/dev" commit -qm "remove hidden record"
hook "$S/dev" origin "refs/heads/main $(git -C "$S/dev" rev-parse main) refs/heads/main $TIP"
check "08 add-then-delete on main blocks (commit-level walk)" 1 $rc "$S/err" "records/hidden.txt"
git -C "$S/dev" reset -q --hard "$TIP"

# ---- 9: new branch off an older base while main gained recorder commits
git -C "$S/dev" checkout -qb newb "$INIT"
commit_file "$S/dev" src/c.txt c "src on newb"
hook "$S/dev" origin "refs/heads/newb $(git -C "$S/dev" rev-parse newb) refs/heads/newb $ZERO40"
check "09 new branch off old base allowed (own contribution only)" 0 $rc

# ---- 10: deletion pushes are skipped
hook "$S/dev" origin "refs/heads/feat $ZERO40 refs/heads/feat $OLD_REMOTE"
check "10 branch deletion allowed" 0 $rc

# ---- 11: add-then-delete records commits on a branch (three-dot-blind)
git -C "$S/dev" checkout -q feat
commit_file "$S/dev" records/smuggle.txt s "add smuggled record"
git -C "$S/dev" rm -q records/smuggle.txt
git -C "$S/dev" commit -qm "remove smuggled record"
hook "$S/dev" origin "refs/heads/feat $(git -C "$S/dev" rev-parse feat) refs/heads/feat $OLD_REMOTE"
check "11 add-then-delete on branch blocks" 1 $rc "$S/err" "records/smuggle.txt"
git -C "$S/dev" reset -q --hard "$LOCAL"

# ---- 12-14: failed refresh — endpoint fallback and fail-closed new refs
git clone -q "$S/origin.git" "$S/dev2" 2>/dev/null
git -C "$S/dev2" checkout -qb fb
commit_file "$S/dev2" records/topo.txt t "records on fb"
T=$(git -C "$S/dev2" rev-parse fb)
git -C "$S/dev2" update-ref refs/remotes/origin/main "$T"      # forge/stale
git -C "$S/dev2" remote set-url origin "$S/does-not-exist.git" # fetch fails
hook "$S/dev2" origin "refs/heads/fb $T refs/heads/fb $TIP"
check "12 failed refresh: existing ref falls back to endpoint, blocks" 1 $rc "$S/err" "records/topo.txt"
hook "$S/dev2" origin "refs/heads/fb $T refs/heads/fb $ZERO40"
check "13 failed refresh: new ref refuses as unverifiable" 1 $rc "$S/err" "cannot verify"
printf '%s\n' "refs/heads/fb $T refs/heads/fb $ZERO40" \
    | (cd "$S/dev2" && THESIS_ALLOW_RECORDS_PUSH=1 sh "$HOOK" origin x 2>"$S/err")
check "14 unverifiable + break-glass allows with notice" 0 $? "$S/err" "THESIS_ALLOW_RECORDS_PUSH=1"

# ---- 15-16: disjoint (orphan) history under the commit walk
git -C "$S/dev" checkout -q --orphan orph
git -C "$S/dev" rm -rq --cached .
rm -rf "$S/dev/src" "$S/dev/records"
commit_file "$S/dev" records/orphan.txt o "orphan with records"
hook "$S/dev" origin "refs/heads/orph $(git -C "$S/dev" rev-parse orph) refs/heads/orph $ZERO40"
check "15 orphan branch with records commit blocks" 1 $rc "$S/err" "records/orphan.txt"
git -C "$S/dev" checkout -q --orphan orph2
git -C "$S/dev" rm -rq --cached .
rm -rf "$S/dev/records" "$S/dev/only-src.txt"
commit_file "$S/dev" only-src.txt s "orphan without records"
hook "$S/dev" origin "refs/heads/orph2 $(git -C "$S/dev" rev-parse orph2) refs/heads/orph2 $ZERO40"
check "16 records-free orphan allowed (contributes no records commits)" 0 $rc

# ---- 17-18: a local branch literally named origin/main cannot shadow
git clone -q "$S/origin.git" "$S/dev4" 2>/dev/null
git -C "$S/dev4" checkout -qb evil
commit_file "$S/dev4" records/amb.txt x "records on evil"
E=$(git -C "$S/dev4" rev-parse evil)
git -C "$S/dev4" branch origin/main "$E"    # refs/heads/origin/main shadow
hook "$S/dev4" origin "refs/heads/evil $E refs/heads/evil $TIP"
check "17 refs/heads/origin-main shadow ignored, blocks" 1 $rc "$S/err" "records/amb.txt"
printf '%s\n' "refs/heads/evil $E refs/heads/evil $TIP" \
    | (cd "$S/dev4" && THESIS_ALLOW_RECORDS_PUSH=1 sh "$HOOK" origin x 2>"$S/err")
check "18 shadow + break-glass allows with notice" 0 $? "$S/err" "THESIS_ALLOW_RECORDS_PUSH=1"

# ---- 19: refspec-less remote — the explicit-refspec fetch must correct a
# forged tracking ref even when remote.origin.fetch is absent
git clone -q "$S/origin.git" "$S/dev5" 2>/dev/null
git -C "$S/dev5" config --unset-all remote.origin.fetch
git -C "$S/dev5" checkout -qb sneak
commit_file "$S/dev5" records/refspec.txt r "records on sneak"
SN=$(git -C "$S/dev5" rev-parse sneak)
git -C "$S/dev5" update-ref refs/remotes/origin/main "$SN"     # forge
hook "$S/dev5" origin "refs/heads/sneak $SN refs/heads/sneak $ZERO40"
check "19 refspec-less remote: fetch repins comparator, blocks" 1 $rc "$S/err" "records/refspec.txt"
if [ "$(git -C "$S/dev5" rev-parse refs/remotes/origin/main)" = "$TIP" ]; then
    echo "PASS 19b forged tracking ref overwritten by pinned fetch"; pass=$((pass+1))
else
    echo "FAIL 19b tracking ref still forged"; fail=$((fail+1))
fi

# ---- 20-21: fork topology — origin cannot vouch for another remote
git clone -q --bare "$S/origin.git" "$S/fork.git" 2>/dev/null
git clone -q "$S/fork.git" "$S/dev6" 2>/dev/null
commit_file "$S/dev6" records/from-fork.txt f "unattested fork-main record"
git -C "$S/dev6" push -q origin HEAD:main                      # fork main only
git -C "$S/dev6" fetch -q origin
git -C "$S/dev6" checkout -qb feat2 origin/main
commit_file "$S/dev6" src/e.txt e "src on feat2"
F2=$(git -C "$S/dev6" rev-parse feat2)
hook "$S/dev6" upstream "refs/heads/feat2 $F2 refs/heads/feat2 $TIP"
check "20 push to non-origin remote uses endpoint range, blocks" 1 $rc "$S/err" "records/from-fork.txt"
hook "$S/dev6" upstream "refs/heads/feat2 $F2 refs/heads/feat2 $ZERO40"
check "21 new ref on non-origin remote refuses as unverifiable" 1 $rc "$S/err" "cannot verify"

# ---- 22: an unreadable range fails closed, not open
git clone -q "$S/origin.git" "$S/dev7" 2>/dev/null
git -C "$S/dev7" checkout -qb broke
commit_file "$S/dev7" src/f.txt f "src on broke"
B7=$(git -C "$S/dev7" rev-parse broke)
MISSING=$(git -C "$S/dev7" rev-parse "$TIP^{tree}")
OBJ="$S/dev7/.git/objects/$(echo "$MISSING" | cut -c1-2)/$(echo "$MISSING" | cut -c3-)"
if [ -f "$OBJ" ]; then
    rm -f "$OBJ"
    hook "$S/dev7" origin "refs/heads/broke $B7 refs/heads/broke $TIP"
    check "22 unreadable history refuses as unverifiable" 1 $rc "$S/err" "cannot verify"
else
    echo "SKIP 22 (base tree object stored in a pack; corruption probe n/a)"
fi

# ---- 23: refs/replace cannot dress up a records commit
git clone -q "$S/origin.git" "$S/dev8" 2>/dev/null
git -C "$S/dev8" checkout -qb cloak
commit_file "$S/dev8" records/cloaked.txt c "records on cloak"
CK=$(git -C "$S/dev8" rev-parse cloak)
git -C "$S/dev8" checkout -q -b decoy "$TIP"
commit_file "$S/dev8" src/g.txt g "clean decoy"
git -C "$S/dev8" replace "$CK" "$(git -C "$S/dev8" rev-parse decoy)"
git -C "$S/dev8" checkout -q cloak
hook "$S/dev8" origin "refs/heads/cloak $CK refs/heads/cloak $TIP"
check "23 replacement ref ignored, records commit still blocks" 1 $rc "$S/err" "records/cloaked.txt"

# ---- 24: multi-ref pushes — one bad ref fails the push and is named
hook "$S/dev" origin \
    "refs/heads/feat $LOCAL refs/heads/feat $OLD_REMOTE" \
    "refs/heads/evilref $LOCAL2 refs/heads/evilref $OLD_REMOTE"
check "24 mixed multi-ref push blocks and names the records commit" 1 $rc "$S/err" "records/evil.txt"

# ---- 25-27: end-to-end through core.hooksPath with real pushes
mkdir -p "$S/hooks"; cp "$HOOK" "$S/hooks/pre-push"; chmod +x "$S/hooks/pre-push"
git -C "$S/dev" config core.hooksPath "$S/hooks"
git -C "$S/dev" checkout -q feat
(cd "$S/dev" && git push -q --force-with-lease origin feat) 2>"$S/err"
check "25 real push of rebased branch succeeds" 0 $?
commit_file "$S/dev" records/evil2.txt e2 "records again"
(cd "$S/dev" && git push -q origin feat) 2>"$S/err"
check "26 real push with records commit refused" 1 $? "$S/err" "BLOCKED"
if [ "$(git -C "$S/origin.git" rev-parse refs/heads/feat)" = "$LOCAL" ]; then
    echo "PASS 26b remote ref unmoved after refusal"; pass=$((pass+1))
else
    echo "FAIL 26b remote ref moved despite refusal"; fail=$((fail+1))
fi
(cd "$S/dev" && THESIS_ALLOW_RECORDS_PUSH=1 git push -q origin feat) 2>"$S/err"
check "27 real push with break-glass succeeds" 0 $? "$S/err" "THESIS_ALLOW_RECORDS_PUSH=1"

# ---- 28-29: merge commits — update-merges are records no-ops, evil
# merges that resolve to content matching no parent still block (the
# provenance audit's #73 exemption rule, mirrored)
git clone -q "$S/origin.git" "$S/dev9" 2>/dev/null
git -C "$S/dev9" checkout -qb um "$INIT"
commit_file "$S/dev9" src/h.txt h "src on um"
git -C "$S/dev9" merge -q --no-edit origin/main
hook "$S/dev9" origin "refs/heads/um $(git -C "$S/dev9" rev-parse um) refs/heads/um $ZERO40"
check "28 update-merge over recorder commits allowed (no-op merge)" 0 $rc
git -C "$S/dev9" checkout -qb em "$INIT"
commit_file "$S/dev9" src/i.txt i "src on em"
git -C "$S/dev9" merge --no-commit --no-edit -q origin/main >/dev/null 2>&1
mkdir -p "$S/dev9/records"
echo evil > "$S/dev9/records/evil-merge.txt"
git -C "$S/dev9" add -A
git -C "$S/dev9" commit -qm "evil merge writes records"
hook "$S/dev9" origin "refs/heads/em $(git -C "$S/dev9" rev-parse em) refs/heads/em $ZERO40"
check "29 evil merge resolving to new records content blocks" 1 $rc "$S/err" "records/evil-merge.txt"

echo
echo "== $pass passed, $fail failed =="
exit $((fail > 0))
