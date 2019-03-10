Contents of `secrets.tar.gz`:
- `credentials.json` - file containing OAuth key/token
  for `cent17710n@gmail.com` Google account (used for tests)
- `secrets.py` - python file containing variables with
  Github and Disqus API tokens (used for tests)
  - `GITHUB_OAUTH_CLIENT_ID` (access protection)
  - `GITHUB_OAUTH_CLIENT_SECRET` (access protection)
  - `GITHUB_TOKEN` (github)
  - `DISQUS_TOKEN` (disqus)
  - `SECRET_KEY` (flask)

Instructions for encrypting/decrypting can be found
in the Travis documentation here:

<https://docs.travis-ci.com/user/encrypting-files/#manual-encryption>

**Step 1: Encrypt Secret File**

To encrypt a file, pick a passphrase and use OpenSSL
to encrypt the file with that passphrase:

```
openssl aes-256-cbc -k "<your password>" -in secrets.tar.gz -out secrets.tar.gz.enc
```

**Step 2: Add password to repository's Travis settings.** 

Log in to Travis and navigate to the project. Modify the
settings of the repository. There is a section where you
can add environment variables.

Add a new environment variable named `credentials_password`
with the value of `<your password>` (same password used in
the above command).

Now you can add the following command in your
`.travis.yml` file to decrypt the secrets file:

```
before_install:
- ...
- cd tests/
- openssl aes-256-cbc -k "$credentials_password" -in secrets.tar.gz.enc -out secrets.tar.gz -d
- ...
```

Once you've added the encrypted secrets file 
(don't add the original, unencrypted secrets file!),
you can commit it along with the `.travis.yml` file,
and Travis should be able to access the secrets
using the secret password provided via the environment
variable.

