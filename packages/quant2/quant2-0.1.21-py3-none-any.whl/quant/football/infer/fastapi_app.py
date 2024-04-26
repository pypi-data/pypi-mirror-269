# uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
# uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --workers 4
# MODEL_ROOT=/workspace/models uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --workers 4
# MODEL_ROOT=/workspace/models uvicorn quant.football.infer.fastapi_app:app --host 0.0.0.0 --port 8000 --workers 4
import os
import pathlib
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from quant.football.infer.football_overunder_v1 import FootballInferencer


def get_predictors(model_root):
    predictors = {}
    for model_archive in pathlib.Path(model_root).glob("*.tar"):
        predictors[model_archive.stem] = FootballInferencer(model_archive)
    return predictors


app = FastAPI()
predictors = get_predictors(os.environ.get("MODEL_ROOT", "/workspace/models"))


@app.post("/predictor")
async def read_section(section: dict):
    try:
        titan = section["mapping_match"]["titan"]

        for key in ["home_half_score", "visiting_half_score"]:
            titan[key] = titan[key] if titan[key] else "0"

        for key_src, key_dst in [("home_team_id", "home_team"), ("visiting_team_id", "visiting_team")]:
            if key_src not in titan:
                titan[key_src] = titan[key_dst]

        # "1"-上场, "2"-中场, "3"-下场, "-1"-结束
        match_state = titan["match_state"]
        real_start_time = titan["real_start_time"]

        crawler_time = section["event_titan"]["crawler_end_time"]

        curr_time = -1
        if match_state == "1":
            curr_time = (crawler_time - real_start_time) / 60
            curr_time = 44.9 if curr_time > 44.9 else curr_time
        elif match_state == "3":
            curr_time = 45 + (crawler_time - real_start_time) / 60
            curr_time = 89.9 if curr_time > 89.9 else curr_time

        curr_time = curr_time if curr_time > 0.1 else -1

        section["curr_time"] = curr_time
        section["game_time"] = int(curr_time + 1.0)

        company = section["bets"]["company"]
        match_id = section["bets"]["match_id"]
        section_data_id = section["section_data_id"]
        action = {"company": company, "match_id": match_id, "action_id": section_data_id, "curr_time": curr_time}

        bets = []
        for _, predictor in predictors.items():
            if predictor.is_valid(section):
                bets.extend(predictor(section))
        action["betsList"] = bets
    except:
        raise HTTPException(status_code=500, detail=traceback.format_exc())

    return JSONResponse(content=action)
