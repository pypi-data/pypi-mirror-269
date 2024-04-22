"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2020-2024 Fair Isaac Corporation. All rights reserved.
"""

import os
import threading
from typing import ValuesView, Optional, Dict, Any, Iterable, Callable

from .. import entities as xi_entities
from .data_connector import DataConnector
from ..entities import get_non_composed_entities_from_names, get_non_composed_entities, basic_types as xi_types


def input_scalars_filter(entity: xi_entities.EntityBase) -> bool:
    """ Filter that accepts only scalar entities that are input and not update-after-execution. """
    return (isinstance(entity, xi_entities.Scalar) and
            entity.is_managed(xi_entities.Manage.INPUT) and
            not entity.update_after_execution)


class AppDataConnector:
    """
    AppDataConnector performs the requests to load / save the data for the application class as a whole.
    It does not subclass DataConnector, but rather wraps one and converts the higher-level requests made of the
    app (e.g. load input entities) to lower-level requests to the table connector (e.g. load these specific
    entities).
    """

    def __init__(self, app, base: DataConnector):
        self._app = app
        self._entities: ValuesView[xi_entities.EntityBase] = app.app_cfg.entities
        self._base = base
        self._original_input_only_scalar_values: Optional[Dict[str, Any]] = None
        self._lock = threading.RLock()  #

    def _load_meta(self):
        # pylint: disable=protected-access
        meta_values = self._base.load_meta()

        if 'http_port' in meta_values[xi_types.integer] and 'http_token' in meta_values[xi_types.string]:
            rest_port = meta_values[xi_types.integer]['http_port']
            rest_token = meta_values[xi_types.string]['http_token']
            # noinspection PyProtectedMember
            self._app.insight._init_rest(rest_port, rest_token)

        if 'app_id' in meta_values[xi_types.string]:
            self._app.insight._app_id = meta_values[xi_types.string]['app_id']

        if 'app_name' in meta_values[xi_types.string]:
            self._app.insight._app_name = meta_values[xi_types.string]['app_name']

        if 'scenario_id' in meta_values[xi_types.string]:
            self._app.insight._scenario_id = meta_values[xi_types.string]['scenario_id']

        if 'scenario_name' in meta_values[xi_types.string]:
            self._app.insight._scenario_name = meta_values[xi_types.string]['scenario_name']

        if 'scenario_path' in meta_values[xi_types.string]:
            self._app.insight._scenario_path = meta_values[xi_types.string]['scenario_path']

    def _warn_about_work_dir(self):
        if os.path.isdir(self._app.insight.work_dir):
            print("Test mode: Using existing Insight working directory.")

    def _check_base_exists(self):
        if self._base.is_empty():
            raise FileNotFoundError(f'Cannot find data store: "{self._base}".')

    def _get_input_only_scalar_values(self) -> Dict[str, any]:
        """ Capture a dictionary of the input-only scalar values (excluding update-after-execution scalars) in
        the app """
        input_scalar_values = {}
        for e in self._app.app_cfg.entities:
            if input_scalars_filter(e) and e.name in self._app.__dict__:
                input_scalar_values[e.name] = self._app.__dict__[e.name]

        return input_scalar_values

    def initialize_entities(self, *, names: Iterable[str] = None,
                            entities: Iterable[xi_entities.EntityBase] = None,
                            manage: xi_entities.Manage = None,
                            entity_filter: Callable[[xi_entities.Entity], bool] = None,
                            overwrite: bool = False):
        """ Initialize entities to their default values.  Entities are filtered by the `names`, `entities`, `manage`
            and `entity_filter` arguments, or all entities will be initialized if none of thesr are set.

        Parameters
        ----------
        names : Iterable[str] = None
            The names of entities to be initialized. Columns can be specified with their full entity names
            (ie "<frame-name>_<col_name>"). If the name of a data frame is included, all its columns will be
            initialized.
        entities: Iterable[EntityBase] = None
            The entities to be initialized. If a DataFrame object is included, all of its columns will be initialized.
            Must not be set if `names` is also set.
        manage: Manage = None
            The manage-type of entities to be initialized.  Applied as an additional filter to the `names`/`entities`
            values (for example, to allow initialization of only RESULT columns of a DataFrame).
        entity_filter: Callable[[Entity], bool] = None
            Function to filter available entities to decide if they are to be initialized.  If an entity filter is
            provided, the `names`, `entities` and `manage` arguments must not be set.
        overwrite: bool = False
            Flag indicating whether we should overwrite existing values.
            If not set to `True` and one of the selected entities has a value, a `ValueError` will be raised.
        """
        if entity_filter:
            #
            if names or entities or manage:
                raise ValueError('When using a filter function, no other entity selection arguments must be passed.')

        else:
            #
            if names is not None and entities is not None:
                raise ValueError('At most one of arguments "names" and "entities" must be passed.')

            #
            if names is not None:
                entity_names = set(e.entity_name for e in get_non_composed_entities_from_names(self._entities, names))
            elif entities is not None:
                entity_names = set(e.entity_name for e in get_non_composed_entities(entities))
            else:
                entity_names = None

            def filter_by_names_and_manage(entity: xi_entities.Entity):
                if entity_names is not None and entity.entity_name not in entity_names:
                    return False
                if manage and entity.manage != manage:
                    return False
                return True

            entity_filter = filter_by_names_and_manage

        with self._lock:
            self._base.initialize_entities(entity_filter=entity_filter, overwrite=overwrite)

    def clear_input(self):
        """ Clear values of input entities, setting parameters/scalars to default values. """
        with self._lock:
            if self._app.insight.test_mode:
                self._warn_about_work_dir()
                is_empty_data_repo = self._base.is_empty()

                if is_empty_data_repo:
                    print(f'Test mode: Creating new data repository in: "{self._app.insight.work_dir}".\n'
                          'Test mode: Setting uninitialized parameters and scalars to default value.\n')

                else:
                    print(f'Test mode: Loading parameters from data repository in: "{self._app.insight.work_dir}".\n'
                          'Test mode: Setting uninitialized scalars to default value.\n')
                    #
                    self._load_meta()
                    #
                    self._base.load_entities(lambda entity: isinstance(entity, xi_entities.Param))

                #
                self._base.initialize_entities(lambda entity: (isinstance(entity, xi_entities.Param) and
                                                               entity.name not in self._app.__dict__))

                #
                self._base.initialize_entities(lambda entity: (isinstance(entity, xi_entities.Scalar) and
                                                               (entity.manage == xi_entities.Manage.RESULT or
                                                                entity.name not in self._app.__dict__)))

                #
                self._base.clean()

                #
                self._base.save_entities(lambda entity: isinstance(entity, xi_entities.Param))

                #
                self._original_input_only_scalar_values = self._get_input_only_scalar_values()

            else:
                self._check_base_exists()

                #
                self._load_meta()
                #
                self._base.load_entities(lambda entity: isinstance(entity, xi_entities.Param))
                #
                self._base.initialize_entities(lambda entity: (isinstance(entity, xi_entities.Scalar) and
                                                               (entity.is_managed == xi_entities.Manage.RESULT or
                                                                entity.name not in self._app.__dict__)))

    def save_input(self):
        """ Save values of input entities. """
        with self._lock:
            self._base.save_entities(lambda entity: entity.is_managed(xi_entities.Manage.INPUT))

    def load_input(self):
        """ Load values of input entities. """
        with self._lock:
            if self._app.insight.test_mode:
                self._warn_about_work_dir()
                if self._base.is_empty():
                    print(f'Test mode: Creating new data repository: "{self._app.insight.work_dir}".\n'
                          'Test mode: Setting uninitialized parameters and scalars to default value.\n'
                          'Test mode: Inputs have to be initialized manually before calling this execution mode.\n')
                    self._base.clean()
                    self._base.initialize_entities(lambda entity: (isinstance(entity, xi_entities.ScalarBase) and
                                                                   entity.is_managed(xi_entities.Manage.INPUT) and
                                                                   entity.name not in self._app.__dict__))
                    self.save_input()

                else:
                    print(f'Test mode: Loading parameters and input from data '
                          f'repository: "{self._app.insight.work_dir}".\n')
                    self._load_meta()
                    self._base.load_entities(lambda entity: entity.is_managed(xi_entities.Manage.INPUT))

                #
                self._original_input_only_scalar_values = self._get_input_only_scalar_values()

            else:
                self._check_base_exists()
                self._load_meta()
                self._base.load_entities(lambda entity: entity.is_managed(xi_entities.Manage.INPUT))

            #
            self._base.initialize_entities(lambda entity: (isinstance(entity, xi_entities.Scalar) and
                                                           entity.manage == xi_entities.Manage.RESULT))

    def save_result(self):
        """ Save values of result and update-after-execution entities. """
        with self._lock:
            if self._app.insight.test_mode:
                #
                #
                #
                input_scalar_values = self._get_input_only_scalar_values()

                #
                if self._original_input_only_scalar_values:
                    for (name, value) in self._original_input_only_scalar_values.items():
                        self._app.__dict__[name] = value

                #
                #
                self._base.save_entities(lambda entity: (entity.is_managed(xi_entities.Manage.RESULT) or
                                                         isinstance(entity, xi_entities.Scalar)))

                #
                #
                for (name, value) in input_scalar_values.items():
                    self._app.__dict__[name] = value

            else:
                #
                self._base.save_entities(lambda entity: entity.is_managed(xi_entities.Manage.RESULT))

    def save_progress(self):
        """ Save values of progress entities. """
        with self._lock:
            self._base.save_entities(lambda entity: entity.update_progress)

    @property
    def base(self):
        """ Generic DataContainer being used by the app. """
        return self._base
