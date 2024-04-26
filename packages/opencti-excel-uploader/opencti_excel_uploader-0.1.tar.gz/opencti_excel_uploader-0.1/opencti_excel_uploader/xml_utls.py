import xml.etree.ElementTree as ET
from datetime import datetime
from opencti_excel_uploader.models import (
    Incident,
    Narrative,
    Observable,
    Identity,
    Event,
    CourseOfAction,
    AttackPattern,
    ThreatActor,
    Report,
)
import uuid
import random
import json
import os

survey_titles = {
    "632407d4-b9bc-f4ee-af74-88926741018a": "report",
    "3f07fbb1-0afd-0a06-0da3-d5dfd6f5f0d7": "incident",
    "b6733ae1-9cef-2741-e15b-9e3ef470cf05": "ticket",
}


def load_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root


def get_qns(root):
    """Retrieves the questions from the survey and pairs them with answers for multiple choice or select"""
    qns = {}
    elements = root.findall(".//Elements")[0]
    for element in elements.iter():
        if element.tag == "Question":
            current_question_id = element.attrib["id"]
            qns[current_question_id] = {
                "question": element.text,
                "possible_answers": {},
            }
        elif element.tag == "Answer":
            if current_question_id:
                qns[current_question_id]["possible_answers"][element.attrib["id"]] = (
                    element.text
                )
    return qns


def get_qids(root):
    """Prints question titles and their IDs to a file"""
    survey_id = root.findall(".//Survey")[0].attrib["alias"]
    with open(f"./qids/{survey_titles[survey_id]}_qids.txt", "w") as f:
        elements = root.findall(".//Elements")[0]
        for element in elements.iter():
            if element.tag == "Question":
                f.write(f"{element.text}: {element.attrib['id']}\n")


def get_answers(root, qns):
    """Retrieves the questions and pairs them with the appropriate questions"""
    result = {
        "survey_id": root.findall(".//Survey")[0].attrib["alias"],
    }

    answers = []
    answersets = root.findall(".//AnswerSet")

    for answerset in answersets:
        current_set = {}
        for element in answerset.iter():
            qid = element.attrib.get("qid")
            if qid:
                if qid not in current_set.keys():
                    current_set[qid] = []
                aid = element.attrib.get("aid")
                if aid:
                    answer = qns[qid]["possible_answers"][aid]
                else:
                    answer = element.text
                current_set[qid].append(answer)
        answers.append(current_set)
    result["answers"] = answers
    return result


def lookup_answer(qid, answers):
    data = answers
    if qid in data.keys():
        return data[qid]
    return None


def answers_to_stix(answers, processed_list=[]):
    """Converts the answers to a STIX object"""
    results = []
    match answers["survey_id"]:
        # Incidents
        case "3f07fbb1-0afd-0a06-0da3-d5dfd6f5f0d7":
            if answers["answers"]:
                for i in range(len(answers["answers"])):
                    if (
                        lookup_answer(
                            "b261ecd5-decf-45a9-8b53-85851ee0fc93",
                            answers["answers"][i],
                        )[0]
                        in processed_list
                    ):
                        break
                    try:
                        first_seen = (
                            (
                                lookup_answer(
                                    "19eb9887-28c5-4660-852d-f4e547a88629",
                                    answers["answers"][i],
                                )
                                or [datetime.now().strftime("%Y-%m-%d")]
                            )[0]
                            + ":"
                            + (
                                lookup_answer(
                                    "529b4a66-8d7f-4270-9313-1773d04a539b",
                                    answers["answers"][i],
                                )
                                or ["00:00:00"]
                            )[0]
                        )

                        label_ids = [
                            "6e8461a8-921a-48e7-9adf-36b8d8900180",
                            "9b77ff7a-f6fd-4643-b6a4-47e3dc3c9d75",
                            "8014863b-dc91-4b55-ac25-fb38941ebd8a",
                            "36d988b6-2b81-406d-a9de-c409329a97d0",
                        ]
                        all_labels = []
                        for label_id in label_ids:
                            if lookup_answer(label_id, answers["answers"][i]):
                                all_labels.append(
                                    lookup_answer(label_id, answers["answers"][i])[0]
                                )

                        # Create the incident
                        incident = Incident(
                            incidentType="x-opencti-case-incident",
                            name=(
                                lookup_answer(
                                    "b261ecd5-decf-45a9-8b53-85851ee0fc93",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            description=(
                                lookup_answer(
                                    "5276e6b4-72ae-417d-b772-d4d4df8dc99c",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0]
                            + (
                                lookup_answer(
                                    "db6f8243-d32d-46e1-85e0-0686245fd9ff",  # Author email
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            confidence=90,
                            first_seen=datetime.strptime(
                                first_seen, "%Y-%m-%d:%H:%M:%S"
                            ),
                            objectMarking="TLP:AMBER+STRICT",
                            objectLabel=all_labels,
                            objective=(
                                lookup_answer(
                                    "1737b237-0010-4853-b5c8-5499423cc6de",
                                    answers["answers"][i],
                                )
                                or [""]
                            ),
                        )
                        print("Incident created successfully")
                    except Exception as e:
                        raise ValueError(
                            "Error in creating incident #{}: {}".format(i, e)
                        )

                    # Add the threat actor
                    try:
                        if lookup_answer(
                            "d4b3f89d-b4f4-4029-8336-968005c21097",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                ThreatActor(
                                    name=lookup_answer(
                                        "d4b3f89d-b4f4-4029-8336-968005c21097",
                                        answers["answers"][i],
                                    )[0],
                                )
                            )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding threat actor to incident #{i}: {e}"
                        )

                    # Add the narrative
                    try:
                        if lookup_answer(
                            "6bfc33f1-90b0-4569-a35a-9f970ffbe1f7",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                Narrative(
                                    name=lookup_answer(
                                        "6bfc33f1-90b0-4569-a35a-9f970ffbe1f7",
                                        answers["answers"][i],
                                    )[0],
                                )
                            )
                    except Exception as e:
                        raise ValueError(
                            "Error in adding narrative to incident #{}: {}".format(i, e)
                        )

                    # Add the URLs
                    urls = [
                        "59b991f3-e036-4165-ac15-b062ad45e990",
                        "90039a01-98ea-40dc-a19d-dc71e2bee0d0",
                        "20f01413-a4ec-4740-86e1-f2a04fe79c02",
                        "aff5636c-0abe-45e2-8f76-beb91c52883f",
                        "346090f1-7120-4613-a868-60f24e838fdb",
                        "55b6fa87-1596-4c35-8c50-1f1d33ae403f",
                        "e8b59141-d9b4-4388-9428-ccf314712b6f",
                        "3f9a63dd-c415-452e-921e-735ee0771efd",
                        "1a2ba265-e2d5-415f-964a-e44ca0878dde",
                        "acc227ca-be3f-459d-b00f-4300d14eddc8",
                    ]
                    dates = [
                        "b093d02e-83c9-45aa-9acc-4d109c919413",
                        "0c9f0a38-1f5f-4000-8f8e-97cd3bde3c0d",
                        "c564403f-e904-47d9-84cc-80bbba7a1d87",
                        "32ff1745-5200-46e1-92f1-34eafcc3416b",
                        "e5857df4-adf9-48d5-8025-3bc0acf1f0c7",
                        "40c2b870-2b55-4299-8998-498e1c7d3a08",
                        "393c048e-10b4-4345-8eda-c0f2125f5883",
                        "ff45e62a-c496-4462-8713-8f52a6a55296",
                        "9dfaa10b-3e0d-4f3d-8e37-42ccc9e625fc",
                        "748c7a7d-375b-4568-8ef4-f0cf962fe16d",
                    ]
                    # archivedUrls = []
                    for j in range(len(urls)):
                        try:
                            if lookup_answer(urls[j], answers["answers"][i]):
                                if lookup_answer(dates[j], answers["answers"][i]):
                                    incident.relatedEntities.append(
                                        Observable(
                                            url=lookup_answer(
                                                urls[j], answers["answers"][i]
                                            )[0],
                                            date=datetime.strptime(
                                                (
                                                    lookup_answer(
                                                        dates[j], answers["answers"][i]
                                                    )
                                                    or [
                                                        datetime.now().strftime(
                                                            "%Y-%m-%d"
                                                        )
                                                    ]
                                                )[0],
                                                "%Y-%m-%d",
                                            ),
                                            # archivedUrl=(lookup_answer(
                                            #     archivedUrls[j], answers["answers"][i]
                                            # ) or [""])[0],
                                        )
                                    )
                                else:
                                    incident.relatedEntities.append(
                                        Observable(
                                            url=lookup_answer(
                                                urls[j], answers["answers"][i]
                                            )[0],
                                        )
                                    )
                        except Exception as e:
                            raise ValueError(
                                f"Error in adding URL {j} to incident #{i}, error {e}"
                            )

                    # Add identities
                    identities = {
                        "05b3cd05-5eaa-4de1-bc05-40b02c22ff3f": [
                            "b9c1cde1-078d-4e79-b27b-e8cad0c73f03",
                            "d8d33af5-5298-41ce-8871-c8dae23a7b84",
                        ],
                        "e142648b-70c5-4928-8b29-442e507811c6": [
                            "33e1da3c-5c18-4eba-a58a-edaffb5f3c7a",
                            "5b87f1e6-71c1-4d31-8a59-d5be7e279901",
                        ],
                        "8573cf26-cadc-418d-ab35-36344b29ff0b": [
                            "0c023514-6031-45f4-a2ef-cd06719088c6",
                            "ec146a02-b81b-4270-af07-bbace7b46fd4",
                        ],
                        "c03a097e-f954-4d40-9799-d4e8102bdbb5": [
                            "b1e3a0c3-bd6e-43e0-8579-66d9b71350cb",
                            "61490303-23b1-47c9-9694-809782529344",
                        ],
                        "6d3505b1-ef3c-4d66-b70b-0587b70a10e0": [
                            "afd76cd1-32b3-4261-8476-9e83f8a0c8c3",
                            "65bd37ae-a7ec-4d52-a9e1-4719573e8eff",
                        ],
                    }
                    try:
                        for key in identities.keys():
                            if lookup_answer(key, answers["answers"][i]):
                                if (
                                    lookup_answer(key, answers["answers"][i])[0]
                                    == "Country"
                                ):
                                    incident.relatedEntities.append(
                                        Identity(
                                            name=lookup_answer(
                                                identities[key][0],
                                                answers["answers"][i],
                                            )[0],
                                            idClass="Country",
                                        )
                                    )
                                else:
                                    incident.relatedEntities.append(
                                        Identity(
                                            name=lookup_answer(
                                                identities[key][1],
                                                answers["answers"][i],
                                            )[0],
                                            idClass=lookup_answer(
                                                key, answers["answers"][i]
                                            ),
                                        )
                                    )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding one or more identity to incident #{i}, error {e}"
                        )

                    # Add event
                    try:
                        if lookup_answer(
                            "933be5c4-865a-46d3-8ff8-8545aecdeb13",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                Event(
                                    name=lookup_answer(
                                        "933be5c4-865a-46d3-8ff8-8545aecdeb13",
                                        answers["answers"][i],
                                    )[0],
                                    location=lookup_answer(
                                        "bd866e29-7564-4cff-bb8b-a271862d9bd1",
                                        answers["answers"][i],
                                    )[0],
                                    start_date=datetime.strptime(
                                        lookup_answer(
                                            "d670e193-bc6f-42a1-ad80-8b2e4f3eb479",
                                            answers["answers"][i],
                                        )[0],
                                        "%Y-%m-%d",
                                    ),
                                    end_date=datetime.strptime(
                                        lookup_answer(
                                            "4753628d-5713-4814-8e0a-d40c79371a0e",
                                            answers["answers"][i],
                                        )[0],
                                        "%Y-%m-%d",
                                    ),
                                )
                            )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding event to incident #{i}, error {e}"
                        )

                    # Add courses of action
                    coas = {
                        "Statement of refutal": [
                            "4a74085e-6687-4e3e-b5c9-f0781522c660",
                            "8e416070-05f9-47fd-bca8-0f965db051ed",
                        ],
                        "Debunking": [
                            "f9a2b289-7dc5-445d-81eb-139d6ae4e3b4",
                            "b6e1864f-fa68-43d4-8493-821d14101e68",
                        ],
                        "Content deleted": [
                            "279fe260-e69a-4168-9168-3548701c9496",
                            "2cdc532e-3f34-417e-9a9b-81b0706b6b2d",
                        ],
                        "Content confined": [
                            "8f5ecb15-625c-4e05-8ae6-e0bba4b7a94b",
                            "a22428cf-c3ec-4069-8a77-8939f9cba42b",
                        ],
                        "Other": [
                            "60bf4a9c-a467-4e17-bfea-cd2590d5d091",
                            "ec060d6e-aeb6-47e3-bfe9-03df97944163",
                        ],
                    }
                    for key in coas.keys():
                        try:
                            if lookup_answer(
                                coas[key][0], answers["answers"][i]
                            ) and lookup_answer(coas[key][1], answers["answers"][i]):
                                incident.relatedEntities.append(
                                    CourseOfAction(
                                        name=key,
                                        description=lookup_answer(
                                            coas[key][0], answers["answers"][i]
                                        )[0],
                                        extRef=lookup_answer(
                                            coas[key][1], answers["answers"][i]
                                        )[0],
                                    )
                                )
                        except Exception as e:
                            raise ValueError(
                                f"Error in adding Countermeasure {key} to incident #{i}, error {e}"
                            )

                    ttps = [
                        "a17a915f-6ac7-4fd0-afaa-e540e1742aba",
                        "02b5e3b4-a1c1-408a-a7f6-90061b531b52",
                        "b5eb3e6a-2c24-404d-b6bd-545f1aa0fa91",
                        "70e7a648-1e42-4a57-a21d-12ac467964ac",
                        "4d6cfc10-7476-4d24-bcb7-83c069be66b7",
                        "444d265a-92c3-48f0-95ee-d86ddf7dd991",
                        "917ee6f6-2c27-463c-ab6d-4da3d14d105d",
                        "1bff8e6c-f7b0-4524-950e-db9726c24877",
                        "c1816ed7-c2a4-43eb-8091-88028997efc6",
                        "709a722c-7ce6-42f6-a7c5-5a70d3726618",
                        "3742835d-575c-4fb4-8cb4-d1f8a1166269",
                        "b3fef493-540e-4db8-887f-5e425dd8398a",
                        "383501f4-f947-4b48-b6ad-a7bca1e8b83e",
                        "d0f47796-25e3-4821-bf01-5e322d8da192",
                        "bb0fc4a9-6afa-45a9-959e-d7855d66420c",
                        "7792d6d5-87e3-495e-aa52-24470ab6ccae",
                    ]
                    try:
                        for ttp in ttps:
                            if lookup_answer(ttp, answers["answers"][i]):
                                for j in lookup_answer(ttp, answers["answers"][i]):
                                    if lookup_answer(j, answers["answers"][i]):
                                        incident.relatedEntities.append(
                                            AttackPattern(
                                                technique=lookup_answer(
                                                    j, answers["answers"][i]
                                                ).split(": ")[1],
                                            )
                                        )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding TTP to incident #{i}, error {e}"
                        )

                    results.append(incident)
                    print(
                        f"Successfully added incident {incident.name} to results with {len(incident.relatedEntities)} related entities"
                    )

        # Reports
        case "632407d4-b9bc-f4ee-af74-88926741018a":
            if answers["answers"]:
                for i in range(len(answers["answers"])):
                    if (
                        lookup_answer(
                            "7998e231-f3cc-48be-9b88-9e3a5f3e3a0e",
                            answers["answers"][i],
                        )[0]
                        in processed_list
                    ):
                        break
                    try:
                        author = lookup_answer(
                            "4fc4b519-a73a-4a46-9301-5bf7e83f64f7",
                            answers["answers"][i],
                        )
                        first_seen = (
                            (
                                lookup_answer(
                                    "ab21fa1f-18e6-4f0b-9403-47872d660a70",
                                    answers["answers"][i],
                                )
                                or [datetime.now().strftime("%Y-%m-%d")]
                            )[0]
                            + ":"
                            + (
                                lookup_answer(
                                    "516485e2-e8ea-4407-94c9-2137c25b34d4",
                                    answers["answers"][i],
                                )
                                or ["00:00:00"]
                            )[0]
                        )

                        label_ids = [
                            "fb4471cf-0bd2-40e7-b959-031039db5d3c",
                            "78a4d7a6-6731-475b-8afe-821b10302427",
                            "e0be8d75-455c-4b02-a9aa-1778ee9f3ba3",
                            "c07ae143-d0bd-47c7-b402-1bc1310b316c",
                        ]
                        all_labels = []
                        for label_id in label_ids:
                            if lookup_answer(label_id, answers["answers"][i]):
                                all_labels.append(
                                    lookup_answer(label_id, answers["answers"][i])[0]
                                )

                        # Create the report
                        incident = Report(
                            name=(
                                lookup_answer(
                                    "7998e231-f3cc-48be-9b88-9e3a5f3e3a0e",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            description=(
                                lookup_answer(
                                    "0e47734c-195c-4a25-ad44-421b36a1ac86",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            confidence=90,
                            first_seen=datetime.strptime(
                                first_seen, "%Y-%m-%d:%H:%M:%S"
                            ),
                            objectMarking="TLP:AMBER+STRICT",
                            objectLabel=all_labels,
                            objective=[""],
                            extRef=(
                                lookup_answer(
                                    "daf23ff5-2046-44a8-9843-8084ad0f9a77",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            author=(author or [""])[0],
                        )
                    except Exception as e:
                        raise ValueError(f"Error in creating report #{i} error: {e}")

                    # Add the threat actor
                    try:
                        if lookup_answer(
                            "ce410c8a-34c7-4b7b-a5a1-df0c4e46a890",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                ThreatActor(
                                    name=lookup_answer(
                                        "ce410c8a-34c7-4b7b-a5a1-df0c4e46a890",
                                        answers["answers"][i],
                                    )[0],
                                )
                            )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding threat actor to report #{i}, error {e}"
                        )

                    # Add the narrative
                    try:
                        if lookup_answer(
                            "94f6fbf3-8adf-4b72-b4c4-3066d6b3ce2d",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                Narrative(
                                    name=lookup_answer(
                                        "94f6fbf3-8adf-4b72-b4c4-3066d6b3ce2d",
                                        answers["answers"][i],
                                    )[0],
                                )
                            )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding narrative to report #{i} error {e}"
                        )

                    # Add the URLs
                    urls = [
                        "69419223-46db-45bb-ae3c-673b6bc6f2e8",
                        "218ab48e-29c2-434a-ae52-4bf9511d5bca",
                        "feb027f9-9786-4cc6-ad84-c9eea986596b",
                        "4ce9d32b-cfdb-4532-8289-45f2f6bb94b1",
                        "c58cd87c-4026-4eea-8b51-a1a1d7d74a02",
                        "8ab06dc9-b47e-4764-b16e-e6b0b7086745",
                        "fd706e0d-224c-491b-8080-10ea0f3b06ed",
                        "7f482b30-93cb-4af4-a6e2-d8037c233247",
                        "4768aeca-2959-4bca-b3d4-60436c65b8af",
                        "d343bfa8-4859-4663-8f3d-d33e9f10588b",
                    ]
                    dates = [
                        "7e71d307-094d-400f-a2d4-5128dbeff640",
                        "3f37767a-a81a-452b-abda-4c7371d2164b",
                        "3d0d1e42-c134-4dd6-aa18-aa7a0923f646",
                        "af101c9f-4e42-4344-bd39-3fd2427fd360",
                        "3fe15b1e-1992-4a2a-a4ed-2ec0d813df9a",
                        "bfc391fc-589e-4d41-b697-25480c8d1ea3",
                        "17dc7d38-c1df-4d5e-819d-c6d3f0c0243c",
                        "4161c85d-5e4f-43a0-a8c5-e47448fe7110",
                        "1de3d502-5a34-472f-8d97-7d7e53ddfdb2",
                        "14688362-b2e2-47c4-a1d8-69f429a88784",
                    ]
                    for j in range(len(urls)):
                        try:
                            if lookup_answer(urls[j], answers["answers"][i]):
                                incident.relatedEntities.append(
                                    Observable(
                                        url=lookup_answer(
                                            urls[j], answers["answers"][i]
                                        )[0],
                                        date=datetime.strptime(
                                            (
                                                lookup_answer(
                                                    dates[j], answers["answers"][i]
                                                )
                                                or [datetime.now().strftime("%Y-%m-%d")]
                                            )[0],
                                            "%Y-%m-%d",
                                        ),
                                        # archivedUrl=(lookup_answer(
                                        #     archivedUrls[j], answers["answers"][i]
                                        # ) or [""])[0],
                                    )
                                )
                        except Exception as e:
                            raise ValueError(
                                f"Error in adding URL {j} to report #{i}, error {e}"
                            )

                    # Add identities
                    identities = {
                        "c288450f-4b1b-4862-829c-b1a37c6964d2": [
                            "3e42d9bc-33a1-408e-aa0b-3abc1bda9063",
                            "743f7d6b-cf0f-44b5-a7fe-3d19ff284de2",
                        ],
                        "3b038356-c007-4fca-9940-2fcef1d402f7": [
                            "3b24eb0d-6d80-4771-8963-6af3518374ce",
                            "56118e4c-3929-4452-8b0b-3099ddd3a960",
                        ],
                        "dfd29f0c-8db2-48a8-8128-f4109ae5b577": [
                            "47c339c7-b928-46a2-b8c6-d97b628db2d4",
                            "24e5bde4-6b4a-4c11-a653-46381cc96937",
                        ],
                        "b1cdf949-62e2-4d10-bcbe-434cf0152a27": [
                            "538a154d-021b-44c6-9422-fa3602d1f9e5",
                            "66ed92b6-903e-4bfc-ac7f-9761afb9116c",
                        ],
                        "adffd6d6-5eab-45c7-8fa5-bf0c4c017762": [
                            "0d5c2d73-32ce-433b-99d4-03dafa7dbb14",
                            "5a23e849-99c1-400c-812e-a031e19b5031",
                        ],
                    }
                    try:
                        for key in identities.keys():
                            if lookup_answer(key, answers["answers"][i]):
                                if (
                                    lookup_answer(key, answers["answers"][i])[0]
                                    == "Country"
                                ):
                                    incident.relatedEntities.append(
                                        Identity(
                                            name=lookup_answer(
                                                identities[key][0],
                                                answers["answers"][i],
                                            )[0],
                                            idClass="Country",
                                        )
                                    )
                                else:
                                    incident.relatedEntities.append(
                                        Identity(
                                            name=lookup_answer(
                                                identities[key][1],
                                                answers["answers"][i],
                                            )[0],
                                            idClass=lookup_answer(
                                                key, answers["answers"][i]
                                            ),
                                        )
                                    )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding one or more identity to report #{i} error {e}",
                        )

                    # Add event
                    try:
                        if lookup_answer(
                            "87f89323-0167-4b5a-ab39-a0a2e36c56d8",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                Event(
                                    name=lookup_answer(
                                        "87f89323-0167-4b5a-ab39-a0a2e36c56d8",
                                        answers["answers"][i],
                                    )[0],
                                    location=lookup_answer(
                                        "dad80ad3-138b-48e5-bee9-9b11d08a6747",
                                        answers["answers"][i],
                                    )[0],
                                    start_date=datetime.strptime(
                                        lookup_answer(
                                            "889e207d-5671-469b-82ab-6322c6ab6f52",
                                            answers["answers"][i],
                                        )[0],
                                        "%Y-%m-%d",
                                    ),
                                    end_date=datetime.strptime(
                                        lookup_answer(
                                            "0979109c-3c7e-4b8f-a3dc-c80f7e321e5f",
                                            answers["answers"][i],
                                        )[0],
                                        "%Y-%m-%d",
                                    ),
                                )
                            )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding event to report #{i}, error {e}"
                        )

                    # Add courses of action
                    coas = {
                        "Statement of refutal": [
                            "0797fc99-0a18-4064-a612-d944d2d8076d",
                            "821fe005-666e-44d5-915c-14fcd5e89d5e",
                        ],
                        "Debunking": [
                            "9e972716-e712-4da9-9e76-7e9c5fa7cd32",
                            "ced4a1ae-7230-45e1-8114-2d3e3127cac2",
                        ],
                        "Content deleted": [
                            "5dfb6543-77c8-4a86-a057-d8db8c3b57da",
                            "09f14a98-0cd2-426b-b036-39bafe7fb82c",
                        ],
                        "Content confined": [
                            "afaba201-a299-4f75-8978-19638e059919",
                            "207ee2f3-84bb-4319-92b8-e349298aea11",
                        ],
                        "Other": [
                            "f071eb1c-a6d0-4ada-b7cc-8c662081bdae",
                            "9a4da50a-4a3a-4aab-9d8e-22a85689a44f",
                        ],
                    }
                    for key in coas.keys():
                        try:
                            if lookup_answer(
                                coas[key][0], answers["answers"][i]
                            ) and lookup_answer(coas[key][1], answers["answers"][i]):
                                incident.relatedEntities.append(
                                    CourseOfAction(
                                        name=key,
                                        description=lookup_answer(
                                            coas[key][0], answers["answers"][i]
                                        )[0],
                                        extRef=lookup_answer(
                                            coas[key][1], answers["answers"][i]
                                        )[0],
                                    )
                                )
                        except Exception as e:
                            raise ValueError(
                                f"Error in adding Countermeasure {key} to report #{i}, error {e}"
                            )

                    ttps = [
                        "294eeb09-6d8f-4053-b5d5-ad8ef3d5bf07",
                        "5f2e0298-6c5e-4342-b73a-0272440c6a70",
                        "123abfd3-b832-4016-9307-89057bc3dd29",
                        "b0808142-979a-457a-be93-6290be27d128",
                        "9c8b2f3d-ebd2-4523-99c4-576dbab14197",
                        "0184b310-3ed9-4fa2-9f0a-b406ab62ab19",
                        "264cd485-859f-4309-a8cf-e5049404cae1",
                        "003901bc-0db1-4ecb-bee2-318607823866",
                        "0ff00f03-839e-4817-b2b5-3d4d40935d5b",
                        "7f4d11cb-8238-4911-870e-cb494e2ddc85",
                        "602bf807-e885-4e6f-83f3-3d4aa85c3c89",
                        "14eddc3d-3418-4129-9a21-cde6b3eda44d",
                        "738da7de-c5cb-43fa-b45c-494b19925216",
                        "200b7744-d4b9-474d-8a0b-64ce288f86ab",
                        "8a25f473-29a9-4e5b-929d-b62e52923421",
                        "65ad9ed5-cdc0-49ed-8ef3-bcce481ad38d",
                    ]
                    try:
                        for ttp in ttps:
                            if lookup_answer(ttp, answers["answers"][i]):
                                for j in lookup_answer(ttp, answers["answers"][i]):
                                    if lookup_answer(j, answers["answers"][i]):
                                        incident.relatedEntities.append(
                                            AttackPattern(
                                                technique=lookup_answer(
                                                    j, answers["answers"][i]
                                                ).split(": ")[1],
                                            )
                                        )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding TTP to report #{i}, error {e}"
                        )

                    results.append(incident)
                    print(
                        f"Successfully added report {incident.name} to results with {len(incident.relatedEntities)} related entities"
                    )

        # Basic ticket
        case "b6733ae1-9cef-2741-e15b-9e3ef470cf05":
            if answers["answers"]:
                for i in range(len(answers["answers"])):
                    if (
                        lookup_answer(
                            "f0f37977-00ee-4889-a2d1-590c214344ff",
                            answers["answers"][i],
                        )[0]
                        in processed_list
                    ):
                        break
                    # Create the ticket
                    try:
                        incident = Incident(
                            incidentType="case-rfi",
                            name=(
                                lookup_answer(
                                    "f0f37977-00ee-4889-a2d1-590c214344ff",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            description=(
                                lookup_answer(
                                    "c32c0b03-0c17-4a54-a192-597e4f8a988b",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0]
                            + " "
                            + (
                                lookup_answer(
                                    "3095f78e-73fc-4466-bf22-d9fc91d8740f",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0]
                            + " "
                            + (
                                lookup_answer(
                                    "b23a6792-c4d1-4f12-8111-9f26d18ee3a2",
                                    answers["answers"][i],
                                )
                                or [""]
                            )[0],
                            confidence=90,
                            first_seen=datetime.now(),
                            objectMarking="TLP:AMBER+STRICT",
                            objective=[""],
                            objectLabel=[],
                        )
                    except Exception as e:
                        raise ValueError(
                            f"Error in creating basic incident #{i}, error {e}"
                        )

                    try:
                        if lookup_answer(
                            "6ca7119f-c649-4998-bad8-358dd9cdf95b",
                            answers["answers"][i],
                        ):
                            incident.relatedEntities.append(
                                Observable(
                                    url=lookup_answer(
                                        "6ca7119f-c649-4998-bad8-358dd9cdf95b",
                                        answers["answers"][i],
                                    )[0],
                                )
                            )
                            print(f"Successfully added URL to basic incident #{i}")
                        urls = lookup_answer(
                            "4b7407dd-4165-4c14-92e9-4d8933511b32",
                            answers["answers"][i],
                        )
                        if urls:
                            if "," in urls[0]:
                                for url in urls[0].split(","):
                                    incident.relatedEntities.append(
                                        Observable(
                                            url=url,
                                        )
                                    )
                            if " " in urls[0]:
                                for url in urls[0].split(" "):
                                    incident.relatedEntities.append(
                                        Observable(
                                            url=url,
                                        )
                                    )
                            if ";" in urls[0]:
                                for url in urls[0].split(";"):
                                    incident.relatedEntities.append(
                                        Observable(
                                            url=url,
                                        )
                                    )
                            if "\n" in urls[0]:
                                for url in urls[0].split("\n"):
                                    incident.relatedEntities.append(
                                        Observable(
                                            url=url,
                                        )
                                    )
                            else:
                                incident.relatedEntities.append(
                                    Observable(
                                        url=urls[0],
                                    )
                                )
                    except Exception as e:
                        raise ValueError(
                            f"Error in adding URLs to basic incident #{i}, error {e}"
                        )

                    results.append(incident)
                    print(
                        f"Successfully added basic incident {incident.name} to results with {len(incident.relatedEntities)} related entities"
                    )
    return results


def drop_duplicates(list_of_dicts):
    """Drops duplicates from a list of dictionaries"""
    unique_dicts = []
    # duplicates = []

    for d in list_of_dicts:
        if d and isinstance(d, dict):
            str_items = [item for item in d.values() if isinstance(item, str)]
            found_duplicate = False

            for existing_dict in unique_dicts:
                if all(item in existing_dict.values() for item in str_items):
                    found_duplicate = True
                    break

            if not found_duplicate:
                unique_dicts.append(d)

    return unique_dicts


def create_bundle(i):
    bundle = {
        "type": "bundle",
        "id": "bundle--"
        + str(uuid.uuid5(uuid.NAMESPACE_DNS, "bundle" + str(random.random()))),
        "bundle_name": "unnamed",
        "objects": [
            {
                "id": "marking-definition--826578e1-40ad-459f-bc73-ede076f81f37",
                "entity_type": "Marking-Definition",
                "standard_id": "marking-definition--826578e1-40ad-459f-bc73-ede076f81f37",
                "definition_type": "TLP",
                "definition": "TLP:AMBER+STRICT",
                "x_opencti_color": "#d84315",
                "x_opencti_order": 3,
                "name": "TLP:AMBER+STRICT",
                "type": "marking-definition",
            }
        ],
    }

    objects = []
    # Create object list
    object_list = [r.create_stix_dict() for r in i.relatedEntities if r]
    object_ids = [r["id"] for r in object_list if r]

    # Create the incident dictionary
    incident_dict = i.create_stix_dict()
    incident_dict["object_refs"] = object_ids
    bundle["bundle_name"] = incident_dict["name"]

    # Add the author if the incident is a report, EEAS if it is an incident
    if isinstance(i, Report) and i.author:
        author_dict = i.find_author()
    else:
        author_dict = {
            "id": "identity--24f595b1-bb5b-5c05-a7d8-337a224de086",
            "identity_class": "individual",
            "name": "EEAS",
            "contact_information": "strat-data-analysis@eeas.europa.eu",
            "x_opencti_firstname": "EEAS",
            "x_opencti_lastname": "STRATCOM",
            "x_opencti_id": "f995efca-7522-438a-b68b-44b9b698a285",
            "x_opencti_type": "Individual",
            "type": "identity",
        }
    if author_dict:
        object_list.append(author_dict)
        object_ids.append(author_dict["id"])
        incident_dict["created_by_ref"] = author_dict["id"]

    # Add the incident to the bundle
    bundle["objects"].append(incident_dict)
    objects.extend(object_list)

    bundle["objects"].extend(
        drop_duplicates(objects)
    )  # Add the unique objects to the bundle
    return bundle


def xml_to_json(xml_file, processed_list=[]):
    xml = load_xml(xml_file)
    qns = get_qns(xml)

    answers = get_answers(xml, qns)
    data = answers_to_stix(answers, processed_list)
    for i in data:
        bundle = create_bundle(i)
        json_filename = (
            "/srv/eusurvey-backend/workbenches/" + bundle["bundle_name"] + ".json"
        )
        with open(json_filename, "w") as f:
            json.dump(bundle, f)
            print(f"Successfully created JSON file {json_filename}")


def folder_to_json(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            existing_files = [
                f.strip(".json")
                for f in os.listdir("/srv/eusurvey-backend/workbenches")
            ]
            if file.endswith(".xml"):
                print(f"Converting {os.path.join(root, file)} to JSON")
                xml_to_json(os.path.join(root, file), existing_files)


def folder_qids(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".xml"):
                print(f"Extracting QIDs from {os.path.join(root, file)}")
                xml = load_xml(os.path.join(root, file))
                get_qids(xml)