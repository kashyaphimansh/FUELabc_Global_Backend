#!/usr/bin/env bash
set -Eeuo pipefail

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

BASE_PATH="${BASE_PATH:-/var/www/fuelabc_au_backend}"
RELEASES_PATH="${RELEASES_PATH:-$BASE_PATH/releases}"
CURRENT_LINK="${CURRENT_LINK:-$BASE_PATH/current}"
SHARED_ENV="${SHARED_ENV:-$BASE_PATH/shared/.env}"
SERVICE_NAME="${SERVICE_NAME:-fuelabc-au-backend}"
PUBLIC_URL="${PUBLIC_URL:-https://au.fuelabc.com}"
REPO_URL="${REPO_URL:-https://github.com/kashyaphimansh/FUELabc_Global_Backend.git}"
LOCK_FILE="${LOCK_FILE:-/var/lock/fuelabc-au-deploy.lock}"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

log() {
    printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*"
}

fail() {
    log "ERROR: $*" >&2
    exit 1
}

if [[ "${EUID}" -ne 0 ]]; then
    fail "This deployment script must run as root, normally through sudo."
fi

if [[ "$#" -ne 1 ]]; then
    fail "Usage: deploy-fuelabc-au <40-character-git-commit-sha>"
fi

COMMIT_SHA="${1,,}"

if [[ ! "$COMMIT_SHA" =~ ^[0-9a-f]{40}$ ]]; then
    fail "Commit SHA must be exactly 40 hexadecimal characters."
fi

command -v git >/dev/null 2>&1 || fail "git is required."
command -v curl >/dev/null 2>&1 || fail "curl is required."
command -v flock >/dev/null 2>&1 || fail "flock is required."
command -v systemctl >/dev/null 2>&1 || fail "systemctl is required."
command -v "$PYTHON_BIN" >/dev/null 2>&1 || fail "$PYTHON_BIN is required."

mkdir -p "$RELEASES_PATH"
touch "$LOCK_FILE"
exec 9>"$LOCK_FILE"

if ! flock -n 9; then
    fail "Another FUELabc AU deployment is already running."
fi

PREVIOUS_RELEASE="$(readlink -f "$CURRENT_LINK" || true)"

if [[ -z "$PREVIOUS_RELEASE" || ! -d "$PREVIOUS_RELEASE" ]]; then
    fail "Current release symlink does not point to an existing directory."
fi

case "$PREVIOUS_RELEASE" in
    "$RELEASES_PATH"/*) ;;
    *) fail "Current release is not under $RELEASES_PATH." ;;
esac

if [[ ! -f "$SHARED_ENV" ]]; then
    fail "Shared environment file does not exist at $SHARED_ENV."
fi

SERVICE_EXEC_START="$(systemctl show "$SERVICE_NAME" --property=ExecStart --value || true)"

if [[ "$SERVICE_EXEC_START" != *"$BASE_PATH/current/.venv/bin/gunicorn"* ]]; then
    if [[ "$SERVICE_EXEC_START" == *"$BASE_PATH/venv/bin/gunicorn"* ]]; then
        fail "Production service is not CI/CD bootstrap ready: Gunicorn does not use current/.venv."
    fi
    fail "Production service is not CI/CD bootstrap ready: Gunicorn does not use current/.venv."
fi

SHORT_SHA="${COMMIT_SHA:0:7}"
RELEASE_NAME="release-$(date -u '+%Y%m%dT%H%M%SZ')-$SHORT_SHA"
RELEASE_DIR="$RELEASES_PATH/$RELEASE_NAME"
TMP_CURRENT_LINK="$CURRENT_LINK.tmp"
ACTIVATED=0

retry() {
    local description="$1"
    shift

    for attempt in $(seq 1 10); do
        if "$@"; then
            log "$description succeeded on attempt $attempt."
            return 0
        fi
        log "$description failed on attempt $attempt."
        sleep 3
    done

    return 1
}

check_systemd_active() {
    systemctl is-active --quiet "$SERVICE_NAME"
}

check_local_healthz() {
    curl --fail --silent --show-error --max-time 5 "http://127.0.0.1:8000/healthz/" >/dev/null
}

check_public_healthz() {
    curl --fail --silent --show-error --max-time 10 "$PUBLIC_URL/healthz/" >/dev/null
}

check_public_readyz() {
    curl --fail --silent --show-error --max-time 10 "$PUBLIC_URL/readyz/" >/dev/null
}

check_public_admin() {
    curl --fail --silent --show-error --max-time 10 "$PUBLIC_URL/admin/" >/dev/null
}

switch_current() {
    local target="$1"
    ln -sfn "$target" "$TMP_CURRENT_LINK"
    mv -Tf "$TMP_CURRENT_LINK" "$CURRENT_LINK"
}

rollback_to_previous_release() {
    log "Attempting code rollback to $PREVIOUS_RELEASE."

    if ! switch_current "$PREVIOUS_RELEASE"; then
        echo "DEPLOYMENT_STATUS=ROLLBACK_FAILED"
        return 1
    fi

    if ! systemctl restart "$SERVICE_NAME"; then
        echo "DEPLOYMENT_STATUS=ROLLBACK_FAILED"
        return 1
    fi

    if ! retry "Rollback systemd active check" check_systemd_active; then
        echo "DEPLOYMENT_STATUS=ROLLBACK_FAILED"
        return 1
    fi

    if ! retry "Rollback public admin check" check_public_admin; then
        echo "DEPLOYMENT_STATUS=ROLLBACK_FAILED"
        return 1
    fi

    echo "DEPLOYMENT_STATUS=FAILED_ROLLED_BACK"
    echo "FAILED_COMMIT=$COMMIT_SHA"
    echo "RESTORED_RELEASE=$PREVIOUS_RELEASE"
    echo "DATABASE_MIGRATIONS_NOT_REVERSED=true"
    echo "STATIC_FILES_NOT_ROLLED_BACK=true"
    return 0
}

cleanup_old_releases() {
    local current_release
    current_release="$(readlink -f "$CURRENT_LINK")"

    mapfile -t release_dirs < <(
        find "$RELEASES_PATH" \
            -mindepth 1 \
            -maxdepth 1 \
            -type d \
            -regextype posix-extended \
            -regex ".*/release-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7}" \
            | sort -r
    )

    local kept=0
    local release_dir

    for release_dir in "${release_dirs[@]}"; do
        case "$release_dir" in
            "$RELEASES_PATH"/*) ;;
            *) continue ;;
        esac

        if [[ "$release_dir" == "$current_release" || "$release_dir" == "$PREVIOUS_RELEASE" ]]; then
            kept=$((kept + 1))
            continue
        fi

        if (( kept < 5 )); then
            kept=$((kept + 1))
            continue
        fi

        log "Removing old release $release_dir."
        rm -rf -- "$release_dir"
    done
}

log "Preparing release $RELEASE_NAME for commit $COMMIT_SHA."
mkdir -p "$RELEASE_DIR"

git clone --no-checkout "$REPO_URL" "$RELEASE_DIR"
git -C "$RELEASE_DIR" checkout --detach "$COMMIT_SHA"

CHECKED_OUT_SHA="$(git -C "$RELEASE_DIR" rev-parse HEAD)"

if [[ "$CHECKED_OUT_SHA" != "$COMMIT_SHA" ]]; then
    fail "Checked out SHA does not match requested SHA."
fi

# python-decouple config() is called from config/settings/*.py and searches
# upward for .env, so the release root .env symlink is the source of truth.
ln -sfn "$SHARED_ENV" "$RELEASE_DIR/.env"

"$PYTHON_BIN" -m venv "$RELEASE_DIR/.venv"
"$RELEASE_DIR/.venv/bin/python" -m pip install --upgrade pip
"$RELEASE_DIR/.venv/bin/python" -m pip install -r "$RELEASE_DIR/requirements.txt" -r "$RELEASE_DIR/requirements/production.txt"
"$RELEASE_DIR/.venv/bin/python" -m pip check
"$RELEASE_DIR/.venv/bin/gunicorn" --version

(
    cd "$RELEASE_DIR"
    DJANGO_SETTINGS_MODULE=config.settings.production "$RELEASE_DIR/.venv/bin/python" manage.py check
    DJANGO_SETTINGS_MODULE=config.settings.production "$RELEASE_DIR/.venv/bin/python" manage.py check --deploy
    DJANGO_SETTINGS_MODULE=config.settings.production "$RELEASE_DIR/.venv/bin/python" manage.py migrate --plan
    DJANGO_SETTINGS_MODULE=config.settings.production "$RELEASE_DIR/.venv/bin/python" manage.py migrate --noinput

    # STATIC_ROOT is shared at /var/www/fuelabc_au_backend/shared/staticfiles.
    # collectstatic may modify live static files before activation, and code
    # rollback does not automatically roll back collected static files.
    DJANGO_SETTINGS_MODULE=config.settings.production "$RELEASE_DIR/.venv/bin/python" manage.py collectstatic --noinput
)

log "Activating release $RELEASE_DIR."
switch_current "$RELEASE_DIR"
ACTIVATED=1

if ! systemctl restart "$SERVICE_NAME"; then
    journalctl -u "$SERVICE_NAME" -n 100 --no-pager || true
    rollback_to_previous_release || exit 1
    exit 1
fi

if ! retry "Systemd active check" check_systemd_active ||
   ! retry "Local healthz check" check_local_healthz ||
   ! retry "Public healthz check" check_public_healthz ||
   ! retry "Public readyz check" check_public_readyz; then
    journalctl -u "$SERVICE_NAME" -n 100 --no-pager || true
    rollback_to_previous_release || exit 1
    exit 1
fi

cleanup_old_releases

echo "DEPLOYMENT_STATUS=SUCCESS"
echo "DEPLOYED_COMMIT=$COMMIT_SHA"
echo "DEPLOYED_RELEASE=$RELEASE_DIR"
