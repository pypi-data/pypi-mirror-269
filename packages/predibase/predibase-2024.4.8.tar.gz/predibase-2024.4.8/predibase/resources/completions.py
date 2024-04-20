from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any

from predibase._errors import PredibaseError
from predibase.resource.llm.interface import _LLMDeployment
from predibase.resources.deployment import DedicatedLLMDeployment, ServerlessLLMDeployment
from predibase.util import log_info

if TYPE_CHECKING:
    from predibase import Predibase
    from predibase.resources.model import FinetunedLLMAdapter
    from predibase.resource.llm.response import GeneratedResponse


class Completions:
    def __init__(self, client: Predibase):
        self._client = client

    def create(
        self,
        data: str | Dict[str, Any],
        *,
        adapter: FinetunedLLMAdapter | None = None,  # TODO: support passing model URI
        deployment: str | DedicatedLLMDeployment | ServerlessLLMDeployment = "auto",
        temperature: float = 0.1,
        new_tokens: int = 128,
        bypass_system_prompt: bool = False,
    ) -> GeneratedResponse:
        """
        Creates a new text completion using the specified adapter and/or deployed LLM.

        :param data: Either a string prompt to pass to the LLM, or a dictionary mapping variable names to values. These
            variable names must appear in the prompt template with which the adapter was fine-tuned, and the mapped
            values will be interpolated into the adapter's prompt template.
        :param adapter: (Optional) The fine-tuned adapter to use for this prompt completion. If not specified, then
            a `deployment` to prompt must be provided.
        :param deployment: (Optional) The deployed LLM instance to prompt. If `adapter` is specified but this field is
            not, a deployment compatible with the selected adapter will be automatically chosen. If `adapter` is not
            specified, then this field must be non-empty.
        :param temperature: Higher temperature settings provide more diversity in LLM responses, while a lower
            temperature will result in more deterministic responses.
        :param new_tokens: The maximum number of output tokens the LLM should generate.
        :param bypass_system_prompt: If True, ignore any default prompt attached to the deployed LLM.
        :return: A GeneratedResponse object.
        """
        if isinstance(deployment, str) and deployment == "auto":
            # TODO: allow passing deployment as string

            if adapter is None:
                raise PredibaseError(f"the target deployment cannot be 'auto' if no adapter is provided")

            deployments = self._client._session.get_json("/llms")
            llms = [_LLMDeployment.from_dict(d) for d in deployments]
            compatible_serverless_llms = [
                llm
                for llm in llms
                if self._adapter_compatible(llm.model_name, adapter.base_model_name) and llm.is_shared
            ]
            compatible_dedicated_llms = [
                llm
                for llm in llms
                if self._adapter_compatible(llm.model_name, adapter.base_model_name) and not llm.is_shared
            ]

            if compatible_serverless_llms:
                deployment = ServerlessLLMDeployment(self._client, compatible_serverless_llms[0].name)
            elif compatible_dedicated_llms:
                deployment = DedicatedLLMDeployment(self._client, compatible_dedicated_llms[0].name)
            else:
                raise PredibaseError(
                    f"no compatible deployments found for adapter's base model {adapter.base_model_name}"
                )

            log_info(
                f"Automatically selected deployment {deployment.name} from those compatible with adapter's base model "
                f"{adapter.base_model_name}"
            )

        # Falling back to the underlying prompt/generate implementation on LLMDeployment for now in order
        # to better pick up expected changes for introducing LoRAX client.
        # TODO: cleaner split once we have more confidence in the new version.
        dep = deployment._refresh()
        if adapter:
            dep = dep.with_adapter(adapter._model)

        return dep.prompt(
            data,
            temperature=temperature,
            max_new_tokens=new_tokens,
            bypass_system_prompt=bypass_system_prompt,
        )

    @staticmethod
    def _adapter_compatible(deployment_model_name, adapter_model_name) -> bool:
        """
        Shortcut helper method that checks for adapter compatibility using some string manipulation
        on the deployment and adapter model names.
        """

        # TODO(PUX-2100): replace this with a more robust API call once it's available.

        def preprocess_name(name: str) -> str:
            ret = name.lower().split("/")[-1]
            if "-hf" in ret:
                ret = ret[: ret.index("-hf")]
            return ret

        deployment_model = preprocess_name(deployment_model_name)
        adapter_model = preprocess_name(adapter_model_name)
        if "-v0.1" in adapter_model:
            adapter_model = adapter_model[: adapter_model.index("-v0.1")]

        return adapter_model in deployment_model
