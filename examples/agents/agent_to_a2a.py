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
import os

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.toolkits import FileWriteToolkit,SearchToolkit,WeatherToolkit

from camel.types import ModelPlatformType, ModelType

# Create a chat agent with a model
model = ModelFactory.create(
    model_platform=ModelPlatformType.QWEN,
    model_type=ModelType.QWEN_2_5_32B,
    api_key="",
)
# Set up output directory
output_dir = "./file_write_outputs"
os.makedirs(output_dir, exist_ok=True)

# Initialize the FileWriteToolkit with the output directory
file_toolkit = FileWriteToolkit(output_dir=output_dir)

# Get the tools from the toolkit
tools_list = [*SearchToolkit().get_tools(),
              *file_toolkit.get_tools(),
              *WeatherToolkit().get_tools(),
]

agent = ChatAgent("You are a helpful assistant.", model=model,tools=tools_list)

# # Create an A2A server from the agent
a2a_server = agent.to_a2a(
    host="0.0.0.0",
    name="demo",
    description="A demonstration of ChatAgent to A2A conversion"
)

# Run the server
a2a_server.run()
