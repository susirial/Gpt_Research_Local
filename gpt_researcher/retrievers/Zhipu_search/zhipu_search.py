# ZhiPu API Retriever

# libraries
import os

from zhipuai import ZhipuAI


class ZhipuSearch():
    """
    Zhipu API Retriever
    """
    def __init__(self, query, topic="general"):
        """
        Initializes the ZhipuSearch object
        Args:
            query:
        """
        self.query = query
        self.api_key = self.get_api_key()
        self.topic = topic

    def get_api_key(self):
        """
        Gets the Zhipui API key
        Returns:

        """
        # Get the API key
        try:
            api_key = os.environ["MY_ZHIPUAI_API_KEY"]
        except:
            raise Exception("Zhipu API key not found. Please set the MY_ZHIPUAI_API_KEY environment variable.")
        return api_key

    def search(self, max_results=5):
        """
        Searches the query
        Returns:

        """
        try:

            client = ZhipuAI(api_key=self.api_key)

            tools = [{
                "type": "web_search",
                "web_search": {
                    "enable": True,
                }
            }]

            messages = [{
                "role": "user",
                "content": self.query
            }]

            response = client.chat.completions.create(
                model="glm-4",
                messages=messages,
                tools=tools
            )

            sources = response.choices[0].message.content
            print('智谱搜索:\n 问题：{}\n回答：{}'.format(self.query, sources))

            if not sources:
                raise Exception("No results found with Zhipu API search.")
            # Return the results

        except Exception as e: # Fallback in case overload on Tavily Search API
            print(f"Zhipu 搜索异常 Error: {e}")
            sources = "Zhipu 搜索 没有找到相关内容."

        search_response = [{"href": obj["url"], "body": obj["content"]} for obj in sources]
        return search_response
