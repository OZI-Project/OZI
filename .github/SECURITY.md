# Security Policy

## Supported Versions

Which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |

This page will be updated for the Alpha release to maturity.

## Disclosure

All known security vulnerabilities must be disclosed publically within 30 days of a detection during regular monitoring.

## Reporting a Vulnerability

A security vulnerability must never be posted in Issues.
This must be done directly through GitHub or via help@oziproject.dev

## Workflows

We maintain a deny-by-default posture on GitHub actions workflows with the following exceptions:
- [x] Allow actions created by OZI-Project
- [x] Allow actions created by GitHub
- [x] Allow actions by Marketplace verified creators
- [x] Allow the following list of actions and reusable workflows:
  - lowlighter/metrics@65836723097537a54cd8eb90f61839426b4266b6
  - python-semantic-release/python-semantic-release@v8.7.2
  - python-semantic-release/upload-to-gh-release@0f96c02a48278aff14251e9f1a0d73122a8c638b
  - slsa-framework/slsa-github-generator/.github/actions/compute-sha256@v1.9.0
  - slsa-framework/slsa-github-generator/.github/actions/detect-workflow-js@v1.9.0
  - slsa-framework/slsa-github-generator/.github/actions/generate-builder@v1.9.0
  - slsa-framework/slsa-github-generator/.github/actions/secure-builder-checkout@v1.9.0
  - slsa-framework/slsa-github-generator/.github/actions/secure-download-artifact@v1.9.0
  - slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.9.0
  - softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844
  - softprops/action-gh-release@v1
