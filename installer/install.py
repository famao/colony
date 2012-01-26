
import glob
import os
import subprocess
import sys
import yaml
from parse_erb import dump_config

def run_command(cmd, redirect_output=True, check_exit_code=True):
    """
    Runs a command in an out-of-process shell, returning the
    output of that command.  Working directory is ROOT.
    """
    if redirect_output:
        stdout = subprocess.PIPE
    else:
        stdout = None

    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=stdout)
    output = proc.communicate()[0]
    if check_exit_code and proc.returncode != 0:
        die('Command "%s" failed.\n%s', ' '.join(cmd), output)
    return output


class ConfigItem(object):
    def __init__(self, name, def_value, *args, **kwargs):
        self._name = name
        self._default_value = def_value
        self._value = None
        self._install = False

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def default_value(self):
        return self._default_value

    @property
    def install(self):
        return self._install

    def ask(self):
        v = raw_input('%s : [default:%s]' % (self._name, self._default_value))
        if not v:
           v = self._default_value
        # validator
        self._value = v
        self._install = True

    def to_dict(self):
        return { self._name : self._value }

class PathConfigItem(ConfigItem):
    pass

class Config(object):
    def __init__(self, filename):
        self._yml = filename
        self._configs = []
        self._components_configs = []

    def _load_config(self):
        items = self._ymlobj['config_item_defaults']
        for item in items:
            config = ConfigItem(item['name'], item['value'])
            self._configs.append(config)

    @property
    def config(self):
        return self._configs

    @property
    def components(self):
        res = {}
        for item in self._components_configs:
            if not res.get(item.name, None):
                res[item.name] = []
            res[item.name].append(item)
        return res

    def _load_components_config(self):
        items = self._ymlobj['component_config_defaults']
        for item in items:
            config = PathConfigItem(item['component'], item['path'])
            self._components_configs.append(config)
        # dodai-deploy needs hostname for component
        for comp_name, value in self.components.iteritems():
            config = ConfigItem(comp_name, '127.0.0.1')
            self._configs.append(config)

    def load(self, filename = None):
        if not self._yml and not filename:
            raise Exception('fuga')
        value = open(self._yml).read()
        self._ymlobj = yaml.load(value)
        self._load_config()
        self._load_components_config()
    
    def _ask(self, name):
        v = raw_input('installing :%s y/N ?' % name)
        if v in ['Y', 'y']:
            return True
        return False

    def ask(self):
        for config in self._configs:
            config.ask()

        for comp_name, components_configs in self.components.iteritems():
            # check install components
            if self._ask(comp_name):
                for config in components_configs:
                    config.ask()


class ConfigManager(object):

    templates = 'templates'

    def _get_templates_path(self, name, path):
        filename = os.path.basename(path)
        return '%s/softwares/%s/%s/%s.erb' % ( os.path.curdir, name, ConfigManager.templates, filename)

    def __init__(self):
        files = glob.glob('./softwares/*/data.yml')
        self._softwares = {}
        for file in files:
            name = os.path.abspath(os.path.dirname(file)).split(os.path.sep)[-1]
            c = Config(file)
            c.load()
            self._softwares[name] = c

    def _ask(self, name):
        v = raw_input('installing :%s y/N ?' % name)
        if v in ['Y', 'y']:
            return True
        return False
        
    def ask(self):
        for name, value in self._softwares.iteritems():
            if self._ask(name):
                value.ask()
                for comp_name, comp_configs in value.components.iteritems():
                    for comp_config in comp_configs:
                        if comp_config.install:
                            template_path = self._get_templates_path(name, comp_config.default_value)
                            dump_config(value.config, template_path, comp_config.value)


cm = ConfigManager()
cm.ask()

"""
for file in files:
    c = Config(file)
    c.load()
    c.ask()
    dump_config(c.config)
"""