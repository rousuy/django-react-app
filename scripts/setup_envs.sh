#!/bin/bash
set -e

echo "🔧 [ENV-SETUP] $1"
echo "Setting up environment files..."

# Detect current OS and set user/group IDs accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    USER_ID=1000
    GROUP_ID=1000
    echo "🍎 macOS detected - Using default IDs"
else
    USER_ID=$(id -u)
    GROUP_ID=$(id -g)
    echo "🐧 Linux detected - Using host IDs: $USER_ID:$GROUP_ID"
fi

# Function to copy a template and replace USER_ID and GROUP_ID in-place
setup_env_file() {
    local src_file="$1"      # Path to the source template file
    local dest_file="$2"     # Path to the destination .env file
    local label="$3"         # Descriptive label (e.g., "Backend", "Frontend")

    echo "Copying $label environment file..."
    cp "$src_file" "$dest_file"
    sed -i -E "s/^USER_ID=.*/USER_ID=$USER_ID/" "$dest_file"
    sed -i -E "s/^GROUP_ID=.*/GROUP_ID=$GROUP_ID/" "$dest_file"
    echo "✅ $label .env created."
}

# Setup Backend .env
SRC="contrib/api_env_sample"
DEST="./api/.env"
LABEL="Backend"
setup_env_file "$SRC" "$DEST" "$LABEL"

echo "✅ Environment files setup completed!"