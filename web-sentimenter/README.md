# Sentimenter

## Overview

Sentimenter is the final project for the "Machine Learning for Text Data" course, supervised by Dr. Anak Agung Istri Ngurah Eka Karyawati, S.Si., M.Eng. The project is a collaborative effort by the following students:

-   **I Wayan Trisna Wahyudi** (2008561018)
-   **I Gusti Ayu Purnami Pinatih** (2008561029)
-   **Revi Valen Sumendap** (2008561099)

## Project Description

Sentimenter is an aspect based sentiment analysis project. Sentiment analysis involves determining the sentiment expressed in a piece of text, whether it's positive, negative, or neutral. This project aims to create a model that can automatically analyze and classify the sentiment of text data.

## How to Run the Project

To run the project, follow the steps below:

1. Ensure that you have the Poetry package installed:

    ```bash
    pip install poetry
    ```

2. Clone the project repository:

    ```bash
    git clone https://github.com/trisnawahyudiii/pmdt-kelompok-2.git
    ```

3. Navigate to the project's "web-sentimenter" directory:

    ```bash
    cd web-sentimenter
    ```

4. Enter the virtual environment:

    ```bash
    poetry shell
    ```

5. Create a `.env` file based on the provided `.env.example`:

    - For Windows:

        ```bash
        copy .env.example .env
        ```

    - For Linux:

        ```bash
        cp .env.example .env
        ```

6. Configure the `.env` file with the required settings.

7. Install project dependencies:

    ```bash
    poetry install
    ```

8. Run the project:

    ```bash
    cd main
    flask run
    ```

## Additional Notes

Feel free to enhance this Markdown file with additional details about the project, such as the technologies used, the dataset employed, and any specific challenges or achievements during the development process. Additionally, provide information on how users can interact with or test the sentiment analysis model.

Happy coding!
