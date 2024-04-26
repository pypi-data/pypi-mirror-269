## PixelyAI Core🧬

### Introduction

PixelyAI Core is the core component of PixelyAI, an AI assistant that helps businesses manage their customers and their
team more effectively. It provides a suite of tools for hosting and interacting with large language models (LLMs),
making it easy to integrate these powerful AI capabilities into your applications.

### Key Features

* **Support for Multiple Backends:** with Using _AgentX_ PixelyAI Core supports popular backends for hosting LLMs
  Like `GGUF`,`Torch`,`EasyDeL` and `OLlama`. This flexibility allows you to choose the backend that best suits
  needs and infrastructure.

* **Simplified API:** PixelyAI Core provides an easy-to-use API for interacting with LLMs. This API makes it simple to
  send queries to LLMs, receive responses, and handle errors.

* **Gradio Integration:** PixelyAI Core integrates seamlessly with `Gradio`, a web framework for building interactive AI
  applications. This integration allows you to create intuitive interfaces for interacting with `LLMs`, making it easier
  for users to access their capabilities.

### Benefits

* **Improved Customer Support:** Empower your customer support team with conversational AI capabilities, enabling them
  to provide more personalized and efficient support.

* **Enhanced Team Collaboration:** Facilitate knowledge sharing and collaboration among team members through natural
  language interactions.

* **Automated Task Delegation:** Automate routine tasks, such as report generation and data analysis, freeing up team
  members to focus on more strategic initiatives.

### Getting Started

To install PixelyAI Core, simply use the following command:

```bash
pip install pixelyai-core
```

Once installed, you can start using the PixelyAI Core API to interact with LLMs. For more information, please refer to
the official documentation.

### Client UseCase Example

Here's a simple use case of PixelyAI Chat and RAG Agents

```python
from pixelyai_core import PixelClient

client = PixelClient(
    "http://127.0.0.1:7860/"
)
# in case that contexts is None the RAG agent won't be used

contexts = None

# Using RAG Agent with contexts be Like

contexts = [
    (
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris,"
        " France. It is named after the engineer Gustave Eiffel, whose company designed"
        " and built the tower. Constructed from 1887 to 1889 as the entrance to the 1889 World's "
        "Fair, it was initially criticized by some of France's leading artists and intellectuals for "
        "its design, but it has become a global cultural icon of France and one of the most recognizable"
        " structures in the world. The Eiffel Tower is the most-visited paid monument in the world; 6.91 "
        "million people ascended it in 2015. The tower is 324 meters (1,063 ft) tall, about the same height "
        "as an 81-story building, and the tallest structure in Paris. Its base is square, measuring 125 meters"
        " (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become "
        "the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New "
        "York City was finished in 1930. It was the first structure to reach a height of 300 meters. Due"
        " to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler"
        " Building by 5.2 meters (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing "
        "structure in France after the Millau Viaduct."
    ),
    (
        "The tower has three levels for visitors, with restaurants on the first and second levels."
        " The top level's upper platform is 276 m (906 ft) above the ground – the highest observation"
        " deck accessible to the public in the European Union. Tickets can be purchased to ascend by "
        "stairs or lift to the first and second levels. The climb from ground level to the first level "
        "is over 300 steps, as is the climb from the first level to the second. Although there is a staircase"
        " to the top level, it is usually accessible only by lift."
    )
]

response = client(
    prompt="who can i travel to canada?",
    contexts=contexts,
    conversation_history=[
        {"user": "hello"},
        {"assistant": "Hello! How can i help you today?"}
    ]
)
```

### Conclusion

PixelyAI Core is a powerful tool for businesses seeking to leverage the capabilities of LLMs to improve their customer
service, collaboration, and productivity. With its support for multiple backends, simplified API, PixelyAI Core provides
a versatile and user-friendly platform for integrating LLMs into your applications.
