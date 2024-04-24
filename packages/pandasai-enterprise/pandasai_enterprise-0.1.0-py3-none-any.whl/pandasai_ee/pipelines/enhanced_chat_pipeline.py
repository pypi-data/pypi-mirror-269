# Copyright (c) 2024 Sinaptik GmbH
from typing import Optional
from pandasai.helpers.logger import Logger
from pandasai.pipelines.chat.generate_chat_pipeline import (
    GenerateChatPipeline,
)
from .enhanced_code_executor import EnhancedCodeExecution
from pandasai.pipelines.pipeline import Pipeline
from pandasai.pipelines.pipeline_context import PipelineContext
from pandasai.pipelines.chat.result_parsing import ResultParsing
from pandasai.pipelines.chat.result_validation import ResultValidation


class EnhancedChatPipeline(GenerateChatPipeline):
    """
    Enhanced Chat Pipeline return chart in json format for custom plotting lib
    Args:
        GenerateChatPipeline (GenerateChatPipeline): Extends the general chat pipeline class
    """

    def __init__(
        self,
        context: Optional[PipelineContext] = None,
        logger: Optional[Logger] = None,
        before_code_execution=None,
        on_result=None,
        **kwargs
    ):
        super().__init__(
            context,
            logger,
            before_code_execution=before_code_execution,
            on_result=on_result,
            **kwargs
        )

        self.code_execution_pipeline = Pipeline(
            context=context,
            logger=logger,
            query_exec_tracker=self.query_exec_tracker,
            steps=[
                EnhancedCodeExecution(
                    before_execution=before_code_execution,
                    on_failure=self.on_code_execution_failure,
                    on_retry=self.on_code_retry,
                ),
                ResultValidation(),
                ResultParsing(
                    before_execution=on_result,
                ),
            ],
        )
