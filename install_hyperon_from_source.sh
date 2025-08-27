#!/bin/bash

# Script to build and install hyperon from source for Python 3.13

echo "Installing hyperon from source for Python 3.13..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install git first:"
    echo "  sudo apt-get install git"
    exit 1
fi

# Check if cargo (Rust) is installed
if ! command -v cargo &> /dev/null; then
    echo "Rust/Cargo is not installed. Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
fi

# Check if cmake is installed
if ! command -v cmake &> /dev/null; then
    echo "CMake is not installed. Please install cmake first:"
    echo "  sudo apt-get install cmake"
    exit 1
fi

# Clone the repository
echo "Cloning hyperon repository..."
git clone https://github.com/trueagi-io/hyperon-experimental.git

# Navigate to the directory
cd hyperon-experimental

# Build the project
echo "Building hyperon..."
cd lib
cargo build --release

# Install Python bindings
echo "Installing Python bindings..."
cd ../python
pip3 install -e .

echo "Installation complete!"
echo "Try importing hyperon in Python:"
echo "  python3 -c 'import hyperon; print(\"Hyperon imported successfully!\")'"