# -*- coding: utf-8 -*-
# Copyright (c) 2020-2023 Salvador E. Tropea
# Copyright (c) 2020-2023 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
import os
from shutil import rmtree
from .gs import GS
from .registrable import Registrable
from .optionable import Optionable
from .error import PlotError, KiPlotConfigurationError
from .misc import PLOT_ERROR, EXIT_BAD_CONFIG, W_KEEPTMP
from .log import get_logger

logger = get_logger(__name__)


class BasePreFlight(Registrable):
    _registered = {}
    _in_use = {}
    _options = {}
    _targets = None
    _configured = False

    def __init__(self, name, value):
        super().__init__()
        self._value = value
        self._name = name
        self._sch_related = False
        self._pcb_related = False
        self._any_related = False    # True if we need an schematic OR a PCB
        self._enabled = True
        self._expand_id = ''
        self._expand_ext = ''
        self._files_to_remove = []
        self._category = None
        # Compatibility with outputs
        self.name = name
        self.comment = ''

    def config(self):
        """ Default configuration assumes this is just a boolean """
        if not isinstance(self._value, bool):
            raise KiPlotConfigurationError('must be boolean')
        self._enabled = self._value

    @staticmethod
    def reset():
        # List of used preflights
        BasePreFlight._in_use = {}
        # Defined options
        BasePreFlight._options = {}
        # Output targets
        BasePreFlight._targets = None
        # No longer configured
        BasePreFlight._configured = False

    @staticmethod
    def add_preflight(o_pre):
        BasePreFlight._in_use[o_pre._name] = o_pre

    @staticmethod
    def add_preflights(pre):
        for p in pre:
            BasePreFlight._in_use[p._name] = p

    @staticmethod
    def get_preflight(name):
        return BasePreFlight._in_use.get(name)

    @staticmethod
    def get_in_use_objs():
        return BasePreFlight._in_use.values()

    @staticmethod
    def get_in_use_names():
        return BasePreFlight._in_use.keys()

    @staticmethod
    def get_registered():
        return BasePreFlight._registered

    @staticmethod
    def _set_option(name, value):
        BasePreFlight._options[name] = value

    @staticmethod
    def get_option(name):
        return BasePreFlight._options.get(name)

    @staticmethod
    def insert_target(out):
        """ Add a target, at the beginning of the list and with high priority """
        try:
            del BasePreFlight._targets[BasePreFlight._targets.index(out)]
        except ValueError:
            pass
        BasePreFlight._targets.insert(0, out)
        out.priority = 90

    @staticmethod
    def configure_all():
        if BasePreFlight._configured:
            return
        try:
            # Configure all of them
            for k, v in BasePreFlight._in_use.items():
                logger.debug('Configuring preflight '+k)
                v.config()
        except KiPlotConfigurationError as e:
            GS.exit_with_error("In preflight `"+str(k)+"`: "+str(e), EXIT_BAD_CONFIG)
        BasePreFlight._configured = True

    @staticmethod
    def run_enabled(targets):
        BasePreFlight._targets = targets
        try:
            for k, v in BasePreFlight._in_use.items():
                if v._enabled:
                    if v.is_sch():
                        GS.check_sch()
                    if v.is_pcb():
                        GS.check_pcb()
                    logger.debug('Preflight apply '+k)
                    v.apply()
            for k, v in BasePreFlight._in_use.items():
                if v._enabled:
                    logger.debug('Preflight run '+k)
                    v.run()
        except PlotError as e:
            GS.exit_with_error("In preflight `"+str(k)+"`: "+str(e), PLOT_ERROR)
        except KiPlotConfigurationError as e:
            GS.exit_with_error("In preflight `"+str(k)+"`: "+str(e), EXIT_BAD_CONFIG)

    def disable(self):
        self._enabled = False

    # def is_enabled(self):
    #     return self._enabled

    def __str__(self):
        return "{}: {}".format(self._name, self._enabled)

    def is_sch(self):
        """ True for preflights that needs the schematic """
        return self._sch_related

    def is_pcb(self):
        """ True for preflights that needs the PCB """
        return self._pcb_related

    def is_any(self):
        """ True for outputs that needs the schematic and/or the PCB """
        return self._any_related

    def get_example():
        """ Returns a YAML value for the example config """
        return 'true'

    @classmethod
    def get_doc(cls):
        return cls.__doc__, None

    def run(self):
        pass

    def apply(self):
        pass

    def get_dependencies(self):
        """ Returns a list of files needed to run this preflight """
        files = []
        if self._sch_related:
            if GS.sch:
                files.extend(GS.sch.get_files())
            else:
                files.append(GS.sch_file)
        if self._pcb_related:
            files.append(GS.pcb_file)
        return files

    def get_targets(self):
        """ Returns a list of targets generated by this preflight """
        return []

    def get_navigate_targets(self, _):
        """ Returns a list of targets suitable for the navigate results """
        return self.get_targets(), None

    def expand_dirname(self, out_dir):
        return Optionable.expand_filename_both(self, out_dir, is_sch=self._sch_related)

    def _find_variant(self):
        # Preflights doesn't have a variant, but we could have one global default
        if hasattr(self, '_variant') and self._variant:
            return self._variant.file_id
        return Optionable._find_global_variant()

    def _find_variant_name(self):
        # Preflights doesn't have a variant, but we could have one global default
        if hasattr(self, '_variant') and self._variant:
            return self._variant.name
        return Optionable._find_global_variant_name()

    def _find_subpcb(self):
        # Preflights doesn't have a variant, but we could have one global default
        if hasattr(self, '_variant') and self._variant and self.variant._sub_pcb:
            return self.variant._sub_pcb.name
        return Optionable._find_global_subpcb()

    def ensure_tool(self, name):
        """ Looks for a mandatory dependency """
        return GS.check_tool_dep(self._name, name, fatal=True)

    def check_tool(self, name):
        """ Looks for a dependency """
        return GS.check_tool_dep(self._name, name, fatal=False)

    def add_extra_options(self, cmd, dir=None):
        """ KiAuto extra options (debug, record, etc.) """
        cmd, video_remove = GS.add_extra_options(cmd)
        if video_remove:
            self._files_to_remove.append(os.path.join(dir or cmd[-1], GS.get_kiauto_video_name(cmd)))
        return cmd

    def exec_with_retry(self, cmd, exit_with=None):
        remove_tmps = False
        try:
            ret = GS.exec_with_retry(cmd, exit_with)
            remove_tmps = True
        finally:
            if GS.debug_enabled and not remove_tmps:
                if self._files_to_remove:
                    logger.warning(W_KEEPTMP+'Keeping temporal files: '+str(self._files_to_remove))
            else:
                self.remove_temporals()
        if self._files_to_remove:
            self.remove_temporals()
        return ret

    def remove_temporals(self):
        logger.debug('Removing temporal files')
        for f in self._files_to_remove:
            if os.path.isfile(f):
                logger.debug('- File `{}`'.format(f))
                os.remove(f)
            elif os.path.isdir(f):
                logger.debug('- Dir `{}`'.format(f))
                rmtree(f)
        self._files_to_remove = []

    @staticmethod
    def get_conf_examples(name, layers):
        return None

    def get_category(self):
        return self._category
