# mkdocs-thebe

MkDocs plugin to turn Python code snippets into interactive examples via
[thebe](https://github.com/executablebooks/thebe)

## Usage

```yaml
# in your mkdocs.yml
plugins:
  - mkdocs-thebe:
      # endpoint to the server that manages Python processes
      baseUrl: https://endpoint.domain.io
```