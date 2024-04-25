import atexit
import re
from collections import defaultdict
from typing import Dict, List, Any, Tuple

from abc import ABC, abstractmethod
from pandas import DataFrame
import time

from .types import AvailableModel, Import, ImportSource
from ..clients.config import Config
from ..compiler import Compiler
from .. import dsl, debugging, metamodel as m

#--------------------------------------------------
# InstallBatch
#--------------------------------------------------

class InstallBatch:
    def __init__(self):
        self.dirty = set()
        self.content:Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.task_map = defaultdict(dict)

    def _cell(self):
        return debugging.jupyter.cell() or ""

    def _check_dirty_cells(self, name:str):
        for cell in debugging.jupyter.dirty_cells:
            self.content[name][cell].clear()
        debugging.jupyter.dirty_cells.clear()

    def append(self, name:str, code:str, task:m.Task|None=None):
        self._check_dirty_cells(name)
        self.dirty.add(name)
        self.content[name][self._cell()].append((code, task))

    def set(self, name:str, code:str, task:m.Task|None=None):
        self.dirty.add(name)
        self.content[name][self._cell()] = [(code, task)]

    def flush(self):
        items = []
        for name in self.dirty:
            all_cells = []
            cur_line = 0
            task_map = self.task_map[name]
            for _, content in self.content[name].items():
                for (code, task) in content:
                    all_cells.append(code)
                    end = code.count("\n") + cur_line + 2
                    task_map[task] = (cur_line, end)
                    cur_line = end
            items.append((name, "\n\n".join(all_cells)))
        self.dirty.clear()
        return items

    def is_dirty(self):
        return len(self.dirty) > 0

    def line_to_task(self, name:str, line:int):
        for task, (start, end) in self.task_map[name].items():
            if start <= line <= end:
                return task
        return None

#--------------------------------------------------
# Resources
#--------------------------------------------------

class ResourceProvider(ABC):
    def __init__(self, profile: str | None = None, config:Config|None=None):
        super().__init__()
        self.config = config or Config(profile)
        atexit.register(self.cancel_pending_transactions)

    @property
    def platform(self):
        return self.config.get("platform")

    @abstractmethod
    def reset(self):
        pass

    #--------------------------------------------------
    # Generic
    #--------------------------------------------------

    @abstractmethod
    def get_version(self):
        pass

    #--------------------------------------------------
    # Engines
    #--------------------------------------------------

    @abstractmethod
    def list_engines(self) -> List[Any]:
        pass

    @abstractmethod
    def get_engine(self, name: str):
        pass

    @abstractmethod
    def create_engine(self, name: str, size: str, pool:str=""):
        pass

    @abstractmethod
    def delete_engine(self, name: str):
        pass

    @abstractmethod
    def suspend_engine(self, name: str):
        pass

    @abstractmethod
    def resume_engine(self, name: str):
        pass

    def get_default_engine_name(self) -> str:
        return self.config.get("engine")

    def get_app_name(self):
        return self.config.get("rai_app_name", "relationalai")

    #--------------------------------------------------
    # Transactions
    #--------------------------------------------------

    @abstractmethod
    def list_transactions(self, limit:int, only_active=False) -> List[dict]:
        pass

    @abstractmethod
    def cancel_transaction(self, transaction_id):
        pass

    @abstractmethod
    def cancel_pending_transactions(self):
        pass

    #--------------------------------------------------
    # Graphs
    #--------------------------------------------------

    @abstractmethod
    def list_graphs(self) -> List[AvailableModel]:
        pass

    @abstractmethod
    def get_graph(self, name:str):
        pass

    @abstractmethod
    def create_graph(self, name: str):
        pass

    @abstractmethod
    def delete_graph(self, name: str):
        pass

    #--------------------------------------------------
    # Models
    #--------------------------------------------------

    @abstractmethod
    def list_models(self, database: str, engine: str):
        pass

    @abstractmethod
    def create_models(self, database: str, engine: str, models:List[Tuple[str, str]]) -> List[Any]:
        pass

    @abstractmethod
    def delete_model(self, database: str, engine: str, name: str):
        pass

    #--------------------------------------------------
    # Exports
    #--------------------------------------------------

    @abstractmethod
    def list_exports(self, database: str, engine: str):
        pass

    @abstractmethod
    def create_export(self, database: str, engine: str, name: str, inputs: List[Tuple[str, str, Any]], out_fields: List[Tuple[str, Any]], code: str):
        pass

    @abstractmethod
    def delete_export(self, database: str, engine: str, name: str):
        pass

    #--------------------------------------------------
    # Imports
    #--------------------------------------------------

    @abstractmethod
    def list_imports(self, model: str) -> list[Import]:
        pass

    @abstractmethod
    def create_import_stream(self, source: ImportSource, model: str, rate: int, options: dict|None):
        pass

    @abstractmethod
    def create_import_snapshot(self, source: ImportSource, model: str, options: dict|None):
        pass

    @abstractmethod
    def delete_import(self, import_name: str, model: str):
        pass

    #--------------------------------------------------
    # Exec
    #--------------------------------------------------

    @abstractmethod
    def exec_raw(self, database: str, engine: str, raw_code: str, readonly: bool = True, inputs={}) -> Any: # @FIXME: Better type annotation
        pass

    @abstractmethod
    def format_results(self, results, task:m.Task|None=None) -> Tuple[DataFrame, List[Any]]:
        pass


#--------------------------------------------------
# Client
#--------------------------------------------------

class Client():
    def __init__(self, resources:ResourceProvider, compiler:Compiler, database:str, dry_run=False):
        self.dry_run = dry_run
        self._database = database
        self.compiler = compiler
        self._install_batch = InstallBatch()
        self.resources = resources

        if not self.dry_run:
            start = time.perf_counter()
            existing = self.resources.get_graph(self._database)
            if not existing:
                self.resources.create_graph(self._database)
                debugging.time("create_database", time.perf_counter() - start)

    def get_engine_name(self, name:str|None=None) -> str:
        return str(name or self.resources.config.get("engine"))

    def report_errors(self, errors:List[Any], abort_on_error=True, task=None):
        maybe_abort = False
        undefineds = []
        if len(errors):
            for problem in errors:
                if problem.get("is_error") or problem.get("is_exception"):
                    maybe_abort = True
                    message = problem.get("message", "")
                    report = problem.get("report", "")
                    path = problem.get("path", "")
                    if problem.get("error_code") == "UNDEFINED_IDENTIFIER":
                        match = re.search(r'`(.+?)` is undefined', message)
                        line = report.split("|")[0]
                        if line:
                            line = int(line) - 1
                        source_task = self._install_batch.line_to_task(path, line) or task
                        source = debugging.get_source(source_task)
                        if not source:
                            source = debugging.SourceInfo()
                        undefineds.append((match.group(1), source))
                    else:
                        if message:
                            print(message)
                        if report:
                            print(report)
        if abort_on_error and maybe_abort:
            from relationalai.errors import RelQueryError, Errors
            if undefineds:
                Errors.rel_undefineds(undefineds)
            raise RelQueryError(errors)

    def load_raw_file(self, path:str):
        content = open(path).read()
        code = self.compiler.compile(dsl.build.raw_task(content))
        self._install_batch.set(path, code)

    def exec_raw(self, code:str, readonly=True, raw_results=True, inputs={}):
        return self.query(dsl.build.raw_task(code), readonly=readonly, raw_results=raw_results, inputs=inputs)

    def install_raw(self, code:str, name:str="pyrel_batch_0"):
        if not name:
            name = "pyrel_batch_0"
        self.compiler.compile(dsl.build.raw_task(code))
        self._install_batch.append(name, code)

    def query(self, task:m.Task, rentrant=False, readonly=True, raw_results=False, inputs={}) -> DataFrame|Any:
        if self._install_batch.is_dirty():
            self._install_batch_flush()

        with debugging.span("query", model=self._database, task=task) as end_span:
            code = self.compiler.compile(task)
            if task.has_persist():
                readonly = False
            if self.dry_run:
                return DataFrame()

            start = time.perf_counter()
            results = self.resources.exec_raw(self._database, self.get_engine_name(), code, readonly=readonly, inputs=inputs)
            dataframe, errors = self.resources.format_results(results, task)
            end_span["results"] = dataframe
            end_span["errors"] = errors
            if raw_results:
                debugging.time("query", time.perf_counter() - start, DataFrame())
                self.report_errors(errors, abort_on_error=False)
                return results
            self.report_errors(errors, task=task)
            debugging.time("query", time.perf_counter() - start, dataframe)
            return dataframe

    def _install_batch_flush(self):
        if not self.dry_run:
            with debugging.span("install_batch", model=self._database):
                start = time.perf_counter()
                code = self._install_batch.flush()
                errors = self.resources.create_models(self._database, self.get_engine_name(), code)
                self.report_errors(errors)
                debugging.time("install_batch", time.perf_counter() - start, code="\n".join([c[1] for c in code]))

    def install(self, name, task:m.Task):
        with debugging.span("rule", model=self._database, task=task, name=name):
            code = self.compiler.compile(task)
            self._install_batch.append("pyrel_batch_0", code, task=task)

    def export_udf(self, name, inputs:List[Tuple[str, m.Var, Any]], outputs, task:m.Task, engine=""):
        cols = task.return_cols()
        if len(outputs) != len(cols):
            raise Exception(f"Expected {len(outputs)} outputs, got {len(cols)}")
        emitted_inputs = [(name, self.compiler.emitter.emit(var), type) for (name, var, type) in inputs]
        outputs = list(zip(cols, outputs))
        if not engine:
            engine = self.get_engine_name()
        if not self.dry_run:
            self.resources.create_export(self._database, engine, name, emitted_inputs, outputs, self.compiler.compile(task))
