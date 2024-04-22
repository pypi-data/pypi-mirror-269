from pathlib import Path
from typing import List, Optional, Union

from osin.apis.osin import Osin
from osin.apis.remote_exp import RemoteExpRun
from osin.models.base import init_db
from osin.models.exp import Exp, ExpRun


class LocalOsin(Osin):
    def __init__(self, osin_dir: Union[Path, str]):
        super().__init__(osin_dir)
        init_db(self.osin_keeper.get_db_file())

    def _find_latest_exp(self, name: str) -> Optional[Exp]:
        exps = (
            Exp.select().where(Exp.name == name).order_by(Exp.version.desc()).limit(1)  # type: ignore
        )
        if len(exps) == 0:
            return None
        else:
            return exps[0]

    def _create_exp(self, exp: Exp) -> Exp:
        if exp.description is None or exp.params is None:
            raise ValueError(
                "Cannot create a new experiment without description and params"
            )
        exp.save(force_insert=True)
        return exp

    def _update_exp(self, exp_id: int, exp: Exp, fields: List[str]):
        Exp.update(**{field: getattr(exp, field) for field in fields}).where(Exp.id == exp_id).execute()  # type: ignore

    def _create_exprun(self, exprun: ExpRun) -> ExpRun:
        exprun.save(force_insert=True)
        return exprun

    def _update_exprun(self, exprun_id: int, exprun: ExpRun, fields: List[str]):
        ExpRun.update(**{field: getattr(exprun, field) for field in fields}).where(ExpRun.id == exprun_id).execute()  # type: ignore

    def _upload_exprun(self, exprun: RemoteExpRun):
        pass
