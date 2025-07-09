# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
import uvicorn
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.utils import new_agent_text_message
from a2a.utils.errors import ServerError

class A2AServer:
    """
    Provides a consistent interface with the `to_mcp()` method,
    enabling the initialization of agent-based servers in a uniform manner.

    Example:
        server = agent.to_a2a()
        server.run()  # Consistent invocation pattern with to_mcp()
    """

    def __init__(self, host, port, server):
        self.host = host
        self.port = port
        self.server = server

    def run(self):
        uvicorn.run(self.server.build(), host=self.host, port=self.port)



class ChatAgentExecutor(AgentExecutor):
    def __init__(self, agent_instance ):
        self.agent_instance = agent_instance
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        try:
            if not context.message:
                raise Exception('No message provided')

            query = context.get_user_input()

            # updater = TaskUpdater(event_queue, context.task_id, context.context_id)

            format_cls = None

            response = await self.agent_instance.astep(query, format_cls)
            await event_queue.enqueue_event(new_agent_text_message(str(response), context.context_id, context.task_id))
        except Exception as e:
            print("Error invoking agent: %s", e)
            raise ServerError(error=ValueError(f"Error invoking agent: {e}")) from e

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')