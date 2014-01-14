GPG
===

This GPG plugin for Sublime Text 3 adds commands to decrypt, encrypt, sign, and authenticate documents.

Menu items added
----------------

- Tools → GPG → Decrypt  
- Tools → GPG → Encrypt  
- Tools → GPG → Sign  
- Tools → GPG → Sign and encrypt  
- Tools → GPG → Verify signature

Flaws and limitations
---------------------

- The passphrase prompt does not hide the text entered. Do *not* use this while someone is looking over your shoulder!
- Signatures can only be created with the default key (the first key in the secret key ring, or else the default specified in gpg.conf).
