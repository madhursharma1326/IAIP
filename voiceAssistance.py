"""
Python Voice Assistant - Single File Version

Features:
- Speech recognition with SpeechRecognition when installed
- Text-to-speech with pyttsx3 when installed
- Weather updates through wttr.in
- Web search in the default browser
- Local schedule storage
- WolframAlpha API support through WOLFRAM_APP_ID
- Basic conversational responses
- Built-in unit tests with: python voice_assistant_single_file.py --test
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
import unittest
import webbrowser
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol


class Speaker(Protocol):
    def speak(self, text: str) -> None:
        ...


class Listener(Protocol):
    def listen(self) -> str:
        ...


class WeatherProvider(Protocol):
    def get_weather(self, location: str) -> str:
        ...


class SearchProvider(Protocol):
    def search(self, query: str) -> str:
        ...


class ScheduleProvider(Protocol):
    def add_event(self, event_text: str) -> str:
        ...

    def list_events(self) -> str:
        ...


class KnowledgeProvider(Protocol):
    def ask(self, question: str) -> str | None:
        ...


@dataclass
class CommandResult:
    response: str
    should_stop: bool = False


@dataclass
class ScheduleEvent:
    text: str
    created_at: str


class Assistant:
    def __init__(
        self,
        speaker: Speaker,
        listener: Listener,
        weather_service: WeatherProvider,
        search_service: SearchProvider,
        schedule_service: ScheduleProvider,
        knowledge_service: KnowledgeProvider,
    ) -> None:
        self.speaker = speaker
        self.listener = listener
        self.weather_service = weather_service
        self.search_service = search_service
        self.schedule_service = schedule_service
        self.knowledge_service = knowledge_service

    def say(self, text: str) -> None:
        self.speaker.speak(text)

    def run(self) -> None:
        while True:
            try:
                command = self.listener.listen()
                result = self.handle_command(command)
                self.say(result.response)
                if result.should_stop:
                    break
            except KeyboardInterrupt:
                self.say("Goodbye.")
                break
            except Exception as exc:
                self.say(f"Sorry, I ran into a problem: {exc}")

    def handle_command(self, raw_command: str) -> CommandResult:
        command = normalize(raw_command)
        if not command:
            return CommandResult("I did not hear a command. Please try again.")

        if command in {"stop", "exit", "quit", "goodbye"}:
            return CommandResult("Goodbye.", should_stop=True)

        if command in {"hello", "hi", "hey"}:
            return CommandResult("Hello. How can I help you today?")

        if command in {"help", "what can you do"}:
            return CommandResult(
                "I can check weather, search the web, manage your schedule, answer questions, and chat."
            )

        if command.startswith("weather"):
            location = extract_after_any(command, ["weather in", "weather for", "weather"])
            if not location:
                return CommandResult("Please tell me a city. For example, weather in Delhi.")
            return CommandResult(self.weather_service.get_weather(location))

        if command.startswith("search"):
            query = extract_after_any(command, ["search for", "search"])
            if not query:
                return CommandResult("Please tell me what to search for.")
            return CommandResult(self.search_service.search(query))

        if command.startswith("schedule") or command.startswith("remind me"):
            event_text = extract_after_any(command, ["schedule", "remind me to", "remind me"])
            if not event_text:
                return CommandResult("Please tell me what to add to your schedule.")
            return CommandResult(self.schedule_service.add_event(event_text))

        if command in {"show schedule", "list schedule", "my schedule", "what is my schedule"}:
            return CommandResult(self.schedule_service.list_events())

        answer = self.knowledge_service.ask(command)
        if answer:
            return CommandResult(answer)

        return CommandResult("I am not sure about that yet. Try asking for weather, search, or schedule.")


class WeatherService:
    def get_weather(self, location: str) -> str:
        safe_location = urllib.parse.quote(location)
        url = f"https://wttr.in/{safe_location}?format=3"
        try:
            with urllib.request.urlopen(url, timeout=8) as response:
                return response.read().decode("utf-8").strip()
        except Exception:
            return f"Sorry, I could not fetch the weather for {location} right now."


class BrowserSearchService:
    def search(self, query: str) -> str:
        url = "https://duckduckgo.com/?q=" + urllib.parse.quote_plus(query)
        try:
            webbrowser.open(url)
            return f"I opened a web search for {query}."
        except Exception:
            return f"Sorry, I could not open a web search for {query}."


class ScheduleService:
    def __init__(self, file_path: str | Path = "schedule.json") -> None:
        self.file_path = Path(file_path)

    def add_event(self, event_text: str) -> str:
        events = self._read_events()
        event = ScheduleEvent(text=event_text, created_at=datetime.now().isoformat(timespec="seconds"))
        events.append(event)
        self._write_events(events)
        return f"Added to your schedule: {event_text}."

    def list_events(self) -> str:
        events = self._read_events()
        if not events:
            return "Your schedule is empty."
        event_lines = [f"{index}. {event.text}" for index, event in enumerate(events, start=1)]
        return "Your schedule: " + "; ".join(event_lines)

    def _read_events(self) -> list[ScheduleEvent]:
        if not self.file_path.exists():
            return []
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            return [ScheduleEvent(**item) for item in data]
        except Exception:
            return []
