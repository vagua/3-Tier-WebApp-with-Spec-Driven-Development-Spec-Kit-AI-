# Contributing to the 3-Tier POS Web Application

Thank you for your interest in contributing to this project! We welcome all contributions, from bug fixes to new features. To ensure a smooth and collaborative process, please follow these guidelines.

## Branching Strategy

We use a simple feature-branch workflow. All new work should be done in a feature branch created from the `main` branch.

1.  **Create a Branch**: Before starting work, create a new branch from the latest `main` branch. Name your branch descriptively, using a prefix like `feat/` for new features or `fix/` for bug fixes.
    ```bash
    # Example for a new feature
    git checkout -b feat/add-payment-gateway

    # Example for a bug fix
    git checkout -b fix/order-total-calculation
    ```

2.  **Develop**: Make your changes on the feature branch.

3.  **Open a Pull Request**: Once your work is complete and tested, push your branch to the remote repository and open a Pull Request (PR) against the `main` branch. Provide a clear title and a detailed description of your changes in the PR.

## Commit Style

We follow the Conventional Commits specification. This helps in creating an explicit commit history and makes it easier to automate changelog generation.

Each commit message should be in the format: `<type>[optional scope]: <description>`

**Common types:**
-   `feat`: A new feature.
-   `fix`: A bug fix.
-   `docs`: Documentation only changes.
-   `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc).
-   `refactor`: A code change that neither fixes a bug nor adds a feature.
-   `test`: Adding missing tests or correcting existing tests.
-   `chore`: Changes to the build process or auxiliary tools and libraries.

**Example:**
```
feat: Add status filter to the kitchen view
```
```
fix: Correctly calculate total price with item discounts
```

## Code Review Checklist

When reviewing a Pull Request, please consider the following points:

-   **Functionality**: Does the code successfully solve the intended problem or implement the feature?
-   **Clarity**: Is the code easy to read and understand? Are variable names clear? Is there sufficient documentation or comments where necessary?
-   **Testing**:
    -   Are there new unit tests covering the changes?
    -   Do all tests (backend and frontend) pass successfully?
-   **Style**: Does the code adhere to the project's coding style and conventions?
-   **Documentation**: If the change affects how the application is run or configured, has the `README.md` or other relevant documentation been updated?