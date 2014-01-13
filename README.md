SublimeGPG
==========

This GPG plugin for Sublime Text 3 adds commands to decrypt, encrypt, sign, and authenticate documents.

Flaws and limitations:

- The passphrase prompt does not hide the text entered. Do *not* use this while someone is looking over your shoulder!
- Signatures can only be created with the default key (the first key in the secret key ring, or else the default specified in gpg.conf).
