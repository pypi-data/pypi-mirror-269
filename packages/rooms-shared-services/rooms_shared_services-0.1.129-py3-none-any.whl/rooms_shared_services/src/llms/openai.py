import json
import os

from openai import OpenAI
from pydantic import BaseModel
from yaml import load as yaml_load

from rooms_shared_services.src.models.texts.variants import LLMRequestVariant

try:
    from yaml import CLoader as Loader  # noqa: WPS433
except ImportError:
    from yaml import Loader  # noqa: WPS440, WPS433


class OpenaiRequestMessage(BaseModel):
    role: str
    content: str  # noqa: WPS110


class OpenaiQueryClient(object):
    def __init__(
        self,
        request_variant: LLMRequestVariant,
        openai_model: str = "gpt-3.5-turbo",
        retry_count: int = 25,
        prompt_filename: str = "rooms_shared_services/src/llms/prompts.yaml",
    ):
        """Set attributes.

        Args:
            openai_model (str): __description__.
            request_variant (LLMRequestVariant): _description_.
            retry_count (int): _description_. Defaults to 25
            prompt_filename (str): _description_. Defaults to "rooms_shared_services/src/llms/prompts.yaml".
        """
        self.openai_model = openai_model
        self.request_variant = request_variant
        self.openai_client = OpenAI()
        cwd = os.getcwd()
        prompt_full_path = os.path.join(cwd, prompt_filename)
        self.retry_count = retry_count
        with open(prompt_full_path) as prompt_obj:
            self.prompt_templates = yaml_load(prompt_obj.read(), Loader=Loader)
            print(self.prompt_templates)

    def create_user_message(self, request_params: dict):
        print(request_params)

        match self.request_variant:
            case LLMRequestVariant.TRANSLATE_PRODUCT_NAME | LLMRequestVariant.TRANSLATE_PRODUCT_SHORT_DESCRIPTION | LLMRequestVariant.TRANSLATE_PRODUCT_FULL_DESCRIPTION | LLMRequestVariant.TRANSLATE_PRODUCT_CATEGORY_NAME:
                message_content = '"""{text}""". This text in triple quotes is a furniture {request_variant_value}. Translate it to {target_language_value}. Remove any quotes.'.format(
                    request_variant_value=self.request_variant.readable,
                    **request_params,
                )

            case LLMRequestVariant.TRANSLATE_PRODUCT_ATTRIBUTE_NAME | LLMRequestVariant.TRANSLATE_PRODUCT_ATTRIBUTE_TERM:
                message_content = '"""{text}""". This text in triple quotes is a furniture {request_variant_value}. Translate it to {target_language_value}.'.format(
                    **request_params,
                )

            case LLMRequestVariant.ASSIGN_PRODUCT_CATEGORY | LLMRequestVariant.ASSIGN_FURNITURE_TYPE:
                message_content = 'The product name is """{product_name}""". The product description is  """{product_description}"""'.format(
                    **request_params,
                )
            case _:
                raise ValueError("Invalid text variant")
        return OpenaiRequestMessage(role="user", content=message_content)

    def retrieve_messages(self, **request_params):
        print(request_params)
        messages = []
        messages.append(self.retrieve_system_message(**request_params))
        messages.append(self.create_user_message(request_params=request_params))
        return messages

    def retrieve_system_message(self, **request_params):
        for prompt_template in self.prompt_templates["system_messages"]:
            if self.request_variant.value.lower() in prompt_template["request_variants"]:
                message_content = prompt_template["text"].format(
                    request_variant_value=self.request_variant.readable,
                    **request_params,
                )
                return OpenaiRequestMessage(role="system", content=message_content)
        return None

    def receive_response(self, messages: list[OpenaiRequestMessage]):
        return self.openai_client.chat.completions.create(
            model=self.openai_model,
            messages=[message.model_dump() for message in messages],
        )

    def validate_json_response(self, response: str, **request_params):
        print(response)
        try:
            response = json.loads(response)["result"]
        except Exception:
            return None
        match self.request_variant:
            case LLMRequestVariant.ASSIGN_PRODUCT_CATEGORY | LLMRequestVariant.ASSIGN_FURNITURE_TYPE:
                if response not in request_params["option_list"]:
                    return None
            case LLMRequestVariant.TRANSLATE_PRODUCT_ATTRIBUTE_NAME | LLMRequestVariant.TRANSLATE_PRODUCT_ATTRIBUTE_TERM | LLMRequestVariant.TRANSLATE_PRODUCT_CATEGORY_NAME:
                pass
            case _:
                raise ValueError("Invalid request variant")
        return response.replace('"', "").replace("[", "").replace("]", "")

    def run_query(self, **request_params):
        print(request_params)
        for _ in range(self.retry_count):
            messages = self.retrieve_messages(request_variant=self.request_variant, **request_params)
            response = self.receive_response(messages=messages)
            response = response.choices[0].message.content
            validated_response = self.validate_json_response(response=response, **request_params)
            if validated_response:
                return validated_response
        raise ValueError("No valid response received")
