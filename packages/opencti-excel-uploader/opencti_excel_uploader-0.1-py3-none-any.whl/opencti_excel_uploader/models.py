from datetime import datetime
import uuid
import os
from pycti import OpenCTIApiClient
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings()

load_dotenv()

opencti_client = OpenCTIApiClient(
    os.getenv("OPENCTI_URL"),
    os.getenv("OPENCTI_TOKEN"),
    log_level=os.getenv("OPENCTI_LOG_LEVEL", "error"),
)


class Incident:
    def __init__(
        self,
        name: str,
        incidentType: str,
        description: str,
        objectLabel: list[str],
        first_seen: datetime,
        confidence: int,
        objective: list[str],
        objectMarking: str,
        relatedEntities: list = [],
        extRef: str = "" or list[str],
    ):
        self.name = name
        self.incidentType = incidentType
        self.description = description
        self.objectLabel = objectLabel
        self.first_seen = first_seen or datetime.now()
        self.confidence = confidence
        self.objective = objective
        self.objectMarking = objectMarking
        self.relatedEntities = relatedEntities
        self.extRef = extRef

    def _eq_(self, other):
        if isinstance(other, Incident):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def create_stix_dict(self):
        octi_id = opencti_client.incident.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if isinstance(self.extRef, str):
            self.extRef = [self.extRef]

        external_references = []
        for i in self.extRef:
            external_references.append(
                {
                    "source_name": "External Reference",
                    "url": i,
                }
            )
        if not octi_id:
            return {
                "type": self.incidentType,
                "id": self.incidentType
                + "--"
                + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.name)),
                "name": self.name,
                "description": self.description,
                "labels": self.objectLabel,
                "first_seen": self.first_seen.isoformat() + ".000Z",
                "confidence": self.confidence,
                "objective": ", ".join(self.objective),
                "object_marking_refs": [
                    "marking-definition--826578e1-40ad-459f-bc73-ede076f81f37"
                ],
                "object_refs": [],
                "external_references": external_references,
            }

    def add_marking(self):
        marking_read = opencti_client.marking_definition.read(
            filters={
                "mode": "and",
                "filters": [{"key": "definition", "values": self.objectMarking}],
                "filterGroups": [],
            }
        )
        return {
            "type": "marking-definition",
            "spec_version": "2.1",
            "id": marking_read["standard_id"],
            "definition_type": marking_read["definition_type"],
            "definition": marking_read["definition"],
        }

    def incident_to_bundle(self):
        bundle = {
            "type": "bundle",
            "id": "bundle--"
            + str(uuid.uuid5(uuid.NAMESPACE_DNS, "bundle" + self.name)),
            "objects": [],
        }
        bundle["objects"].append(self.create_stix_dict())

        marking = self.add_marking()
        bundle["objects"][0]["object_refs"].append(marking["id"])
        bundle["objects"].append(marking)

        for i in self.relatedEntities:
            current_entity = i.create_stix_dict()
            if current_entity:
                bundle["objects"][0]["object_refs"].append(current_entity["id"])
                bundle["objects"].append(current_entity)

        return bundle


class Report:
    def __init__(
        self,
        name: str,
        description: str,
        objectLabel: list[str],
        first_seen: datetime,
        confidence: int,
        objective: list[str],
        objectMarking: str = "TLP:AMBER+STRICT",
        relatedEntities: list = [],
        extRef: str = "",
        author: str = "",
    ):
        self.name = name
        self.description = description
        self.objectLabel = objectLabel
        self.first_seen = first_seen or datetime.now()
        self.confidence = confidence
        self.objective = objective
        self.objectMarking = objectMarking
        self.relatedEntities = relatedEntities
        self.extRef = extRef
        self.author = author

    def __eq__(self, other):
        if isinstance(other, Report):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def create_stix_dict(self):
        octi_id = opencti_client.incident.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if not octi_id:
            return {
                "type": "report",
                "id": "report--" + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.name)),
                "name": self.name,
                "description": self.description,
                "labels": self.objectLabel,
                "first_seen": self.first_seen.isoformat() + ".000Z",
                "confidence": self.confidence,
                "objective": ", ".join(self.objective),
                "object_marking_refs": [
                    "marking-definition--826578e1-40ad-459f-bc73-ede076f81f37"
                ],
                "object_refs": [],
                "external_references": [
                    {
                        "source_name": "External Reference",
                        "url": self.extRef,
                    }
                ],
            }
        else:
            raise ValueError("Report already exists")

    def find_author(self):
        """Search by name to see if author already exists"""
        author_entity = opencti_client.identity.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.author}],
                "filterGroups": [],
            },
        )
        if author_entity:
            author_dict = {
                "type": "identity",
                "id": author_entity["id"],
                "name": author_entity["name"],
                "identity_class": author_entity["identity_class"],
            }
            return author_dict
        else:
            return None

    def add_marking(self):
        marking_read = opencti_client.marking_definition.read(
            filters={
                "mode": "and",
                "filters": [{"key": "definition", "values": self.objectMarking}],
                "filterGroups": [],
            }
        )
        return {
            "type": "marking-definition",
            "spec_version": "2.1",
            "id": marking_read["standard_id"],
            "definition_type": marking_read["definition_type"],
            "definition": marking_read["definition"],
        }

    def report_to_bundle(self):
        bundle = {
            "type": "bundle",
            "id": "bundle--"
            + str(uuid.uuid5(uuid.NAMESPACE_DNS, "bundle" + self.name)),
            "objects": [],
        }
        bundle["objects"].append(self.create_stix_dict())

        marking = self.add_marking()
        bundle["objects"][0]["object_refs"].append(marking["id"])
        bundle["objects"].append(marking)

        for i in self.relatedEntities:
            current_entity = i.create_stix_dict()
            if current_entity:
                bundle["objects"][0]["object_refs"].append(current_entity["id"])
                bundle["objects"].append(current_entity)

        return bundle


class AttackPattern:
    def __init__(
        self,
        technique: str = "",
        tactic: str = "",
        stage: str = "",
        description: str = "",
    ):
        self.technique = technique
        self.tactic = tactic
        self.stage = stage
        self.description = description

    def create_stix_dict(self):
        octi_id = opencti_client.attack_pattern.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.technique}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "attack-pattern",
                "id": octi_id["standard_id"],
                "name": self.technique,
            }


class Campaign:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        extRef: str = "",
    ):
        self.name = name
        self.description = description
        self.extRef = extRef

    def create_stix_dict(self):
        octi_id = opencti_client.campaign.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "campaign",
                "id": octi_id["standard_id"],
                "name": self.name,
            }
        else:
            return {
                "type": "campaign",
                "id": "campaign--" + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.name)),
                "name": self.name,
                "description": self.description,
                "external_references": [
                    {
                        "source_name": "External Reference",
                        "url": self.extRef,
                        "description": self.description,
                    }
                ],
            }


class CourseOfAction:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        extRef: str = "",
    ):
        self.name = name
        self.description = description
        self.extRef = extRef

    def create_stix_dict(self):
        octi_id = opencti_client.course_of_action.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "course-of-action",
                "id": octi_id["standard_id"],
                "name": self.name,
                "external_references": [
                    {
                        "source_name": "External Reference",
                        "url": self.extRef,
                        "description": self.description,
                    }
                ],
            }


class Event:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        start_date: datetime = datetime.now(),
        end_date: datetime = datetime.now(),
        location: str = "",
    ):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location

    def fuzzy_match(self):
        """Search by date and location and keywords to see if event can be found"""
        pass

    def create_stix_dict(self):
        octi_id = opencti_client.event.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "event",
                "id": octi_id["standard_id"],
                "name": self.name,
            }
        else:
            return {
                "type": "event",
                "id": "event--" + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.name)),
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date.isoformat() + ".000Z",
                "end_date": self.end_date.isoformat() + ".000Z",
            }


class Identity:
    def __init__(
        self,
        name: str = "",
        alias: str = "",
        description: str = "",
        idClass: str = "",
    ):
        self.name = name
        self.alias = alias
        self.description = description
        self.idClass = idClass

    def fuzzy_match(self):
        """Search by alias or names w/ without middle name or title to see if identity already exists"""
        pass

    def create_stix_dict(self):
        if self.idClass == "Individual" or self.idClass == "Organization":
            octi_id = opencti_client.identity.read(
                filters={
                    "mode": "and",
                    "filters": [{"key": "name", "values": self.name}],
                    "filterGroups": [],
                },
                customAttributes="standard_id",
            )
            if octi_id:
                return {
                    "type": "identity",
                    "id": octi_id["standard_id"],
                    "name": self.name,
                    "identity_class": self.idClass,
                }
            else:
                return {
                    "type": "identity",
                    "id": "identity--" + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.name)),
                    "name": self.name,
                    "alias": self.alias,
                    "description": self.description,
                    "identity_class": self.idClass,
                }
        elif self.idClass == "Unknown":
            return {
                "type": "location",
                "x_opencti_location_type": "Area",
                "id": "location--"
                + str(uuid.uuid5(uuid.NAMESPACE_DNS, str(self.name))),
                "name": self.name,
                "alias": self.alias,
                "description": self.description,
            }
        else:
            octi_id = opencti_client.location.read(
                filters={
                    "mode": "and",
                    "filters": [{"key": "name", "values": self.name}],
                    "filterGroups": [],
                },
                customAttributes="standard_id",
            )
            if octi_id:
                return {
                    "type": "location",
                    "x_opencti_location_type": "Country",
                    "id": octi_id["standard_id"],
                    "name": self.name,
                }
            else:
                return {
                    "type": "location",
                    "x_opencti_location_type": "Area",
                    "id": "location--" + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.name)),
                    "name": self.name,
                    "alias": self.alias,
                    "description": self.description,
                }


class Narrative:
    def __init__(
        self,
        name: str = "",
        description: str = "",
    ):
        self.name = name
        self.description = description

    def create_stix_dict(self):
        octi_id = opencti_client.narrative.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "narrative",
                "id": octi_id["standard_id"],
                "name": self.name,
            }


class Observable:
    def __init__(
        self,
        url: str = "",
        date: datetime = datetime.now(),
        archivedUrl: str = "",
        language: list[str] = [],
    ):
        self.url = (
            url.replace("http://", "").replace("https://", "").replace("www.", "")
        )
        self.date = date
        self.archivedUrl = archivedUrl
        self.language = language

    def find_channel(self):
        """Search by domain and keywords to see if channel exists"""
        pass

    def create_stix_dict(self):
        octi_id = opencti_client.stix_cyber_observable.read(
            filters={
                "mode": "and",
                "filters": [{"key": "value", "values": self.url}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "media-content",
                "id": octi_id["standard_id"],
                "value": self.url,
                "url": self.url,
            }
        else:
            return {
                "type": "media-content",
                "id": "media-content--" + str(uuid.uuid5(uuid.NAMESPACE_DNS, self.url)),
                "value": self.url,
                "date": self.date.isoformat() + ".000Z",
                "external_references": [
                    {
                        "source_name": "External Reference",
                        "url": self.archivedUrl,
                        "description": "archived url",
                    }
                ],
            }


class ThreatActor:
    def __init__(
        self,
        name: str = "",
        alias: str = "",
    ):
        self.name = name
        self.alias = alias

    def create_stix_dict(self):
        octi_id = opencti_client.threat_actor.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "threat-actor",
                "id": octi_id["standard_id"],
                "name": self.name,
            }


class Vulnerability:
    def __init__(
        self,
        name: str = "",
        description: str = "",
    ):
        self.name = name
        self.description = description

    def create_stix_dict(self):
        octi_id = opencti_client.vulnerability.read(
            filters={
                "mode": "and",
                "filters": [{"key": "name", "values": self.name}],
                "filterGroups": [],
            },
            customAttributes="standard_id",
        )
        if octi_id:
            return {
                "type": "vulnerability",
                "id": octi_id["standard_id"],
                "name": self.name,
            }
