"""GPG plugin for Sublime Text 3.

This GPG plugin for Sublime Text 3 adds commands to decrypt, encrypt, sign, and
authenticate documents.
"""

__author__ = 'crowsonkb@gmail.com (Katherine Crowson)'

import sublime, sublime_plugin

import platform
import shutil
import subprocess

PASSPHRASE_APPLESCRIPT = '''
set passphrase to text returned of ¬
    (display dialog ¬
        "Enter your passphrase…" with title ¬
        "SublimeGPG" with icon ¬
        note default answer ¬
        "" with hidden answer)
'''

PIPE = subprocess.PIPE


def gpg(window, data, opts):
    """gpg calls the gpg binary to process the data and returns the result."""

    s = sublime.load_settings('gpg.sublime-settings')
    gpg_command = s.get('gpg_command')
    opts = [shutil.which(gpg_command),
            '--armor',
            '--batch',
            '--trust-model', 'always',
            '--yes'] + opts
    for _ in range(0, s.get('verbosity')):
        opts.append('--verbose')
    if not opts[0]:
        panel(window, 'Error: could not locate the gpg binary')
        return None
    try:
        gpg_process = subprocess.Popen(opts,
                                       stdin=PIPE, stdout=PIPE, stderr=PIPE)
        gpg_process.stdin.write(data.encode())
        result, error = gpg_process.communicate()
        if error:
            panel(window, error.decode())
        if gpg_process.returncode:
            return None
        return result.decode()
    except IOError as e:
        panel(window, 'Error: %s' % e)
        return None
    except OSError as e:
        panel(window, 'Error: %s' % e)
        return None


def panel(window, message):
    """panel displays gpg's stderr at the bottom of the window."""

    p = window.create_output_panel('gpg_message')
    p.run_command('gpg_message', {'message': message})
    p.show(p.size())
    window.run_command('show_panel', {'panel': 'output.gpg_message'})


def get_passphrase(window, callback):
    """get_passphrase prompts the user for their passphrase."""

    if platform.system() == 'Darwin':
        osa_process = subprocess.Popen('osascript',
                                       stdin=PIPE, stdout=PIPE, stderr=PIPE)
        osa_process.stdin.write(PASSPHRASE_APPLESCRIPT.encode())
        result, error = osa_process.communicate()
        if error:
            return
        callback(result.decode().rstrip())
    else:
        window.show_input_panel('Passphrase:', '', callback, None, None)


class GpgMessageCommand(sublime_plugin.TextCommand):
    """A helper command for panel."""

    def run(self, edit, message):
        self.view.insert(edit, self.view.size(), message)


class GpgCommand(sublime_plugin.TextCommand):
    """A helper command to replace the document content with new content."""

    def run(self, edit, opts):
        doc = sublime.Region(0, self.view.size())
        data = gpg(self.view.window(), self.view.substr(doc), opts)
        if data:
            self.view.replace(edit, doc, data)


class GpgDecryptCommand(sublime_plugin.WindowCommand):
    """Decrypts an OpenPGP format message."""

    def run(self):
        get_passphrase(self.window, self.on_done)

    def on_done(self, passphrase):
        opts = ['--passphrase', passphrase]
        self.window.active_view().run_command('gpg', {'opts': opts})


class GpgEncryptCommand(sublime_plugin.WindowCommand):
    """Encrypts plaintext to an OpenPGP format message."""

    def run(self):
        self.window.show_input_panel('Recipient:', '', self.on_done, None, None)

    def on_done(self, recipient):
        opts = ['--encrypt', '--recipient', recipient]
        self.window.active_view().run_command('gpg', {'opts': opts})


class GpgSignCommand(sublime_plugin.WindowCommand):
    """Signs the document using a clear text signature."""

    def run(self):
        get_passphrase(self.window, self.on_done)

    def on_done(self, passphrase):
        opts = ['--clearsign', '--passphrase', passphrase]
        self.window.active_view().run_command('gpg', {'opts': opts})


class GpgSignAndEncryptCommand(sublime_plugin.WindowCommand):
    """Encrypts plaintext to a signed OpenPGP format message."""

    def run(self):
        self.window.show_input_panel('Recipient:', '', self.on_done, None, None)

    def on_done(self, recipient):
        self.recipient = recipient
        get_passphrase(self.window, self.on_done2)

    def on_done2(self, passphrase):
        opts = ['--sign',
                '--encrypt',
                '--recipient', self.recipient,
                '--passphrase', passphrase]
        self.window.active_view().run_command('gpg', {'opts': opts})


class GpgVerifyCommand(sublime_plugin.WindowCommand):
    """Verifies the document's signature without altering the document."""

    def run(self):
        opts = ['--verify']
        self.window.active_view().run_command('gpg', {'opts': opts})
