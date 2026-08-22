# Contributing to LEAP

Thank you for your interest in contributing to the LEAP Methodology & Tooling! We welcome contributions of all forms: bug fixes, documentation improvements, new features, and design revisions.

---

## 🚀 Getting Started

To submit your contribution, please follow these steps:

1.  **Fork the Repository:** Create a personal fork of this repository on GitHub.
2.  **Clone your Fork:**
    ```bash
    git clone https://github.com/your-username/leap.git
    cd leap
    ```

3.  **Create a Branch:** Always create a descriptive branch for your changes starting from `main` using the standard LEAP branch pattern `<username>/<feature-name>`:
    ```bash
    git checkout -b username/feature-name
    ```

4.  **Make your Changes:** Implement your bug fix, feature, or documentation update. **Ensure you follow our quality standards and testing guidelines below.**
5.  **Run Quality Checks Locally:** Run our linter to ensure that all changes adhere to our formatting and structural rules:
    ```bash
    check-md kb/
    ```

6.  **Commit and Push:** Write clear, concise, and professional commit messages, then push your branch to your GitHub fork:
    ```bash
    git push origin username/feature-name
    ```

7.  **Submit your Pull Request:** 
    - Navigate to the original [LEAP Repository on GitHub](https://github.com/blunderstone/leap) and click **"New Pull Request"**.
    - Select your fork and branch as the source.
    - **Use your Completion Summary as the PR Description:** In accordance with the LEAP Methodology, your pull request description must be the literal markdown contents of your feature branch's `completion-summary.md` (or your `pr-description.md` if the former is extremely large).
    - Ensure your description references any relevant GitHub issues (e.g., `Closes #14`).

---

## 🛠 Guidelines & Quality Standards

Before submitting your Pull Request, please ensure your changes meet our repository standards:

### 1. LEAP Methodology & Compliance Levels

All contributions to this repository must strictly follow the **LEAP (Literate Extended-by-Agent Programming) Methodology**. We enforce specific compliance standards for all pull requests based on the risk and complexity of the proposed changes:

*   **LEAP Feature Branches:** Every contribution must be developed on a dedicated feature branch named `<username>/<feature-name>` and accompanied by its corresponding feature documentation folder under `kb/feature/<username>/<feature-name>/` containing `goals.md`, `plan.md` (for multi-phase features), and `completion-summary.md`.
*   **Compliance Levels:** We enforce specific compliance levels depending on the scope of the change:
    - **Compliance Level 1 (Essential):** Minimally required for very simple, low-risk, and low-complexity changes (e.g., trivial edits, typo corrections, small bug fixes).
    - **Compliance Level 2 (Standard):** Required for all other changes, including new features, script modifications, or moderate/complex bug fixes.
*   For complete details on the requirements, checklists, and testing expectations of each compliance level, please refer directly to the [LEAP Compliance Levels Guide](kb/guide-compliance-levels.md).

### 2. Markdown Standards

All Markdown documents must strictly adhere to our formatting standards, ensuring clean headers, proper block separation, and compliant metadata fields.

- Always run the local `check-md` linter over the repository before submitting your PR to ensure zero formatting violations:
  ```bash
  check-md kb/
  ```

### 3. Testing Requirements

We utilize Test-Driven Development (TDD) as our standard practice for all new feature development and defect repair.

- Ensure any code changes are covered by comprehensive unit/integration tests (e.g., within `/check-md/tests/` or other script-level tests).
- All tests must pass cleanly in your environment before you submit your Pull Request.

### 4. Commits & Message Conventions

- Write clear, professional, imperative commit messages (e.g., `feat(workflow): ...` or `fix(linter): ...`).
- Refer to [Commit Messages Guidelines](kb/guide-methodology.md#commit-messages) for detailed formatting examples.

---

## ⚖️ Contribution Licensing Agreement (Implicit CLA)

To maintain clean intellectual property hygiene and allow us to offer both a robust, free open-source core and premium commercial enterprise features/services, we utilize an **Implicit Sublicensable Contribution** model.

### Agreement Terms

By submitting a contribution to this project (including but not limited to any Pull Request, Issue, or direct Commit), you agree that:

1.  **License Grant:** You grant **Blunderstone LLC** a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable, fully sublicensable license to use, reproduce, modify, prepare derivative works of, publicly display, publicly perform, distribute, and re-license your contribution under any terms, including our community open-source license (Apache-2.0) and proprietary commercial agreements.
2.  **Representations and Warranties:** You represent and warrant that each contribution is your original creation, and that you have the full legal right and authority to make this submission (including any necessary permissions or waivers from your employer, if applicable).
3.  **No Warranty:** Except for the representations above, you provide your contributions on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
