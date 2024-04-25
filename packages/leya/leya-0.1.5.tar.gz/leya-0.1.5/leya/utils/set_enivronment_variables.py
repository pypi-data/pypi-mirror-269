import os

def set_environment_variables():
    """Set environment variables for Pinecone and OpenAI keys if not already set."""
    pinecone_key = os.getenv('PINECONE_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')

    if not pinecone_key:
        pinecone_key = input("Enter your Pinecone API key: ")
        os.environ['PINECONE_KEY'] = pinecone_key
        write_to_env_file('PINECONE_KEY', pinecone_key)

    if not openai_key:
        openai_key = input("Enter your OpenAI API key: ")
        os.environ['OPENAI_API_KEY'] = openai_key
        write_to_env_file('OPENAI_API_KEY', openai_key)

def write_to_env_file(key, value):
    """Write the environment variable to a .env file."""
    with open('.env', 'a') as env_file:
        env_file.write(f"{key}={value}\n")

