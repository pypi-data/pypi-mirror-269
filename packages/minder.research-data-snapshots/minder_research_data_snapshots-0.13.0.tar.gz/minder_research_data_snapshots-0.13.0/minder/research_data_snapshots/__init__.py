"""minder.research-data-snapshots."""

import os
from pathlib import Path

import platformdirs
import requests
from tqdm import tqdm


def _download_dataset(
    dataset: str,
    organization: str,
    folder: Path,
    refresh: bool,
    token: str,
    api: str,
) -> Path:
    file = (folder / organization / dataset).with_suffix(".parquet")
    if file.exists() and not refresh:
        return file
    file.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(
        f"{api}/data/organization/{organization}/{dataset}.parquet",
        headers={"Authorization": f"Bearer {token}"},
        stream=True,
        timeout=3600,
    )
    response.raise_for_status()
    with file.open(mode="wb") as f:
        progress = tqdm(
            desc=str(file),
            total=int(response.headers.get("content-length", -1)),
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        )
        for chunk in response.iter_content(1024):
            f.write(chunk)
            progress.update(len(chunk))
    return file


def download_datasets(
    datasets: list[str],
    organizations: list[str] | None = None,
    folder: Path | None = None,
    refresh: bool = False,
    token_path: Path | None = None,
    csv: bool = False,
) -> list[Path]:
    """Download one or more datasets.

    Parameters
    ----------
    datasets
        List of datasets to retrieve e.g. `["raw_heart_rate"]`
    organizations
        List of cohorts to include e.g. `["EMXHH7vg3xHNM7k2862nD6"]`. Defaults to all cohorts that you have access to.
    folder
        Path of destination folder for downloaded files. Defaults to user data folder (exact location depends on your
        operating system).
    refresh
        Whether to overwrite existing files. Set this to `True` if you want to update your downloaded data. Defaults to
        `False`.
    token_path
        Path of file containing your personal access token (PAT) from the Research Portal. If not specified then the
        value of the `RESEARCH_PORTAL_TOKEN_PATH` environment variable is used.
    csv
        Convert Parquet files to CSV. Set this to `True` if you're using Excel for data analysis. Otherwise Parquet is a
        superior format. Defaults to `False`.

    Returns
    -------
    List of paths of downloaded Parquet files. Length will be number of datasets * number of cohorts.

    """
    RESEARCH_PORTAL_API = os.getenv("RESEARCH_PORTAL_API", "https://research.minder.care/api")
    MINDER_TOKEN = (
        os.environ["MINDER_TOKEN"]
        if "MINDER_TOKEN" in os.environ
        else Path(token_path or os.environ["RESEARCH_PORTAL_TOKEN_PATH"]).read_text("utf-8").rstrip()
    )
    if organizations is None:
        response = requests.get(
            f"{RESEARCH_PORTAL_API}/info/organizations",
            headers={"Authorization": f"Bearer {MINDER_TOKEN}"},
            timeout=5,
        )
        response.raise_for_status()
        organizations = [organization["id"] for organization in response.json()["organizations"]]
    if folder is None:
        folder = platformdirs.user_cache_path("research-data-snapshots")
    parquets = [
        _download_dataset(dataset, organization, folder, refresh, MINDER_TOKEN, RESEARCH_PORTAL_API)
        for dataset in datasets
        for organization in organizations
    ]
    if csv:
        import pyarrow.csv
        import pyarrow.parquet

        csvs = []
        for parquet in parquets:
            csv_path = parquet.with_suffix(".csv")
            pyarrow.csv.write_csv(pyarrow.parquet.read_table(parquet), csv_path)
            csvs.append(csv_path)
        return csvs
    return parquets
