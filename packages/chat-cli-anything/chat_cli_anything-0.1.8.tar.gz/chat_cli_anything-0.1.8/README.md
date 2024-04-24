![chat-cli-anything](./logo.png)

```
# Chat-Cli-Anything

Interact with GPT-like services from the command line, supporting local RAG, and pipe input.

Why:
① Developers spend a significant amount of time using the terminal to interact with the system, and when encountering issues in the terminal, they expect not to have to switch to a search engine or elsewhere.
② By leveraging the language model's excellent text capabilities and text processing abilities, it helps us achieve code generation, explanation, and translation beyond simple searches, as well as document Q&A.

## Tutorial

1. Installation

```shell
pip install "chat-cli-anything"
```

To simplify command length, you can set command aliases (optional):

```shell
# put this in your ~/.bashrc or ~/.zshrc
alias config="cc-config"
alias code="cc-code"
alias chat="cc-chat"
alias db="cc-db"
alias service="cc-service"
```

2. Add LLM provider

```
cc-config add "openai" "https://api.openai.com/v1"  --api-key "your-api-key"
```

If command aliases are set:

```
config add "openai" "https://api.openai.com/v1"  --api-key "your-api-key"
```

3. Start Using

**example 1** Normal question

```
cc-ask "Who is the author of the science fiction novel 'Three Body'?"
```

```
cc-ask "How to get the memory size occupied by a process in Linux?"
```

**example 2** Using pipe

```
# Find the filename with the maximum size in the current directory
ls -lah | cc-ask "filename with max size"
```

```
# For debugging error
gcc -o a.out a.cpp 2>&1 | cc-ask "what is the error" -s
```

**example 3** Interactive questioning

```
cc-chat "What is the capital of France?"
```

**example 4** Local document Q&A

```
cc-ask "Which school did the candidate graduate from?" -f resume.pdf
```

**example 5** Local document collection

Step 1: Digest text to build a local database

```
# d2light code
cc-db ingest "/path/to/detectron2-light" -n d2light
```

Step 2: Ask a question

```
# For open questions, the '-a/--advance' option would be helpful
cc-ask -d d2light "DETR implementation" -a
```

**example 6** Code explanation

```
# Explain line by line
cc-code explain /path/to/your/code.py -l

# If the code is lengthy, add the -l parameter to continue generating
cc-code explain /path/to/your/code.py -l -c
```

### Notice
It depends on `torch` version 2.2, so it may override the current environment version.

## Command Explanation

### cc-config

Configure LLM provider

#### 1. Add LLM provider

```
cc-config add [OPTIONS] NAME BASE_URL

Options:
  --model TEXT
  --api-key TEXT
  --proxy TEXT
  --help          Show this message and exit.
```

Example:

```
cc-config add "openai" "https://api.openai.com/v1"  --model "gpt-3.5-turbo-1106" --api-key "sk-xxxxxxxxxxx"
```

#### 2. Test provider

```
cc-config ping [OPTIONS] NAME

Ping provider.

Options:
  --help  Show this message and exit.
```

#### 3. List all providers

```
cc-config list [OPTIONS]

List all configurations.

Options:
  -s, --show-api-key
  --help              Show this message and exit.
```

The default api-key is hidden; use `-s/--show-api-key` to display the key.

#### 4. Remove provider

```
cc-config remove [OPTIONS] [NAME]

Remove a configuration.

Options:
  --help  Show this message and exit.
```

#### 5. Switch active provider

```
ask.py cc-config switch [OPTIONS] NAME

Switch to a different configuration and save the change.

Options:
  --help  Show this message and exit.
```

#### 6. Load configuration file

```
Import configurations.

Options:
  -o, --override  Whether to override the original config.
  --help          Show this message and exit.
```

#### 7. Export configuration file

```
ask.py cc-config dump [OPTIONS] PATH

Export current configurations.

Options:
  -o, --override  Whether to override the existing file.
  --help          Show this message and exit.
```

### cc-ask

Perform a question-answering task

```
cc-ask [OPTIONS] QUERY

Start a chat session with the given query.

Options:
  -d, --db TEXT        Name of database.
  -f, --filename TEXT  Name of file.
  -r, --rerank         Whether to rerank the results.
  -s, --show-chunks    Whether to show the related chunks retrieved from
                       the database.
  -a, --advance        Whether to use advance RAG.
  --help               Show this message and exit.
```

### cc-chat

Interactive Q&A

```
cc-chat [OPTIONS] [QUERY]

Interactive chat. Enter '/quit' to exit.

Options:
  -d, --db TEXT          Name of the database.
  -f, --filename TEXT    Name of the file.
  -n, --not-interactive
  -s, --show-history
  -c, --clear
  --help                 Show this message and exit.
```

### cc-code

Some common commands for code based on cc-ask.

#### Code Explanation

```
cc-code explain [OPTIONS] [FILENAME]

Explain code.

Options:
  -o, --object-name TEXT
  -l, --line               Line by line.
  -c, --continue-generate
  --help                   Show this message and exit.
```

Example 1: Specify filename

```
cc-code explain some_complex_scripts.py
```

Example 2: Specify a particular function

```
cc-code explain some_complex_scripts.py -o SomeClass::some_function
```

Example 3: Use pipe

```
cat some_complex_scripts.py | cc-code explain
```

#### Fix Issues

```
cc-code fix [OPTIONS] [FILENAME]

Fix code.

Options:
  -o, --object-name TEXT
  -c, --continue-generate
  --help                   Show this message and exit.
```

#### Code Refactoring

```
cc-code refactor [OPTIONS] [FILENAME]

Refactor code.

Options:
  -o, --object-name TEXT
  -c, --continue-generate
  --help                   Show this message and exit.
```

#### Code Review

```
cc-code review [OPTIONS] [FILENAME]

Review code.

Options:
  -o, --object-name TEXT
  -c, --continue-generate
  --help                   Show this message and exit.
```

#### Code Translation

```
cc-code translate [OPTIONS] LANGUAGE [FILENAME]

Translate code from one language to another. Supported languages include c++, cpp,
c, rust, typescript, javascript, markdown, html.

Options:
  -o, --object-name TEXT
  -c, --continue-generate
  --help                   Show this message and exit.
```

#### Select Code from Generated Results

Used to select code snippets from the generated responses of the above commands

```
cc-code select [OPTIONS] [INDEX]

Select code snippet from the last output.

Argument:     index: code snippet index

Options:
  -c, --count  get the number of code snippets
  --help       Show this message and exit.
```

`-c/--count` Get the number of candidate code blocks in the last response

Example:

```
>>> cc-code select -c
2

# Select the second code block from the last output
# For macOS
>>> cc-code select 1 | pbcopy
# For Linux
>>> cc-code select 1 | xclip -selection clipboard
```

### cc-db

#### list: List all text collections

```
cc-db list [OPTIONS] [NAME]

List all document databases.

Options:
  -s, --short  List in short format.
  --help       Show this message and exit.
```

#### ingest: Digest documents

```
cc-db ingest [OPTIONS] [FILES]...

Read documents and convert them into a searchable database.

Options:
  -n, --name TEXT     The name of the knowledge base.
  -m, --comment TEXT  Add comment to info.
  --help              Show this message and exit.
```

#### remove: Remove document collection

```
cc-db remove [OPTIONS] NAME

Remove database with the given name.

Options:
  -d, --remove-documents  Remove documents if data.
  --help                  Show this message and exit.
```

#### search: Search within a document collection

```
cc-db search [OPTIONS] DB QUERY

Options:
  -k, --topk INTEGER  Number of top results to return.
  --help              Show this message and exit.
```

### cc-service

Used to manage local text-to-index services.

If you want to run a text-to-index service on your local machine, execute the command `"pip install chat-cli-anything[all]"`.

#### start:

```
cc-service start [OPTIONS]

Options:

--help  Show this message and exit.
```

This process may take some time (~1min) to load the model, and you can check if it has started with `cc-service status`.

#### stop

```
cc-service stop [OPTIONS]

Options:
  --help  Show this message and exit.
```

#### status

```
cc-service status [OPTIONS]

Options:
  --help  Show this message and exit.
```
