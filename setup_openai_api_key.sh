#!/bin/bash

# Function to add the API key to the shell configuration file
add_api_key() {
  local shell_config_file=$1
  local api_key=$2

  # Check if the export command already exists in the file
  if grep -q "export OPENAI_API_KEY=" "$shell_config_file"; then
    echo "Updating existing OPENAI_API_KEY in $shell_config_file"
    sed -i.bak "s|export OPENAI_API_KEY=.*|export OPENAI_API_KEY='$api_key'|" "$shell_config_file"
  else
    echo "Adding OPENAI_API_KEY to $shell_config_file"
    echo "export OPENAI_API_KEY='$api_key'" >> "$shell_config_file"
  fi
}

# Prompt the user to enter the OpenAI API key
read -p "Enter your OpenAI API key: " api_key

# Determine which shell is being used
if [ -n "$BASH_VERSION" ]; then
  shell_config_file="$HOME/.bash_profile"  # Use .bash_profile on macOS
elif [ -n "$ZSH_VERSION" ]; then
  shell_config_file="$HOME/.zshrc"
else
  echo "Unsupported shell. Please manually add the following line to your shell configuration file:"
  echo "export OPENAI_API_KEY='$api_key'"
  exit 1
fi

# Add the API key to the shell configuration file
add_api_key "$shell_config_file" "$api_key"

# Source the updated configuration file
echo "Sourcing $shell_config_file"
source "$shell_config_file"

echo "OPENAI_API_KEY has been set successfully."