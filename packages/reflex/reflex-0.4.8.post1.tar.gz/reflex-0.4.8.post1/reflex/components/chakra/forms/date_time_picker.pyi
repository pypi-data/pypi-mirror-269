"""Stub file for reflex/components/chakra/forms/date_time_picker.py"""
# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------

from typing import Any, Dict, Literal, Optional, Union, overload
from reflex.vars import Var, BaseVar, ComputedVar
from reflex.event import EventChain, EventHandler, EventSpec
from reflex.style import Style
from reflex.components.chakra.forms.input import Input
from reflex.vars import Var

class DateTimePicker(Input):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        type_: Optional[Union[Var[str], str]] = None,
        value: Optional[Union[Var[str], str]] = None,
        default_value: Optional[Union[Var[str], str]] = None,
        placeholder: Optional[Union[Var[str], str]] = None,
        error_border_color: Optional[Union[Var[str], str]] = None,
        focus_border_color: Optional[Union[Var[str], str]] = None,
        is_disabled: Optional[Union[Var[bool], bool]] = None,
        is_invalid: Optional[Union[Var[bool], bool]] = None,
        is_read_only: Optional[Union[Var[bool], bool]] = None,
        is_required: Optional[Union[Var[bool], bool]] = None,
        variant: Optional[
            Union[
                Var[Literal["outline", "filled", "flushed", "unstyled"]],
                Literal["outline", "filled", "flushed", "unstyled"],
            ]
        ] = None,
        size: Optional[
            Union[Var[Literal["sm", "md", "lg", "xs"]], Literal["sm", "md", "lg", "xs"]]
        ] = None,
        name: Optional[Union[Var[str], str]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, str]]] = None,
        on_blur: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_change: Optional[
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
        on_focus: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_key_down: Optional[
            Union[EventHandler, EventSpec, list, function, BaseVar]
        ] = None,
        on_key_up: Optional[
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
    ) -> "DateTimePicker":
        """Create an Input component.

        Args:
            *children: The children of the component.
            type_: The type of input.
            value: State var to bind the input.
            default_value: The default value of the input.
            placeholder: The placeholder text.
            error_border_color: The border color when the input is invalid.
            focus_border_color: The border color when the input is focused.
            is_disabled: If true, the form control will be disabled. This has 2 side effects - The FormLabel will have `data-disabled` attribute - The form element (e.g, Input) will be disabled
            is_invalid: If true, the form control will be invalid. This has 2 side effects - The FormLabel and FormErrorIcon will have `data-invalid` set to true - The form element (e.g, Input) will have `aria-invalid` set to true
            is_read_only: If true, the form control will be readonly.
            is_required: If true, the form control will be required. This has 2 side effects - The FormLabel will show a required indicator - The form element (e.g, Input) will have `aria-required` set to true
            variant: "outline" | "filled" | "flushed" | "unstyled"
            size: "lg" | "md" | "sm" | "xs"
            name: The name of the form field
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The properties of the component.

        Returns:
            The component.
        """
        ...
