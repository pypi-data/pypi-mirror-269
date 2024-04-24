import subprocess as sp
import tempfile
from typing import Union, Literal, List, Dict, Union
from .wrapper import jarfile
from .io import write_to_brat, parse_output

def evaluate(
        ground_truth: Union[Dict, List[Dict]],
        prediction: Union[List[Dict]],
        span_match: Union[Literal["exact", "overlap"], float] = "exact",
        type_match: Literal["exact", "inexact"] = "exact"
    ):
    # Ensure list type
    if isinstance(ground_truth, dict):
        ground_truth = [ground_truth]
    else:
        ground_truth = list(ground_truth)
    if isinstance(prediction, dict):
        prediction = [prediction]
    else:
        prediction = list(prediction)

    if len(prediction) != len(ground_truth):
        raise ValueError("Number of documents from ground truth and prediction does not match.")

    # parse configuration parameters
    span_match_params = None
    if isinstance(span_match, str):
        span_match = span_match.strip()

    if span_match in ["exact", "overlap"]:
        span_match_params = ["-s", span_match.upper()]
    elif isinstance(span_match, float):
        assert span_match <= 1.0
        assert span_match >= 0.0
        # approximate
        span_match_params = ["-s", "APPROXIMATE", str(span_match)]
    else:
        raise ValueError("Unknown span match parameter: {}".format(span_match))

    type_match_params = None
    type_match = type_match.strip()
    if type_match in ["exact", "inexact"]:
        type_match_params = ["-t", type_match.upper()]
    else:
        raise ValueError("Unknown type match parameter: {}".format(type_match))

    # prepare files
    with tempfile.TemporaryDirectory() as gt_dir, tempfile.TemporaryDirectory() as pd_dir:
        for i, (gt_itm, pd_itm) in enumerate(zip(ground_truth,prediction)):
            ### Ground truth data
            write_to_brat(gt_itm, str(i+1), gt_dir)
            ### Predicted data
            write_to_brat(pd_itm, str(i+1), pd_dir)

            if gt_itm["text"] != pd_itm["text"]:
                raise ValueError("At document {} the text did not match.".format(i+1))

        locale_args = ["-Duser.language=en", "-Duser.country=US"]
        # run brateval
        try:
            stdout = sp.check_output([
                "java", *locale_args, "-cp", jarfile(), "au.com.nicta.csp.brateval.CompareEntities", pd_dir, gt_dir,
                *span_match_params, *type_match_params
            ])
        except:
            raise Exception("Calling brateval.jar ({}) caused a runtime error...".format(jarfile()))

        # extract results
        results = parse_output(stdout)
        return results

if __name__ == "__main__":
    # Test cases...
    gt_line = {
        "text": "This is bad", "label": [
            [8, 10, "adj"]
        ]
    }

    pd_line = {
        "text": "This is bad", "label": [
            [8, 10, "adj"]
        ]
    }

    x = evaluate(gt_line, pd_line)
    y = evaluate([gt_line], [pd_line])