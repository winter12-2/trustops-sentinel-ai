from __future__ import annotations

from typing import Any

from tavily import TavilyClient

from app.config import settings


# class TavilyService:
#     def __init__(self) -> None:
#         self.api_key = settings.tavily_api_key
#         self.client = TavilyClient(api_key=self.api_key) if self.api_key else None

#     def is_configured(self) -> bool:
#         return bool(self.client)

#     def search(self, query: str, max_results: int = 5) -> dict[str, Any]:
#         if not self.client:
#             return {
#                 "success": False,
#                 "error": "Tavily API key is not configured.",
#                 "results": [],
#             }

#         try:
#             response = self.client.search(
#                 query=query,
#                 max_results=max_results,
#                 search_depth="basic",
#                 include_answer=True,
#             )
#             return {
#                 "success": True,
#                 "query": query,
#                 "response": response,
#             }
#         except Exception as exc:
#             return {
#                 "success": False,
#                 "error": str(exc),
#                 "results": [],
#             }


# tavily_service = TavilyService()


class TavilyService:
    def __init__(self) -> None:
        self.api_key = settings.tavily_api_key
        self.client = TavilyClient(api_key=self.api_key) if self.api_key else None

    def is_configured(self) -> bool:
        return bool(self.client)

    def search(self, query: str, max_results: int = 5) -> dict[str, Any]:
        if not self.client:
            return {
                "success": False,
                "error": "Tavily API key is not configured.",
                "results": [],
            }

        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",
                include_answer=True,
            )
            return {
                "success": True,
                "query": query,
                "response": response,
            }
        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "results": [],
            }

    def verify_claim(self, text: str) -> dict[str, Any]:
        if not self.client:
            return {
                "verified": False,
                "reason": "Tavily API key is not configured.",
                "sources": [],
            }

        try:
            response = self.client.search(
                query=text,
                max_results=3,
                search_depth="basic",
                include_answer=True,
            )

            results = response.get("results", [])
            sources = [
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                }
                for item in results
            ]

            verified = len(results) > 0

            return {
                "verified": verified,
                "answer": response.get("answer"),
                "sources": sources,
            }
        except Exception as exc:
            return {
                "verified": False,
                "reason": str(exc),
                "sources": [],
            }


tavily_service = TavilyService()