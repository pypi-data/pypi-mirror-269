from lxml import etree
from faker import Faker
from collections import defaultdict
from typing import Dict
import json
from os import path
from xml.sax.saxutils import XMLGenerator
import re

"""
BBXMLAnonymiser
Handles the parsing, anonymizing, and writing of XML files.

Initialization Parameters:
mapping_path: str - The path to the JSON file where user mappings are stored. If the file exists, mappings are loaded; otherwise, a new mapping is created.
bank_pattern: str - A regular expression pattern used to identify companies related to a bank role in conversation (mapped to "BANK" in final xml).
role_field: str, optional - The XML tag that contains company information for role identification, default is "CompanyName".
bank_value: str, optional - The value to replace the company name with if it matches the bank_pattern, default is "BANK".
"""


class BBXMLAnonymiser:
    def __init__(
        self,
        mapping_path,
        bank_pattern,
        role_field="CompanyName",
        bank_value="BANK",
    ):
        self.mapping_path = mapping_path

        self.bank_pattern = bank_pattern
        self.role_field = role_field
        self.bank_value = bank_value
        self._xmlwriter = None
        self._current_user = None
        self._inside_user = False
        self.user_generator = FakeUserGenerator()

        self._load_or_initialize_mapping()

    def _load_or_initialize_mapping(self):
        if path.isfile(self.mapping_path):
            with open(self.mapping_path, "r", encoding="utf-8") as fp:
                existing_mappings = json.load(fp)
        else:
            existing_mappings = {}

        self.login_to_participant = defaultdict(
            self.user_generator.generate_user_data, existing_mappings
        )

    def anonymise_xml(self, xml_in, xml_out):
        context = etree.iterparse(xml_in, events=("start", "end"))
        self._inside_user = False
        with open(xml_out, "w", encoding="UTF-8") as fp:
            self._xmlwriter = XMLGenerator(
                fp, encoding="UTF-8", short_empty_elements=False
            )
            self._xmlwriter.startDocument()

            for event, elem in context:
                if event == "start":
                    self._element_start(elem)
                elif event == "end":
                    self._element_end(elem)
                    elem.clear()

            self._xmlwriter.endDocument()
        self.save_mapping()

    def _element_start(self, elem):
        self._xmlwriter.startElement(name=elem.tag, attrs=elem.attrib)
        if elem.tag == "User":
            self._inside_user = True

        if self._inside_user and elem.tag == "LoginName":
            self._current_user = self.login_to_participant[elem.text]

    def _element_end(self, elem):
        if elem.tag == self.role_field and re.search(
            self.bank_pattern, str(elem.text), flags=re.IGNORECASE
        ):
            elem.text = self.bank_value
            if self._inside_user:
                self._current_user[elem.tag] = self.bank_value
        elif (
            self._inside_user and elem.tag in self.user_generator.elements_to_anonymise
        ):
            self._current_user[f"{elem.tag}_original"] = elem.text
            elem.text = self._current_user[elem.tag]

        if elem.text:
            self._xmlwriter.characters(elem.text)

        self._xmlwriter.endElement(name=elem.tag)
        self._xmlwriter.characters("\n")

        if elem.tag == "User":
            self._inside_user = False
            self._current_user = None

    def save_mapping(self):
        with open(self.mapping_path, "w", encoding="utf-8") as fp:
            json.dump(self.login_to_participant, fp, indent=4)


class FakeUserGenerator:
    def __init__(self):
        Faker.seed(42)
        self.fake = Faker()
        self.elements_to_anonymise = {
            "LoginName",
            "FirstName",
            "LastName",
            "CompanyName",
            "EmailAddress",
            "UUID",
            "FirmNumber",
            "AccountNumber",
            "CorporateEmailAddress",
        }
        self._users_count = 0

    def generate_user_data(self) -> Dict:
        self._users_count += 1

        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        login = f"{first_name}_{last_name}_{self._users_count:0{6}d}"
        company = self.fake.company()
        email = f"{login}@{company.lower().replace(' ', '').replace(',','').replace('-','')}.com"

        return {
            "FirstName": first_name,
            "LastName": last_name,
            "LoginName": login,
            "EmailAddress": email,
            "UUID": f"{self._users_count:0{7}d}",
            "FirmNumber": f"{self._users_count:0{4}d}",
            "AccountNumber": f"{self._users_count:0{6}d}",
            "CompanyName": company,
            "CorporateEmailAddress": email,
        }


"""
A convenience function to create an instance of BBXMLAnonymiser and anonymize an XML file.

Parameters:
xml_in: str - The input XML file path.
xml_out: str - The output file path where the anonymized XML will be saved.
mapping: str - The path to the JSON mapping file.
bank_pattern: str - Regular expression pattern to identify bank side in conversation.
"""


def anonymise_bbg_xml(xml_in, xml_out, mapping, bank_pattern):
    anonymiser = BBXMLAnonymiser(mapping_path=mapping, bank_pattern=bank_pattern)
    anonymiser.anonymise_xml(xml_in, xml_out)


if __name__ == "__main__":
    anonymise_bbg_xml(
        "./example.xml",
        "./test.xml",
        "./mapping.json",
        r"\bbank\b",
    )
