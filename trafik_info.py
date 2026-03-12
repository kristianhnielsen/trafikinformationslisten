import datetime
import os
from typing import Any
import requests
from docxtpl import DocxTemplate
import pandas as pd
from dotenv import load_dotenv

from local_logs import update_log


def get_data(params: dict[str, Any]):
    url = "https://kortservice.vejle.dk/gis/rest/services/SEPTIMA/vej_sw/MapServer/23/query"

    # Make the request
    response = requests.get(url, params=params)
    data = response.json()
    # Extract name values from features
    porperties = [feature["properties"] for feature in data.get("features", [])]
    return porperties


def format_data(df: pd.DataFrame):
    for col in df.columns:
        if df[col].dtype == "object":
             df[col]= df[col].str.replace("&", "&amp;").str.strip()


    # format road info and user direction
    df["road_info"] = df["oov2roaduserdescription"].str.strip()

    # rename column dataframe columns to match the template
    df.rename(
        columns={
            "oov2roadinfo": "title",
            "contractorcontactperson": "contractor_contact_person",
            "contractormobile": "contractor_phone",
            "ownermailaddress": "contractor_email",
            "name": "contractor_company",
            "oov2roadmarkstart": "starttime",
            "oov2roadmarkend": "endtime",
            "serialnumber": "case_id",
            "modulename": "source",
        },
        inplace=True,
    )

    # convert date columns to datetime
    datetime_format = "%d-%m-%Y"
    # Convert to datetime but do NOT immediately convert back to string
    df["startdate"] = pd.to_datetime(df["startdate"], errors="coerce")
    df["enddate"] = pd.to_datetime(df["enddate"], errors="coerce")

    # Now sorting will work as expected, because columns are datetime objects
    df.sort_values(by=["startdate", "starttime"], inplace=True, ascending=False)

    # If you need to display them as strings later:
    df["startdate"] = df["startdate"].dt.strftime(datetime_format)
    df["enddate"] = df["enddate"].dt.strftime(datetime_format)

    # add starttime and endtime to period, if startdate and enddate are the same
    df["duration"] = df.apply(
        lambda row: (
            f"{row['startdate']} fra kl. {row['starttime']} til kl. {row['endtime']}"
            if row["startdate"] == row["enddate"]
            and row["starttime"] is not None
            and row["endtime"] is not None
            else f"fra {row['startdate']} til {row['enddate']}"
        ),
        axis=1,
    )

    # Capitalize the contractor contact person names
    df["contractor_contact_person"] = df["contractor_contact_person"].apply(
        lambda x: (
            " ".join(name_element.capitalize() for name_element in x.split(" "))
            if isinstance(x, str)
            else x
        )
    )



def get_file_output_path(filename: str) -> str:
    # Set up environment
    load_dotenv()  # Load environment variables from .env

    today_date, _, _ = get_dt_data()

    output_folder_base = os.getenv("OUTPUT_FOLDER", "")  # Get from .env
    output_folder = os.path.join(output_folder_base, str(today_date.year))
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)
    return output_path


def get_dt_data():
    today_date = datetime.datetime.today().date()
    today_date_text = today_date.strftime("%d-%m-%Y")
    next_week_number = today_date.isocalendar()[1] + 1
    return today_date, today_date_text, next_week_number


def get_dk_month_name(month_number: int) -> str:
    month_names = {
        1: "januar",
        2: "februar",
        3: "marts",
        4: "april",
        5: "maj",
        6: "juni",
        7: "juli",
        8: "august",
        9: "september",
        10: "oktober",
        11: "november",
        12: "december",
    }
    return month_names.get(month_number, "")


def get_report(output_filename: str, query_params: dict[str, Any]):
    today_date, today_date_text, next_week_number = get_dt_data()
    output_path = get_file_output_path(output_filename)

    # get the data from the API
    data = get_data(params=query_params)

    df = pd.DataFrame(data)
    format_data(df)

    # remove duplicates based on case_id and source
    df.drop_duplicates(
        subset=["case_id", "source"],
        inplace=True,
    )

    # read the template and render the data
    doc_template = DocxTemplate("trafik_info_template.docx")

    roadwork = df.to_dict(orient="records")

    contents = {
        "roadwork": roadwork,
        "today_date": today_date_text,
        "current_year": today_date.year,
        "week_number": next_week_number,
        "document_type": (
            f"UGE {next_week_number}"
            if "UGE" in output_filename
            else f"MÅNED {get_dk_month_name(today_date.month)}"
        ),
    }
    doc_template.render(contents)
    doc_template.save(output_path)


def weekly_report():
    try:
        today_date, _, next_week_number = get_dt_data()

        query_params = {
            "returnGeometry": "true",
            "outSR": "25832",
            "f": "geojson",
            "outFields": "*",
            "where": "traficstatus = 'Trafikudmeldt' and dagetilstart <= 10",
            "orderByFields": "startdate",
        }
        filename = f"TRAFIK-INFO - UGE {next_week_number} {today_date.year}.docx"

        get_report(filename, query_params)
        update_log(f"Weekly Report script executed successfully.")
    except Exception as e:
        update_log(f"Weekly Report Error: {str(e)}")
        raise e


def monthly_report():
    try:
        today_date, _, _ = get_dt_data()
        month_name = get_dk_month_name(today_date.month)

        query_params = {
            "returnGeometry": "true",
            "outSR": "25832",
            "f": "geojson",
            "outFields": "*",
            "where": "traficstatus = 'Trafikudmeldt' and dagetilstart <= 32",
            "orderByFields": "startdate",
        }

        filename = f"TRAFIK-INFO - MÅNED {month_name} {today_date.year}.docx"
        get_report(filename, query_params)
        update_log(f"Monthly Report script executed successfully.")
    except Exception as e:
        update_log(f"Monthly Report Error: {str(e)}")
        raise e
