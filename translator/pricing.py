from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ModelPricing:
    input_cost: Decimal
    output_cost: Decimal


model_pricing_dict = {
    "gpt-4-1106-preview": ModelPricing(Decimal("0.01"), Decimal("0.03")),
    "gpt-4-1106-vision-preview": ModelPricing(Decimal("0.01"), Decimal("0.03")),
    "gpt-4": ModelPricing(Decimal("0.03"), Decimal("0.06")),
    "gpt-4-32k": ModelPricing(Decimal("0.06"), Decimal("0.12")),
    "gpt-3.5-turbo-1106": ModelPricing(Decimal("0.0010"), Decimal("0.0020")),
    "gpt-3.5-turbo-instruct": ModelPricing(Decimal("0.0015"), Decimal("0.0020")),
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> Decimal:
    model_pricing = model_pricing_dict[model]
    input_cost = model_pricing.input_cost * input_tokens
    output_cost = model_pricing.output_cost * output_tokens
    return (input_cost + output_cost) / 1000
