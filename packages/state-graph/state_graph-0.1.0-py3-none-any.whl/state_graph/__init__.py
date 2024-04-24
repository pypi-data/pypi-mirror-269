from re import I
from regex import P
from rich import print
import os
from typing import TypedDict, Any, get_type_hints, Annotated, get_origin
import operator
from abc import ABC, abstractmethod
import numpy as np
import ipdb
import operator
from pydantic import BaseModel
from typing import (
    Awaitable,
    Callable,
    Literal,
    get_args,
    TypeVar,
    Any,
    Annotated,
)
import asyncio
import networkx as nx

# beartype_this_package()

T = TypeVar("T", bound=BaseModel)


def is_mutable(model_class):
    current_class = model_class
    while issubclass(current_class, BaseModel):
        if hasattr(current_class, "Config"):
            if hasattr(current_class.Config, "frozen"):
                if current_class.Config.frozen:
                    return False
        current_class = current_class.__base__
    return True


class Node(BaseModel):
    name: str
    color: str = "blue"
    static_context: BaseModel | None = None
    _stream_token: list[Callable[[str], Awaitable]] = []

    class Config:
        frozen = True

    @property
    def stream_token(self):
        assert len(self._stream_token) == 1, "stream_token must be set."
        return self._stream_token[0]

    def _set_stream_token(self, value: Callable[[str], Awaitable]):
        if len(self._stream_token) > 0:
            # replace it
            self._stream_token[0] = value
        else:
            self._stream_token.append(value)

    async def run(self, context: T) -> dict | T:
        return {}

    def __init__(self, static_context: BaseModel | None = None, **kwargs):
        super().__init__(**kwargs, static_context=static_context)
        if static_context is not None:
            # check that it is frozen
            assert not is_mutable(
                static_context.__class__
            ), "Static context must be frozen"


class WaitingNode(Node):
    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__(name=name, color="orange", _is_waiting=True)


class StartNode(Node):
    def __init__(self) -> None:
        super().__init__(name="start", color="green")


class EndNode(Node):
    def __init__(self, name="end") -> None:
        super().__init__(name=name, color="red")


class Edge(BaseModel):
    fn: Callable
    out_nodes: tuple[str, ...]
    labels: tuple[str, ...]
    name: str
    start_node: str

    def __call__(self, context: dict) -> str:
        return self.fn(context)

    class Config:
        frozen = True


class SimpleEdge(Edge):
    def __init__(
        self,
        start_node: str | Node,
        out_node: str | Node,
        name: str | None = None,
        label: str | None = None,
    ) -> None:
        out_node = out_node.name if isinstance(out_node, Node) else out_node
        start_node = start_node.name if isinstance(start_node, Node) else start_node

        def _fn(_: dict) -> str:
            return out_node

        name = name if name else f"{start_node}->{out_node}"
        label = label if label else ""
        super().__init__(
            fn=_fn,
            out_nodes=(out_node,),
            name=name,
            start_node=start_node,
            labels=(label,),
        )


def edge(start_node: str | Node):
    start_node = start_node.name if isinstance(start_node, Node) else start_node

    def decorator(fn: Callable) -> Edge:
        return_type = fn.__annotations__.get("return")
        assert (
            return_type is not None
        ), f"Function {fn.__name__} must have a return type annotation"
        out_nodes = (
            get_args(return_type)
            if not get_origin(return_type) == Annotated
            else get_args(get_args(return_type)[0])
        )
        # checks if the return type has metadata
        if hasattr(return_type, "__metadata__") and return_type.__metadata__:
            if len(return_type.__metadata__) != len(out_nodes):
                raise ValueError(
                    f"""If you annotate the return type of an edge, the function must return the same number of nodes as the return type annotation.
found len({return_type.__metadata__})=={len(return_type.__metadata__)} != len({out_nodes})=={len(out_nodes)}
"""
                )
            labels = return_type.__metadata__
        else:
            labels = tuple(f"{start_node}->{node}" for node in out_nodes)
        assert all(
            isinstance(node, str) for node in out_nodes
        ), f"All literal values in the return type annotation of function {fn.__name__} must be strings"
        name = fn.__name__
        return Edge(
            fn=fn, out_nodes=out_nodes, name=name, start_node=start_node, labels=labels
        )

    return decorator


def node(fn: Callable):
    class _Node(Node):
        def __init__(self, name: str) -> None:
            super().__init__(name=name)

        async def run(self, context: dict) -> dict:
            return await fn(context)

    return _Node(name=fn.__name__)


T = TypeVar("T", bound=BaseModel)


def merge_context(context: T, input: dict[str, Any] | T) -> T:
    """
    Merge the input into the context without mutating the original context. Creates and returns a new instance.
    This function is generic and can handle any subclass of BaseModel.
    Assumptions:
    - the input keys are a subset of the context keys
    - the context may contain some keys that have an Annotated type. If they are Annotated,
      the annotation must be a function that takes the value coming from the context and
      the one from the input, and defines how to merge them.
    """
    if isinstance(input, BaseModel):
        return input.model_copy()
    new_context = context.model_copy()
    annotations = get_type_hints(context.__class__, include_extras=True)
    assert input is not None
    for key, value in input.items():
        if key in annotations:
            annotation = annotations[key]
            if hasattr(annotation, "__metadata__") and annotation.__metadata__:
                # Extract the function from Annotated type
                merge_func = annotation.__metadata__[0]
                setattr(new_context, key, merge_func(getattr(new_context, key), value))
            else:
                setattr(new_context, key, value)
        else:
            # Default behavior for keys without special annotations
            setattr(new_context, key, value)

    return new_context


def update_context(context: BaseModel, input: dict[str, Any] | BaseModel) -> BaseModel:
    input = input.model_dump() if isinstance(input, BaseModel) else input
    return context.model_copy(update=input)


class Graph:
    nodes: dict[str, Node]
    edges: dict[str, Edge]
    graph: nx.MultiDiGraph
    current_node: Node
    context: BaseModel
    __initial_context: BaseModel
    __on_state_enter_callbacks: dict[str, Callable[[BaseModel], Awaitable] | None]
    __on_state_exit_callbacks: dict[str, Callable[[BaseModel], Awaitable] | None]

    @property
    def stream_token(self):
        return self.__stream_token

    @stream_token.setter
    def stream_token(self, value: Callable[[str], Awaitable]):
        self.__stream_token = value
        for node in self.nodes.values():
            node._set_stream_token(value)

    def compile(self) -> None:
        """
        Check that the graph looks right.
        Using the already built MultiDiGraph object, check the following:
            - node start has exactly one edge going out
            - node end has exactly zero edges going in
            - the end node, if present, has zero edges going out
            - no node has zero edges going in, except for the start node.
            - check that the nodes that each edge points to exist
            - check that the nodes that each edge comes from exist
            - check that all nodes, except for the end node, have at least one edge goin out
        Raises an exception if any of these conditions are not met.
        """
        start_node_out_edges = self.graph.out_edges("start")
        if len(start_node_out_edges) != 1:
            raise ValueError(
                f"'start' node must have exactly one edge going out, found {len(start_node_out_edges)}"
            )
        end_node_out_edges = self.graph.out_edges("end")
        if len(end_node_out_edges) != 0:
            raise ValueError(
                f"'end' node must have zero edges going out, found {len(end_node_out_edges)}"
            )

        for node in self.graph.nodes:
            if node != "start" and self.graph.in_degree(node) == 0:
                raise ValueError(
                    f"Node '{node}' has zero edges going in, which is not allowed except for the start node."
                )

        for edge in self.edges.values():
            target_nodes = edge.out_nodes
            for target_node in target_nodes:
                if target_node not in self.nodes:
                    raise ValueError(
                        f"Edge '{edge.name}' points to non-existent node '{target_node}'"
                    )
            if edge.start_node not in self.nodes:
                raise ValueError(
                    f"Edge '{edge.name}' points to non-existent node '{edge.start_node}'"
                )

        for node in self.nodes.values():
            if node.name != "end" and self.graph.out_degree(node.name) == 0:
                raise ValueError(
                    f"Node '{node.name}' has zero edges going out, which is not allowed except for the end node."
                )

        self.__is_compiled = True

    def reset(self, new_state: dict[str, Any] | None = None) -> "Graph":
        new_state = new_state or {}
        initial_context = self.__initial_context.__class__(
            **self.__initial_context.model_copy().model_dump() | new_state
        )
        new_graph = Graph(
            context=initial_context,
            name=self.graph.name,
            nodes=self.nodes.copy(),
            edges=self.edges.copy(),
            stream_token=self.__stream_token,
            _is_compiled=self.__is_compiled,
        )
        return new_graph

    __stream_token: Callable[[str], Awaitable]

    def __init__(
        self,
        *,
        context: BaseModel,
        name: str = "graph",
        nodes: dict[str, Node] | None = None,
        edges: dict[str, Edge] | None = None,
        stream_token: Callable[[str], Awaitable] | None = None,
        on_state_enter: (
            dict[str, Callable[[BaseModel], Awaitable] | None] | None
        ) = None,
        on_state_exit: dict[str, Callable[[BaseModel], Awaitable] | None] | None = None,
        _is_compiled: bool = False,
    ) -> None:
        nodes = nodes if nodes is not None else {}
        edges = edges if edges is not None else {}
        self.nodes = {}
        self.edges = {}
        self.name = name
        self.graph = nx.MultiDiGraph(name=name)
        self.__initial_context = context
        self.context = context.copy()
        self.__is_compiled = _is_compiled

        async def _stream_token(token: str):
            pass

        self.__stream_token = (
            stream_token if stream_token is not None else _stream_token
        )
        if "start" not in nodes:
            # self.add_node(StartNode())
            self.nodes["start"] = StartNode()

        for node in nodes.values():
            self.add_node(node)

        for edge in edges.values():
            self.add_edge(edge)

        self.current_node = self.nodes["start"]

        self.__on_state_enter_callbacks = (
            on_state_enter if on_state_enter is not None else {}
        )
        self.__on_state_exit_callbacks = (
            on_state_exit if on_state_exit is not None else {}
        )

    def on_state_enter(self, state: str, callback: Callable):
        assert state in self.nodes, f"Node {state} does not exist."
        self.__on_state_enter_callbacks[state] = callback

    def on_state_exit(self, state: str, callback: Callable):
        assert state in self.nodes, f"Node {state} does not exist."
        self.__on_state_exit_callbacks[state] = callback

    def add_node(self, node: Node):
        assert node.name not in self.nodes, f"Node {node.name} already exists"
        self.nodes[node.name] = node
        self.graph.add_node(node.name, color=node.color)
        node._set_stream_token(self.__stream_token)

    def add_edge(self, edge: Edge):
        assert edge.name not in self.edges, f"Edge {edge.name} already exists"
        assert (
            edge.start_node in self.nodes
        ), f"Edge {edge.name} points to non-existent node {edge.start_node}"
        assert all(
            out_node in self.nodes for out_node in edge.out_nodes
        ), f"Edge {edge.name} points to non-existent node(s)"
        self.edges[edge.name] = edge
        for out_node in edge.out_nodes:
            self.graph.add_edge(
                edge.start_node, out_node, label=edge.name, directed=True
            )

    def add_simple_edge(
        self,
        start_node: str | Node,
        out_node: str | Node,
        name: str | None = None,
        label: str | None = None,
    ):
        self.add_edge(SimpleEdge(start_node, out_node, name, label))

    async def run(self, input: dict[str, Any] | None = None) -> tuple[BaseModel, bool]:
        assert self.__is_compiled, "Graph must be compiled before running"
        input = input or {}
        self.context = merge_context(self.context, input)
        is_end = False
        while True:
            if self.current_node.name in self.__on_state_exit_callbacks:
                callback = self.__on_state_exit_callbacks[self.current_node.name]
                if callback is not None:
                    await callback(self.context)

            self.current_node = self.get_next_node(self.current_node.name, self.context)
            print(
                f"[red bold underline] {self.current_node.name} [/red bold underline]"
            )
            if self.current_node.name in self.__on_state_enter_callbacks:
                callback = self.__on_state_enter_callbacks[self.current_node.name]
                if callback is not None:
                    await callback(self.context)

            if isinstance(self.current_node, EndNode):
                is_end = True
                break

            if isinstance(self.current_node, WaitingNode):
                return self.context, False

            context_update = await self.current_node.run(self.context)
            self.context = update_context(self.context, context_update)

        return self.context, is_end

    def get_next_node(self, current_node_name: str, context: BaseModel) -> Node:
        matching_edges = [
            e for e in self.edges.values() if e.start_node == current_node_name
        ]
        assert len(matching_edges) != 0, f"No edges found for node {current_node_name}"
        assert (
            len(matching_edges) == 1
        ), f"Multiple edges found for node {current_node_name}"
        for edge in matching_edges:
            next_node_name = edge.fn(context)
            assert (
                next_node_name in edge.out_nodes
            ), f"Edge {edge.name} does not have a valid out node"
            return self.nodes[next_node_name]

        raise RuntimeError("No next node found")

    def plot(self, destination: str = "."):
        assert self.__is_compiled, "Graph must be compiled before plotting"
        # Start of the Mermaid.js diagram
        mermaid_diagram = f"""
---        
title: {self.name}
---
stateDiagram-v2
"""
        # Unique color tracking for class definition
        color_classes = {}
        class_counter = 1

        # Collect all unique colors and define class styles
        for node in self.nodes.values():
            if hasattr(node, "color") and node.color not in color_classes:
                class_name = f"class{class_counter}"
                color_classes[node.color] = class_name
                mermaid_diagram += (
                    f"    classDef {class_name} fill:{node.color}, stroke:#333\n"
                )
                class_counter += 1

        # Adding all transitions
        for edge in self.edges.values():
            for i, out_node in enumerate(edge.out_nodes):
                transition = (
                    f"    {edge.start_node} --> {out_node} : {edge.labels[i]}\n"
                )
                mermaid_diagram += transition

        # Assigning classes to nodes based on their colors
        for node_name, node in self.nodes.items():
            if hasattr(node, "color"):
                mermaid_diagram += (
                    f"    class {node_name} {color_classes[node.color]}\n"
                )

        # return mermaid_diagram
        out_html = f"""
        <!DOCTYPE html>
        <html style="background-color: #222; padding: 0; margin:0;">
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>mermaid.initialize({{startOnLoad:true, theme:'dark', zoom: true, move: true}});</script>
        </head>
        <body style="background-color: #222; padding: 0; margin:0;">
            <div class="mermaid">
                {mermaid_diagram}
            </div>
        </body>
        </html>"""

        with open(os.path.join(destination, "graph.html"), "w") as f:
            f.write(out_html)


async def main():

    async def stream_token(token: str):
        print(token)

    class Context(BaseModel):
        chat: Annotated[list[dict[str, str]], operator.add]

    class Node1(Node):
        async def run(self, context: Context) -> dict | BaseModel:

            # gets the last user message (if any)
            last_user_message = next(
                (
                    message
                    for message in reversed(context.chat)
                    if message["role"] == "user"
                ),
                None,
            )
            if last_user_message is not None:
                print(f"Last user message: {last_user_message['content']}")
            context.chat.append(
                dict(
                    role="assistant",
                    content=f"Hello, {last_user_message['content'] if last_user_message else ''}",
                )
            )
            await self.stream_token(context.chat[-1]["content"])
            return context

    node1 = Node1(name="node1")
    node2 = WaitingNode(name="node2")

    # Create edges
    @edge("node1")
    def edge1(context: dict) -> Literal["node2"]:
        return "node2"

    @edge("node2")
    def edge2(context: dict) -> Literal["node1"]:
        return "node1"

    # Create a graph
    graph = Graph(stream_token=stream_token, context=Context(chat=[]))
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_edge(SimpleEdge("start", "node1"))
    graph.add_edge(edge1)
    graph.add_edge(edge2)

    print(graph.graph)
    # Plot the graph
    # graph.plot()

    # Run the graph
    is_end = False
    while not is_end:
        # If the execution is not ended, it means a waiting node is encountered
        some_input = input(f"Enter input for node {graph.current_node.name}: ")
        _, is_end = await graph.run(
            input=dict(chat=[dict(role="user", content=some_input)])
        )


if __name__ == "__main__":
    asyncio.run(main())
