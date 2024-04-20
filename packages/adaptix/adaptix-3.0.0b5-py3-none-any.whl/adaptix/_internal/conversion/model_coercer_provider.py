from inspect import Parameter, Signature
from typing import Iterable, List, Mapping, Optional, Tuple

from ..code_tools.compiler import BasicClosureCompiler, ClosureCompiler
from ..code_tools.name_sanitizer import BuiltinNameSanitizer, NameSanitizer
from ..common import Coercer
from ..conversion.broaching.code_generator import BroachingCodeGenerator, BroachingPlan, BuiltinBroachingCodeGenerator
from ..conversion.broaching.definitions import (
    AccessorElement,
    ConstantElement,
    FuncCallArg,
    FunctionElement,
    KeywordArg,
    ParameterElement,
    PositionalArg,
)
from ..conversion.request_cls import (
    CoercerRequest,
    ConstantLinking,
    ConversionDestItem,
    ConversionSourceItem,
    FieldLinking,
    LinkingRequest,
    LinkingResult,
    UnlinkedOptionalPolicyRequest,
)
from ..model_tools.definitions import DefaultValue, InputField, InputShape, OutputShape, ParamKind, create_key_accessor
from ..morphing.model.basic_gen import compile_closure_with_globals_capturing, fetch_code_gen_hook
from ..provider.essential import CannotProvide, Mediator, mandatory_apply_by_iterable
from ..provider.fields import input_field_to_loc, output_field_to_loc
from ..provider.location import OutputFieldLoc
from ..provider.request_cls import LocStack, TypeHintLoc
from ..provider.shape_provider import InputShapeRequest, OutputShapeRequest, provide_generic_resolved_shape
from ..utils import add_note
from .provider_template import CoercerProvider


class ModelCoercerProvider(CoercerProvider):
    def __init__(self, *, name_sanitizer: NameSanitizer = BuiltinNameSanitizer()):
        self._name_sanitizer = name_sanitizer

    def _provide_coercer(self, mediator: Mediator, request: CoercerRequest) -> Coercer:
        dst_shape = self._fetch_dst_shape(mediator, request.dst)
        src_shape = self._fetch_src_shape(mediator, request.src)
        broaching_plan = self._make_broaching_plan(
            mediator=mediator,
            request=request,
            dst_shape=dst_shape,
            src_shape=src_shape,
        )
        return self._make_coercer(mediator, request, broaching_plan)

    def _make_coercer(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        broaching_plan: BroachingPlan,
    ):
        code_gen = self._create_broaching_code_gen(broaching_plan)
        closure_name = self._get_closure_name(request)
        dumper_code, dumper_namespace = code_gen.produce_code(
            signature=Signature(
                parameters=[
                    Parameter("data", Parameter.POSITIONAL_ONLY),
                    Parameter("ctx", Parameter.POSITIONAL_ONLY),
                ],
            ),
            closure_name=closure_name,
        )
        return compile_closure_with_globals_capturing(
            compiler=self._get_compiler(),
            code_gen_hook=fetch_code_gen_hook(mediator, request.dst),
            namespace=dumper_namespace,
            closure_code=dumper_code,
            closure_name=closure_name,
            file_name=self._get_file_name(request),
        )

    def _get_closure_name(self, request: CoercerRequest) -> str:
        src = request.src.last.cast(TypeHintLoc).type
        dst = request.dst.last.cast(TypeHintLoc).type
        return self._name_sanitizer.sanitize(f"coerce_{src}_to_{dst}")

    def _get_file_name(self, request: CoercerRequest) -> str:
        src = request.src.last.cast(TypeHintLoc).type
        dst = request.dst.last.cast(TypeHintLoc).type
        return self._name_sanitizer.sanitize(f"coerce_{src}_to_{dst}")

    def _fetch_dst_shape(self, mediator: Mediator, loc_stack: LocStack[ConversionDestItem]) -> InputShape:
        return provide_generic_resolved_shape(
            mediator,
            InputShapeRequest(loc_stack=loc_stack),
        )

    def _fetch_src_shape(self, mediator: Mediator, loc_stack: LocStack[ConversionSourceItem]) -> OutputShape:
        return provide_generic_resolved_shape(
            mediator,
            OutputShapeRequest(loc_stack=loc_stack),
        )

    def _get_compiler(self) -> ClosureCompiler:
        return BasicClosureCompiler()

    def _create_broaching_code_gen(self, plan: BroachingPlan) -> BroachingCodeGenerator:
        return BuiltinBroachingCodeGenerator(plan=plan, name_sanitizer=self._name_sanitizer)

    def _fetch_linkings(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        dst_shape: InputShape,
        src_shape: OutputShape,
    ) -> Iterable[Tuple[InputField, Optional[LinkingResult]]]:
        sources = tuple(
            request.src.append_with(output_field_to_loc(src_field))
            for src_field in src_shape.fields
        )

        def fetch_field_linking(dst_field: InputField) -> Tuple[InputField, Optional[LinkingResult]]:
            destination = request.dst.append_with(input_field_to_loc(dst_field))
            try:
                linking = mediator.provide(
                    LinkingRequest(
                        sources=sources,
                        context=request.ctx,
                        destination=destination,
                    ),
                )
            except CannotProvide as e:
                if dst_field.is_required:
                    add_note(e, "Note: This is a required field, so it must take value")
                    raise

                policy = mediator.mandatory_provide(
                    UnlinkedOptionalPolicyRequest(loc_stack=destination),
                )
                if policy.is_allowed:
                    return dst_field, None
                add_note(
                    e,
                    "Note: Current policy forbids unlinked optional fields,"
                    " so you need to link it to another field"
                    " or explicitly confirm the desire to skipping using `allow_unlinked_optional`",
                )
                raise
            return dst_field, linking

        return mandatory_apply_by_iterable(
            fetch_field_linking,
            zip(dst_shape.fields),
            lambda: "Cannot create coercer for models. Linkings for some fields are not found",
        )

    def _field_linking_to_sub_plan(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        input_field: InputField,
        linking: FieldLinking,
    ) -> BroachingPlan:
        if linking.coercer is not None:
            coercer = linking.coercer
        else:
            coercer = mediator.provide(
                CoercerRequest(
                    src=linking.source,
                    ctx=request.ctx,
                    dst=request.dst.append_with(input_field_to_loc(input_field)),
                ),
            )

        return FunctionElement[BroachingPlan](
            func=coercer,
            args=(
                PositionalArg(self._get_field_coercer_data_arg(mediator, request, linking)),
                PositionalArg(ParameterElement("ctx")),
            ),
        )

    def _get_field_coercer_data_arg(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        linking: FieldLinking,
    ) -> BroachingPlan:
        if linking.source in request.ctx.loc_stacks:
            if len(request.ctx.params) == 1:
                return ParameterElement("ctx")
            return AccessorElement(
                ParameterElement("ctx"),
                create_key_accessor(
                    key=request.ctx.loc_stacks.index(linking.source),
                    access_error=None,
                ),
            )
        return AccessorElement(ParameterElement("data"), linking.source.last.cast(OutputFieldLoc).accessor)

    def _generate_constant_linking_to_sub_plan(
        self,
        mediator: Mediator,
        linking: ConstantLinking,
    ) -> BroachingPlan:
        if isinstance(linking.constant, DefaultValue):
            return ConstantElement(value=linking.constant.value)
        return FunctionElement(func=linking.constant.factory, args=())

    def _generate_field_to_sub_plan(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        field_linkings: Iterable[Tuple[InputField, LinkingResult]],
    ) -> Mapping[InputField, BroachingPlan]:
        def generate_sub_plan(input_field: InputField, linking_result: LinkingResult):
            if isinstance(linking_result.linking, ConstantLinking):
                return self._generate_constant_linking_to_sub_plan(
                    mediator=mediator,
                    linking=linking_result.linking,
                )
            return self._field_linking_to_sub_plan(
                mediator=mediator,
                request=request,
                input_field=input_field,
                linking=linking_result.linking,
            )

        field_sub_plans = mandatory_apply_by_iterable(
            generate_sub_plan,
            field_linkings,
            lambda: "Cannot create coercer for models. Coercers for some linkings are not found",
        )
        return {
            dst_field: sub_plan
            for (dst_field, linking), sub_plan in zip(field_linkings, field_sub_plans)
        }

    def _make_broaching_plan(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        dst_shape: InputShape,
        src_shape: OutputShape,
    ) -> BroachingPlan:
        field_linkings = self._fetch_linkings(
            mediator=mediator,
            request=request,
            dst_shape=dst_shape,
            src_shape=src_shape,
        )
        field_to_sub_plan = self._generate_field_to_sub_plan(
            mediator=mediator,
            request=request,
            field_linkings=[
                (dst_field, linking)
                for dst_field, linking in field_linkings
                if linking is not None
            ],
        )
        return self._make_constructor_call(
            dst_shape=dst_shape,
            field_to_linking=dict(field_linkings),
            field_to_sub_plan=field_to_sub_plan,
        )

    def _make_constructor_call(
        self,
        dst_shape: InputShape,
        field_to_linking: Mapping[InputField, Optional[LinkingResult]],
        field_to_sub_plan: Mapping[InputField, BroachingPlan],
    ) -> BroachingPlan:
        args: List[FuncCallArg[BroachingPlan]] = []
        has_skipped_params = False
        for param in dst_shape.params:
            field = dst_shape.fields_dict[param.field_id]

            if field_to_linking[field] is None:
                has_skipped_params = True
                continue

            sub_plan = field_to_sub_plan[field]
            if param.kind == ParamKind.KW_ONLY or has_skipped_params:
                args.append(KeywordArg(param.name, sub_plan))
            elif param.kind == ParamKind.POS_ONLY and has_skipped_params:
                raise CannotProvide(
                    "Can not generate consistent constructor call,"
                    " positional-only parameter is skipped",
                    is_demonstrative=True,
                )
            else:
                args.append(PositionalArg(sub_plan))

        return FunctionElement(
            func=dst_shape.constructor,
            args=tuple(args),
        )
