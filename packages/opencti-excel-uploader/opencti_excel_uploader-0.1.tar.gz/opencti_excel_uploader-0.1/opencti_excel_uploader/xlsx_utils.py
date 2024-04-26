import pandas as pd
from opencti_excel_uploader.models import (
    # Incident,
    Narrative,
    Observable,
    Identity,
    Event,
    Campaign,
    Vulnerability,
    CourseOfAction,
    AttackPattern,
    ThreatActor,
    Report,
    opencti_client,
)
import uuid
import datetime
import os
import json
import random
from opencti_excel_uploader.xml_utils import create_bundle
import openpyxl

now = datetime.datetime.now()
published = now.isoformat() + "Z"


def stix_id(entity_type):
    random_str = str(random.randint(1000, 9999))
    return f"{entity_type}--{str(uuid.uuid5(uuid.NAMESPACE_DNS, random_str))}"


def load_excel(file):
    # Load the workbook and get sheet names
    sheets = openpyxl.load_workbook(file).sheetnames
    df = {}

    for sheet in sheets:
        # Read each sheet into a DataFrame
        sheet_df = pd.read_excel(file, sheet_name=sheet, engine="openpyxl")

        # Normalize column names by removing all whitespaces
        sheet_df.columns = [col.strip() for col in sheet_df.columns]

        df[sheet] = sheet_df

    df = {
        key.strip(): value.fillna("").rename(columns=lambda x: x.strip())
        for key, value in df.items()
    }
    return df


def process_threat_actor(threat_actor_data, instructions):
    # Drop first row with instructions
    if instructions:
        threat_actor_data = threat_actor_data.drop(0)

    # Create a list of threat actors
    threat_actors = []
    for _, row in threat_actor_data.iterrows():
        threat_actors.append(ThreatActor(name=row["Name"]))
    return threat_actors


def process_observables(observables_data, instructions):
    # Drop first row with instructions
    if instructions:
        observables_data = observables_data.drop(0)

    # Create a list of observables
    observables = []
    for _, row in observables_data.iterrows():
        if row["URL"] == "":
            break
        observable = Observable(
            url=row["URL"],
            date=row["Datetime"],
            archivedUrl=row["Archived link"],
            language=row["Language"],
        )
        observables.append(observable)
    return observables


def process_identity(identity_data, instructions):
    # Drop first row with instructions
    if instructions:
        identity_data = identity_data.drop(0)

    # Create a list of identities
    identities = []
    for _, row in identity_data.iterrows():
        identity_name = row["Name"]
        lookup_filters = {
            "mode": "and",
            "filters": [
                {
                    "key": "alias",
                    "values": identity_name,
                    "operator": "contains",
                },
                {
                    "key": "name",
                    "values": identity_name,
                },
            ],
            "filterGroups": [],
        }

        lookup_location = opencti_client.location.read(filters=lookup_filters)
        if lookup_location:
            identities.append(
                Identity(
                    name=lookup_location[0]["name"],
                    idClass=lookup_location[0]["identity_class"],
                )
            )
            break

        lookup_identity = opencti_client.identity.read(filters=lookup_filters)
        if lookup_identity:
            identities.append(
                Identity(
                    name=lookup_identity[0]["name"],
                    idClass=lookup_identity[0]["identity_class"],
                )
            )
            break

        identities.append(
            Identity(
                name=row["Name"],
                idClass="Unknown",
                description=row["Description"],
            )
        )
    return identities


def process_event(event_data, instructions):
    # Drop first row with instructions
    if instructions:
        event_data = event_data.drop(0)

    # Create a list of events
    events = []
    for _, row in event_data.iterrows():
        event = Event(
            name=row["Name"],
            description=row["Description"],
            start_date=datetime.datetime.strptime(row["Start date"], "%Y-%m-%d"),
            end_date=datetime.datetime.strptime(row["End date"], "%Y-%m-%d"),
        )
        events.append(event)
    return events


def process_attack_pattern(attack_pattern_df):
    # Find TTPs used in Incident
    attack_pattern_df["Used in Incident"] = attack_pattern_df[
        "Used in Incident"
    ].str.upper()
    attack_pattern_df = attack_pattern_df[
        attack_pattern_df["Used in Incident"] == "X"
    ].reset_index()

    # Return all attack patterns used in the incident
    attack_patterns = [
        AttackPattern(technique=row["Technique"].split(": ")[-1].strip())
        for _, row in attack_pattern_df.iterrows()
    ]
    return attack_patterns


def process_narratives(narratives_data, instructions):
    # Drop first row with instructions
    if instructions:
        narratives_data = narratives_data.drop(0)

    # Create a list of narratives
    narratives = []
    for _, row in narratives_data.iterrows():
        narrative = Narrative(
            name=row["Name"],
            description=row["Description"],
        )
        narratives.append(narrative)
    return narratives


def process_course_of_action(coa_df, external_ref_list, instructions):
    # Drop first row with instructions
    if instructions:
        coa_df = coa_df.drop(0)

    # Create a list of COAs
    coas = []
    for _, row in coa_df.iterrows():
        if row["Name"] == "":
            break
        if row["External Reference"]:
            external_ref_list.append(row["External Reference"])
        coas.append(
            CourseOfAction(
                name=row["Name"],
                description=row["Description"],
                extRef=row["External Reference"],
            )
        )
    return coas


def process_campaign(campaign_data, external_ref_list, instructions):
    # Drop first row with instructions
    if instructions:
        campaign_data = campaign_data.drop(0)

    # Create a list of campaigns
    campaigns = []
    for _, row in campaign_data.iterrows():
        if row["External Reference"]:
            external_ref_list.append(row["External Reference"])
        campaign = Campaign(
            name=row["Name"],
            description=row["Description"],
            extRef=row["External Reference"],
        )
        campaigns.append(campaign)
    return campaigns


def process_vulnerabilities(vulnerabilities_data, instructions):
    # Drop first row with instructions
    if instructions:
        vulnerabilities_data = vulnerabilities_data.drop(0)

    # Create a list of vulnerabilities
    vulnerabilities = []
    for _, row in vulnerabilities_data.iterrows():
        vulnerability = Vulnerability(
            name=row["Name"],
            description=row["Description"],
        )
        vulnerabilities.append(vulnerability)
    return vulnerabilities


def process_report(df):
    # Initialize related objects and external references
    related_objects = []
    external_ref_list = []
    data = df["Incident"]
    instructions = True

    # Check length of data
    if len(data) == 1:
        instructions = False
    else:
        print("Dropping first row with instructions for all sheets.")

    data = data.iloc[-1]

    # Retrieve related objects
    for key in df.keys():
        if key == "Threat Actor":
            related_objects.extend(process_threat_actor(df[key], instructions))
        if key == "Identity":
            related_objects.extend(process_identity(df[key], instructions))
        if key == "Event":
            related_objects.extend(process_event(df[key], instructions))
        if key == "Narratives":
            related_objects.extend(process_narratives(df[key], instructions))
        if key == "Observables":
            related_objects.extend(process_observables(df[key], instructions))
        if key == "Attack Pattern":
            related_objects.extend(process_attack_pattern(df[key]))
        if key == "Course of Action":
            related_objects.extend(
                process_course_of_action(df[key], external_ref_list, instructions)
            )
        if key == "Campaign":
            related_objects.extend(
                process_campaign(df[key], external_ref_list, instructions)
            )
        if key == "Vulnerabilities":
            related_objects.extend(process_vulnerabilities(df[key], instructions))

    return Report(
        name=data["Name"],
        description=data["Description"],
        objectLabel=[],
        first_seen=now,
        confidence=90,
        objective=[],
        objectMarking="TLP:AMBER+STRICT",
        extRef=[data["External Reference"]].extend(external_ref_list),
        author="EEAS",
        relatedEntities=related_objects,
    )


def excel_to_json(file):
    df = load_excel(file)
    report = process_report(df)
    bundle = create_bundle(report)
    for item in bundle["objects"]:
        print(item)
    with open(f"./excel_workbenches/{report.name}.json", "w") as f:
        print(f"Writing {report.name}.json to 'excel_workbenches' folder.")
        json.dump(bundle, f)


def folder_to_json(folder):
    for root, _, files in os.walk(folder):
        # If the folder has no xlsx files, skip
        if not any(file.endswith(".xlsx") for file in files):
            print(f"No Excel files found in {root}. Moving to next folder.")
            continue
        for file in files:
            if file.endswith(".xlsx"):
                print(f"Converting {os.path.join(root, file)} to JSON")
                excel_to_json(os.path.join(root, file))
