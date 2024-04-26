import uvicorn
import os
from fastapi import BackgroundTasks, FastAPI
from dbt.cli.main import dbtRunner
from pydantic import BaseModel
import multiprocessing

app = FastAPI()

class DbtRunConfig(BaseModel):
    cmd: str
    parameters: dict = {}  # New field for parameters

    def prepare_command(self):
        cmd_list = self.cmd.split(" ")[1:]
        for key, value in self.parameters.items():
            cmd_list.extend([key, value])
        return cmd_list


def dbt_task(cmd_list):
    dbt = dbtRunner()
    dbt.invoke(cmd_list)


def run_dbt(runConfig: DbtRunConfig):
    cmd = runConfig.prepare_command()
    proc = multiprocessing.Process(
        target=dbt_task,
        args=(cmd,))
    proc.start()
    
    return {'pid': proc.pid}


@app.get('/callback')
def root():
    return {'message': 'This endpoint works!'}


@app.post("/dbt")
async def run_dbt_command_endpoint(runConfig: DbtRunConfig, background_tasks: BackgroundTasks):
    return run_dbt(runConfig)