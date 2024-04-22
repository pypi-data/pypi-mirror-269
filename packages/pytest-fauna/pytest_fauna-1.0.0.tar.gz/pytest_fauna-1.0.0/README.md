# pytest-fauna

pytest-fauna contains some helpful [pytest] fixtures for [Fauna DB].

# Table of contents

[[_TOC_]]

# Installation

Install with the usual [Python] package manager. Here's an example with [pip]:

```bash
pip install pytest-fauna
```

If you would like to use the [AWS SecretsManager] integration for retrieval of the fauna
secret key, you will need to install the `aws` extra. Here's an example with [pip]:

```bash
pip install pytest-fauna[aws]
```

If you are using [Fluctuate] and want to use the fixtures that automatically apply
migrations, you will need to install the `fluctuate` extra. Here's an example with
[pip]:

```bash
pip install pytest-fauna[fluctuate]
```

# Fixtures

Please see the [plugin.py] file for details on the available fixtures.

[Fauna DB]: https://docs.fauna.com/fauna/current/
[pytest]: https://docs.pytest.org/en/stable/
[Python]: https://www.python.org/
[pip]: https://pip.pypa.io/en/stable/
[AWS SecretsManager]: https://docs.aws.amazon.com/secretsmanager/
[plugin.py]: pytest_fauna/plugin.py
[Fluctuate]: https://gitlab.com/munipal-oss/fluctuate
