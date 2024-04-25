# Leya

AI coding assistant which can directly be ported into the terminal and be used to query complex Git repositories

## Overview

The Git Coding Assistant is a versatile tool designed to streamline coding workflows by providing convenient features for repository management and code queries. Leveraging the power of Git and various AI technologies, it offers functionalities such as cloning repositories, selecting repositories for focused queries, and extracting relevant code snippets based on user queries.

## Features

- **Repository Cloning**: Easily clone GitHub repositories directly from the command line.
- **Repository Selection**: Select repositories to work with, enabling focused queries and interactions.
- **Code Querying**: Query repositories for specific code issues or information using natural language queries.
- **Function-based Queries**: Narrow down queries by specifying function names to focus on.
- **Intelligent Answer Generation**: Utilize AI to extract and provide intelligent answers to code-related queries.

## Usage

1. **Downloading the package**:
   ```bash
   $ pip install leya
   
2. **Cloning Repositories and uploading repo chunks to pinecone**:
   ```bash
   $ leya -r <repository_url>
3. **Selecting Repositories**:
   ```bash
   $ leya -s
4. **Querying Repositories**:
   ```bash
   $ leya -q "<query>" 
5. **Optional addition of Function-based Queries**:
   ```bash
   $ leya -q "<query>" -f <function_name_1> <function_name_2> ...

## Setup

Provide Pinecone and OpenAI keys when prompted for initial setup

## Contributing

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

## Credits

Developed by: PranavN1234


### Store repositories

![Screenshot 2024-04-23 200705](https://github.com/PranavN1234/Vela/assets/44135759/6cbf32f5-e077-4c59-962f-611c798fa85b)

### Swap between stored repositories 

![Screenshot 2024-04-23 200630](https://github.com/PranavN1234/Vela/assets/44135759/bf702ac3-3b82-4cf9-98b2-8bb2e78c9e65)

### Sample queries

![Screenshot 2024-04-23 200502](https://github.com/PranavN1234/Vela/assets/44135759/17108bd9-9a72-4653-be05-c5d9c2932dae)

![Screenshot 2024-04-23 200444](https://github.com/PranavN1234/Vela/assets/44135759/929238b7-e793-47a4-b4b8-3d59e8fa3d7d)




