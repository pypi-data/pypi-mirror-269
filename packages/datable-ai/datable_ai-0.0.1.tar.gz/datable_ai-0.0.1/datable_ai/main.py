from dotenv import load_dotenv
from datable_ai.core.llm import LLM_TYPE
from datable_ai.structured_output import StructuredOutput


if __name__ == "__main__":
    load_dotenv()

    fields = [
        {"name": "product_name", "type": str, "description": "The name of the product"},
        {
            "name": "rating",
            "type": int,
            "description": "The rating of the product (1-5)",
        },
        {
            "name": "review",
            "type": str,
            "description": "The review text",
        },
    ]

    prompt_template = """Please provide a review for the following product:
Product Name: {product_name} {product_version}

Review the product based on your experience and provide the following information:
- Rating (1-5):
- Review Text:
    """

    llm_type = LLM_TYPE.OPENAI
    structured_output = StructuredOutput(llm_type, prompt_template, fields)

    product_name = "iPhone"
    product_version = "13 Pro"
    output = structured_output.invoke(
        product_name=product_name, product_version=product_version
    )
    print(output)
