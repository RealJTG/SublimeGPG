GPG
===

This GPG plugin for Sublime Text 3 adds commands to decrypt, encrypt, sign, and authenticate documents. It requires a working copy of [GPG](http://www.gnupg.org/) with a key already generated. (If you haven't generated a key, see [this mini-HOWTO](http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto-3.html#ss3.1).) If the gpg binary is not in `$PATH`, you will have to set its location in Preferences → Package Settings → GPG. On Mac OS, I recommend installing GPG using the [Homebrew package manager](http://brew.sh/): after installing Homebrew, run `brew install gpg`.

Menu items added
----------------

- Preferences → Package Settings → GPG
- Tools → GPG → Decrypt  
- Tools → GPG → Encrypt  
- Tools → GPG → Sign  
- Tools → GPG → Sign and encrypt  
- Tools → GPG → Verify signature

Flaws and limitations
---------------------

- The passphrase prompt does not hide the text entered. Do *not* use this while someone is looking over your shoulder!
- Signatures can only be created with the default key (the first key in the secret key ring, or else the default specified in gpg.conf).
