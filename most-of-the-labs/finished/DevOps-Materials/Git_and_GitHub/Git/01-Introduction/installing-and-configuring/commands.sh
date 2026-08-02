#!/bin/bash
# Topic: Installing and Configuring Git
# Description: Git installation verification and essential configuration

# --- Verify Installation ---
git --version

# --- Essential Configuration ---
# Set your identity (appears in every commit)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Set default editor (VS Code)
git config --global core.editor "code --wait"

# --- View Configuration ---
# List all configuration
git config --list

# Check specific values
git config user.name
git config user.email

# --- Configuration Levels ---
# System level (all users): git config --system
# Global level (current user): git config --global
# Local level (current repo): git config --local

# --- View the config file directly ---
cat ~/.gitconfig
