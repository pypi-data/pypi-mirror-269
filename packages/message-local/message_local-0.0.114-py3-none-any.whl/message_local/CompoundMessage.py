# TODO Please make sure every src file will have a test file i.e. CompoundMessage

import json
from collections import defaultdict

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from profiles_local.profiles_local import ProfilesLocal
from user_context_remote.user_context import UserContext
from variable_local.template import ReplaceFieldsWithValues

from .MessageChannels import MessageChannel
from .MessageConstants import object_message
from .MessageTemplates import MessageTemplates
from .Recipient import Recipient

recipients_preferred_lang_code_str = {}
JSON_VERSION = "240416"  # TODO: make it generic


class CompoundMessage(GenericCRUD, metaclass=MetaLogger, object=object_message):
    def __init__(self, campaign_id: int = None, message_template_id: int = None, body: str = None, subject: str = None,
                 recipients: list[Recipient] = None, message_id: int = None, is_test_data: bool = False, ui_schema=None,
                 schema=None, field_id=None, form_id: int = None, debug: bool = False):
        self.user_context = UserContext()
        super().__init__(default_schema_name="message", default_table_name="message_table",
                         default_view_table_name="message_sent_view", default_id_column_name="message_id",
                         is_test_data=is_test_data)

        self.campaign_id = campaign_id
        self.message_template_id = message_template_id
        self.body = body
        self.subject = subject
        self.recipients = recipients
        self.message_id = message_id
        self.form_id = form_id
        self.debug = debug
        self.__compound_message = {}
        self.ui_schema = ui_schema
        self.schema = schema
        self.field_id = field_id
        self.profile_local = ProfilesLocal()
        self.message_template = MessageTemplates()
        self.set_compound_message_after_text_template()

    # def _get_template_ids_by_campaign(self, campaign_id: int) -> list[int]:
    #     """Returns a random template id from the campaign"""
    #
    #     possible_template_ids = self.select_multi_tuple_by_id(
    #         schema_name="campaign", view_table_name="campaign_view",
    #         id_column_name="campaign_id", id_column_value=campaign_id,
    #         select_clause_value="message_template_id")
    #
    #     return [message_template_id[0] for message_template_id in possible_template_ids]

    def set_compound_message_after_text_template(
            self, campaign_id: int = None, message_template_id: int = None, body: str = None, subject: str = None,
            recipients: list[Recipient] = None, message_id: int = None, form_id: int = None,
            debug: bool = False) -> None:
        """ Sets the compound message in the instance and in the database using the following structure:"""

        # Allow overiding instance vars
        campaign_id = campaign_id or self.campaign_id
        message_template_id = message_template_id or self.message_template_id
        body = body or self.body
        subject = subject or self.subject
        recipients = recipients or self.recipients or []
        message_id = message_id or self.message_id
        form_id = form_id or self.form_id
        debug = debug or self.debug

        if body:  # TODO constract textblocks_and_attributes
            textblocks_and_attributes = [{}]  # one textblock
            # for message_channel, template_header in channels_mapping.items():
            #     textblocks_and_attributes[0][template_header["body"]] = body
            #     textblocks_and_attributes[0][template_header["subject"]] = subject

        elif form_id:  # If body is not given, get it from the database
            textblocks_and_attributes = self.message_template.get_textblocks_and_attributes_by_form_id(form_id)
        else:
            textblocks_and_attributes = self.message_template.get_textblocks_and_attributes()
        if not textblocks_and_attributes:
            raise ValueError(f"No text blocks found for form_id: {form_id}")

        compound_message = {"json_version": JSON_VERSION, "data": {}}
        for channel in MessageChannel:
            compound_message_json = self.create_compound_message_json(
                textblocks_and_attributes=textblocks_and_attributes, channel=channel,
                form_id=form_id, recipients=recipients, debug=debug)
            if compound_message_json:
                compound_message["data"][channel.name] = compound_message_json

        # save in message table
        if message_id:
            self.update_by_id(id_column_value=message_id,
                              data_json={"compound_message_json": json.dumps(compound_message),
                                         "compound_message": json.dumps(compound_message),
                                         "compound_message_json_version": JSON_VERSION})
        else:
            self.message_id = self.insert(data_json={"compound_message_json": json.dumps(compound_message),
                                                     "compound_message": json.dumps(compound_message),
                                                     "compound_message_json_version": JSON_VERSION})

        self.__compound_message = compound_message
        self.logger.debug(object=locals())

    def get_profiles_blocks(self, text_block: dict, recipients: list[Recipient], message_template_id: int,
                            content_per_language: dict, possible_answers_per_question_id: dict) -> list[dict]:
        """Each profile block contains the following keys:
subject_locale [Optional] possible values he-il, en-us, en-gb https://www.science.co.il/language/Locale-codes.php
subject_text (aliases title/headline/question_title) [Optional]
body_locale
body_text / question_title
question_id
variable_id
default_possible_answer_id
is_visible
possible answers
    possible_answer_locale
    possible_answer_text
"""
        criteria_json = self.message_template.get_critiria_json(message_template_id=message_template_id)
        potentials_recipients = self.message_template.get_potentials_recipients(criteria_json, recipients)

        profiles_blocks = []
        for recipient in recipients:
            profile_id = recipient.get_profile_id()
            if profile_id not in recipients_preferred_lang_code_str:  # TODO
                recipients_preferred_lang_code_str[profile_id] = LangCode.ENGLISH.value or (
                    self.profile_local.get_preferred_lang_code_by_profile_id(profile_id).value)
            if any(recipient.get_profile_id() == potential_recipient["profile_id"]
                   for potential_recipient in potentials_recipients) and text_block["question_id"]:
                question_id = text_block["question_id"]
                profile_block = {
                    "profile_id": profile_id,
                    "preferred_language": recipients_preferred_lang_code_str[profile_id],
                    "subject_per_language": {
                        lang: self._process_text_block(content, recipient)
                        for lang, content in content_per_language[question_id]["subject_per_language"].items()},
                    "body_per_language": None if question_id else {
                        lang: self._process_text_block(content, recipient)
                        for lang, content in content_per_language[question_id]["body_per_language"].items()},
                    "question_per_language": None if not question_id else {
                        lang: self._process_text_block(content, recipient) for lang, content in
                        content_per_language[question_id]["question_per_language"].items()},
                    "question_id": question_id,
                    "variable_id": text_block["variable_id"],
                    "default_question_possible_answer_id": text_block["default_question_possible_answer_id"],
                    "is_visible": text_block["message_template_text_block_is_visible"],
                    "is_required": text_block.get("is_required") or False,
                    "possible_answers": possible_answers_per_question_id[question_id]
                }
                if "question_title" not in text_block and "body_text" not in text_block:
                    self.logger.warning("No question_title or body_text in text_block",
                                        object={"text_block": text_block})
                profiles_blocks.append(profile_block)
        return profiles_blocks

    def create_compound_message_json(self, *, textblocks_and_attributes: list[dict], channel: MessageChannel,
                                     form_id: int = None, recipients: list[Recipient], debug: bool) -> dict or None:
        """Specs: https://docs.google.com/document/d/1UvdU9WrK7RwMNnLLBwdye9HbUzgMGEG8wsIMxxYrxa4/edit?usp=sharing
Returns dict with the following structure:
form_id = 2 [if form_id]
form_name [if form_id and debug=true]
Page[]
    page_number
    message_seq_in_page [If debug=true] - Sorted by message_seq_in_page
    Message Templates - Not need hierarchy in the JSON. Container of message_template_text_blocks
        index_number - i.e. child number (default 1)
        index_name - i.e. Home/Work (default "")
        message_template_id (i.e 3000)
        message_template_name [If debug=true]
        MessageTemplateTextBlocks (message, question) - Not need hierarchy in the JSON
            message_template_text_block_seq [If debug=true] - Sorted by message_template_text_block_seq
            message_template_text_block_id
            message_template_text_block_name [If debug=true]
            subject_templates [If debug=true] Based on channel
            body_templates - message_template_text_block_ml.default_subject_template [If debug=true] Based on Channel
            question_templates
            question_schema
            question_uischema
            Profiles[] - Generated by message-local-python-package based on message_template_text_block_ml.default_subject_template in the relevant language/channel - Index is profile_id
                profile_id
                preferred_language
                subject_per_language = {"en": "..."}
                body_per_language = {"en": "..."} or null
                question_per_language = {"en": "..."} or null
                question_id
                variable_id
                default_question_possible_answer_id
                is_visible
                possible answers
                    possible_answer_locale
                    possible_answer_text
"""
        # Group the fetched data by page and message_template_id
        grouped_data = {}
        for row in textblocks_and_attributes:
            # TODO: get the actual page_number if not form. Currently, it's always 1.
            page_number = row.get("form_page", 1)
            message_template_id = row["message_template_id"]
            if page_number not in grouped_data:
                grouped_data[page_number] = {}
            if message_template_id not in grouped_data[page_number]:
                grouped_data[page_number][message_template_id] = []
            grouped_data[page_number][message_template_id].append(row)
        self.logger.info(object={"grouped_data": grouped_data})

        compound_message_json = {"Page": []}
        if form_id:
            compound_message_json["form_id"] = form_id
        if debug:
            if form_id:
                compound_message_json["form_name"] = textblocks_and_attributes[0]["form_name"]

        # Iterate through the fetched data and structure it into the JSON
        for page_number, message_templates in grouped_data.items():
            page = {
                "page_number": page_number,
                "MessageTemplates": []
            }
            # TODO: do we need this?
            # if campaign_id and not message_template_id:
            #     possible_template_ids = self._get_template_ids_by_campaign(campaign_id=campaign_id)
            #     message_template_id = random.choice(possible_template_ids)
            for message_template_id, text_blocks in message_templates.items():
                if not text_blocks:
                    continue
                message_template_data = {
                    "message_template_id": message_template_id,
                    "MessageTemplateTextBlocks": []
                }
                if form_id:
                    message_template_data["index_number"] = list(
                        range(text_blocks[0]["min_message_template"], text_blocks[0]["max_message_template"] + 1)),
                    message_template_data["index_name"] = None  # will be filled by the frontend

                if debug:
                    message_template_data["message_template_name"] = text_blocks[0].get("message_template_name")
                    # TODO: get the actual message_seq_in_page if not form. Currently, it's always 1.
                    message_template_data["message_seq_in_page"] = text_blocks[0].get("form_message_seq_in_page", 1)

                # Group possible answers by question_id
                possible_answers_per_question_id = defaultdict(list)
                for text_block in text_blocks:
                    if text_block.get("possible_answer"):
                        # TODO: multiple languages
                        lang_code = text_block["question_ml_lang_code"] or LangCode.ENGLISH.value
                        possible_answers_per_question_id[text_block["question_id"]].append(
                            {lang_code: text_block["possible_answer"]})

                # Group questions by language:
                content_per_language = defaultdict(lambda: {"body_per_language": {},
                                                            "subject_per_language": {},
                                                            "question_per_language": {}})

                body_key = (channel.name.lower() + "_body") if channel != MessageChannel.EMAIL else "email_body_html"
                if f"{body_key}_template" not in text_blocks[0]:
                    return None  # no special template for this channel
                field_to_lang_field = {
                    f"{body_key}_template": ("body_per_language", "message_template_text_block_ml_lang_code"),
                    f"{channel.name}_subject_template": (
                    "subject_per_language", "message_template_text_block_ml_lang_code"),
                    "question_title": ("question_per_language", "question_ml_lang_code")}

                text_blocks_by_question_id = defaultdict(list)
                for text_block in text_blocks:
                    text_blocks_by_question_id[text_block["question_id"]].append(text_block)

                for question_id, _text_blocks in text_blocks_by_question_id.items():
                    for text_block in text_blocks:
                        for field, (lang_field, lang_code_field) in field_to_lang_field.items():
                            lang_code = text_block[lang_code_field] or LangCode.ENGLISH.value
                            if text_block.get(field) and text_block["question_id"] == question_id:
                                content_per_language[question_id][lang_field][lang_code] = text_block[field]

                # remove duplicated text_blocks
                unique_text_blocks = []
                for text_block in text_blocks:
                    columns_to_ignore = ["possible_answer"]
                    for field, (lang_field, lang_code_field) in field_to_lang_field.items():
                        columns_to_ignore.extend([field, lang_code_field])
                    unique_text_block = {k: v for k, v in text_block.items() if k not in columns_to_ignore}
                    if unique_text_block not in unique_text_blocks:
                        unique_text_blocks.append(unique_text_block)

                for text_block in unique_text_blocks:
                    text_block_data = {
                        "message_template_text_block_id": text_block["message_template_text_block_id"],
                        "question_schema": text_block["question_type_schema_attributes"] or text_block[
                            "schema_attribute"],
                        "question_uischema": text_block["question_type_uischema_attributes"] or text_block[
                            "uischema_attribute"],
                        "Profiles": self.get_profiles_blocks(text_block=text_block, recipients=recipients,
                                                             message_template_id=message_template_id,
                                                             content_per_language=content_per_language,
                                                             possible_answers_per_question_id=possible_answers_per_question_id)
                    }
                    if not text_block_data["Profiles"]:
                        continue  # There's no one to send to

                    # if channel == MessageChannel.FORM_REACTJS:
                    #     text_block_data["question_schema"] = text_block["question_type_schema_attributes"] or text_block["schema_attribute"]
                    #     text_block_data["question_uischema"] = text_block["question_type_uischema_attributes"] or text_block["uischema_attribute"]

                    if debug:
                        text_block_data["message_template_text_block_seq"] = text_block[
                            "message_template_text_block_seq"]
                        text_block_data["message_template_text_block_name"] = text_block[
                            "message_template_text_block_name"]
                        text_block_data["subject_templates"] = content_per_language[text_block["question_id"]][
                            "subject_per_language"]
                        text_block_data["body_templates"] = content_per_language[text_block["question_id"]][
                            "body_per_language"]
                        text_block_data["question_templates"] = content_per_language[text_block["question_id"]][
                            "question_per_language"]

                    message_template_data["MessageTemplateTextBlocks"].append(text_block_data)

                if message_template_data["MessageTemplateTextBlocks"]:
                    page["MessageTemplates"].append(message_template_data)

            if page["MessageTemplates"]:
                compound_message_json["Page"].append(page)

        if not compound_message_json["Page"]:
            return None
        return compound_message_json

    def _process_text_block(self, text_block_body: str, recipient: Recipient) -> str:
        template = ReplaceFieldsWithValues(message=text_block_body,
                                           # TODO language -> lang_code_str ?
                                           language=recipient.get_preferred_lang_code_str(),
                                           variable=recipient.get_profile_variables())
        processed_text_block = template.get_variable_values_and_chosen_option(
            profile_id=recipient.get_profile_id(),
            kwargs={"recipient.first_name": recipient.get_first_name(),
                    "first_name": recipient.get_first_name(),
                    "sender.first_name": self.user_context.get_real_first_name(),
                    "message_id": self.message_id
                    })
        return processed_text_block

    def get_compound_message_dict(self, channel: MessageChannel = None) -> dict:
        if channel is None:
            return self.__compound_message["data"]
        else:
            compound_message_dict = {channel.name: self.__compound_message["data"].get(channel.name, {})}
            if channel != MessageChannel.DEFAULT:
                compound_message_dict["DEFAULT"] = self.__compound_message["data"].get("DEFAULT", {})
            return compound_message_dict

    def get_compound_message_str(self, channel: MessageChannel = None) -> str:
        return json.dumps(self.get_compound_message_dict(channel=channel))

    def get_profile_blocks(self, profile_id: int, channel: MessageChannel) -> list[dict]:
        compound_message_dict = self.get_compound_message_dict(channel=channel)
        if "Page" not in compound_message_dict[channel.name]:
            channel = MessageChannel.DEFAULT

        profile_blocks = []
        for page in compound_message_dict[channel.name]["Page"]:
            for message_template in page["MessageTemplates"]:
                for text_block in message_template["MessageTemplateTextBlocks"]:
                    for profile_block in text_block["Profiles"]:
                        if profile_block["profile_id"] == profile_id and profile_block not in profile_blocks:
                            profile_blocks.append(profile_block)
        return profile_blocks

    def get_message_fields(self) -> dict:
        # TODO: where are we using it?
        if self.recipients:
            recipients_mapping = {recipient.get_profile_id(): recipient.to_json() for recipient in self.recipients}
        else:
            recipients_mapping = {}
        return {
            "campaign_id": self.campaign_id,
            "body": self.body,
            "subject": self.subject,
            "message_id": self.message_id,
            "ui_schema": self.ui_schema,
            "schema": self.schema,
            "field_id": self.field_id,
            "recipients": recipients_mapping,
            "json_version": JSON_VERSION,
        }
