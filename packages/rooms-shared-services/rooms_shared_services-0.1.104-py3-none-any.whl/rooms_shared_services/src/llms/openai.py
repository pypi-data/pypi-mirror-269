import os

from openai import OpenAI
from pydantic import BaseModel
from yaml import load as yaml_load

from rooms_shared_services.src.models.texts.variants import TextVariant

try:
    from yaml import CLoader as Loader  # noqa: WPS433
except ImportError:
    from yaml import Loader  # noqa: WPS440, WPS433


class OpenaiRequestMessage(BaseModel):
    role: str
    content: str  # noqa: WPS110


class OpenaiQueryClient(object):
    def __init__(self, prompt_filename: str = "rooms_shared_services/src/llms/prompts.yaml"):
        """Set attributes.

        Args:
            prompt_filename (str): _description_. Defaults to "rooms_shared_services/src/llms/prompts.yaml".
        """
        self.openai_client = OpenAI()
        cwd = os.getcwd()
        prompt_full_path = os.path.join(cwd, prompt_filename)
        with open(prompt_full_path) as prompt_obj:
            self.prompt_templates = yaml_load(prompt_obj.read(), Loader=Loader)
            print(self.prompt_templates)

    def create_user_message(self, text_variant: TextVariant, request_params: dict):
        print(request_params)
        print("request_params: product_name: {product_name}".format(product_name=request_params["product_name"]))

        match text_variant:
            case TextVariant.PRODUCT_NAME | TextVariant.PRODUCT_SHORT_DESCRIPTION | TextVariant.PRODUCT_FULL_DESCRIPTION | TextVariant.PRODUCT_ATTRIBUTE_NAME | TextVariant.PRODUCT_ATTRIBUTE_TERM:
                message_content = '"""{text}""". This text in triple quotes is a furniture {text_variant_value}. Translate it to {target_language_value}. Remove any quotes.'.format(
                    text_variant_value=text_variant.readable,
                    **request_params,
                )

            case TextVariant.PRODUCT_CATEGORY:
                print(request_params)
                print("product_name: {product_name}".format(product_name="some name"))
                message_content = 'The product name is """{product_name}""". The product description is  """{product_description}"""'.format(
                    **request_params,
                )
            case _:
                raise ValueError("Invalid text variant")
        return OpenaiRequestMessage(role="user", content=message_content)

    def retrieve_messages(self, text_variant: TextVariant, **request_params):
        print(request_params)
        messages = []
        messages.append(self.retrieve_system_message(text_variant=text_variant))
        messages.append(self.create_user_message(text_variant=text_variant, request_params=request_params))
        return messages

    def retrieve_system_message(self, text_variant: TextVariant):
        for prompt_template in self.prompt_templates["system_messages"]:
            if text_variant.value.lower() in prompt_template["text_variants"]:
                return OpenaiRequestMessage(role="system", content=prompt_template["text"])
        return None

    def receive_response(self, messages: list[OpenaiRequestMessage]):
        return self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[message.model_dump() for message in messages],
        )

    def run_query(self, text_variant: TextVariant, **request_params):
        print(request_params)
        messages = self.retrieve_messages(text_variant=text_variant, **request_params)
        response = self.receive_response(messages=messages)
        return response.choices[0].message.content
