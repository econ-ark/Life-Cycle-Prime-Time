#!/bin/bash
# Single Source of Truth for Life-Cycle-Prime-Time environment setup
# Used by both Dockerfile and devcontainer.json
#
# Creates platform and architecture-specific virtual environments:
#   .venv-darwin-arm64    (macOS Apple Silicon)
#   .venv-darwin-x86_64   (macOS Intel)
#   .venv-linux-aarch64   (Linux ARM64)
#   .venv-linux-x86_64    (Linux x86_64)
#
# Usage:
#   bash setup.sh                      # Run with default settings
#   WORKSPACE_DIR=/path bash setup.sh  # Override workspace directory

set -e

echo "🚀 Setting up Life-Cycle-Prime-Time development environment..."

# ============================================================================
# Helper Functions
# ============================================================================

# Detect platform and architecture, return venv path
get_platform_venv_path() {
    local workspace_dir="$1"
    local platform=""
    local arch=""

    # Detect platform
    case "$(uname -s)" in
        Darwin)
            platform="darwin"
            # macOS: Check actual hardware, not Rosetta-reported arch
            if sysctl -n hw.optional.arm64 2>/dev/null | grep -q 1; then
                arch="arm64"
            else
                arch="x86_64"
            fi
            ;;
        Linux)
            platform="linux"
            arch="$(uname -m)"
            ;;
        *)
            # Fallback for unknown platforms
            echo "$workspace_dir/.venv"
            return
            ;;
    esac

    # Normalize architecture names
    case "$arch" in
        arm64) arch="arm64" ;;       # macOS ARM
        aarch64) arch="aarch64" ;;   # Linux ARM
        x86_64) arch="x86_64" ;;     # Both platforms
        *) ;;                        # Keep original value
    esac

    echo "$workspace_dir/.venv-$platform-$arch"
}

# Ensure UV is in PATH
ensure_uv_in_path() {
    case ":$PATH:" in
        *":$HOME/.local/bin:"*) ;;
        *) export PATH="$HOME/.local/bin:$PATH" ;;
    esac
    case ":$PATH:" in
        *":$HOME/.cargo/bin:"*) ;;
        *) export PATH="$HOME/.cargo/bin:$PATH" ;;
    esac
}

# ============================================================================
# Main Setup
# ============================================================================

# Detect workspace directory from script path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
WORKSPACE_DIR="${WORKSPACE_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

# Get platform-specific venv path
VENV_PATH=$(get_platform_venv_path "$WORKSPACE_DIR")
VENV_NAME=$(basename "$VENV_PATH")

echo "📁 Workspace: $WORKSPACE_DIR"
echo "🖥️  Platform: $(uname -s) ($(uname -m))"
echo "📦 Venv: $VENV_NAME"
echo ""

# Ensure UV is in PATH (for existing installations)
ensure_uv_in_path

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # shellcheck disable=SC1091
    source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
fi

# Verify uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ Failed to install uv"
    exit 1
fi

echo "✓ uv version: $(uv --version)"

# Create/sync virtual environment with all dependency groups
cd "$WORKSPACE_DIR"
echo "🐍 Setting up Python environment at $VENV_NAME..."

# Use UV_PROJECT_ENVIRONMENT to specify the venv location
export UV_PROJECT_ENVIRONMENT="$VENV_PATH"
uv sync --all-groups

# Verify virtual environment
if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "❌ Virtual environment not created at $VENV_PATH"
    exit 1
fi

echo "✅ Virtual environment created: $VENV_NAME"

# ============================================================================
# Shell Auto-Activation Configuration
# ============================================================================

echo ""
echo "Configuring shell auto-activation..."

# Create activation code for shell RC files
# This code detects platform and architecture, then activates the correct venv
# shellcheck disable=SC2016
ACTIVATION_CODE='
# Auto-activate Life-Cycle-Prime-Time virtual environment (platform and architecture-specific)
if [ -z "${VIRTUAL_ENV:-}" ]; then
    # Determine workspace directory
    LCPT_WORKSPACE="/workspace"
    if [ ! -d "$LCPT_WORKSPACE" ]; then
        # Fallback: try common locations
        for dir in "/workspace" "$HOME/Life-Cycle-Prime-Time" "$HOME/workspace"; do
            if [ -d "$dir" ] && [ -f "$dir/pyproject.toml" ]; then
                LCPT_WORKSPACE="$dir"
                break
            fi
        done
    fi

    # Detect platform and architecture
    LCPT_VENV=""
    LCPT_ARCH=$(uname -m)
    case "$(uname -s)" in
        Darwin)
            # macOS: check actual hardware for Apple Silicon detection
            if sysctl -n hw.optional.arm64 2>/dev/null | grep -q 1; then
                LCPT_ARCH="arm64"
            fi
            if [ -f "$LCPT_WORKSPACE/.venv-darwin-$LCPT_ARCH/bin/activate" ]; then
                LCPT_VENV="$LCPT_WORKSPACE/.venv-darwin-$LCPT_ARCH"
            fi
            ;;
        Linux)
            if [ -f "$LCPT_WORKSPACE/.venv-linux-$LCPT_ARCH/bin/activate" ]; then
                LCPT_VENV="$LCPT_WORKSPACE/.venv-linux-$LCPT_ARCH"
            fi
            ;;
    esac

    # Activate if found
    if [ -n "$LCPT_VENV" ] && [ -f "$LCPT_VENV/bin/activate" ]; then
        source "$LCPT_VENV/bin/activate"
        export PYTHONPATH="$LCPT_WORKSPACE/src:$PYTHONPATH"
    fi
fi'

# Add activation code to .bashrc
if [ -f "$HOME/.bashrc" ] || [ "$(uname -s)" = "Linux" ]; then
    [ -f "$HOME/.bashrc" ] || touch "$HOME/.bashrc"
    if ! grep -q "Auto-activate Life-Cycle-Prime-Time" "$HOME/.bashrc" 2>/dev/null; then
        echo "$ACTIVATION_CODE" >> "$HOME/.bashrc"
        echo "✅ Added activation code to ~/.bashrc"
    else
        echo "✅ Activation code already in ~/.bashrc"
    fi
fi

# Add activation code to .zshrc
if [ -f "$HOME/.zshrc" ] || [ "$(uname -s)" = "Darwin" ]; then
    [ -f "$HOME/.zshrc" ] || touch "$HOME/.zshrc"
    if ! grep -q "Auto-activate Life-Cycle-Prime-Time" "$HOME/.zshrc" 2>/dev/null; then
        echo "$ACTIVATION_CODE" >> "$HOME/.zshrc"
        echo "✅ Added activation code to ~/.zshrc"
    else
        echo "✅ Activation code already in ~/.zshrc"
    fi
fi

# ============================================================================
# Summary
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Environment setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   Platform:   $(uname -s) ($(uname -m))"
echo "   Python:     $(uv run python --version)"
echo "   Venv:       $VENV_NAME"
echo "   Workspace:  $WORKSPACE_DIR"
echo ""
echo "To activate manually:"
echo "   source $VENV_PATH/bin/activate"
echo "   export PYTHONPATH=\"$WORKSPACE_DIR/src:\$PYTHONPATH\""
echo ""
