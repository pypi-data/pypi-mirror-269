import unittest

from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
)
from transformers.utils.import_utils import (
    is_flash_attn_2_available,
    is_torch_sdpa_available,
)


TINY_MISTRAL = "hf-internal-testing/tiny-random-MistralForCausalLM"


class ModelUtilsTest(unittest.TestCase):
    def test_model_from_pretrained_attn_implementation(self):
        # test that the model can be instantiated with attn_implementation of either
        # 1. explicit from_pretrained's attn_implementation argument
        # 2. explicit from_pretrained's attn_implementation argument with a config argument
        attn_implementation_available = ["eager"]
        if is_torch_sdpa_available():
            attn_implementation_available.append("sdpa")

        if is_flash_attn_2_available():
            attn_implementation_available.append("flash_attention_2")

        mistral_attention_classes = {
            "eager": "MistralAttention",
            "sdpa": "MistralSdpaAttention",
            "flash_attention_2": "MistralFlashAttention2",
        }
        for requested_attn_implementation in attn_implementation_available:
            model = AutoModelForCausalLM.from_pretrained(
                TINY_MISTRAL, attn_implementation=requested_attn_implementation
            )
            self.assertEqual(model.config._attn_implementation, requested_attn_implementation)
            for module in model.modules():
                if "Attention" in module.__class__.__name__:
                    self.assertEqual(
                        module.__class__.__name__, mistral_attention_classes[requested_attn_implementation]
                    )

            config = AutoConfig.from_pretrained(TINY_MISTRAL)
            model = AutoModelForCausalLM.from_pretrained(
                TINY_MISTRAL, config=config, attn_implementation=requested_attn_implementation
            )
            self.assertEqual(model.config._attn_implementation, requested_attn_implementation)
            for module in model.modules():
                if "Attention" in module.__class__.__name__:
                    self.assertEqual(
                        module.__class__.__name__, mistral_attention_classes[requested_attn_implementation]
                    )
