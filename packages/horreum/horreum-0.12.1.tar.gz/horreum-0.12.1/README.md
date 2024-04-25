<div align="center">

# horreum-client-python

<a href="https://horreum.hyperfoil.io/"><img alt="Website" src="https://img.shields.io/website?up_message=live&url=https%3A%2F%2Fhorreum.hyperfoil.io/"></a>
<a href="https://github.com/Hyperfoil/horreum-client-python/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Hyperfoil/horreum-client-python"></a>
<a href="https://github.com/Hyperfoil/horreum-client-python/fork"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Hyperfoil/horreum-client-python"></a>
<a href="https://github.com/Hyperfoil/horreum-client-python/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Hyperfoil/horreum-client-python"></a>
<a href="https://github.com/Hyperfoil/horreum-client-python/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/Hyperfoil/horreum-client-python"></a> 

</div>

---
## What is Horreum Python Client?

Horreum python client is a high-level python library to interact with [Horreum](#what-is-horreum) web server.

The raw client is generated using [kiota](https://github.com/microsoft/kiota) openapi generator tool starting from 
the [Horreum OpenAPI spec](https://github.com/Hyperfoil/Horreum/blob/master/docs/site/content/en/openapi/openapi.yaml).

Refer to the [get started guide](docs/GET_STARTED.md) for comprehensive instructions on installing and utilizing this library.

## What is Horreum?

[Horreum](https://github.com/Hyperfoil/Horreum) is a service for storing performance data and regression analysis.

Please, visit our project website: 

[https://horreum.hyperfoil.io](https://horreum.hyperfoil.io)

for more information.

[Horreum](https://github.com/Hyperfoil/Horreum) is a [Quarkus](https://quarkus.io/) based application which uses
[Quinoa](https://quarkiverse.github.io/quarkiverse-docs/quarkus-quinoa/dev/) as its [Node.js](https://nodejs.org/en) engine.

This project is about providing a simplified setup and examples to use 
[Horreum](https://github.com/Hyperfoil/Horreum) using the [Python](https://www.python.org/) programming language.

## 🧑‍💻 Contributing

Contributions to `horreum-client-python` Please check our [CONTRIBUTING.md](./CONTRIBUTING.md)

### Development

Install poetry dependency (consider using Python virtual environments):
```bash
pip install --constraint=./dev-constraints.txt poetry
poetry --version
```

Generate source files
```bash
make generate
```

Build the library using `poetry`:
```bash
poetry build
```

#### Tests
Tests can be executed using [nox](https://nox.thea.codes/en/stable/) sessions.

To install it in your local environment, please run:
```bash
pip install --constraint=./dev-constraints.txt nox nox-poetry
nox --version
```

To check available sessions, run:
```bash
nox -l
```

And execute them by running:
```
nox -s <session>
```

Right now integrations tests are not fully automated, therefore you need to start up the Horreum server manually, 
you can check more details in [Horreum README](https://github.com/Hyperfoil/Horreum/blob/master/README.md#getting-started-with-development-server).

> **_NOTE_**: The database should be empty to get all tests working

Once the Horreum server is up and running on `localhost:8080`, you can trigger integration tests by running:
```bash
nox -s its
```

### If you have any idea or doubt 👇

* [Ask a question](https://github.com/Hyperfoil/horreum-client-python/discussions)
* [Raise an issue](https://github.com/Hyperfoil/horreum-client-python/issues)
* [Feature request](https://github.com/Hyperfoil/horreum-client-python/issues)
* [Code submission](https://github.com/Hyperfoil/horreum-client-python/pulls)

Contribution is the best way to support and get involved in community !

Please, consult our [Code of Conduct](./CODE_OF_CONDUCT.md) policies for interacting in our
community.

Consider giving the project a [star](https://github.com/Hyperfoil/horreum-client-python/stargazers) on
[GitHub](https://github.com/Hyperfoil/horreum-client-python/) if you find it useful.

## License

[Apache-2.0 license](https://opensource.org/licenses/Apache-2.0)

## Thanks to all the Contributors ❤️

<img src="https://contrib.rocks/image?repo=Hyperfoil/horreum-client-python" />
