import sublime, sublime_plugin

import os
import shutil
import subprocess

def gpg(window, data, opts):
    s = sublime.load_settings('GPG.sublime-settings')
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
        return data
    try:
        gpg_process = subprocess.Popen(opts,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        gpg_process.stdin.write(data.encode())
        result, error = gpg_process.communicate()
        if error:
            panel(window, error.decode())
        if gpg_process.returncode:
            return data
        return result.decode()
    except IOError as e:
        panel(window, 'Error: %s' % e)
        return data
    except OSError as e:
        panel(window, 'Error: %s' % e)
        return data


def panel(window, message):
    p = window.create_output_panel('gpg_error')
    p.run_command('gpg_message', {'message': message})
    p.show(p.size())
    window.run_command('show_panel', {'panel': 'output.gpg_error'})


class GpgMessageCommand(sublime_plugin.TextCommand):
    def run(self, edit, message):
        self.view.insert(edit, self.view.size(), message)


class GpgCommand(sublime_plugin.TextCommand):
    def run(self, edit, opts):
        doc = sublime.Region(0, self.view.size())
        data = gpg(self.view.window(), self.view.substr(doc), opts)
        self.view.replace(edit, doc, data)


class GpgDecryptCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Passphrase:', '', self.on_done, None, None)

    def on_done(self, passphrase):
        opts = ['--passphrase', passphrase]
        self.window.active_view().run_command('gpg', {'opts': opts})


class GpgEncryptCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Recipient:', '', self.on_done, None, None)

    def on_done(self, recipient):
        opts = ['-e', '-r', recipient]
        self.window.active_view().run_command('gpg', {'opts': opts})


class GpgSignCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Passphrase:', '', self.on_done, None, None)

    def on_done(self, passphrase):
        opts = ['--clearsign', '--passphrase', passphrase]
        self.window.active_view().run_command('gpg', {'opts': opts})
