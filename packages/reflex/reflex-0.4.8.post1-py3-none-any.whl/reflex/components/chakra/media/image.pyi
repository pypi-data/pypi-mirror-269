"""Stub file for reflex/components/chakra/media/image.py"""
# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------

from typing import Any, Dict, Literal, Optional, Union, overload
from reflex.vars import Var, BaseVar, ComputedVar
from reflex.event import EventChain, EventHandler, EventSpec
from reflex.style import Style
from typing import Any, Optional, Union
from reflex.components.chakra import ChakraComponent, LiteralImageLoading
from reflex.components.component import Component
from reflex.vars import Var

class Image(ChakraComponent):
    def get_event_triggers(self) -> dict[str, Union[Var, Any]]: ...
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        align: Optional[Union[Var[str], str]] = None,
        fallback: Optional[Component] = None,
        fallback_src: Optional[Union[Var[str], str]] = None,
        fit: Optional[Union[Var[str], str]] = None,
        html_height: Optional[Union[Var[str], str]] = None,
        html_width: Optional[Union[Var[str], str]] = None,
        ignore_fallback: Optional[Union[Var[bool], bool]] = None,
        loading: Optional[
            Union[Var[Literal["eager", "lazy"]], Literal["eager", "lazy"]]
        ] = None,
        src: Optional[Union[Var[Any], Any]] = None,
        alt: Optional[Union[Var[str], str]] = None,
        src_set: Optional[Union[Var[str], str]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, str]]] = None,
        on_blur: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_click: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_context_menu: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_double_click: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_error: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_focus: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_load: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mount: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_down: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_enter: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_leave: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_move: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_out: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_over: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_mouse_up: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_scroll: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_unmount: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        **props
    ) -> "Image":
        """Create an Image component.

        Args:
            *children: The children of the image.
            align: How to align the image within its bounds. It maps to css `object-position` property.
            fallback: Fallback Reflex component to show if image is loading or image fails.
            fallback_src: Fallback image src to show if image is loading or image fails.
            fit: How the image to fit within its bounds. It maps to css `object-fit` property.
            html_height: The native HTML height attribute to the passed to the img.
            html_width: The native HTML width attribute to the passed to the img.
            ignore_fallback: If true, opt out of the fallbackSrc logic and use as img.
            loading: "eager" | "lazy"
            src: The path/url to the image or PIL image object.
            alt: The alt text of the image.
            src_set: Provide multiple sources for an image, allowing the browser  to select the most appropriate source based on factors like  screen resolution and device capabilities.  Learn more _[here](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)_
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the image.

        Returns:
            The Image component.
        """
        ...
