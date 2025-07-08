from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

class CamelAgentExecutor(AgentExecutor):
    def __init__(self, agent):
        self.agent = agent
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        context_id = context.context_id
        task_id = context.task_id

        if not context.message:
            raise Exception('No message provided')

        format_cls = None

        response = await self.agent(query, format_cls)

        await event_queue.enqueue_event(new_agent_text_message(str(response), context_id, task_id))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')