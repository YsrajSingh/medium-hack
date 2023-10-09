# The Medium Hack Application

The Medium Hack Application is a Python script that allows users to fetch and follow other users on the Medium platform. This README provides an overview of the application, its usage, and instructions for getting started.

## Table of Contents

-   Features
-   Getting Started
    -   Prerequisites
    -   Installation
-   Usage
-   Configuration
-   Contributing
-   License

## Features

-   Fetch and save the followers and following lists for specified usernames on Medium.
-   Follow users based on the fetched data.
-   Option to use a previous authentication token for convenience.
-   Easy-to-use command-line interface.

## Getting Started

Follow these instructions to set up and run The Medium Hack Application on your local machine.

### Prerequisites

Before you begin, ensure you have met the following requirements:

-   Python 3.x installed on your machine.
-   Internet access to fetch data from the Medium platform.

### Installation

1. Clone the repository to your local machine:
    ```
    git@github.com:YsrajSingh/medium-hack.git
    ```
1. Change to the project directory:
    ```
    cd medium-hack
    ```
1. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

To use The Medium Hack Application, follow these steps:

1. Run the script:
    ```
    python app.py
    ```
1. Follow the prompts to enter your authentication details and preferences.
1. The application will fetch and save the followers and following lists for the specified usernames.
1. You will have the option to follow users based on the fetched data

## Configuration

-   The configuration for The Medium Hack Application is defined in the secret/json/config.json and secret/constants.py file. You can modify this file to change application settings, such as URLs, API's and error messages.

## Contributors

- [Gurinder Batth](https://github.com/Gurinder-Batth)

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
1. Create a new branch for your feature or bug fix.
1. Make your changes and commit them with descriptive commit messages.
1. Push your changes to your fork.
1. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License.
