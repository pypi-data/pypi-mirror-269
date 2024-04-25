# ignore all type errors
import json

import pandas as pd

from lastmile_eval.rag.debugger.api import evaluation

project_id = "clv4clhdv009wqpl2xy6febdc"
evaluation_test_set_id = "clv4cnhek004yqyy92wsl320s"

prod_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..i4MtL9O76DKs-6Vg.wiKue2CUsvsau5jDwIfDjc-PMAhcFYpM43t_HbL_0Q2j79HGDlBkRXG71sXBTpFzNNOq5SsrA06akX-l6LQWPQbUKZ-MVz3b-ceKuKlA0uH-xJNr6HVXHcVBfLx7SHeLinK8W_eYN4MeJOJ8n8T4ILnpy7Li19hZRouMVLC_HezlpGQPG4pQfYkoq1BLWfecgFErtlb7QmWnwujc6N4pvqlahpLJw4DBiJOicGJWHHd52yg40Vu7n_J9C-y02X8.YFl27avAV7Mr_WBoQmcvEg"
# local_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..7rMlewjboJd7DEDV.vtCWhtrJNwTEuuoX8ZkwgJJSRviHjJdNQkWav71CEkYQ6X75N4-oZ-AhLWzPzt-hxfrzEo9p9Ko82SCFMMoHfBBXklngg4wT3jm5ejDgI5RGixtlgoHxOI3H_iUopZ3ySYnT38Z9mUZyoUlfQI0tqG3XsBUxqy5wTWTcGlgQBPPFviQzUt781b7VWUDhX1StXaIe2-VWkUJJyjOlxHNxpN8nuI5BkMtAdhHCdNHdz2-FphnhbwkcCxo9PWPzZp0.883S1KtkWbVglb68NHVkMA"
token_rd = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..3yBBdax1yZpLb4ht.iBeSuj_MYLs4DOyrWSb1XqFCdfUSnSMBENE5wISbETBbD68MByM4oae0Pxpxfv5S-YydMn4GVBWE0ViDkv2M9oe5ttU4IHwHYWPfHM4zhUXOVfCmZQLs7KbEmQXVc2s5VOIiNIApKUfU6AnlpDhkLrwL5Yr-ukRUvHKezhN9Pa9qwtEi5LwR4gY2pw5S3mTmAgOqzjUD3wUoKsAV0SUtnYkwGtIAHrICK9jJob-K6k0P6NeiXxlU7kU.7ef6pOZ3yXTmLlCK4klpsA"


def main():
    test1()
    test2()


def test2():
    project_id = "clv4clhdv009wqpl2xy6febdc"

    token = token_rd

    dfrqt = evaluation.download_rag_query_traces(
        lastmile_api_token=token, project_id=project_id
    )

    dfrqt["query"] = [{"query": "what color is the quick fox?"}] * len(dfrqt)

    print("DFRQT")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    print(
        dfrqt[
            [
                "ragQueryTraceId",
                "paramSet",
                "query",
                "context",
                "fullyResolvedPrompt",
                "output",
                "ragIngestionTraceId",
                "ragIngestionTrace",
            ]
        ]
    )

    create_res = evaluation.create_test_set_from_rag_query_traces(
        dfrqt,
        "Test Evaluation Set",
        lastmile_api_token=token,
        ground_truth=["xyz"] * len(dfrqt),
    )

    print(f"{create_res=}")

    downloaded = evaluation.download_test_set(
        create_res.ids[0],
        lastmile_api_token=token,
    )

    print(
        "Just created + downloaded:\n",
        json.dumps(downloaded.to_dict("records"), indent=2),
    )


def test1():
    token = prod_token
    # def pdoptions(r=2, c=20, w=50):
    #     pd.set_option("display.max_rows", r)
    #     pd.set_option("display.max_columns", c)
    #     pd.set_option("display.max_colwidth", w)

    dfts = evaluation.download_test_set(evaluation_test_set_id, prod_token)
    # pdoptions(r=None)
    print("DFTS")
    print(dfts.T)

    def eval1(df_test_cases):
        # print(f"eval1: {df_test_cases.T}")
        return (
            df_test_cases.apply(lambda r: r.groundTruth in r.output, axis=1)
            .to_frame("substr")
            .astype(float)
            .substr
        )

    trace_level_evaluators = {
        "substr": eval1,
    }
    dataset_level_evaluators = {}

    dfe_t, dfe_d = evaluation.run_evaluations(
        dfts,
        trace_level_evaluators=trace_level_evaluators,
        dataset_level_evaluators=dataset_level_evaluators,
    )

    print("DFE_T")
    print(dfe_t)
    print("DFE_D")
    print(dfe_d)

    upload_result = evaluation.store_evaluation_set_results(
        project_id, dfe_t, dfe_d, token_rd
    )
    print(f"Upload result:\n{upload_result}")

    result2 = evaluation.run_and_store_evaluations(
        evaluation_test_set_id,
        project_id,
        trace_level_evaluators,
        dataset_level_evaluators,
        token,
        evaluation_set_name="Test Evaluation Set",
    )

    print(f"Result2: {result2}")


if __name__ == "__main__":
    main()
