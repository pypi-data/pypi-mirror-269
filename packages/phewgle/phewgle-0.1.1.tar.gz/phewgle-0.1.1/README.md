# phewgle

**A custom-build version of the Fugle library `fugle-trade-python` with customized features.**

## Prerequisite
1. Modify the `User` field in the `.ini` config file by adding `Password` and `CertPassword` sub-items.
    ```
    ...
    [User]
    Account = <account_id>
    Password = <account_password>
    CertPassword = <certificate_password>
    ```

2. Upload the `cert.p12` certificate file to your Google Cloud Storage bucket.

## Usage

#### _Initializing and authenticating the connector_

```python
from configparser import ConfigParser
from phewgle.fugle import FugleTrader

config: ConfigParser = ConfigParser()
sdk = FugleTrader(config)
sdk.login()
```
